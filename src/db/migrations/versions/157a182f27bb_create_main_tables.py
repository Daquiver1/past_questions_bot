"""create main tables

Revision ID: 157a182f27bb
Revises:
Create Date: 2024-01-26 06:11:04.247982

"""

from typing import Optional, Sequence, Tuple, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = "157a182f27bb"
down_revision: Optional[str] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    """Create timestamp in DB."""
    return (
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=func.now()
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),
    )


def create_users_table() -> None:
    """Create users table."""
    op.create_table(
        "users",
        sa.Column(
            "telegram_id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
            unique=True,
            index=True,
        ),
        sa.Column("username", sa.String(), index=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String()),
        *timestamps(),
    )


def create_past_questions_table() -> None:
    """Create past questions table."""
    op.create_table(
        "past_questions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("course_code", sa.String(), index=True, nullable=False),
        sa.Column("course_name", sa.String(), index=True, nullable=False),
        sa.Column("course_title", sa.String(), index=True, nullable=False),
        sa.Column("lecturer_name", sa.String(), index=True, nullable=False),
        sa.Column("past_question_url", sa.String(), nullable=False),
        sa.Column("semester", sa.String(), index=True, nullable=False),
        sa.Column("year", sa.String(), index=True, nullable=False),
        *timestamps(),
    )


def create_subscriptions_table() -> None:
    """Create subscriptions table."""
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True, nullable=False),
        sa.Column(
            "user_telegram_id",
            sa.Integer(),
            sa.ForeignKey("users.telegram_id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("transaction_id", sa.String, nullable=False),
        sa.Column("tier", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, index=True, default=True),
        sa.Column(
            "balance", sa.Numeric(precision=10, scale=2), nullable=False, default=0
        ),
        *timestamps(),
        sa.CheckConstraint(
            "tier IN ('Basic', 'Standard', 'Premium')",
            name="tier check",
        ),
    )


def create_subscription_history_table() -> None:
    """Create subscription history table."""
    op.create_table(
        "subscription_history",
        sa.Column("id", sa.Integer(), primary_key=True, index=True, nullable=False),
        sa.Column(
            "subscription_id",
            sa.Integer(),
            sa.ForeignKey("subscriptions.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "user_telegram_id",
            sa.Integer(),
            sa.ForeignKey("users.telegram_id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("transaction_id", sa.String, nullable=False),
        sa.Column("tier", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, index=True, default=True),
        sa.Column(
            "amount", sa.Numeric(precision=10, scale=2), nullable=False, default=0
        ),
        *timestamps(),
        sa.CheckConstraint(
            "tier IN ('Basic', 'Standard', 'Premium')",
            name="tier check",
        ),
    )


def create_downloads_table() -> None:
    """Create downloads table."""
    op.create_table(
        "downloads",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "user_telegram_id",
            sa.Integer(),
            sa.ForeignKey("users.telegram_id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "past_question_id",
            sa.Integer(),
            sa.ForeignKey("past_questions.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        *timestamps(),
    )


def create_help_tickets_table() -> None:
    """Create help tickets table."""
    op.create_table(
        "help_tickets",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "user_telegram_id",
            sa.Integer(),
            sa.ForeignKey("users.telegram_id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.String(),
            nullable=False,
        ),
        *timestamps(),
        sa.CheckConstraint(
            "status IN ('open', 'in_progress', 'resolved', 'closed')",
            name="status_check",
        ),
    )


def upgrade() -> None:
    """Upgrade DB."""
    create_users_table()
    create_past_questions_table()
    create_downloads_table()
    create_subscriptions_table()
    create_subscription_history_table()
    create_help_tickets_table()


def downgrade() -> None:
    """Downgrade DB."""
    op.drop_table("downloads")
    op.drop_table("help_tickets")
    op.drop_table("past_questions")
    op.drop_table("subscription_history")
    op.drop_table("subscriptions")
    op.drop_table("users")
