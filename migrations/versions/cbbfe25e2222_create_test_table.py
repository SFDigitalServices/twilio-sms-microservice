# pylint: skip-file
"""create test table

Revision ID: cbbfe25e2222
Revises: 
Create Date: 2020-07-09 17:04:06.526263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbbfe25e2222'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'testtable',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True)),
        sa.Column('data', sa.JSON)
    )



def downgrade():
    op.drop_table('testtable')
