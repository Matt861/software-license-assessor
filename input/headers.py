# headers.py

"""
Dictionary of known header regex patterns per file extension
Used by file_header_detector.py to detect file headers.
"""

known_headers = {
    # Python: triple-quoted docstring or comment block at top
    ".py": [
        (r'^(\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\')', "docstring"),
        (r'^(#[^\n]*\n)+', "comment block")
    ],
    # JavaScript, TypeScript, C, C++, Java: multiline comment at top
    (".js", ".ts", ".c", ".cpp", ".java"): [
        (r'^(\/\*[\s\S]*?\*\/)', "multiline comment"),
        (r'^(\/\/[^\n]*\n)+', "comment block")
    ],
    # Shell script: hash comment
    ".sh": [
        (r'^(#[^\n]*\n)+', "comment block")
    ],
    # HTML: <!-- comment -->
    ".html": [
        (r'^(<!--[\s\S]*?-->)', "HTML comment")
    ],
    # XML: <!-- comment -->
    ".xml": [
        (r'^(<!--[\s\S]*?-->)', "XML comment")
    ],
    # Add more file types as needed below
    # Example: ".rb": [ ... ]
}