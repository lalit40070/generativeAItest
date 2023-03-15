from alembic import op
import sqlalchemy as sa
from typing import Tuple
from sqlalchemy import func

revision = '5e58395622b2'
down_revision = None
branch_labels = None
depends_on = None

def create_updated_at_trigger() -> None:
    op.execute(
        """
    CREATE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS
    $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    )


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.current_timestamp(),
        ),
    )

def create_notification_table() -> None:
    op.create_table(
        "notifications",
        sa.Column("is_allowed", sa.Boolean, nullable=False, default=False),
        sa.Column("user_id", sa.String, unique=True, nullable=False, index=True),
        *timestamps(),
    )

def create_purchase_table() -> None:
    op.create_table(
        "purchases",
        sa.Column("purchase_id", sa.BigInteger, nullable=False, unique=True, index=True),
        sa.Column("user_identifier", sa.String, nullable=False, index=True),
        sa.Column("pack_id", sa.String, nullable=False, index=True),
        sa.Column("styles_list", sa.String, nullable=False, index=False),
        sa.Column("purchase_status", sa.String, nullable=False),
        *timestamps(),
    )

def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, nullable=False, index=True),
        sa.Column("identifier", sa.String, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("hashed_password", sa.Text),
        sa.Column("device_id",sa.Text, nullable=True),
        sa.Column("fcm_token",sa.Text, nullable=True),
        sa.Column("is_subscribed", sa.Boolean, nullable=False, default=False),
        sa.Column("auth_type", sa.Text, nullable=False),
        sa.Column("id_for_apple", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=True),
        *timestamps(),
    )

def create_packs_table() -> None:
    op.create_table(
        "packs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("pack_id", sa.String, unique=True, nullable=False, index=True),
        sa.Column("pack_name", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("pack_price", sa.Float, nullable=False),
        sa.Column("images_per_pack", sa.Integer,nullable=False),
        *timestamps(),
    )


def create_styles_table() -> None:
    op.create_table(
        "style",
        sa.Column("style_id", sa.Integer, nullable=False, unique=True, index=True),
        sa.Column("name", sa.String, unique=False, nullable=False),
        sa.Column("prompt_positive", sa.String, nullable=True),
        sa.Column("prompt_negative", sa.String, nullable=True),
        sa.Column("seed", sa.BigInteger, nullable=True),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("gender", sa.String, nullable=False),
        sa.Column("sample_image", sa.String, nullable=False),
        sa.Column("diffusion_version", sa.String, nullable=True),
        
        *timestamps(),
    )

def create_image_table() -> None:
    op.create_table(
        "images",
        sa.Column("type", sa.String, nullable=False),
        sa.Column("url", sa.String, nullable=False, index=True),
        sa.Column("style", sa.Integer, nullable=False),
        sa.Column("user_identifier", sa.String, nullable=False, index=True),
        sa.Column("purchase_id", sa.BigInteger, nullable=False),
        *timestamps(),
    )

def create_tasks_table() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer,index=True, nullable=False, primary_key=True),
        sa.Column("purchase_id", sa.BigInteger, nullable=False, index=True),
        sa.Column("user_identifier", sa.String, nullable=False),
        sa.Column("style_list", sa.String, nullable=False, index=True),
        sa.Column("gender", sa.String, nullable=False),
        sa.Column("pack_id", sa.String, nullable=False),
        sa.Column("task_status", sa.String, nullable=False),
        *timestamps(),
    )

def upgrade() -> None:
    create_users_table()
    create_notification_table()
    create_packs_table()
    create_styles_table()
    create_purchase_table()
    create_image_table()
    create_tasks_table()


def downgrade() -> None:
    pass