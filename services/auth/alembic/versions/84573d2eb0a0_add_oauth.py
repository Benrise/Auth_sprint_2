"""add oauth

Revision ID: 84573d2eb0a0
Revises: 80fadf40fb89
Create Date: 2024-08-17 21:43:02.156274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84573d2eb0a0'
down_revision: Union[str, None] = '80fadf40fb89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oauth2_users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('oauth_id', sa.String(), nullable=False),
    sa.Column('provider', sa.String(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_oauth2_users_id'), 'oauth2_users', ['id'], unique=False)
    op.create_unique_constraint(None, 'login_history', ['id'])
    op.create_unique_constraint(None, 'roles', ['id'])
    op.add_column('users', sa.Column('is_oauth2', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'is_oauth2')
    op.drop_constraint(None, 'roles', type_='unique')
    op.drop_constraint(None, 'login_history', type_='unique')
    op.drop_index(op.f('ix_oauth2_users_id'), table_name='oauth2_users')
    op.drop_table('oauth2_users')
    # ### end Alembic commands ###
