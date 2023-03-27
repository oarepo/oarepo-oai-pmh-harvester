#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""initial revision"""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy.dialects import mysql, postgresql

# revision identifiers, used by Alembic.
revision = "b2a45c3a744e"
down_revision = "cecc281d2938"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "oaibatch_metadata",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oaibatch_metadata")),
    )
    op.create_table(
        "oaibatch_metadata_version",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id", "transaction_id", name=op.f("pk_oaibatch_metadata_version")
        ),
    )
    op.create_index(
        op.f("ix_oaibatch_metadata_version_end_transaction_id"),
        "oaibatch_metadata_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oaibatch_metadata_version_operation_type"),
        "oaibatch_metadata_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oaibatch_metadata_version_transaction_id"),
        "oaibatch_metadata_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "oaiharvester_metadata",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oaiharvester_metadata")),
    )
    op.create_table(
        "oaiharvester_metadata_version",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id", "transaction_id", name=op.f("pk_oaiharvester_metadata_version")
        ),
    )
    op.create_index(
        op.f("ix_oaiharvester_metadata_version_end_transaction_id"),
        "oaiharvester_metadata_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oaiharvester_metadata_version_operation_type"),
        "oaiharvester_metadata_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oaiharvester_metadata_version_transaction_id"),
        "oaiharvester_metadata_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "oairecord_metadata",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oairecord_metadata")),
    )
    op.create_table(
        "oairecord_metadata_version",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id", "transaction_id", name=op.f("pk_oairecord_metadata_version")
        ),
    )
    op.create_index(
        op.f("ix_oairecord_metadata_version_end_transaction_id"),
        "oairecord_metadata_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oairecord_metadata_version_operation_type"),
        "oairecord_metadata_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oairecord_metadata_version_transaction_id"),
        "oairecord_metadata_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "oairun_metadata",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_oairun_metadata")),
    )
    op.create_table(
        "oairun_metadata_version",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id", "transaction_id", name=op.f("pk_oairun_metadata_version")
        ),
    )
    op.create_index(
        op.f("ix_oairun_metadata_version_end_transaction_id"),
        "oairun_metadata_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oairun_metadata_version_operation_type"),
        "oairun_metadata_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oairun_metadata_version_transaction_id"),
        "oairun_metadata_version",
        ["transaction_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_oairun_metadata_version_transaction_id"),
        table_name="oairun_metadata_version",
    )
    op.drop_index(
        op.f("ix_oairun_metadata_version_operation_type"),
        table_name="oairun_metadata_version",
    )
    op.drop_index(
        op.f("ix_oairun_metadata_version_end_transaction_id"),
        table_name="oairun_metadata_version",
    )
    op.drop_table("oairun_metadata_version")
    op.drop_table("oairun_metadata")
    op.drop_index(
        op.f("ix_oairecord_metadata_version_transaction_id"),
        table_name="oairecord_metadata_version",
    )
    op.drop_index(
        op.f("ix_oairecord_metadata_version_operation_type"),
        table_name="oairecord_metadata_version",
    )
    op.drop_index(
        op.f("ix_oairecord_metadata_version_end_transaction_id"),
        table_name="oairecord_metadata_version",
    )
    op.drop_table("oairecord_metadata_version")
    op.drop_table("oairecord_metadata")
    op.drop_index(
        op.f("ix_oaiharvester_metadata_version_transaction_id"),
        table_name="oaiharvester_metadata_version",
    )
    op.drop_index(
        op.f("ix_oaiharvester_metadata_version_operation_type"),
        table_name="oaiharvester_metadata_version",
    )
    op.drop_index(
        op.f("ix_oaiharvester_metadata_version_end_transaction_id"),
        table_name="oaiharvester_metadata_version",
    )
    op.drop_table("oaiharvester_metadata_version")
    op.drop_table("oaiharvester_metadata")
    op.drop_index(
        op.f("ix_oaibatch_metadata_version_transaction_id"),
        table_name="oaibatch_metadata_version",
    )
    op.drop_index(
        op.f("ix_oaibatch_metadata_version_operation_type"),
        table_name="oaibatch_metadata_version",
    )
    op.drop_index(
        op.f("ix_oaibatch_metadata_version_end_transaction_id"),
        table_name="oaibatch_metadata_version",
    )
    op.drop_table("oaibatch_metadata_version")
    op.drop_table("oaibatch_metadata")
    # ### end Alembic commands ###