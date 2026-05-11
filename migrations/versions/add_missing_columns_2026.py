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
    # Add missing columns to book table
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('openlibrary_id', sa.String(200), nullable=True))
        batch_op.add_column(sa.Column('page_count', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('publish_year', sa.Integer(), nullable=True))

    # Add missing avatar column to user table
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.String(255), nullable=True))


def downgrade():
    # Remove columns from user table
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('avatar')

    # Remove columns from book table
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('publish_year')
        batch_op.drop_column('page_count')
        batch_op.drop_column('openlibrary_id')
