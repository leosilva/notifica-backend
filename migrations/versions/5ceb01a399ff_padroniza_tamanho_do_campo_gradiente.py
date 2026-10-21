"""padroniza tamanho do campo gradiente

Revision ID: 5ceb01a399ff
Revises: 3c7b63c1547f
Create Date: 2026-10-21 14:16:50.147199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ceb01a399ff'
down_revision = '3c7b63c1547f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('noticia', schema=None) as batch_op:
        batch_op.alter_column(
            'gradiente',
            existing_type=sa.Text(),
            type_=sa.String(length=500),
            existing_nullable=True
        )

    with op.batch_alter_table('postagem', schema=None) as batch_op:
        batch_op.alter_column(
            'gradiente',
            existing_type=sa.String(length=64),
            type_=sa.String(length=500),
            existing_nullable=True
        )


def downgrade():
    with op.batch_alter_table('postagem', schema=None) as batch_op:
        batch_op.alter_column(
            'gradiente',
            existing_type=sa.String(length=500),
            type_=sa.String(length=64),
            existing_nullable=True
        )

    with op.batch_alter_table('noticia', schema=None) as batch_op:
        batch_op.alter_column(
            'gradiente',
            existing_type=sa.String(length=500),
            type_=sa.Text(),
            existing_nullable=True
        )
