"""Survey's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from core.template import Template
from core.database import Database

from survey.schemas import SurveyModelSchema
from survey.models import Survey, SurveyModel, Question, Option
from auth.exceptions import InvalidCredentials

router = APIRouter()


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

    survey_model = database.query(SurveyModel).filter(SurveyModel.id==id)
    if not survey_model:
        raise HTTPException(status_code = 404, detail = "Survey model not found")

    survey_model = survey_model.first()

    for question in survey_model.questions:
        question.options

    context['model'] = survey_model

    return template.TemplateResponse('survey/edit_model.html', context)


@router.get('/model/list', response_class=HTMLResponse)
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


@router.get('/list',response_class=HTMLResponse)
async def survey_sent_page(
    request: Request,
    template: Jinja2Templates = Depends(Template),
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        return RedirectResponse('/login')

    context = {'request' : request}
    context['subtitle'] = 'List Survey Sent'

    surveys = database.query(Survey).all()
    context['surveys'] = surveys

    return template.TemplateResponse('survey/sent.html', context)


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


@router.post('/model/edit/{id}', status_code=200)
async def model_edit(
    request: Request,
    id: int,
    model_data: SurveyModelSchema,
    database: Session = Depends(Database)
):
    if not request.state.authenticated:
        raise InvalidCredentials

    db_survey_model = database.query(SurveyModel).filter(SurveyModel.id==id)
    if not db_survey_model:
        raise HTTPException(status_code = 404, detail = "Survey model not found")

    db_survey_model = db_survey_model.first()

    db_survey_model.name = model_data.name
    db_survey_model.description = model_data.description

    if model_data.questions:
        for question in db_survey_model.questions:
            for option in question.options:
                database.delete(option)
            database.delete(question)

        for question_data in model_data.questions:
            question = Question(
                description=question_data['description'],
                type=question_data['type'],
                survey_model_id=db_survey_model.id
            )

            database.add(question)
            database.flush()

            if 'options' in question_data:
                for option_data in question_data['options']:
                    option = Option(
                        description=option_data['description'],
                        question_id=question.id
                    )
                    database.add(option)

    database.commit()

    return {
        'message': f"Modelo de questionário '{db_survey_model.name}' editado com sucesso!",
        'survey_model_id': {database.query(SurveyModel).order_by(SurveyModel.id.desc()).first()}
    }


@router.delete('/model/delete/{id}', status_code=200)
async def model_delete(request: Request, id: int, database: Session = Depends(Database)):
    if not request.state.authenticated:
        return InvalidCredentials

    survey_model = database.query(SurveyModel).filter(SurveyModel.id==id)
    if not survey_model:
        raise HTTPException(status_code = 404, detail = "Survey model not found")

    survey_model = survey_model.first()

    for question in survey_model.questions:
        for option in question.options:
            database.delete(option)
        database.delete(question)

    database.delete(survey_model)
    database.commit()

    return {'message': "Modelo deletado com sucesso!"}
