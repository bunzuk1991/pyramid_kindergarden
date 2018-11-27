"""updated table organisation1

Revision ID: 8b9c2705dede
Revises: 731acdda2975
Create Date: 2018-11-22 21:31:57.922871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b9c2705dede'
down_revision = '731acdda2975'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('organisation', sa.Column('address', sa.UnicodeText, nullable=True, default=""))
    op.add_column('organisation', sa.Column('kod_zkpo', sa.UnicodeText, default="", nullable=True))
    op.add_column('organisation', sa.Column('kod_ipn', sa.UnicodeText, default="", nullable=True))
    op.add_column('organisation', sa.Column('disabled', sa.Boolean, server_default=sa.text('FALSE'), nullable=True))


def downgrade():
    op.drop_column('organisation', 'address')
    op.drop_column('organisation', 'kod_zkpo')
    op.drop_column('organisation', 'kod_ipn')
    op.drop_column('organisation', 'disabled')
