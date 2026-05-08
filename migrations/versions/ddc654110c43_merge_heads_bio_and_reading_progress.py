"""merge heads bio and reading-progress

Revision ID: ddc654110c43
Revises: 2af98138d473, 3e66512bc8bf
Create Date: 2026-05-08 19:32:14.313303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddc654110c43'
down_revision = ('2af98138d473', '3e66512bc8bf')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
