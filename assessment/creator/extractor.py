#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from assessment.creator import archive_extractor, compression_extractor
from configuration import Configuration as Config


def is_ignored_dir(src_dir: Path) -> bool:
    src_dir_str = str(src_dir)
    for ignore_dir in Config.ignore_dirs:
        if ignore_dir in str(src_dir_str):
            return True
    return False


def classify(path: Path) -> str:
    """
    Classify the file:
    - "multi"   -> multi-file archive
    - "single"  -> single-file compression
    - "none"    -> normal file
    """
    if archive_extractor.is_multi_archive(path):
        return "multi"
    if compression_extractor.is_single_compressed(path):
        return "single"
    return "none"


def copy_or_extract_file(src_file: Path, dest_root: Path, rel_path: Path) -> None:
    """
    Handle a single file during the initial copy phase:
    - normal file: copy
    - single compressed: decompress to same path minus last extension
    - multi archive: extract as directory (contents only)
    """
    kind = classify(src_file)

    if kind == "none":
        dest_file = dest_root / rel_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dest_file)

    elif kind == "single":
        # e.g. src/test/witness/compress1.txt.gz -> compress1.txt
        dest_rel = rel_path.with_suffix("")  # drop only final extension
        dest_file = dest_root / dest_rel
        compression_extractor.decompress_single(src_file, dest_file)

    else:  # "multi"
        archive_extractor.extract_multi(src_file, dest_root, rel_path)


def copy_tree_with_extraction(src: Path, dest_root: Path) -> None:
    """
    Copy a directory from src to dest_root, extracting archives/compressed files
    encountered in src. This handles only archives present in the source tree
    itself; nested archives created by extraction are handled in a second phase.
    """
    if not src.is_dir():
        raise ValueError(f"copy_tree_with_extraction expects a directory, got {src}")

    for dirpath, dirnames, filenames in os.walk(src):
        dirpath = Path(dirpath)
        rel_dir = dirpath.relative_to(src)

        if is_ignored_dir(dirpath):
            continue

        for filename in filenames:
            src_file = dirpath / filename

            if rel_dir == Path("."):
                rel_path = Path(filename)
            else:
                rel_path = rel_dir / filename

            copy_or_extract_file(src_file, dest_root, rel_path)


# ---------- Nested extraction phase (in-place in destination) ----------

def extract_nested_archives(dest_root: Path) -> None:
    """
    Repeatedly scan dest_root for archive/compressed files and extract them
    in-place until no more remain.

    - For single-file compression: foo.txt.gz -> foo.txt (and remove .gz)
    - For multi-file archives:    foo.tar.gz -> foo/ (dir) and remove archive
    """
    while True:
        changed = False

        for dirpath, dirnames, filenames in os.walk(dest_root):
            dirpath = Path(dirpath)

            if is_ignored_dir(dirpath):
                continue

            for filename in filenames:
                abs_path = dirpath / filename
                kind = classify(abs_path)

                if kind == "none":
                    continue

                rel_path = abs_path.relative_to(dest_root)

                if kind == "single":
                    dest_rel = rel_path.with_suffix("")
                    dest_file = dest_root / dest_rel
                    compression_extractor.decompress_single(abs_path, dest_file)
                    abs_path.unlink()  # remove original compressed file
                    changed = True

                else:  # "multi"
                    archive_extractor.extract_multi(abs_path, dest_root, rel_path)
                    abs_path.unlink()  # remove original archive
                    changed = True

        if not changed:
            break


def main(source_dir, dest_dir):
    if source_dir.is_dir():
        # Normal directory: copy + first-level extraction, then nested extraction
        copy_tree_with_extraction(source_dir, dest_dir)

    elif source_dir.is_file():
        # Top-level is a single file (could be archive/compressed/normal):
        # Treat it as if it were a file inside a virtual root and process it,
        # then run nested extraction on whatever it produced.
        rel_path = Path(source_dir.name)
        copy_or_extract_file(source_dir, dest_dir, rel_path)

    else:
        raise ValueError(f"Source path {source_dir} is neither a file nor a directory")

    # Second phase: extract all nested archives/compressed files in-place
    extract_nested_archives(dest_dir)