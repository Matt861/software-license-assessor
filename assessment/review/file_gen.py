import shutil
from pathlib import Path
from configuration import Configuration as Config


def is_ignored_dir(src_dir: Path) -> bool:
    src_dir_str = str(src_dir)
    for ignore_dir in Config.ignore_dirs:
        if ignore_dir in str(src_dir_str):
            return True
    return False


def copy_unresolved_files(src_path) -> None:
    """
    Iterate each file in src_dir and copy it to dst_dir if condition(file_path) is True.

    - src_dir: directory to read files from
    - dst_dir: directory to copy matching files into (created if it doesn't exist)
    - condition: function that takes a Path and returns True/False
    """

    dst_path = Path(Config.review_file_dir).resolve()
    dst_path.mkdir(parents=True, exist_ok=True)
    review_file_count = 0

    for file_path in src_path.rglob("*"):
        if file_path.is_file():
            if is_ignored_dir(file_path):
                continue
            file_data = Config.file_data_manager.get_file_data(file_path)
            if file_data:
                if not file_data.header_matches:
                    # Preserve directory structure under dst_dir
                    rel_path = file_path.relative_to(src_path)
                    target_path = dst_path / rel_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, target_path)
                    review_file_count += 1
            else:
                print(f"Could not find file data for file: {file_path}")
                continue

    print(f"{"Review file count: "}{review_file_count}")