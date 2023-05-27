"""Create main tables

Revision ID: ccf36cec622e
Revises:
Create Date: 2023-05-26 19:05:17.551904

"""
from typing import Tuple

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ccf36cec622e"
down_revision = None
branch_labels = None
depends_on = None


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    """Create timestamp in DB."""
    return (
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            index=indexed,
        ),
    )


def create_users_table() -> None:
    """Create User table."""
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer,
            primary_key=True,
        ),
        sa.Column("uuid", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("username", sa.Text, unique=True, index=True),
        sa.Column("telegram_id", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("is_subscribed", sa.Integer, nullable=False, default=0),
        sa.Column("is_eligible", sa.Integer, nullable=False, default=0),
        sa.Column("balance", sa.Float, nullable=False, default=0.0),
        *timestamps(),
    )
    op.execute("DROP TRIGGER IF EXISTS user_trigger_created_at")
    op.execute("DROP TRIGGER IF EXISTS user_trigger_updated_at")
    op.execute(
        """
            CREATE TRIGGER user_trigger_created_at
            AFTER INSERT ON users
            BEGIN
                UPDATE users SET created_at = DATETIME('now') where id = new.id;
                UPDATE users SET updated_at = DATETIME('now') where id = new.id;
            END;

"""
    )
    op.execute(
        """
          CREATE TRIGGER user_trigger_updated_at
            AFTER UPDATE ON users
            BEGIN
                UPDATE users SET updated_at = DATETIME('now') where id = new.id;
            END;
        """
    )


def create_past_question_categories_table() -> None:
    """Create Past Question Categories table."""
    op.create_table(
        "past_question_categories",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("uuid", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("category_name", sa.String, nullable=False, unique=True),
        *timestamps(),
    )
    op.execute("DROP TRIGGER IF EXISTS past_question_categories_trigger_created_at")
    op.execute("DROP TRIGGER IF EXISTS past_question_categories_trigger_updated_at")
    op.execute(
        """
            CREATE TRIGGER past_question_categories_trigger_created_at
            AFTER INSERT ON past_question_categories
            BEGIN
                UPDATE past_question_categories SET created_at = DATETIME('now') WHERE id = new.id;
                UPDATE past_question_categories SET updated_at = DATETIME('now') WHERE id = new.id;
            END;
"""
    )
    op.execute(
        """
          CREATE TRIGGER past_question_categories_trigger_updated_at
            AFTER UPDATE ON past_question_categories
            BEGIN
                update past_question_categories SET updated_at = DATETIME('now') WHERE id = new.id;
            END;
        """
    )


def create_past_questions_table() -> None:
    """Create Past Question table."""
    op.create_table(
        "past_questions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("uuid", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("course_code", sa.String, nullable=False, index=True),
        sa.Column("course_name", sa.String, nullable=False, index=True),
        sa.Column("past_question_url", sa.String, nullable=False),
        sa.Column("lecturer", sa.String, nullable=False, index=True),
        sa.Column("year", sa.String, nullable=False, index=True),
        sa.Column("semester", sa.String, nullable=False, index=True),
        sa.Column(
            "category_id",
            sa.Integer,
            sa.ForeignKey("past_question_categories.id", ondelete="CASCADE"),
        ),
        *timestamps(),
    )
    op.execute("DROP TRIGGER IF EXISTS past_question_trigger_created_at")
    op.execute("DROP TRIGGER IF EXISTS past_question_trigger_updated_at")
    op.execute(
        """
            CREATE TRIGGER past_question_trigger_created_at
            AFTER INSERT ON past_questions
            BEGIN
                UPDATE past_questions SET created_at = DATETIME('now') WHERE id = new.id;
                UPDATE past_questions SET updated_at = DATETIME('now') WHERE id = new.id;
            END;
"""
    )
    op.execute(
        """
          CREATE TRIGGER past_question_trigger_updated_at
            AFTER UPDATE ON past_questions
            BEGIN
                update past_questions SET updated_at = DATETIME('now') WHERE id = new.id;
            END;
        """
    )


def upgrade() -> None:
    create_users_table()
    create_past_question_categories_table()
    create_past_questions_table()


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("past_question_categories")
    op.drop_table("past_questions")
