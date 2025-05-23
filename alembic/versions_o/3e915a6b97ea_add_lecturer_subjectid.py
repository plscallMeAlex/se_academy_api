"""add lecturer&subjectid

Revision ID: 3e915a6b97ea
Revises: 3324c018f09d
Create Date: 2024-10-02 13:57:18.598275

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e915a6b97ea"
down_revision: Union[str, None] = "3324c018f09d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("course", sa.Column("subjectid", sa.String(), nullable=True))
    op.drop_column("course", "subjectID")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column(
        "course",
        sa.Column("subjectID", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("course", "subjectid")
    # ### end Alembic commands ###
