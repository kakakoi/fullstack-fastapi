import sqlalchemy as sa
from app.db.connect import metadata

user = sa.Table(
    "user",
    metadata,
    sa.Column("user_email", sa.String, primary_key=True),
    sa.Column("user_name", sa.String),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
)
