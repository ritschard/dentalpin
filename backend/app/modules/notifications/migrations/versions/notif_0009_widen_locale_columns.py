"""notifications: widen locale columns to fit script-tagged codes (notif_0009).

``notification_templates.locale`` and ``notification_preferences.preferred_locale``
were VARCHAR(5) — enough for ``es`` or ``pt-BR`` but not for the
script-tagged Serbian locales (``sr-Cyrl`` / ``sr-Latn``, 7 chars): a clinic
template or patient preference in either would fail with "value too long".
Widened to 10, matching ``patients.preferred_language``.

Downgrade narrows back to 5 and refuses to run while a longer code is
stored, rather than truncating ``sr-Cyrl`` into a meaningless ``sr-Cy``.

Revision ID: notif_0009
Revises: notif_0008
Create Date: 2026-10-21
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "notif_0009"
down_revision: str | None = "notif_0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

COLUMNS: tuple[tuple[str, str], ...] = (
    ("notification_templates", "locale"),
    ("notification_preferences", "preferred_locale"),
)


def upgrade() -> None:
    for table, column in COLUMNS:
        op.alter_column(
            table,
            column,
            type_=sa.String(length=10),
            existing_type=sa.String(length=5),
            existing_nullable=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    for table, column in COLUMNS:
        too_long = bind.execute(
            sa.text(f"SELECT count(*) FROM {table} WHERE length({column}) > 5")
        ).scalar_one()
        if too_long:
            raise RuntimeError(
                f"{table}.{column} holds {too_long} locale code(s) longer than 5 "
                "characters (e.g. sr-Cyrl); change or delete them before downgrading."
            )
        op.alter_column(
            table,
            column,
            type_=sa.String(length=5),
            existing_type=sa.String(length=10),
            existing_nullable=False,
        )
