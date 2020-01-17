#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create invenio-oarepo-oai-pmh-harvester"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9968e56e476f'
down_revision = None
branch_labels = ('invenio_oarepo_oai_pmh_harvester',)
depends_on = None


def upgrade():
    """Upgrade database."""
    pass


def downgrade():
    """Downgrade database."""
    pass
