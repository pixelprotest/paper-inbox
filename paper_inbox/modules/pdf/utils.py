from __future__ import annotations
import subprocess, os
from paper_inbox.modules.pdf import validators, exceptions
import typing as t
if t.TYPE_CHECKING:
    from pathlib import Path

def is_canva(filepath: str | Path) -> bool:
    info = info_as_dict(filepath)
    creator = info.get('Creator', None)
    producer = info.get('Producer', None)
    if creator and creator.lower()=='canva':
        return True
    if producer and producer.lower()=='canva':
        return True
    return False

def is_valid(filepath: str | Path) -> bool:
    """ validates the PDF to make sure it conforms and will be printable """
    try:
        validators.validate_magic_header(filepath)
        validators.validate_file_head(filepath)
        validators.validate_structure(filepath)
        validators.validate_not_html(filepath)
        validators.validate_mime_type(filepath)
        return True
    except exceptions.PDFError as e:
        return False

def info_as_string(filepath: str | Path) -> str:
    """ returns string stderr + stdout of the 'pdfinfo' call"""
    result = subprocess.run(["pdfinfo", filepath], capture_output=True, text=True)

    ## combine the stderr and stdout for full context.
    return result.stdout + result.stderr

def info_as_dict(filepath: str | Path) -> dict:
    """ returns a dictionary of the 'pdfinfo' out"""
    raw = info_as_string(filepath)

    info = {}
    for line in raw.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()

    return info