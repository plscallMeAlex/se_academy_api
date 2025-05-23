"""add course id to achievement

Revision ID: e2614b6ee9a1
Revises: 56db77c40372
Create Date: 2024-11-14 17:10:39.523974

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e2614b6ee9a1"
down_revision: Union[str, None] = "56db77c40372"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("achievement", sa.Column("course_id", sa.UUID(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("achievement", "course_id")
    # ### end Alembic commands ###
