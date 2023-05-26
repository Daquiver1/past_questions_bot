"""Create main tables

Revision ID: ccf36cec622e
Revises:
Create Date: 2023-05-26 19:05:17.551904

"""
from alembic import op
from typing import Tuple

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccf36cec622e'
down_revision = None
branch_labels = None
depends_on = None


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    """Create timestamp in DB."""
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_users_table() -> None:
    """Create User table."""
    op.create_table(
        "users",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("telegram_id", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("is_subscribed", sa.Integer, nullable=False, default=0),
        sa.Column(
            "is_eligible", sa.Integer, nullable=False, default=0
        ),
        *timestamps(),
    )
    op.execute("DROP TRIGGER IF EXISTS update_timestamp")
    op.execute(
        """
        CREATE TRIGGER update_timestamp
        AFTER UPDATE ON users
        FOR EACH ROW
        BEGIN
            UPDATE users
            SET updated_at = datetime('now')
            WHERE id = OLD.id;
        END;
        """
    )


def create_past_questions_table() -> None:
    """Create User table."""
    op.create_table(
        "past_questions",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("course_code", sa.String, nullable=False, index=True),
        sa.Column("course_description", sa.String, nullable=False, index=True),
        sa.Column("past_question_url", sa.String, nullable=False),
        sa.Column("lecturer", sa.String, nullable=False, index=True),
        sa.Column("year", sa.String, nullable=False, index=True),
        sa.Column("semester", sa.String, nullable=False, index=True),
        *timestamps(),
    )
    op.execute("DROP TRIGGER IF EXISTS update_timestamp")
    op.execute(
        """
        CREATE TRIGGER update_timestamp
        AFTER UPDATE ON past_questions
        FOR EACH ROW
        BEGIN
            UPDATE past_questions
            SET updated_at = datetime('now')
            WHERE id = OLD.id;
        END;
        """
    )


def upgrade() -> None:
    create_users_table()
    create_past_questions_table()


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("past_questions")