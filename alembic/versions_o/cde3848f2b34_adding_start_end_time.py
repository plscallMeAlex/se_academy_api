"""adding start&end time

Revision ID: cde3848f2b34
Revises: 20b58e263a8d
Create Date: 2024-11-10 19:33:42.834872

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cde3848f2b34"
down_revision: Union[str, None] = "20b58e263a8d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "enrolled_course_video", sa.Column("started_at", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "enrolled_course_video", sa.Column("ended_at", sa.DateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("enrolled_course_video", "ended_at")
    op.drop_column("enrolled_course_video", "started_at")
    # ### end Alembic commands ###
