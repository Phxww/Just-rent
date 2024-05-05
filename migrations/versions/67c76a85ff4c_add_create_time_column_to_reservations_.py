"""add create time column to reservations table

Revision ID: 67c76a85ff4c
Revises: d7f46cb373ce
Create Date: 2024-05-01 09:39:37.388615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67c76a85ff4c'
down_revision = 'd7f46cb373ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
