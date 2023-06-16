"""Survey's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from core.template import Template
from core.database import Database

from survey.schemas import SurveyModelSchema, QuestionSchema, OptionSchema
from survey.models import SurveyModel, Question, Option
from auth.exceptions import InvalidCredentials

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

@router.get('/editmodels/{id}', response_class=HTMLResponse)
async def models_edit_page(request: Request, id: int, template: Jinja2Templates = Depends(Template), database: Session = Depends(Database)):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request': request}
    context['subtitle'] = 'Models'
    
    surveymodel = database.query(SurveyModel),filter(id == id).first()
    
    if not surveymodel :
        raise HTTPException(status_code = 404, detail = "surveymodel not found")
    
    context['models'] = surveymodel
    
    return template.TemplateResponse('survey/edit.html', context)

@router.get('/models', response_class=HTMLResponse)
async def models_list_page(request: Request, template: Jinja2Templates = Depends(Template), database: Session = Depends(Database)):
    if not request.state.authenticated:
        return RedirectResponse('/login')
    context = {'request': request}
    context['subtitle'] = 'List Survey Model'
    models = database.query(SurveyModel).all()
    context['models'] = models
    return template.TemplateResponse('survey/models.html', context)

@router.post('/createmodel', response_class=HTMLResponse, status_code=201)
async def model_create(
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
