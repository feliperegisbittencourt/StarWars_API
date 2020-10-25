"""empty message

Revision ID: db7b25f48589
Revises: 
Create Date: 2020-10-25 18:22:42.816061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db7b25f48589'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('planets', sa.Column('planetsid', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'planets', ['planetname'])
    op.drop_column('planets', 'planetid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('planets', sa.Column('planetid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'planets', type_='unique')
    op.drop_column('planets', 'planetsid')
    # ### end Alembic commands ###
