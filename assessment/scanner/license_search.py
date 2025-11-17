# pattern_search.py
import os
import re
from pathlib import Path
from typing import Dict, List
from assessment.scanner import utils
import main


def load_license_texts(license_dirs: List[Path]) -> Dict[Path, str]:
    """
    Load all .txt files from patterns_dir.

    Returns a dict:
        { pattern_file_path: pattern_text }

    Leading and trailing whitespace in each pattern text is stripped, so
    extra whitespace before/after in the pattern files is not required
    to match.
    """
    licenses: Dict[Path, str] = {}

    for base_dir in license_dirs:
        if not os.path.isdir(base_dir):
            print(f"Warning: pattern directory does not exist or is not a directory: {base_dir}")
            continue

        for dirpath, dirnames, filenames in os.walk(base_dir):
            for filename in filenames:
                if not filename.lower().endswith(".txt"):
                    continue

                license_path = Path(dirpath, filename).resolve()

                try:
                    with open(license_path, "r", encoding="utf-8") as f:
                        raw_text = f.read()
                except Exception as e:
                    print(f"Could not read pattern file {license_path}: {e}")
                    continue

                license_text = raw_text.strip()  # ignore extra whitespace before/after

                if not license_text:
                    # Skip completely empty patterns
                    continue

                licenses[license_path] = license_text

    return licenses


def search_full_license_text_in_files(licenses: Dict[Path, str],):
    """
    For each pattern (full text from a pattern file), check whether it
    appears in any of the iterated files stored as FileData instances.

    Returns:
        {
            pattern_file_path: [file_path_1, file_path_2, ...],
            ...
        }

    Only patterns actually found in at least one file will have
    non-empty lists. Patterns with no matches will have an empty list.
    """

    # Pre-normalize all patterns once
    normalized_licenses: Dict[Path, str] = {
        path: utils.normalize_without_empty_lines_and_dates(text)
        for path, text in licenses.items()
    }

    # Iterate over all files you've already read into FileData
    for file_data in main.file_data_manager.get_all_file_data():
        file_text = utils.to_text(file_data.file_content)
        normalized_file_text = utils.normalize_without_empty_lines_and_dates(file_text)
        license_matches = Dict[str, str]

        for license_path, license_text in normalized_licenses.items():
            # Full-text match: we look for the entire content of the pattern file
            # inside the file's text. Leading/trailing whitespace of the pattern
            # has already been stripped.
            if license_text and license_text in normalized_file_text:
                license_name = utils.get_file_name_from_path_without_extension(license_path)
                license_matches = {"License_name": license_name, "License_text": license_text}
                file_data.license_matches = license_matches