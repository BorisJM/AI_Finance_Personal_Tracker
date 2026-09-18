"""initial migration

Revision ID: 0abb102c7bfb
Revises:
Create Date: 2026-09-18 20:26:17.809953
"""

from hashlib import sha256

from alembic import op
import sqlalchemy as sa


revision = "0abb102c7bfb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # SQLite nie obsługuje bezpośredniego ALTER COLUMN,
    # dlatego używamy batch_alter_table.

    with op.batch_alter_table("category") as batch_op:
        batch_op.alter_column(
            "color",
            existing_type=sa.VARCHAR(length=6),
            type_=sa.String(length=9),
            existing_nullable=False,
        )

    # Dodajemy identifier jako nullable, ponieważ tabela
    # może już zawierać istniejące transakcje.
    op.add_column(
        "transaction",
        sa.Column(
            "transaction_identifier",
            sa.String(length=64),
            nullable=True,
        ),
    )

    connection = op.get_bind()

    transactions = connection.execute(
        sa.text("""
                SELECT id,
                       currency,
                       transaction_date,
                       amount,
                       merchant_id,
                       original_description,
                       cleaned_description,
                       category_id,
                       account_id,
                       transaction_type,
                       source_file_id,
                       counterparty_account
                FROM "transaction"
                """)
    ).fetchall()

    for transaction in transactions:
        values = "|".join(str(value) for value in transaction)

        identifier = sha256(
            values.encode("utf-8")
        ).hexdigest()

        connection.execute(
            sa.text("""
                    UPDATE "transaction"
                    SET transaction_identifier = :identifier
                    WHERE id = :id
                    """),
            {
                "identifier": identifier,
                "id": transaction.id,
            },
        )

    # Teraz, kiedy wszystkie istniejące rekordy mają identifier,
    # możemy zrobić kolumnę NOT NULL + UNIQUE.
    with op.batch_alter_table("transaction") as batch_op:
        batch_op.alter_column(
            "transaction_identifier",
            existing_type=sa.String(length=64),
            nullable=False,
        )

        batch_op.create_unique_constraint(
            "uq_transaction_transaction_identifier",
            ["transaction_identifier"],
        )


def downgrade():
    with op.batch_alter_table("transaction") as batch_op:
        batch_op.drop_constraint(
            "uq_transaction_transaction_identifier",
            type_="unique",
        )

        batch_op.drop_column("transaction_identifier")

    with op.batch_alter_table("category") as batch_op:
        batch_op.alter_column(
            "color",
            existing_type=sa.String(length=9),
            type_=sa.VARCHAR(length=6),
            existing_nullable=False,
        )