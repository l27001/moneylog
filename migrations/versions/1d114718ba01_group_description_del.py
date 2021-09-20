"""Group description del

Revision ID: 1d114718ba01
Revises: 1ec373170fe7
Create Date: 2021-09-20 17:27:54.259077

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1d114718ba01'
down_revision = '1ec373170fe7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('description', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128), nullable=False))
    # ### end Alembic commands ###
