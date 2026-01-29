"""Initial schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2023-01-01 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('tier', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False, server_default='free'),
        sa.Column('tier_expires_at', sa.DateTime(), nullable=True),
        sa.Column('timezone', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False, server_default='UTC'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Create courses table
    op.create_table('courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=False),
        sa.Column('free_chapter_limit', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('required_tier', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False, server_default='free'),
        sa.Column('total_chapters', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('difficulty_level', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False, server_default='intermediate'),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('ix_courses_slug', 'courses', ['slug'])

    # Create chapters table
    op.create_table('chapters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('chapter_number', sa.Integer(), nullable=False),
        sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=500), nullable=False),
        sa.Column('content_key', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('previous_chapter_id', sa.Integer(), nullable=True),
        sa.Column('next_chapter_id', sa.Integer(), nullable=True),
        sa.Column('estimated_minutes', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('word_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('requires_premium', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('embedding', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id']),
        sa.ForeignKeyConstraint(['previous_chapter_id'], ['chapters.id']),
        sa.ForeignKeyConstraint(['next_chapter_id'], ['chapters.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_chapters_course_id', 'chapters', ['course_id'])
    op.create_index('ix_chapters_slug', 'chapters', ['slug'])

    # Create quizzes table
    op.create_table('quizzes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=500), nullable=False),
        sa.Column('difficulty', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False, server_default='medium'),
        sa.Column('passing_score', sa.Integer(), nullable=False, server_default='70'),
        sa.Column('max_attempts', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('time_limit_minutes', sa.Integer(), nullable=True),
        sa.Column('requires_premium', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_quizzes_chapter_id', 'quizzes', ['chapter_id'])

    # Create questions table
    op.create_table('questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.Column('question_number', sa.Integer(), nullable=False),
        sa.Column('question_text', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=False),
        sa.Column('question_type', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
        sa.Column('answer_config', sa.Text(), nullable=False),
        sa.Column('case_sensitive', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('trim_whitespace', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('allow_partial', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('points', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_questions_quiz_id', 'questions', ['quiz_id'])

    # Create quiz_attempts table
    op.create_table('quiz_attempts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.Column('attempt_number', sa.Integer(), nullable=False),
        sa.Column('answers', sa.Text(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('correct_count', sa.Integer(), nullable=False),
        sa.Column('total_questions', sa.Integer(), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('started_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('time_taken_seconds', sa.Integer(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_quiz_attempts_user_id', 'quiz_attempts', ['user_id'])
    op.create_index('ix_quiz_attempts_quiz_id', 'quiz_attempts', ['quiz_id'])

    # Create progress table
    op.create_table('progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_position', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_accessed_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('current_streak', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('longest_streak', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_activity_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_progress_user_id', 'progress', ['user_id'])
    op.create_index('ix_progress_chapter_id', 'progress', ['chapter_id'])

    # Create achievements table
    op.create_table('achievements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('achievement_type', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
        sa.Column('achievement_name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('achievement_description', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('context_course_id', sa.Integer(), nullable=True),
        sa.Column('context_chapter_id', sa.Integer(), nullable=True),
        sa.Column('context_quiz_id', sa.Integer(), nullable=True),
        sa.Column('earned_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_notified', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['context_course_id'], ['courses.id']),
        sa.ForeignKeyConstraint(['context_chapter_id'], ['chapters.id']),
        sa.ForeignKeyConstraint(['context_quiz_id'], ['quizzes.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_achievements_user_id', 'achievements', ['user_id'])
    op.create_index('ix_achievements_achievement_type', 'achievements', ['achievement_type'])


def downgrade() -> None:
    # Drop tables in reverse order (reverse of creation)
    op.drop_index('ix_achievements_achievement_type', table_name='achievements')
    op.drop_index('ix_achievements_user_id', table_name='achievements')
    op.drop_table('achievements')

    op.drop_index('ix_progress_chapter_id', table_name='progress')
    op.drop_index('ix_progress_user_id', table_name='progress')
    op.drop_table('progress')

    op.drop_index('ix_quiz_attempts_quiz_id', table_name='quiz_attempts')
    op.drop_index('ix_quiz_attempts_user_id', table_name='quiz_attempts')
    op.drop_table('quiz_attempts')

    op.drop_index('ix_questions_quiz_id', table_name='questions')
    op.drop_table('questions')

    op.drop_index('ix_quizzes_chapter_id', table_name='quizzes')
    op.drop_table('quizzes')

    op.drop_index('ix_chapters_slug', table_name='chapters')
    op.drop_index('ix_chapters_course_id', table_name='chapters')
    op.drop_table('chapters')

    op.drop_index('ix_courses_slug', table_name='courses')
    op.drop_table('courses')

    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')