#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Remove oai-identifier from oai_record_exc"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0daaf698ec07'
down_revision = '9438b43e3f51'
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_oai_record_exc_oai_identifier', 'oai_record_exc', type_='unique')
    op.drop_column('oai_record_exc', 'oai_identifier')
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('oai_record_exc', sa.Column('oai_identifier', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint('uq_oai_record_exc_oai_identifier', 'oai_record_exc', ['oai_identifier'])
    # ### end Alembic commands ###
