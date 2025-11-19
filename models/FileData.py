from pathlib import Path
from typing import Optional, List, Dict

class FileData:
    def __init__(self, file_path, file_content, file_extension):
        self._file_path = file_path
        self._file_content = file_content
        self._file_extension = file_extension
        self._file_header = None
        self._keyword_matches = None
        self._license_matches = None
        self._header_is_license = False
        self._license_name = None
        self._is_released = False
        self._exact_license_match = None
        # self._header_data = header_data if header_data is not None else []
        # self._file_entry = file_entry if file_entry is not None else []
        # self._file_search_data = file_search_data if file_search_data is not None else []
        # self._file_assessment = file_assessment
        # self._is_archive = is_archive
        # self._could_read = could_read
        # self._has_license = has_license
        # self._is_license = is_license
        # self._license_data = license_data if license_data is not None else []

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path

    @property
    def file_content(self):
        return self._file_content

    @file_content.setter
    def file_content(self, file_content):
        self._file_content = file_content

    @property
    def file_extension(self):
        return self._file_extension

    @file_extension.setter
    def file_extension(self, file_extension):
        self._file_extension = file_extension

    @property
    def file_header(self):
        return self._file_header

    @file_header.setter
    def file_header(self, header_matches):
        self._file_header = header_matches

    @property
    def keyword_matches(self):
        return self._keyword_matches

    @keyword_matches.setter
    def keyword_matches(self, keyword_matches):
        self._keyword_matches = keyword_matches

    @property
    def license_matches(self):
        return self._license_matches

    @license_matches.setter
    def license_matches(self, license_matches):
        self._license_matches = license_matches

    @property
    def header_is_license(self):
        return self._header_is_license

    @header_is_license.setter
    def header_is_license(self, header_is_license):
        self._header_is_license = header_is_license

    @property
    def license_name(self):
        return self._license_name

    @license_name.setter
    def license_name(self, license_name):
        self._license_name = license_name

    @property
    def is_released(self):
        return self._is_released

    @is_released.setter
    def is_released(self, is_released):
        self._is_released = is_released
    #
    # @property
    # def header_data(self):
    #     return self._header_data
    #
    # @header_data.setter
    # def header_data(self, header_data):
    #     self._header_data = header_data
    #
    # @property
    # def file_entry(self):
    #     return self._file_entry
    #
    # @file_entry.setter
    # def file_entry(self, file_entry):
    #     self._file_entry = file_entry
    #
    # @property
    # def file_search_data(self):
    #     return self._file_search_data
    #
    # @file_search_data.setter
    # def file_search_data(self, file_search_data):
    #     self._file_search_data = file_search_data
    #
    # @property
    # def file_assessment(self):
    #     return self._file_assessment
    #
    # @file_assessment.setter
    # def file_assessment(self, file_assessment):
    #     self._file_assessment = file_assessment
    #
    # @property
    # def is_archive(self):
    #     return self._is_archive
    #
    # @is_archive.setter
    # def is_archive(self, is_archive):
    #     self._is_archive = is_archive
    #
    # @property
    # def could_read(self):
    #     return self._could_read
    #
    # @could_read.setter
    # def could_read(self, could_read):
    #     self._could_read = could_read
    #
    # @property
    # def has_license(self):
    #     return self._has_license
    #
    # @has_license.setter
    # def has_license(self, has_license):
    #     self._has_license = has_license
    #
    # @property
    # def is_license(self):
    #     return self._is_license
    #
    # @is_license.setter
    # def is_license(self, is_license):
    #     self._is_license = is_license
    #
    # @property
    # def license_data(self):
    #     return self._license_data
    #
    # @license_data.setter
    # def license_data(self, license_data):
    #     self._license_data = license_data


class FileDataManager:
    def __init__(self):
        self.file_data_dict: Dict[Path, FileData] = {}

    def add_file_data(self, file_info: FileData):
        """Adds a File instance to the manager."""
        self.file_data_dict[file_info.file_path] = file_info

    def get_file_data(self, file_path: Path) -> Optional[FileData]:
        """Retrieves a FileData instance by file path."""
        return self.file_data_dict.get(file_path)

    def get_all_file_data(self) -> List[FileData]:
        """Returns a list of all FileData instances."""
        return list(self.file_data_dict.values())