"""add quiz model

Revision ID: a010f369cccd
Revises: e2614b6ee9a1
Create Date: 2024-11-16 19:51:24.399536

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a010f369cccd"
down_revision: Union[str, None] = "e2614b6ee9a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "quiz",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=True),
        sa.Column("question", sa.String(), nullable=True),
        sa.Column("choices", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("correct_answer", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_quiz_id"), "quiz", ["id"], unique=False)
    op.create_table(
        "quiz_submission",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("course_id", sa.UUID(), nullable=True),
        sa.Column("quiz_answers", sa.JSON(), nullable=True),
        sa.Column("scores", sa.Integer(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_quiz_submission_id"), "quiz_submission", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_quiz_submission_id"), table_name="quiz_submission")
    op.drop_table("quiz_submission")
    op.drop_index(op.f("ix_quiz_id"), table_name="quiz")
    op.drop_table("quiz")
    # ### end Alembic commands ###
