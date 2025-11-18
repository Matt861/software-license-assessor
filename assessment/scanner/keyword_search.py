# match_scanner.py
from typing import Dict, List, Union
from assessment.scanner.utils import to_text
from configuration import Configuration as Config
from input.file_search_strings import copyright_matches, license_matches, prohibitive_matches, general_matches, \
    export_matches, custom_search_matches

ALL_MATCH_LISTS: Dict[str, List[str]] = {
    "copyright": copyright_matches,
    "license": license_matches,
    "prohibitive": prohibitive_matches,
    "general": general_matches,
    "export": export_matches,
    "custom": custom_search_matches,
}


def _find_matches_in_content(content: Union[str, bytes]) -> Dict[str, List[str]]:
    """
    Given a file's content, return a dict of:
        { category_name: [matched_strings_from_that_category] }

    Matching is:
    - Case-insensitive
    - Based on full strings from the lists (e.g. we look specifically
      for 'Eclipse Public License', not just 'Eclipse').
    """
    text = to_text(content)
    text_lower = text.lower()

    matches: Dict[str, List[str]] = {}

    for category, terms in ALL_MATCH_LISTS.items():
        found_terms: List[str] = []
        for term in terms:
            if term.lower() in text_lower:
                # Full string from the list is present in the content
                found_terms.append(term)

        if found_terms:
            matches[category] = found_terms

    return matches


def scan_all_files_for_matches():
    for file_data in Config.file_data_manager.get_all_file_data():
        file_matches = _find_matches_in_content(file_data.file_content)
        if file_matches:
            file_data.keyword_matches = file_matches
