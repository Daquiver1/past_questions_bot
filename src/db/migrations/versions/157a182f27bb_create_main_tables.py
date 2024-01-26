"""create main tables

Revision ID: 157a182f27bb
Revises:
Create Date: 2024-01-26 06:11:04.247982

"""
from typing import Optional, Sequence, Tuple, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "157a182f27bb"
down_revision: Optional[str] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_updated_at_trigger() -> None:
    """Update timestamp trigger."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


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
    """Create users table."""
    op.create_table(
        "users",
        sa.Column(
            "telegram_id",
            sa.String(),
            primary_key=True,
            nullable=False,
            unique=True,
            index=True,
        ),
        sa.Column("username", sa.String(), index=True),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_time
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def create_past_questions_table() -> None:
    """Create past questions table."""
    op.create_table(
        "past_questions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("course_code", sa.String(), index=True, nullable=False),
        sa.Column("course_name", sa.String(), index=True, nullable=False),
        sa.Column("lecturer_name", sa.String(), index=True, nullable=False),
        sa.Column("past_question_url", sa.String(), nullable=False),
        sa.Column("semester", sa.String(), index=True, nullable=False),
        sa.Column("year", sa.String(), index=True, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_past_questions_time
            BEFORE UPDATE
            ON past_questions
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def create_downloads_table() -> None:
    """Create downloads table."""
    op.create_table(
        "downloads",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "telegram_id",
            sa.String(),
            sa.ForeignKey("users.telegram_id"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "past_question_id",
            sa.Integer(),
            sa.ForeignKey("past_questions.id"),
            nullable=False,
            index=True,
        ),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_downloads_time
            BEFORE UPDATE
            ON downloads
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def create_help_ticket_status_enum() -> None:
    """Create enum type for status."""
    status_enum = sa.Enum(
        "open", "in_progress", "resolved", "closed", name="help_ticket_status_enum"
    )
    status_enum.create(op.get_bind(), checkfirst=True)


def create_help_tickets_table() -> None:
    """Create help tickets table."""
    op.create_table(
        "help_tickets",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "telegram_id",
            sa.String(),
            sa.ForeignKey("users.telegram_id"),
            nullable=False,
            index=True,
        ),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "open",
                "in_progress",
                "resolved",
                "closed",
                name="help_ticket_status_enum",
                metadata=sa.MetaData(),
                create_type=False,
            ),
            nullable=False,
        ),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_help_tickets_time
            BEFORE UPDATE
            ON help_tickets
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def upgrade() -> None:
    """Upgrade DB."""
    create_updated_at_trigger()
    create_users_table()
    create_past_questions_table()
    create_downloads_table()
    create_help_ticket_status_enum()
    create_help_tickets_table()


def downgrade() -> None:
    """Downgrade DB."""
    op.drop_table("downloads")
    op.drop_table("help_tickets")
    op.drop_table("past_questions")
    op.drop_table("users")

    op.execute("DROP TYPE help_ticket_status_enum")
    op.execute("DROP FUNCTION update_updated_at_column")
