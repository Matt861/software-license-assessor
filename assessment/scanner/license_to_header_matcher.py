import os
from pathlib import Path
from typing import Dict, List

from assessment.scanner import utils
from configuration import Configuration as Config


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
    normalized_license_headers = load_normalized_license_header_texts(Config.all_license_headers_normalized_dir)

    for file_data in Config.file_data_manager.get_all_file_data():
        if file_data.header_matches:
            for license_header_path, license_header_text in normalized_license_headers.items():
                if license_header_text:
                    # if "compress2.txt" in str(file_data.file_path):
                    #     print('found it')
                    file_data_header_normalized = utils.placeholder_to_regex(file_data.header_matches)
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