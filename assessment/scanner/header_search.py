import re

import main


def _detect_file_header(file_data):
    """
    Determines if the given file content contains a header and retrieves it.
    Handles source code, markup, and text-based file types.

    Args:
        content (str): The full file content.
        extension (str): The file extension, e.g., '.py', '.java', '.html', etc.

    Returns:
        (bool, str|None): Tuple (has_header, header_text). header_text is None if no header is found.
    """

    lines = file_data.file_content.strip().splitlines()
    if not lines:
        return

    ext = file_data.file_extension.lower().lstrip(".")

    # CSV: First line which contains likely field names
    if ext == "csv":
        first_row = lines[0].strip()
        if any(not re.match(r'^-?\d+(\.\d+)?$', cell.strip()) for cell in first_row.split(",")):
            file_data.header_matches = first_row
            return

    # Text, Markdown: Non-empty first line or Markdown header
    if ext in ("txt", "md"):
        first_line = lines[0].strip()
        if ext == "md":
            if first_line.startswith("#"):
                file_data.header_matches = first_line
                return
        if first_line:
            file_data.header_matches = first_line
            return

    # Python (.py): Triple-quoted docstring, or top block of comments (#)
    if ext == "py":
        if lines[0].startswith(('"""', "'''")):
            quote = lines[0][:3]
            header_lines = [lines[0]]
            for line in lines[1:]:
                header_lines.append(line)
                if line.strip().endswith(quote):
                    break
            file_data.header_matches = "\n".join(header_lines)
            return
        i = 0
        while i < len(lines) and lines[i].strip().startswith("#"):
            i += 1
        if i > 0:
            file_data.header_matches = "\n".join(lines[:i])
            return

    # Java, JS, TS, C, CPP, CSS, SH: Block comments at top (/* ... */ or //...), or # for sh
    if ext in ("java", "js", "ts", "c", "cpp", "css"):
        # Check for top block comment /* ... */
        if lines[0].strip().startswith("/*"):
            header_lines = [lines[0]]
            for line in lines[1:]:
                header_lines.append(line)
                if "*/" in line:
                    break
            file_data.header_matches = "\n".join(header_lines)
            return
        # Check for contiguous // at top
        i = 0
        while i < len(lines) and lines[i].strip().startswith("//"):
            i += 1
        if i > 0:
            file_data.header_matches = "\n".join(lines[:i])
            return
    if ext == "sh":
        i = 0
        while i < len(lines) and lines[i].strip().startswith("#"):
            i += 1
        if i > 0:
            file_data.header_matches = "\n".join(lines[:i])
            return

    # XML, HTML: <!-- ... --> block at top
    if ext in ("xml", "html"):
        if lines[0].strip().startswith("<!--"):
            header_lines = [lines[0]]
            for line in lines[1:]:
                header_lines.append(line)
                if "-->" in line:
                    break
            file_data.header_matches = "\n".join(header_lines)
            return

    # Fallback: first non-empty line as potential header
    # first_line = lines[0].strip()
    # if first_line:
    #     return True, first_line

    return


def scan_all_files_for_headers():
    for file_data in main.file_data_manager.get_all_file_data():
        _detect_file_header(file_data)
