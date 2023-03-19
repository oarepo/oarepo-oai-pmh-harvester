import functools
import sys

import click
from flask.cli import with_appcontext
from invenio_access.permissions import system_identity
from oarepo_runtime.cli import as_command, oarepo
from tqdm import tqdm

from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.oai_harvester.proxies import (
    current_service as harvester_service,
)


@oarepo.group(name="oai")
def oai():
    """Classifier commands."""


@oai.group(name="harvester")
def harvester():
    """OAI PMH harvester"""


def harvester_parameters(in_creation=False):
    def wrapper(f):
        @functools.wraps(f)
        @click.argument("code", required=True)
        @click.option("--name", help="OAI server name", required=in_creation)
        @click.option("--url", help="OAI base url", required=in_creation)
        @click.option("--set", help="OAI set", required=in_creation)
        @click.option("--prefix", help="OAI metadata prefix", required=in_creation)
        @click.option(
            "--loader",
            help="OAI metadata loader name",
            required=False,
            default="marcxml" if in_creation else None,
        )
        @click.option(
            "--transformer",
            help="Transformer name",
            required=in_creation,
            multiple=True,
        )
        @click.option("--writer", help="Writer name", required=in_creation)
        @click.option("--comment", help="Comment", default="" if in_creation else None)
        @click.option(
            "--max-records",
            help="Max records to download in one run",
            type=int,
            required=False,
        )
        @click.option(
            "--batch-size",
            help="Batch size for transformer/writer",
            type=int,
            default=100 if in_creation else None,
        )
        def wrapped(
            *,
            code=None,
            url=None,
            prefix=None,
            comment=None,
            name=None,
            set=None,
            loader=None,
            transformer=None,
            writer=None,
            max_records=None,
            batch_size=None,
            **kwargs,
        ):
            metadata = {
                "code": code,
                "baseurl": url,
                "metadataprefix": prefix,
                "comment": comment,
                "name": name,
                "setspecs": set,
                "loader": loader,
                "transformers": transformer,
                "writer": writer,
            }
            if max_records:
                metadata["max_records"] = max_records

            if batch_size:
                metadata["batch_size"] = batch_size

            f(metadata, **kwargs)

        return wrapped

    return wrapper


def _add_harvester(metadata):
    """Add a new harvester"""
    code = metadata["code"]
    harvester = False
    harvesters = list(
        harvester_service.scan(system_identity, params={"facets": {"code": [code]}})
    )

    if len(harvesters) > 0:
        harvester = harvesters[0]

    if harvester:
        print(f"Harvester with code {code} already exists")
        return harvester

    harvester = harvester_service.create(system_identity, metadata)

    harvester_service.indexer.refresh()
    return harvester


add = as_command(
    harvester, "add", harvester_parameters(True), with_appcontext, _add_harvester
)


@harvester.command()
@click.option("--code", help="OAI server code", required=True)
@with_appcontext
def delete(
    code,
):
    _delete_harvester(
        code,
    )


def _delete_harvester(code):
    harvesters = list(
        harvester_service.scan(system_identity, params={"facets": {"code": [code]}})
    )

    if len(harvesters) > 0:
        harvester_service.delete(system_identity, harvesters[0]["id"])

    harvester_service.indexer.refresh()


def _run_harvester(metadata, on_background, all_records, identifier):
    """Run/Start a harvester. Only the code is required, other arguments
    might be used to override harvester settings stored in the database"""
    code = metadata.pop("code")
    harvesters = list(
        harvester_service.scan(system_identity, params={"facets": {"code": [code]}})
    )

    if not harvesters:
        click.secho(
            f"Harvester with code {code} not found. Please create it at first with 'invenio oarepo harvester add' command",
            file=sys.stderr,
        )
        sys.exit(1)

    harvester = dict(harvesters[0])
    harvester.pop("links")
    harvester.pop("created")
    harvester.pop("updated")
    harvester.pop("revision_id")
    harvester.update({k: v for k, v in metadata.items() if v})

    click.secho(f"Running harvester {code} with parameters:", file=sys.stderr)
    for k, v in sorted(harvester.items()):
        click.secho(f"    {k:20s}: {v}", file=sys.stderr)

    with tqdm() as bar:
        last = [0]

        def progress(read, **kwargs):
            bar.update(read - last[0])
            last[0] = read

        harvest(
            harvester,
            all_records=all_records,
            on_background=on_background,
            identifiers=identifier or None,
            progress_callback=progress,
        )
    bar.close()


run = as_command(
    harvester,
    "run",
    click.option("--on-background/--on-foreground"),
    click.option("--all-records/--modified-records"),
    click.option("--identifier", multiple=True),
    harvester_parameters(False),
    with_appcontext,
    _run_harvester,
)
