"""empty message

Revision ID: 82a52a67209f
Revises: 899d4b542e10
Create Date: 2021-09-17 16:34:31.918035

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '82a52a67209f'
down_revision = '899d4b542e10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('group', 'name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               nullable=False)
    op.alter_column('money_log', 'group_id',
               existing_type=mysql.SMALLINT(display_width=6),
               nullable=False)
    op.alter_column('money_log', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('money_log', 'cost',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_index('ix_money_log_cost', table_name='money_log')
    op.create_index(op.f('ix_money_log_group_id'), 'money_log', ['group_id'], unique=False)
    op.create_index(op.f('ix_money_log_user_id'), 'money_log', ['user_id'], unique=False)
    op.drop_constraint('money_log_ibfk_1', 'money_log', type_='foreignkey')
    op.drop_constraint('money_log_ibfk_2', 'money_log', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('money_log_ibfk_2', 'money_log', 'user', ['user_id'], ['id'])
    op.create_foreign_key('money_log_ibfk_1', 'money_log', 'group', ['group_id'], ['id'])
    op.drop_index(op.f('ix_money_log_user_id'), table_name='money_log')
    op.drop_index(op.f('ix_money_log_group_id'), table_name='money_log')
    op.create_index('ix_money_log_cost', 'money_log', ['cost'], unique=False)
    op.alter_column('money_log', 'cost',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('money_log', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('money_log', 'group_id',
               existing_type=mysql.SMALLINT(display_width=6),
               nullable=True)
    op.alter_column('group', 'name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               nullable=True)
    # ### end Alembic commands ###