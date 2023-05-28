import logging

from mimesis import Generic
from mimesis.locales import Locale
from sqlalchemy.orm import sessionmaker

from core.database import engine
from admin.models import Admin
from sap.models import Superior, Area
from survey.models import Survey, SurveyModel, Question, Option, Answer
from user.models import Token


logger = logging.getLogger('sqhg')
SessionLocal = sessionmaker(bind=engine)


def generate_data(times=1):
    generic = Generic(locale=Locale.PT_BR)
    session = SessionLocal()

    for _ in range(times):
        logger.info('Generating data for admins...')
        admin_data = [
            Admin(
                tag=generic.random.randint(100000000000, 999999999999),
                name=generic.person.full_name(),
                birth_date=generic.datetime.date(start=1900, end=2000),
                email=generic.person.email(),
                phone=generic.person.telephone(mask='#############'),
                password=generic.person.password(),
            ) for _ in range(8000)
        ]
        logger.info('Finished Generating')
        session.bulk_save_objects(admin_data)

        logger.info('Generating data for areas...')
        area_data = [
            Area(
                name=generic.text.word(),
                register_date=generic.datetime.date(start=1900, end=2023),
                deactivation_date=generic.datetime.date(start=2024, end=2200),
                status=generic.random.randint(0, 1),
            ) for _ in range(10000)
        ]
        logger.info('Finished Generating')
        session.bulk_save_objects(area_data)

        logger.info('Generating data for superiors...')
        area_ids = session.query(Area.id).all()
        superior_data = [
            Superior(
                name=generic.person.full_name(),
                position=generic.person.occupation(),
                area_id=generic.random.choice(area_ids)[0],
            ) for _ in range(14000)
        ]
        logger.info('Finished Generating')
        session.bulk_save_objects(superior_data)

        logger.info('Generating data for survey models...')
        survey_model_data = [
            SurveyModel(
                name=generic.text.word(),
                description=generic.text.sentence(),
            ) for _ in range(7000)
        ]
        logger.info('Finished Generating')
        session.bulk_save_objects(survey_model_data)

        logger.info('Generating data for questions...')
        survey_model_ids = session.query(SurveyModel.id).all()
        question_data = [
            Question(
                description=generic.text.sentence(),
                type=generic.random.randint(1, 3),
                survey_model_id=generic.random.choice(survey_model_ids)[0],
            ) for _ in range(14000)
        ]
        logger.info('Finished Generating')
        session.bulk_save_objects(question_data)

        logger.info('Generating data for options...')
        question_ids = session.query(Question.id).all()
        option_data = [
            Option(
                description=generic.text.word(),
                question_id=generic.random.choice(question_ids)[0],
            ) for _ in range(20000)
        ]
        logger.info('Finished Generating')
        session.bulk_save_objects(option_data)

        logger.info('Generating data for surveys...')
        admin_ids = session.query(Admin.id).all()
        superior_ids = session.query(Superior.id).all()
        survey_data = [
            Survey(
                name=generic.text.title(),
                description=generic.text.sentence(),
                start_date=generic.datetime.date(start=2020, end=2023),
                end_date=generic.datetime.date(start=2024, end=2050),
                created_by=generic.random.choice(admin_ids)[0],
                superior_id=generic.random.choice(superior_ids)[0],
                survey_model_id=generic.random.choice(survey_model_ids)[0],
            ) for _ in range(5000)
        ]
        logger.info('Finished Generating')
        session.bulk_save_objects(survey_data)

        logger.info('Generating data for answers...')
        survey_ids = session.query(Survey.id).all()
        answer_data = [
            Answer(
                answer=generic.text.word(),
                question_id=generic.random.choice(question_ids)[0],
                survey_id=generic.random.choice(survey_ids)[0],
            ) for _ in range(10000)
        ]
        logger.info('Finished Generating')
        session.bulk_save_objects(answer_data)

        logger.info('Generating data for tokens...')
        token_data = [
            Token(
                survey_id=generic.random.choice(survey_ids)[0],
                token=generic.cryptographic.uuid(),
                status=generic.random.randint(0, 1),
            ) for _ in range(20000)
        ]
        logger.info('Finished Generating')
        session.bulk_save_objects(token_data)

        logger.info('Commiting changes')
        session.commit()

    session.close()
