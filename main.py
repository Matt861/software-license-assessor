#!/usr/bin/env python3
from pathlib import Path

from assessment.timer import Timer
from assessment.creator import extractor
from assessment.review import file_gen
from assessment import print_utils
from assessment.scanner import file_reader, keyword_search, license_search, header_search
from models.FileData import FileDataManager

p = Path(__file__).resolve()

timer = Timer()
timer.start()

# Global instance of file data manager
file_data_manager = FileDataManager()

source_dir = Path(r"C:\Users\mattw\Documents\temp\logback-v_1.5.21.zip").resolve()
dest_dir = Path(r"assessments").resolve()
licenses_dir = Path(r"input\licenses").resolve()
manual_licenses_dir = Path(r"input\manual_licenses").resolve()
all_licenses_dir = [licenses_dir, manual_licenses_dir]
unresolved_file_dir = Path(r"output\review").resolve()

def main() -> None:

    dest_dir.mkdir(parents=True, exist_ok=True)
    extractor.main(source_dir, dest_dir)
    file_reader.read_all_files_in_directory(dest_dir)
    keyword_search.scan_all_files_for_matches()
    licenses = license_search.load_license_texts(all_licenses_dir)
    license_search.search_full_license_text_in_files(licenses)
    header_search.scan_all_files_for_headers()

    file_gen.copy_unresolved_files(dest_dir)



if __name__ == "__main__":
    main()

    #print_utils.print_keyword_matches()
    #print_utils.print_license_matches()
    #print_utils.print_header_matches()
    #print_utils.print_header_and_keyword_matches()
    print_utils.print_total_file_count(dest_dir, True)

    timer.stop()
    print(timer.elapsed())
