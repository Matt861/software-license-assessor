import os
from pathlib import Path
from typing import Union
from assessment.scanner import utils
import main
from models.FileData import FileData


def read_all_files_in_directory(root_dir):
    """
    Iterates through all files in root_dir (including subdirectories),
    reads their content, and creates FileData instances for each file.
    """

    # # Optional: start with a clean registry for each run
    # FileData.clear_registry()

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = Path(dirpath, filename).resolve()

            try:
                # Try reading as text
                with open(file_path, "r", encoding="utf-8") as f:
                    content: Union[str, bytes] = f.read()
            except UnicodeDecodeError:
                # Fallback to binary
                with open(file_path, "rb") as f:
                    content = f.read()
            except Exception as e:
                print(f"Could not read {file_path}: {e}")
                continue

            file_extension = utils.get_file_extension(file_path)
            file_data = FileData(file_path, content, file_extension)
            main.file_data_manager.add_file_data(file_data)