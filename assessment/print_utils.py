from configuration import Configuration as Config
from pathlib import Path


def print_total_file_count(dir_path, recursive: bool = False):

    if recursive:
        # All files in this directory and subdirectories
        print(f"{"Total files: "}{sum(1 for p in dir_path.rglob("*") if p.is_file())}")
    else:
        # Only files directly in this directory (no subdirectories)
        print(f"{"Total files: "}{sum(1 for p in dir_path.iterdir() if p.is_file())}")


def print_keyword_matches():
    file_keyword_match_count = 0
    for file_data in Config.file_data_manager.get_all_file_data():
        if file_data.keyword_matches:
            file_keyword_match_count += 1
            print(f"{"Keyword matches: "}{file_data.keyword_matches}")
    print(f"{"Total files with keyword matches: "}{file_keyword_match_count}")


def print_license_matches():
    file_license_match_count = 0
    for file_data in Config.file_data_manager.get_all_file_data():
        if file_data.license_matches:
            file_license_match_count += 1
            print(f"{"License matches: "}{file_data.license_matches}")
    print(f"{"Total files with license matches: "}{file_license_match_count}")


def print_header_matches():
    file_header_match_count = 0
    for file_data in Config.file_data_manager.get_all_file_data():
        if file_data.file_header:
            file_header_match_count += 1
            print(f"{"Header matches: "}{file_data.file_header}")
    print(f"{"Total files with header matches: "}{file_header_match_count}")


def print_header_and_keyword_matches():
    file_header_and_keyword_match_count = 0
    for file_data in Config.file_data_manager.get_all_file_data():
        if file_data.file_header and file_data.keyword_matches:
            file_header_and_keyword_match_count += 1
            print(f"{"File name: "}{file_data.file_path}")
            print(f"{"Header and keyword matches: "}{file_data.file_header}")
    print(f"{"Total files with header and keyword matches: "}{file_header_and_keyword_match_count}")


def print_keyword_matches_without_header_matches():
    file_keyword_match_count = 0
    for file_data in Config.file_data_manager.get_all_file_data():
        if not file_data.header_is_license and file_data.keyword_matches:
            file_keyword_match_count += 1
            print(f"{"File name: "}{file_data.file_path}")
            print(f"{"Keyword matches: "}{file_data.keyword_matches}")
    print(f"{"Total files with keyword matches but no header match: "}{file_keyword_match_count}")


def print_license_header_matches():
    file_header_license_match_count = 0
    for file_data in Config.file_data_manager.get_all_file_data():
        if file_data.file_header and file_data.header_is_license:
            file_header_license_match_count += 1
            #print(f"{"File name: "}{file_data.file_path}")
            #print(f"{"License name: "}{file_data.license_name}")
    print(f"{"Total files with header that matches license: "}{file_header_license_match_count}")


def print_file_extension_counts():
    file_extension_count_dict = {}
    for file_data in Config.file_data_manager.get_all_file_data():
        if file_data.file_extension:
            if file_data.file_extension in file_extension_count_dict:
                file_extension_count_dict[file_data.file_extension] += 1
            else:
                file_extension_count_dict[file_data.file_extension] = 1

    print("Total file extension counts: ")
    for extension_type, extension_type_count in file_extension_count_dict.items():
        print(f"Extension type: {extension_type} Count: {extension_type_count}")