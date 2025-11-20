import subprocess
from pathlib import Path


def decompile_class_file(class_file: Path, cfr_jar: Path) -> Path:
    """
    Decompile a single .class file using CFR into the same directory.
    Returns the expected .java file path (whether or not CFR succeeded).
    """
    class_file = class_file.resolve()
    output_dir = class_file.parent.resolve()

    result = subprocess.run(
        [
            "java",
            "-jar",
            str(cfr_jar),
            str(class_file),
            "--outputdir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[ERROR] Failed to decompile {class_file}")
        print(result.stderr)
    else:
        print(f"[OK] Decompiled {class_file}")

    return class_file.with_suffix(".java")


def decompile_all_classes(
    root_dir: str,
    cfr_jar_path: str,
    delete_class_files: bool = False,
) -> None:
    """
    Walk root_dir, look at every file, and only decompile those that are .class files.
    Optionally delete the .class file after successful decompile.
    """
    root = Path(root_dir).resolve()
    cfr_jar = Path(cfr_jar_path).resolve()

    if not cfr_jar.is_file():
        raise FileNotFoundError(f"CFR jar not found: {cfr_jar}")

    print(f"Root directory: {root}")
    print(f"Using CFR jar:  {cfr_jar}")

    # Walk every file and selectively handle .class files
    for path in root.rglob("*"):
        if not path.is_file():
            continue

        # Only act on .class files
        if path.suffix != ".class":
            # Just skip non-class files
            continue

        # Optional: skip inner/anonymous classes like MyClass$1.class
        if "$" in path.stem:
            print(f"[SKIP] Inner/anonymous class: {path}")
            continue

        java_file = decompile_class_file(path, cfr_jar)

        if delete_class_files and java_file.is_file():
            try:
                path.unlink()
                print(f"[DEL] Deleted original .class: {path}")
            except Exception as e:
                print(f"[WARN] Could not delete {path}: {e}")


if __name__ == "__main__":
    # EDIT THESE
    ROOT_DIR = r"C:\Users\mattw\PycharmProjects\SLA\test\input\dot_class_files"
    CFR_JAR = r"C:\Users\mattw\Tools\cfr-0.152.jar"
    DELETE_CLASS_FILES = True  # set True if you want .class -> .java

    decompile_all_classes(ROOT_DIR, CFR_JAR, delete_class_files=DELETE_CLASS_FILES)
