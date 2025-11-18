import os
from assessment.scanner import utils
from configuration import Configuration as Config
from pathlib import Path

p = Path(__file__).resolve()


def main(src_dir, dest_dir) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)

    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.lower().endswith(".txt"):
                #src_path = os.path.join(root, filename)
                src_path = Path(dirpath, filename).resolve()

                # Read content
                content = utils.read_file_to_string(str(src_path))

                # Pass to your custom handler
                normalized_content = utils.placeholder_to_regex(content)

                # Write to new directory with same file name
                #dest_path = os.path.join(dest_dir, filename)
                dest_path = Path(dest_dir, filename).resolve()
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(normalized_content)


if __name__ == "__main__":
    src_dir = Config.manual_license_headers_dir
    dest_dir = Path('input/manual_license_headers_normalized').resolve()
    main(src_dir, dest_dir)
    src_dir = Config.license_headers_dir
    dest_dir = Path('input/license_headers_normalized').resolve()
    main(src_dir, dest_dir)
