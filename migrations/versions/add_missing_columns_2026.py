"""Add missing columns to book and user tables (merge heads)

Revision ID: add_missing_columns_2026
Revises: ddc654110c43, c7a08c4cf64b
Create Date: 2026-05-11 11:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_missing_columns_2026'
down_revision = ('ddc654110c43', 'c7a08c4cf64b')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
