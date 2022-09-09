"""empty message

Revision ID: cd8189b7f472
Revises: 
Create Date: 2022-05-14 14:38:42.477300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd8189b7f472'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('focus_symbol',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('exchange', sa.String(length=10), nullable=False),
    sa.Column('symbol_A', sa.String(length=10), nullable=False),
    sa.Column('symbol_B', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('exchange', 'symbol_A', 'symbol_B')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('focus_symbol')
    # ### end Alembic commands ###
