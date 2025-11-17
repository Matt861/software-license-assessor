import os
from jproperties import Properties
from dotenv import load_dotenv
from pathlib import Path

p = Path(__file__).resolve()


class Configuration:
    load_dotenv()
    configs = Properties()
    properties_file = Path('app-config.properties').resolve()
    with open(properties_file, 'rb') as config_file:
        configs.load(config_file)

    ignore_dirs_str = configs.get('IGNORE_DIRS').data
    ignore_dirs = [part.strip() for part in ignore_dirs_str.split(",")]
    review_file_dir = configs.get('REVIEW_FILE_DIR').data

