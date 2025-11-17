#!/usr/bin/env python3

import shutil
import gzip
import bz2
import lzma
from pathlib import Path



def is_single_compressed(path: Path) -> bool:
    """Return True if this path is treated as a single-file compressed file."""
    suffix = path.suffix.lower()

    if suffix in {".bz2", ".xz", ".lzma"}:
        return True

    if suffix == ".gz":
        # If there's another extension before .gz (e.g. ".txt.gz"), treat as single-file
        return "." in path.stem

    return False


def decompress_single(src_file: Path, dest_file: Path) -> None:
    """Decompress single-file compressed src_file to dest_file."""
    dest_file.parent.mkdir(parents=True, exist_ok=True)

    openers = {
        ".gz": gzip.open,
        ".bz2": bz2.open,
        ".xz": lzma.open,
        ".lzma": lzma.open,
    }

    opener = openers.get(src_file.suffix.lower())
    if opener is None:
        raise ValueError(f"Unsupported single-file compression: {src_file}")

    with opener(src_file, "rb") as f_in, open(dest_file, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)