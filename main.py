#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from assessment.timer import Timer
#from assessment.creator import extractor
from assessment.creator2 import extractor
from assessment.review import file_gen, data_gen
from assessment import print_utils
from configuration import Configuration as Config
from assessment.scanner import (file_reader, keyword_search, license_search, header_search, license_to_header_matcher,
                                file_release_search, hash_reader)

p = Path(__file__).resolve()

timer = Timer()
timer.start()


def main() -> None:
    Config.dest_dir.mkdir(parents=True, exist_ok=True)
    extractor.main(Config.source_dir, Config.dest_dir)
    file_reader.read_all_files_in_directory(Path(Config.dest_dir, Config.project_name))
    file_release_search.scan_all_files()
    hash_reader.main()
    license_search.search_full_license_text_in_files()
    # SEARCH FULL HEADER TEXT IN FILE, SOME FILES ARE ONLY THE HEADER LICENSE TEXT WITHOUT A HEADER (output/review/logback-v_1.5.21/logback-core-blackbox/LICENSE.txt)
    header_search.scan_all_files_for_headers()
    license_to_header_matcher.search_file_data_headers_for_licenses()
    keyword_search.scan_all_files_for_matches()
    # FULL LICENSE OR FULL HEADER MATCHES = EXACT LICENSE MATCH
    # HEADER MATCH = STRONG MATCH
    # KEYWORD MATCH = WEAK MATCH
    # DETERMINE IF HEADER IS A LICENSE
    # MOVE KEYWORD SEARCH TO HAPPEN HERE
    # ADD LOGIC TO MANUALLY EXCLUDE/INFER INDIVIDUAL FILES
    # ADD LOGIC TO CREATE FINALIZED ASSESSMENT TO USE FOR DIFF COMPARE
    # DIFF COMPARE SHOULD OUTPUT TOTAL NUMBER OF NEW FILES AND NUMBER OF FILES CHANGED
    # ASSIGN LICENSES VALUES OF PERMISSIBLE AND IMPERMISSIBLE

    file_gen.copy_unresolved_files(Path(Config.dest_dir, Config.project_name))
    data_gen.write_license_data_to_csv("assessment_data.csv")



if __name__ == "__main__":
    main()

    # print_utils.print_keyword_matches()
    # print_utils.print_license_matches()
    # print_utils.print_header_matches()
    # print_utils.print_header_and_keyword_matches()
    print_utils.print_license_header_matches()
    print_utils.print_keyword_matches_without_header_matches()
    print_utils.print_total_file_count(Config.dest_dir, True)
    print_utils.print_file_extension_counts()

    timer.stop()
    print(timer.elapsed())