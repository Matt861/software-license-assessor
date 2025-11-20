#!/usr/bin/env python3
import shutil
import zipfile
import tarfile
from pathlib import Path


def _looks_like_hex_hash(name: str) -> bool:
    """
    Heuristic: filename looks like a hash (Docker/OCI layers often do this).
    We treat any reasonably long, all-hex string with no extension as a candidate.
    """
    name = name.lower()
    if not (32 <= len(name) <= 128):
        return False
    return all(c in "0123456789abcdef" for c in name)


def is_multi_archive(path: Path) -> bool:
    """Return True if this path is treated as a multi-file archive."""
    name = path.name.lower()

    # Common multi-file archives by extension
    if name.endswith((".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz")):
        return True
    if path.suffix.lower() in {".zip", ".tar"}:
        return True

    # Special rule for .gz:
    #   - name has another extension before .gz -> single-file compression
    #   - otherwise -> treat as multi-file archive (e.g., "compress1.gz")
    if path.suffix.lower() == ".gz" and "." not in path.stem:
        return True

    # --- NEW: detect hash-named layer files with no extension that are tar archives ---
    # Many Docker/OCI layers are stored as tar files with filenames such as:
    #   "a3b55f0c1c7c4c92f8d8a8c2c8f5fe..." (hex hash, no extension)
    if path.suffix == "" and _looks_like_hex_hash(path.name):
        try:
            if tarfile.is_tarfile(path):
                return True
        except Exception:
            # If anything goes wrong, just don't treat it as a multi archive
            pass

    return False


def strip_multi_suffix(rel_path: Path) -> Path:
    """
    For multi-file archives, strip the archive extension(s) to get the
    directory name.

    Examples:
      src/test/compress1.tar.gz -> src/test/compress1
      src/test/compress1.tgz    -> src/test/compress1
      src/test/compress1.gz     -> src/test/compress1
    """
    s = str(rel_path)
    lower = s.lower()

    # Compound tar extensions
    for suf in (".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz"):
        if lower.endswith(suf):
            return Path(s[:-len(suf)])

    # Fallback: remove just the last suffix
    return rel_path.with_suffix("")


def safe_extract_tar(tar_obj: tarfile.TarFile, path: Path) -> None:
    """
    Safely extract a tarfile to 'path' by preventing path traversal.
    """
    path = path.resolve()
    for member in tar_obj.getmembers():
        member_path = (path / member.name).resolve()
        if not str(member_path).startswith(str(path)):
            raise Exception("Unsafe path in tar archive (path traversal attempt)")
    tar_obj.extractall(path)


def safe_extract_zip(zf: zipfile.ZipFile, path: Path) -> None:
    """
    Safely extract a zipfile to 'path' by preventing path traversal.
    """
    path = path.resolve()
    for info in zf.infolist():
        # Directories: just ensure they exist
        if info.is_dir():
            (path / info.filename).resolve().mkdir(parents=True, exist_ok=True)
            continue

        dest = (path / info.filename).resolve()
        if not str(dest).startswith(str(path)):
            raise Exception("Unsafe path in zip archive (path traversal attempt)")

        dest.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(info, "r") as src, open(dest, "wb") as dst:
            shutil.copyfileobj(src, dst)


def extract_multi(src_file: Path, dest_root: Path, rel_path: Path) -> None:
    """
    Extract a multi-file archive.

    The archive at rel_path is extracted to a directory with the same path
    minus the archive extension(s).

    Special flattening:
    - If the archive base name matches a single top-level directory inside
      the archive, we flatten that extra directory level.
      e.g. example.zip containing "example/..." -> example/..., not example/example/...
    """
    target_dir_rel = strip_multi_suffix(rel_path)
    target_dir = dest_root / target_dir_rel
    target_dir.mkdir(parents=True, exist_ok=True)

    base_name = target_dir_rel.name  # e.g. "example" from "example.zip"

    # zip?
    if zipfile.is_zipfile(src_file):
        with zipfile.ZipFile(src_file, "r") as zf:
            # Detect single top-level directory name in the archive
            names = [i.filename for i in zf.infolist() if i.filename]
            top_levels = set(
                n.split("/", 1)[0].rstrip("/")
                for n in names
                if n and not n.startswith("__MACOSX")
            )

            # If the only top-level name matches the base name, flatten one level
            if len(top_levels) == 1:
                only = next(iter(top_levels))
                if only == base_name:
                    # Flatten: extract into the parent of target_dir
                    target_dir = target_dir.parent
                    target_dir.mkdir(parents=True, exist_ok=True)

            safe_extract_zip(zf, target_dir)
        return

    # tar? (auto-detect compression; works for .tar, .tar.gz, etc.)
    if tarfile.is_tarfile(src_file):
        with tarfile.open(src_file, mode="r:*") as tf:
            names = [m.name for m in tf.getmembers() if m.name]
            top_levels = set(
                n.split("/", 1)[0].rstrip("/")
                for n in names
                if n and n not in (".", "/")
            )

            if len(top_levels) == 1:
                only = next(iter(top_levels))
                if only == base_name:
                    target_dir = target_dir.parent
                    target_dir.mkdir(parents=True, exist_ok=True)

            safe_extract_tar(tf, target_dir)
        return

    # If we got here, we thought it was multi, but Python doesn't recognize it.
    # Fall back to copying it as a normal file.
    dest_file = dest_root / rel_path
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_file, dest_file)