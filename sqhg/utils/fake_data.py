import logging

from mimesis import Generic
from mimesis.locales import Locale

from admin.models import Admin
from sap.models import Superior, Area
from survey.models import Survey, SurveyModel, Question, Option, Answer
from user.models import Token


logger = logging.getLogger('sqhg')

generic = Generic(locale=Locale.PT_BR)


ADMIN_RANGE = 1000
ANSWER_RANGE = 2600
AREA_RANGE = 800
MODEL_RANGE = 700
OPTION_RANGE = 2000
QUESTION_RANGE = 2400
SUPERIOR_RANGE = 1400
SURVEY_RANGE = 1400
TOKEN_RANGE = 3000


def generate_admin_data(n):
    print(f'Process {n} - Generating data for admins...', flush=True)
    admin_data = [
        Admin(
            tag=generic.random.randint(100000000000, 999999999999),
            name=generic.person.full_name(),
            birth_date=generic.datetime.date(start=1900, end=2000),
            email=generic.person.email(),
            phone=generic.person.telephone(mask='#############'),
            password=generic.person.password(),
        ) for _ in range(ADMIN_RANGE)
    ]
    print(f'Process {n} - Finished generating admins', flush=True)

    return admin_data


def generate_area_data(n):
    print(f'Process {n} - Generating data for areas...', flush=True)
    area_data = [
        Area(
            name=generic.text.word(),
            register_date=generic.datetime.date(start=1900, end=2023),
            deactivation_date=generic.datetime.date(start=2024, end=2200),
            status=generic.random.randint(0, 1),
        ) for _ in range(AREA_RANGE)
    ]
    print(f'Process {n} - Finished generating areas', flush=True)

    return area_data


def generate_superior_data(n):
    print(f'Process {n} - Generating data for superiors...', flush=True)
    superior_data = [
        Superior(
            name=generic.person.full_name(),
            position=generic.person.occupation(),
            area_id=generic.choice.choice([i for i in range(AREA_RANGE)]),
        ) for _ in range(SUPERIOR_RANGE)
    ]
    print(f'Process {n} - Finished generating superiors', flush=True)

    return superior_data


def generate_survey_model_data(n):
    print(f'Process {n} - Generating data for survey models...', flush=True)
    survey_model_data = [
        SurveyModel(
            name=generic.text.word(),
            description=generic.text.sentence(),
        ) for _ in range(MODEL_RANGE)
    ]
    print(f'Process {n} - Finished generating survey models', flush=True)

    return survey_model_data


def generate_question_data(n):
    print(f'Process {n} - Generating data for questions...', flush=True)
    question_data = [
        Question(
            description=generic.text.sentence(),
            type=generic.random.randint(1, 3),
            survey_model_id=generic.choice.choice([i for i in range(MODEL_RANGE)]),
        ) for _ in range(QUESTION_RANGE)
    ]
    print(f'Process {n} - Finished generating questions', flush=True)

    return question_data


def generate_option_data(n):
    print(f'Process {n} - Generating data for options...', flush=True)
    option_data = [
        Option(
            description=generic.text.word(),
            question_id=generic.choice.choice([i for i in range(QUESTION_RANGE)]),
        ) for _ in range(OPTION_RANGE)
    ]
    print(f'Process {n} - Finished generating options', flush=True)

    return option_data


def generate_survey_data(n):
    print(f'Process {n} - Generating data for surveys...', flush=True)
    survey_data = [
        Survey(
            name=generic.text.title(),
            description=generic.text.sentence(),
            start_date=generic.datetime.date(start=2020, end=2023),
            end_date=generic.datetime.date(start=2024, end=2050),
            created_by=generic.choice.choice([i for i in range(ADMIN_RANGE)]),
            superior_id=generic.choice.choice([i for i in range(SUPERIOR_RANGE)]),
            survey_model_id=generic.choice.choice([i for i in range(MODEL_RANGE)]),
        ) for _ in range(SURVEY_RANGE)
    ]
    print(f'Process {n} - Finished generating surveys', flush=True)

    return survey_data


def generate_answer_data(n):
    print(f'Process {n} - Generating data for answers...', flush=True)
    answer_data = [
        Answer(
            answer=generic.text.word(),
            question_id=generic.choice.choice([i for i in range(QUESTION_RANGE)]),
            survey_id=generic.choice.choice([i for i in range(SURVEY_RANGE)]),
        ) for _ in range(ANSWER_RANGE)
    ]
    print(f'Process {n} - Finished generating answers', flush=True)

    return answer_data


def generate_token_data(n):
    print(f'Process {n} - Generating data for tokens...', flush=True)
    token_data = [
        Token(
            survey_id=generic.choice.choice([i for i in range(SURVEY_RANGE)]),
            token=generic.cryptographic.uuid(),
            status=generic.random.randint(0, 1),
        ) for _ in range(TOKEN_RANGE)
    ]
    print(f'Process {n} - Finished generating tokens', flush=True)

    return token_data
