import os
import re
from pathlib import Path
from typing import Dict, List
from assessment.scanner import utils
from input import license_header_keys
from configuration import Configuration as Config


# Regexes to detect year ranges and single years
YEAR_RANGE_RE = re.compile(r'\b(19|20)\d{2}\s*[-–]\s*(19|20)\d{2}\b')
YEAR_SINGLE_RE = re.compile(r'\b(19|20)\d{2}\b')


def normalize_c_style_file_header(header: str) -> str:
    """
    Remove Java block comment markers, line comment prefixes, and leading '*'
    characters, then normalize whitespace so the raw text can be compared.
    Handles both:
      - /** ... */ style
      - // ... style
    """
    lines = []
    for line in header.splitlines():
        stripped = line.strip()

        # Skip pure block comment delimiter lines like '/**', '/*', '*/'
        if stripped in ("/**", "/*", "*/"):
            continue

        # If block comment delimiters are on the same line as text, strip them
        if stripped.startswith("/**") or stripped.startswith("/*"):
            stripped = re.sub(r"^/\*+\s*", "", stripped)
        if stripped.endswith("*/"):
            stripped = re.sub(r"\s*\*+/$", "", stripped)

        # Remove leading '*' (Javadoc style) and following space
        if stripped.startswith("*"):
            stripped = stripped[1:].lstrip()

        # Handle single-line comment style: // ...
        if stripped.startswith("//"):
            stripped = stripped[2:].lstrip()

        lines.append(stripped)

    # Join and normalize all whitespace to single spaces
    text = "\n".join(lines)
    text = re.sub(r"\s+", " ", text).strip()
    text = remove_years_and_ranges(text)
    return text


def normalize_plain_text(text: str) -> str:
    """
    Normalize whitespace in a plain text block.
    """
    text = re.sub(r"\s+", " ", text).strip()
    text = remove_years_and_ranges(text)
    return text


def remove_years_and_ranges(text: str) -> str:
    """
    Remove year ranges (e.g., 1999-2022) and single years (e.g., 2024)
    from the text, then re-normalize whitespace.
    """
    # Remove year ranges first
    text = YEAR_RANGE_RE.sub("", text)
    # Then remove single years
    text = YEAR_SINGLE_RE.sub("", text)
    # Normalize whitespace again after removals
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_normalized_license_header_texts(normalized_license_header_dirs: List[Path]) -> Dict[Path, str]:
    """
    Load all .txt files from patterns_dir.

    Returns a dict:
        { pattern_file_path: pattern_text }

    Leading and trailing whitespace in each pattern text is stripped, so
    extra whitespace before/after in the pattern files is not required
    to match.
    """
    normalized_license_headers: Dict[Path, str] = {}

    for base_dir in normalized_license_header_dirs:
        if not os.path.isdir(base_dir):
            print(f"Warning: pattern directory does not exist or is not a directory: {base_dir}")
            continue

        for dirpath, dirnames, filenames in os.walk(base_dir):
            for filename in filenames:
                if not filename.lower().endswith(".txt"):
                    continue

                normalized_license_header_path = Path(dirpath, filename).resolve()

                try:
                    with open(normalized_license_header_path, "r", encoding="utf-8", errors="replace") as f:
                        raw_text = f.read()
                except Exception as e:
                    print(f"Could not read pattern file {normalized_license_header_path}: {e}")
                    continue

                license_text = raw_text.strip()  # ignore extra whitespace before/after

                if not license_text:
                    # Skip completely empty patterns
                    continue

                normalized_license_headers[normalized_license_header_path] = license_text

    return normalized_license_headers



def search_file_data_headers_for_licenses():
    for file_data in Config.file_data_manager.get_all_file_data():
        if file_data.file_header:
            file_header = str(file_data.file_header).lower()
            for license_name, license_identifiers in license_header_keys.dual_license_keys.items():
                if all(identifier.lower() in file_header for identifier in license_identifiers):
                    file_data.header_is_license = True
                    file_data.license_name = license_name
                    break
            if not file_data.license_name:
                for license_name, license_identifiers in license_header_keys.multi_license_keys.items():
                    if any(identifier.lower() in file_header for identifier in license_identifiers):
                        file_data.header_is_license = True
                        file_data.license_name = license_name
                        break
            if not file_data.license_name:
                for license_name, license_identifiers in license_header_keys.multi_license_inclusive_keys.items():
                    if all(identifier.lower() in file_header for identifier in license_identifiers):
                        file_data.header_is_license = True
                        file_data.license_name = license_name
                        break
            if not file_data.license_name:
                for license_name, license_identifier in license_header_keys.license_keys.items():
                    if license_identifier.lower() in file_header:
                        file_data.header_is_license = True
                        file_data.license_name = license_name






def search_file_data_headers_for_licenses2():
    normalized_license_headers = load_normalized_license_header_texts(Config.all_license_headers_normalized_dir)

    for file_data in Config.file_data_manager.get_all_file_data():
        if file_data.file_header:
            for license_header_path, license_header_text in normalized_license_headers.items():
                if license_header_text:
                    # if "compress2.txt" in str(file_data.file_path):
                    #     print('found it')
                    file_data_header_normalized = utils.placeholder_to_regex(file_data.file_header)
                    if license_header_text in file_data_header_normalized:
                        file_data.header_is_license = True
                        file_data.license_name = utils.get_file_name_from_path_without_extension(license_header_path)
                    elif file_data_header_normalized in license_header_text and file_data_header_normalized != '.+?':
                        file_data.header_is_license = True
                        file_data.license_name = utils.get_file_name_from_path_without_extension(license_header_path)



    # # Pre-normalize all patterns once
    # normalized_licenses: Dict[Path, str] = {
    #     path: utils.normalize_without_empty_lines_and_dates(text)
    #     for path, text in normalized_license_headers.items()
    # }
    #
    # # Iterate over all files you've already read into FileData
    # for file_data in Config.file_data_manager.get_all_file_data():
    #     file_text = utils.to_text(file_data.file_content)
    #     normalized_file_text = utils.normalize_without_empty_lines_and_dates(file_text)
    #     license_matches = Dict[str, str]
    #
    #     for license_path, license_text in normalized_licenses.items():
    #         # Full-text match: we look for the entire content of the pattern file
    #         # inside the file's text. Leading/trailing whitespace of the pattern
    #         # has already been stripped.
    #         if license_text and license_text in normalized_file_text:
    #             license_name = utils.get_file_name_from_path_without_extension(license_path)
    #             license_matches = {"License_name": license_name, "License_text": license_text}
    #             file_data.license_matches = license_matches