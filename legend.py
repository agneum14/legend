from dataclasses import dataclass
import os
import sys

from tinytag import TinyTag
from functional import seq


@dataclass
class Metadata:
    folder: str
    artist: str
    album: str
    year: str
    depth: int


def metadata(dir: str) -> Metadata:
    flacs = [os.path.join(dp, f) for dp, dn, filenames in os.walk(
        dir) for f in filenames if os.path.splitext(f)[1] == '.flac']
    if not flacs:
        return None

    flac = flacs.pop()
    tag: TinyTag = TinyTag.get(flac)

    folder = dir
    artist = tag.artist
    album = tag.album
    year = tag.year
    depth = tag.bitdepth

    return Metadata(folder, artist, album, year, depth)


def name(meta: Metadata) -> str:
    return "{} - {} ({}) [FLAC {}bit]".format(meta.album, meta.artist, meta.year, meta.depth)


if __name__ == '__main__':
    metas = seq(sys.argv[1:]).map(metadata).filter(lambda x: x)
    for meta in metas:
        new_name = name(meta)
        print(new_name)
