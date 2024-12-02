"""Create tables

Revision ID: 23ca21a33940
Revises: adfe8399daed
Create Date: 2024-11-29 17:59:44.719482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '23ca21a33940'
down_revision: Union[str, None] = 'adfe8399daed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achievement',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('badge', sa.String(), nullable=True),
    sa.Column('course_id', sa.UUID(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_achievement_id'), 'achievement', ['id'], unique=False)
    op.create_table('category',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=False)
    op.create_table('course',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('subjectid', sa.String(), nullable=True),
    sa.Column('course_image', sa.String(), nullable=True),
    sa.Column('category_list', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('lecturer', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', 'suspended', name='statusenum'), nullable=True),
    sa.Column('total_video', sa.Integer(), nullable=True),
    sa.Column('total_duration', sa.Float(), nullable=True),
    sa.Column('enrolled', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_id'), 'course', ['id'], unique=False)
    op.create_table('quiz',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('course_id', sa.UUID(), nullable=True),
    sa.Column('question', sa.String(), nullable=True),
    sa.Column('choices', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('correct_answer', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_id'), 'quiz', ['id'], unique=False)
    op.create_table('quiz_submission',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('course_id', sa.UUID(), nullable=True),
    sa.Column('quiz_answers', sa.JSON(), nullable=True),
    sa.Column('scores', sa.Integer(), nullable=True),
    sa.Column('submitted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_submission_id'), 'quiz_submission', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('role', sa.Enum('freshman', 'sophomore', 'junior', 'senior', 'graduated', 'admin', name='roleenum'), nullable=True),
    sa.Column('level', mysql.INTEGER(unsigned=True), nullable=True),
    sa.Column('score', mysql.INTEGER(unsigned=True), nullable=True),
    sa.Column('study_hours', sa.Float(), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', 'suspended', name='statusenum'), nullable=True),
    sa.Column('achievements', sa.ARRAY(sa.UUID()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('course_video',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('course_id', sa.UUID(), nullable=True),
    sa.Column('chapter', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('video_description', sa.String(), nullable=True),
    sa.Column('video_path', sa.String(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_video_id'), 'course_video', ['id'], unique=False)
    op.create_table('enrolled_course',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('course_id', sa.UUID(), nullable=True),
    sa.Column('enrolled_at', sa.DateTime(), nullable=True),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enrolled_course_id'), 'enrolled_course', ['id'], unique=False)
    op.create_table('token',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('state', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('expired_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_id'), 'token', ['id'], unique=False)
    op.create_index(op.f('ix_token_token'), 'token', ['token'], unique=True)
    op.create_table('enrolled_course_video',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('enrolled_course_id', sa.UUID(), nullable=True),
    sa.Column('course_video_id', sa.UUID(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['course_video_id'], ['course_video.id'], ),
    sa.ForeignKeyConstraint(['enrolled_course_id'], ['enrolled_course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enrolled_course_video_id'), 'enrolled_course_video', ['id'], unique=False)
    op.create_table('user_progress',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('enrolled_course_id', sa.UUID(), nullable=True),
    sa.Column('enrolled_course_video_id', sa.UUID(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['enrolled_course_id'], ['enrolled_course.id'], ),
    sa.ForeignKeyConstraint(['enrolled_course_video_id'], ['enrolled_course_video.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_progress_id'), 'user_progress', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_progress_id'), table_name='user_progress')
    op.drop_table('user_progress')
    op.drop_index(op.f('ix_enrolled_course_video_id'), table_name='enrolled_course_video')
    op.drop_table('enrolled_course_video')
    op.drop_index(op.f('ix_token_token'), table_name='token')
    op.drop_index(op.f('ix_token_id'), table_name='token')
    op.drop_table('token')
    op.drop_index(op.f('ix_enrolled_course_id'), table_name='enrolled_course')
    op.drop_table('enrolled_course')
    op.drop_index(op.f('ix_course_video_id'), table_name='course_video')
    op.drop_table('course_video')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_quiz_submission_id'), table_name='quiz_submission')
    op.drop_table('quiz_submission')
    op.drop_index(op.f('ix_quiz_id'), table_name='quiz')
    op.drop_table('quiz')
    op.drop_index(op.f('ix_course_id'), table_name='course')
    op.drop_table('course')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')
    op.drop_index(op.f('ix_achievement_id'), table_name='achievement')
    op.drop_table('achievement')
    # ### end Alembic commands ###