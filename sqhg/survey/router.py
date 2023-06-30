"""Survey's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends, BackgroundTasks, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy.orm import Session

from core.template import Template
from core.database import Database
from core.email import Email

from auth.exceptions import InvalidCredentials
from auth.utils import generate_random_token
from sap.models import Superior
from user.models import Token

from survey.schemas import SurveyModelSchema, SurveySchema
from survey.models import Survey, SurveyModel, QuestionModel, OptionModel, QuestionType

router = APIRouter()


@router.get('/list', response_class=HTMLResponse)
async def survey_list_page(
    request: Request,
    template: Jinja2Templates = Depends(Template),
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Survey Model List'
    context['models'] = database.query(SurveyModel).filter(SurveyModel.is_archived==False).all()  # noqa: E712

    return template.TemplateResponse('survey/list.html', context)


@router.get('/create', response_class=HTMLResponse)
async def survey_create_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Create Survey Model'

    return template.TemplateResponse('survey/create.html', context)


@router.get('/edit/{id}', response_class=HTMLResponse)
async def survey_edit_page(
    request: Request,
    id: int,
    template: Jinja2Templates = Depends(Template),
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Edit Survey Model'
    context['question_type'] = QuestionType

    survey_model = database.query(SurveyModel).filter(SurveyModel.id==id)
    if not survey_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Survey model not found')
    context['model'] = survey_model.first()

    return template.TemplateResponse('survey/edit.html', context)


@router.get('/send', response_class=HTMLResponse)
async def survey_send_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Send Survey'

    return template.TemplateResponse('survey/send.html', context)


@router.get('/sent',response_class=HTMLResponse)
async def survey_sent_page(
    request: Request,
    template: Jinja2Templates = Depends(Template),
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Sent Surveys'
    context['surveys'] = database.query(Survey).all()

    return template.TemplateResponse('survey/sent.html', context)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def survey_create(
    request: Request,
    model_data: SurveyModelSchema,
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        raise InvalidCredentials

    survey_model = SurveyModel(
        name=model_data.name,
        description=model_data.description
    )

    if model_data.questions:
        for question_data in model_data.questions:
            question = QuestionModel(
                description=question_data['description'],
                type=question_data['type'],
                survey_model=survey_model
            )

            if 'options' in question_data:
                for option_data in question_data['options']:
                    option = OptionModel(
                        description=option_data['description'],
                        question_model=question
                    )
                    question.options_model.append(option)

            survey_model.questions_model.append(question)

    database.add(survey_model)
    database.commit()

    return {'message': f"Modelo de questionário '{survey_model.name}' criado com sucesso!"}


@router.post('/edit/{id}', status_code=status.HTTP_200_OK)
async def survey_edit(
    request: Request,
    id: int,
    model_data: SurveyModelSchema,
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        raise InvalidCredentials

    db_survey_model = database.query(SurveyModel).filter(SurveyModel.id==id)
    if not db_survey_model:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Survey model not found")

    db_survey_model = db_survey_model.first()

    db_survey_model.name = model_data.name
    db_survey_model.description = model_data.description

    if model_data.questions:
        for question in db_survey_model.questions_model:
            for option in question.options_model:
                database.delete(option)
            database.delete(question)

        for question_data in model_data.questions:
            question = QuestionModel(
                description=question_data['description'],
                type=question_data['type'],
                survey_model_id=db_survey_model.id
            )

            database.add(question)
            database.flush()

            if 'options' in question_data:
                for option_data in question_data['options']:
                    option = OptionModel(
                        description=option_data['description'],
                        question_model_id=question.id
                    )
                    database.add(option)

    database.commit()

    return {'message': f"Modelo de questionário '{db_survey_model.name}' editado com sucesso!"}


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
async def survey_delete(request: Request, id: int, database: Session = Depends(Database)):
    if not request.state.authenticated:
        return InvalidCredentials

    survey_model = database.query(SurveyModel).filter(SurveyModel.id==id)
    if not survey_model:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Survey model not found")

    survey_model = survey_model.first()
    survey_model.is_archived = True

    database.commit()

    return {'message': 'Modelo arquivado com sucesso!'}


@router.post('/send', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def send_survey(
    request: Request,
    survey_data: SurveySchema,
    background_tasks: BackgroundTasks,
    database: Session = Depends(Database),
    email: FastMail = Depends(Email)
):
    if not request.state.authenticated:
        raise InvalidCredentials

    for superior_id in survey_data.superiors:
        superior = database.query(Superior).filter(Superior.id == superior_id).first()
        tokens = []

        #############################################
        ###
        ### Inserir lógica para envio de questionário
        ###
        #############################################

        for _ in superior.subordinates:
            token = Token(
                survey_id=0,  # Placeholder / ID do questionário criado acima
                token=generate_random_token()
            )

            tokens.append(token.token)
            database.add(token)

        email_context = {}
        email_context['user'] = request.state.user
        email_context['survey'] = None  # Entidade do questionário
        email_context['tokens'] = tokens

        email_body = MessageSchema(
            subject='SQHG - Chaves de Acesso',
            recipients=[request.state.user.email],
            template_body=email_context,
            subtype=MessageType.html,
        )

        background_tasks.add_task(email.send_message, email_body, template_name='token_list.html')

    database.commit()

    return {'message': 'Questionários enviados com sucesso!'}
