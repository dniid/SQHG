"""Survey's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends, BackgroundTasks, HTTPException
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
from survey.models import SurveyModel, Question, Option

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def survey_sent_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Sent Surveys'

    return template.TemplateResponse('survey/sent.html', context)


@router.get('/model/create', response_class=HTMLResponse)
async def survey_create_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Create Survey Model'

    return template.TemplateResponse('survey/create_model.html', context)


@router.get('/model/send', response_class=HTMLResponse)
async def survey_send_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Send Survey'

    return template.TemplateResponse('survey/send_model.html', context)


@router.get('/model/edit/{id}', response_class=HTMLResponse)
async def models_edit_page(
    request: Request,
    id: int,
    template: Jinja2Templates = Depends(Template),
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Models'

    survey_model = database.query(SurveyModel).filter(id == id).first()

    if not survey_model:
        raise HTTPException(status_code = 404, detail = "Survey model not found")

    survey_model.questions
    for question in survey_model.questions:
        question.options

    context['model'] = survey_model

    return template.TemplateResponse('survey/edit_model.html', context)


@router.get('/model', response_class=HTMLResponse)
async def models_list_page(
    request: Request,
    template: Jinja2Templates = Depends(Template),
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'List Survey Model'

    models = database.query(SurveyModel).all()
    context['models'] = models

    return template.TemplateResponse('survey/list_model.html', context)


@router.post('/model/create', status_code=201)
async def model_create(
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
            question = Question(
                description=question_data['description'],
                type=question_data['type'],
                survey_model=survey_model
            )

            if 'options' in question_data:
                for option_data in question_data['options']:
                    option = Option(
                        description=option_data['description'],
                        question=question
                    )
                    question.options.append(option)

            survey_model.questions.append(question)

    database.add(survey_model)
    database.commit()

    return {
        'message': f"Modelo de questionário '{survey_model.name}' criado com sucesso!",
        'survey_model_id': {database.query(SurveyModel).order_by(SurveyModel.id.desc()).first()}
    }


@router.post('/send', response_class=HTMLResponse, status_code=200)
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
