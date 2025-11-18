import unittest
import os
from pathlib import Path
from assessment.scanner.file_reader import read_all_files_in_directory
from assessment.scanner.utils import read_file_to_string, placeholder_to_regex
from configuration import Configuration as Config
from assessment.scanner.header_search import detect_file_header
from models.FileData import FileData

p = Path(__file__).resolve()

class TestFileHeaderDetector(unittest.TestCase):

    def test_detect_file_header(self):
        file_path = Path("input/JoranConfiguratorBase.java").resolve()
        read_all_files_in_directory(Path("input").resolve())
        file_data = Config.file_data_manager.get_file_data(file_path)
        detect_file_header(file_data)
        header_text_stripped = placeholder_to_regex(file_data.header_matches)
        license_header_path = 'C:/Users/mattw/PycharmProjects/SLA/input/manual_license_headers/logback_header.txt'
        license_header_text = read_file_to_string(license_header_path)
        license_header_text_stripped = placeholder_to_regex(license_header_text)
        if header_text_stripped == license_header_text_stripped:
            print('THEY THE SAME')
        if license_header_text_stripped in header_text_stripped:
            print('FOUND IT')
        print('Done')

if __name__ == "__main__":
    unittest.main()