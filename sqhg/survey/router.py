"""Survey's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends, BackgroundTasks
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

from survey.schemas import SurveyModelSchema, QuestionSchema, OptionSchema, SurveySchema
from survey.models import SurveyModel, Question, Option

router = APIRouter()


@router.get('/')
async def dummy_endpoint():
    return {'message': 'survey'}


@router.get('/create', response_class=HTMLResponse)
async def survey_create_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Create Survey Model'

    return template.TemplateResponse('survey/create.html', context)


@router.get('/sent', response_class=HTMLResponse)
async def survey_sent_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Sent Surveys'

    return template.TemplateResponse('survey/sent.html', context)


@router.get('/send', response_class=HTMLResponse)
async def survey_send_page(request: Request, template: Jinja2Templates = Depends(Template)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Send Survey'

    return template.TemplateResponse('survey/send.html', context)


@router.post('/createmodel', response_class=HTMLResponse, status_code=201)
async def survey_model_create(
    request: Request,
    survey_model_data: SurveyModelSchema,
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        raise InvalidCredentials

    survey_model = SurveyModel(
        name=survey_model_data.name,
        description=survey_model_data.description,
    )

    database.add(survey_model)
    database.commit()

    return {
        'message': f"Modelo de questionário '{survey_model_data.name}' criado com sucesso!",
        'survey_model_id': {database.query(SurveyModel).order_by(SurveyModel.id.desc()).first()}
    }


@router.post('/createquestion', response_class=HTMLResponse, status_code=201)
async def question_create(request: Request, question_data: QuestionSchema, database: Session = Depends(Database)):
    if not request.state.authenticated:
        raise InvalidCredentials

    question = Question(
        description=question_data.description,
        type=question_data.type,
        survey_model_id=question_data.survey_model_id,
    )

    database.add(question)
    database.commit()

    return {
        'message': f"Questão '{question_data.description}' criada com sucesso!",
        'question_id': {database.query(Question).order_by(Question.id.desc()).first()}
    }


@router.post('/createoption', response_class=HTMLResponse, status_code=201)
async def option_create(request: Request, option_data: OptionSchema, database: Session = Depends(Database)):
    if not request.state.authenticated:
        raise InvalidCredentials

    option = Option(
        description=option_data.description,
        question_id=option_data.question_id,
    )

    database.add(option)
    database.commit()

    return {'message': f"Opção '{option_data.description}' criada com sucesso!"}


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

    for superior in survey_data.superiors:
        superior = database.query(Superior).filter(Superior.id == superior).first()
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
