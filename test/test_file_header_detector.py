import unittest
import os
from pathlib import Path
from assessment.scanner.file_reader import read_all_files_in_directory
from assessment.scanner.utils import read_file_to_string, placeholder_to_regex
from assessment.scanner.license_to_header_matcher import normalize_plain_text, normalize_c_style_file_header
from configuration import Configuration as Config
from assessment.scanner.header_search import (detect_file_header, detect_c_style_file_header,
                                              detect_xml_style_file_header)
from models.FileData import FileData

p = Path(__file__).resolve()

class TestFileHeaderDetector(unittest.TestCase):

    def test_detect_file_header(self):
        file_path = Path("input/files_with_headers/example.java").resolve()
        read_all_files_in_directory(Path("input").resolve())
        file_data = Config.file_data_manager.get_file_data(file_path)
        detect_file_header(file_data)
        header_text_stripped = placeholder_to_regex(file_data.file_header)
        license_header_path = 'C:/Users/mattw/PycharmProjects/SLA/input/manual_license_headers/logback_header.txt'
        license_header_text = read_file_to_string(license_header_path)
        license_header_text_stripped = placeholder_to_regex(license_header_text)
        if header_text_stripped == license_header_text_stripped:
            print('THEY THE SAME')
        if license_header_text_stripped in header_text_stripped:
            print('FOUND IT')
        print('Done')


    def test_detect_c_style_file_header(self):
        file_path = Path("input/files_with_headers/example.java").resolve()
        read_all_files_in_directory(Path("input").resolve())
        file_data = Config.file_data_manager.get_file_data(file_path)
        java_header = detect_c_style_file_header(file_data)
        print(java_header)
        file_path = Path("input/files_with_headers/example2.java").resolve()
        file_data = Config.file_data_manager.get_file_data(file_path)
        java_header = detect_c_style_file_header(file_data)
        print(java_header)
        print('Done')

    def test_detect_xml_style_file_header(self):
        read_all_files_in_directory(Path("input/files_with_headers").resolve())
        file_path = Path("input/files_with_headers/example.xml").resolve()
        file_data = Config.file_data_manager.get_file_data(file_path)
        xml_header = detect_xml_style_file_header(file_data)
        print(xml_header)
        file_path = Path("input/files_with_headers/example.html").resolve()
        file_data = Config.file_data_manager.get_file_data(file_path)
        html_header = detect_xml_style_file_header(file_data)
        print(html_header)
        print('Done')

    def test_c_style_header_matching(self):
        read_all_files_in_directory(Path("input/files_with_headers").resolve())
        file_with_c_style_header_path = Path("input/files_with_headers/example.java").resolve()
        file_data = Config.file_data_manager.get_file_data(file_with_c_style_header_path)
        file_header_path = Path("input/headers/logback_header.txt").resolve()
        c_style_header = detect_c_style_file_header(file_data)
        path = Path(file_header_path)
        with path.open("r", encoding="utf-8") as f:
            header_text = f.read()
        norm_header = normalize_c_style_file_header(c_style_header)
        print(norm_header)
        norm_plain = normalize_plain_text(header_text)
        print(norm_plain)
        if norm_header == norm_plain:
            print('match')
        else:
            print('not match')


if __name__ == "__main__":
    unittest.main()