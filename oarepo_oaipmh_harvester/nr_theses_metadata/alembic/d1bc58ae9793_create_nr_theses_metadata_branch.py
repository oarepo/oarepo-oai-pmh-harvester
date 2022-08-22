#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create nr_theses_metadata branch."""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'd1bc58ae9793'
down_revision = None
branch_labels = ('nr_theses_metadata',)
depends_on = None


def upgrade():
    """Upgrade database."""
    pass


def downgrade():
    """Downgrade database."""
    pass
