"""Initial migration

Revision ID: e857f4f9eb94
Revises: 
Create Date: 2020-04-12 14:10:21.260129+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e857f4f9eb94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('short', sa.String(length=32), nullable=True),
    sa.Column('target', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_urls_short'), 'urls', ['short'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_urls_short'), table_name='urls')
    op.drop_table('urls')
    # ### end Alembic commands ###