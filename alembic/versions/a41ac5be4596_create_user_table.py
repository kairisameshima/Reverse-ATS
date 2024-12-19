"""create user table

Revision ID: a41ac5be4596
Revises: 
Create Date: 2024-12-18 19:40:49.509888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a41ac5be4596'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('google_user_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('email', 'uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('google_user_id'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###