"""fix achievement model

Revision ID: 9e64a18dc752
Revises: cde3848f2b34
Create Date: 2024-11-10 22:13:56.094360

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e64a18dc752"
down_revision: Union[str, None] = "cde3848f2b34"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("achievement", sa.Column("course_id", sa.UUID(), nullable=True))
    op.drop_constraint(
        "achievement_category_id_fkey", "achievement", type_="foreignkey"
    )
    op.create_foreign_key(None, "achievement", "course", ["course_id"], ["id"])
    op.drop_column("achievement", "category_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "achievement",
        sa.Column("category_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "achievement", type_="foreignkey")
    op.create_foreign_key(
        "achievement_category_id_fkey",
        "achievement",
        "category",
        ["category_id"],
        ["id"],
    )
    op.drop_column("achievement", "course_id")
    # ### end Alembic commands ###
