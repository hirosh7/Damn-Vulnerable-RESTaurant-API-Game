"""Add phone verification

Revision ID: a1b2c3d4e5f6
Revises: f23331e973f8
Create Date: 2026-02-03 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "f23331e973f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add phone verification fields to users table"""
    # Add phone_verified column (default False for new users)
    op.add_column(
        "users",
        sa.Column("phone_verified", sa.Boolean(), nullable=False, server_default="0")
    )
    
    # Add phone_verification_code column
    op.add_column(
        "users",
        sa.Column("phone_verification_code", sa.String(), nullable=True)
    )
    
    # Add phone_verification_code_expiry column
    op.add_column(
        "users",
        sa.Column("phone_verification_code_expiry", sa.DateTime(), nullable=True)
    )
    
    # For existing users (Chef, Employee roles), mark as verified since they were created
    # before phone verification was implemented
    op.execute("""
        UPDATE users 
        SET phone_verified = 1 
        WHERE role IN ('Chef', 'Employee')
    """)


def downgrade() -> None:
    """Remove phone verification fields from users table"""
    op.drop_column("users", "phone_verification_code_expiry")
    op.drop_column("users", "phone_verification_code")
    op.drop_column("users", "phone_verified")
