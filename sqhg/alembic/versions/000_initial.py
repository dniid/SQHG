"""initial

Revision ID: bda7e54a051b
Revises:
Create Date: 2023-04-17 19:15:55.326303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bda7e54a051b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=12), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=13), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_id'), 'admin', ['id'], unique=False)
    op.create_table('area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('register_date', sa.Date(), nullable=False),
    sa.Column('deactivation_date', sa.Date(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_area_id'), 'area', ['id'], unique=False)
    op.create_table('survey_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_survey_model_id'), 'survey_model', ['id'], unique=False)
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('survey_model_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['survey_model_id'], ['survey_model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_id'), 'question', ['id'], unique=False)
    op.create_index(op.f('ix_question_survey_model_id'), 'question', ['survey_model_id'], unique=False)
    op.create_table('superior',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('position', sa.String(length=45), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['area_id'], ['area.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_superior_area_id'), 'superior', ['area_id'], unique=False)
    op.create_index(op.f('ix_superior_id'), 'superior', ['id'], unique=False)
    op.create_table('option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_option_id'), 'option', ['id'], unique=False)
    op.create_index(op.f('ix_option_question_id'), 'option', ['question_id'], unique=False)
    op.create_table('survey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('superior_id', sa.Integer(), nullable=False),
    sa.Column('survey_model_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['admin.id'], ),
    sa.ForeignKeyConstraint(['superior_id'], ['superior.id'], ),
    sa.ForeignKeyConstraint(['survey_model_id'], ['survey_model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_survey_created_by'), 'survey', ['created_by'], unique=False)
    op.create_index(op.f('ix_survey_id'), 'survey', ['id'], unique=False)
    op.create_index(op.f('ix_survey_superior_id'), 'survey', ['superior_id'], unique=False)
    op.create_index(op.f('ix_survey_survey_model_id'), 'survey', ['survey_model_id'], unique=False)
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=255), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_answer_id'), 'answer', ['id'], unique=False)
    op.create_index(op.f('ix_answer_question_id'), 'answer', ['question_id'], unique=False)
    op.create_index(op.f('ix_answer_survey_id'), 'answer', ['survey_id'], unique=False)
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=128), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_token_id'), 'token', ['id'], unique=False)
    op.create_index(op.f('ix_token_survey_id'), 'token', ['survey_id'], unique=False)

    # ### Creates a superuser ###
    import os

    from auth.utils import get_password_hash

    SUPERUSER_EMAIL = os.getenv('SUPERUSER_EMAIL', 'admin@admin.com')
    SUPERUSER_USERNAME = os.getenv('SUPERUSER_USERNAME', 'admin')
    SUPERUSER_PASSWORD = os.getenv('SUPERUSER_PASSWORD', '')

    password = get_password_hash(SUPERUSER_PASSWORD)

    op.execute(f"INSERT INTO admin (tag, name, birth_date, email, phone, password) VALUES ('000000000000', '{SUPERUSER_USERNAME}', '2000-01-01', '{SUPERUSER_EMAIL}', '00000000000', '{password}')")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_token_survey_id'), table_name='token')
    op.drop_index(op.f('ix_token_id'), table_name='token')
    op.drop_table('token')
    op.drop_index(op.f('ix_answer_survey_id'), table_name='answer')
    op.drop_index(op.f('ix_answer_question_id'), table_name='answer')
    op.drop_index(op.f('ix_answer_id'), table_name='answer')
    op.drop_table('answer')
    op.drop_index(op.f('ix_survey_survey_model_id'), table_name='survey')
    op.drop_index(op.f('ix_survey_superior_id'), table_name='survey')
    op.drop_index(op.f('ix_survey_id'), table_name='survey')
    op.drop_index(op.f('ix_survey_created_by'), table_name='survey')
    op.drop_table('survey')
    op.drop_index(op.f('ix_option_question_id'), table_name='option')
    op.drop_index(op.f('ix_option_id'), table_name='option')
    op.drop_table('option')
    op.drop_index(op.f('ix_superior_id'), table_name='superior')
    op.drop_index(op.f('ix_superior_area_id'), table_name='superior')
    op.drop_table('superior')
    op.drop_index(op.f('ix_question_survey_model_id'), table_name='question')
    op.drop_index(op.f('ix_question_id'), table_name='question')
    op.drop_table('question')
    op.drop_index(op.f('ix_survey_model_id'), table_name='survey_model')
    op.drop_table('survey_model')
    op.drop_index(op.f('ix_area_id'), table_name='area')
    op.drop_table('area')
    op.drop_index(op.f('ix_admin_id'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
