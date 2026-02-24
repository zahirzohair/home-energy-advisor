"""initial_homes_table

Revision ID: abc123
Revises:
Create Date: 2026-02-23 12:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "abc123"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use func.now() for dialect-agnostic timestamp (SQLite + PostgreSQL)
    op.create_table(
        "homes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("size_sqm", sa.Integer(), nullable=False),
        sa.Column("year_built", sa.Integer(), nullable=True),
        sa.Column("heating_type", sa.Enum("GAS", "OIL", "ELECTRIC", "HEAT_PUMP", "DISTRICT", name="heatingtype"), nullable=False),
        sa.Column("insulation", sa.Enum("NONE", "PARTIAL", "GOOD", "EXCELLENT", name="insulationlevel"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_homes_id"), "homes", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_homes_id"), table_name="homes")
    op.drop_table("homes")
    # PostgreSQL uses named ENUM types; SQLite does not
    if op.get_bind().dialect.name == "postgresql":
        op.execute("DROP TYPE heatingtype")
        op.execute("DROP TYPE insulationlevel")
