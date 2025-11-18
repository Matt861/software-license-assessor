import os
import re
from pathlib import Path
from typing import Union, Callable

_YEAR_OR_RANGE_RE = re.compile(
    r"\b(19|20)\d{2}(?:\s*[-–]\s*(19|20)\d{2})?\b"
)


def get_file_extension(path_or_filename):
    base = os.path.basename(path_or_filename)
    if base.startswith('.') and base.count('.') == 1:
        return base.lower()
    ext = os.path.splitext(base)[1]
    return ext.lower() if ext else base.lower()


def to_text(content: Union[str, bytes]) -> str:
    """
    Ensure we are working with a text string.
    If content is bytes, decode as UTF-8 (ignoring errors).
    """
    if isinstance(content, str):
        return content
    return content.decode("utf-8", errors="ignore")


def normalize_without_empty_lines(text: str) -> str:
    """
    Normalize text by:
      - Stripping leading/trailing whitespace
      - Removing completely empty lines (lines where line.strip() == "")
    """
    text = text.strip()
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip() != ""]
    return "\n".join(non_empty_lines)


def normalize_without_empty_lines_and_dates(text: str) -> str:
    """
    Normalize text for matching by:
      - Stripping leading/trailing whitespace
      - Removing completely empty lines
      - Removing 4-digit years and year ranges (e.g., 1999-2024)
      - Collapsing multiple spaces
      - Collapsing multiple newlines
    """
    # Strip outer whitespace
    text = text.strip()

    # Remove empty lines
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip() != ""]
    text = "\n".join(non_empty_lines)

    # Remove years and year ranges
    text = _YEAR_OR_RANGE_RE.sub("", text)

    # Collapse multiple spaces/tabs into a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse multiple newlines into a single newline
    text = re.sub(r"\n+", "\n", text)

    # Final strip
    return text.strip()


def get_file_name_from_path_without_extension(path: Path) -> str:
    """
    Strip everything before the last path separator and remove the file extension.
    Works with both '\\' and '/' as separators.
    """
    # Get the last part after any slash or backslash
    filename = re.split(r"[\\/]", str(path))[-1]

    # Strip the extension
    name_without_ext, _ = os.path.splitext(filename)

    return name_without_ext


def to_windows_path(path: str | Path) -> str:
    """Return a string path using backslashes."""
    return str(path).replace("/", "\\")


def to_backslash_path(path: str) -> str:
    # Convert to a Path (handles things like ".", "..", etc.)
    p = Path(path)
    # Get the string form and replace any forward slashes with backslashes
    return str(p).replace("/", "\\")


def read_file_to_string(file_path: str) -> str:
    """Read the entire contents of a text file into a single string."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def placeholder_to_regex(text: str) -> str:
    """
    Converts placeholders in license_text to regex patterns.
    Recognizes placeholders like [yyyy], [year], [name of copyright owner], <year>, <name of author>, etc.
    """
    text = normalize_without_empty_lines_and_dates(text)
    # Replace [yyyy], [year], <year> with a year pattern (4 digits)
    text = re.sub(r"(\[yyyy\]|\[year\]|<year>)", r"\\d{4}", text)
    # Replace [name of copyright owner], <name of copyright owner>, <name of author>, etc. with any non-newline pattern
    text = re.sub(r"(\[name of copyright owner\]|<name of copyright owner>|<name of author>)", r".+?", text)
    # Remove the literal strings <!-- and -->
    text = re.sub(r'<!--|-->', '', text)
    # Replace generic bracket or angle placeholders: [.*?] or <.*?>
    text = re.sub(r"\[[^\[\]]+?\]", r".+?", text)
    text = re.sub(r"<[^<>]+?>", r".+?", text)
    # Escape special regex characters except for our replacements
    text = re.escape(text)
    # Unescape the regex patterns we inserted
    text = text.replace(r"\d{4}", r"\d{4}").replace(r"\.\+\?", r".+?")

    return text