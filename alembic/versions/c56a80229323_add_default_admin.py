"""add default admin

Revision ID: c56a80229323
Revises: 8b12a4aa6961
Create Date: 2025-11-30 10:59:19.511015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from utils.hasher import get_password_hash
from models.user_models import UserInDB, UserRole, UserStatus
from utils.session import SessionLocal 


# revision identifiers, used by Alembic.
revision: str = 'c56a80229323'
down_revision: Union[str, Sequence[str], None] = '8b12a4aa6961'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD = "admin"

def upgrade():
    session = SessionLocal()
    # Check if the admin user already exists
    admin_exists = session.query(UserInDB).filter(UserInDB.email == ADMIN_EMAIL).first()

    if not admin_exists:
        # Create the admin user if not exists
        admin_user = UserInDB(
            email = ADMIN_EMAIL, 
            password=get_password_hash(ADMIN_PASSWORD),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        session.add(admin_user)
        session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

def downgrade():
    session = SessionLocal()

    # Optionally, remove the admin user when rolling back the migration
    admin_user = session.query(UserInDB).filter(UserInDB.email == ADMIN_EMAIL).first()
    if admin_user:
        session.delete(admin_user)
        session.commit()
        print("Admin user removed.")