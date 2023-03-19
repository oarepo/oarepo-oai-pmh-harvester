import gzip
from pathlib import Path
from typing import Iterator

import yaml
from oarepo_runtime.datastreams import BaseReader, StreamEntry
from oarepo_runtime.tasks.datastreams import _deserialize_entries


class OAIDirReader(BaseReader):
    def __iter__(self) -> Iterator[StreamEntry]:
        parent_dir = Path(self.source)
        files = list(parent_dir.glob("*.yaml.gz"))
        files.sort()
        for f in files:
            with gzip.open(f, "rt") as ff:
                yield from _deserialize_entries(yaml.safe_load(ff))
