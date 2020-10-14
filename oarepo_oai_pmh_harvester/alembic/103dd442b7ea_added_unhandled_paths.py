#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Added unhandled paths"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '103dd442b7ea'
down_revision = 'e6e68975d321'
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('oarepo_oai_provider', sa.Column('unhandled_paths', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('oarepo_oai_provider', 'unhandled_paths')
    # ### end Alembic commands ###
