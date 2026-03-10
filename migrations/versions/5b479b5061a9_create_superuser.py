"""create_superuser

Revision ID: 5b479b5061a9
Revises: 9cc92b5c7e39
Create Date: 2026-03-10 23:33:27.526510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from api.core.security import hash_password
from api.config import settings

# revision identifiers, used by Alembic.
revision: str = '5b479b5061a9'
down_revision: Union[str, Sequence[str], None] = '9cc92b5c7e39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'users'


def upgrade():
    bind = op.get_bind()

    hashed_password = hash_password(settings.superuser_password)

    bind.execute(
        sa.text(f"""
            INSERT INTO {table_name} (username, hashed_password, is_admin)
            VALUES ('{settings.superuser_name}', '{hashed_password}', true)
        """)
    )


def downgrade():
    bind = op.get_bind()
    bind.execute(
        sa.text(
            f"DELETE FROM {table_name} WHERE username = '{settings.superuser_name}'"
        )
    )
