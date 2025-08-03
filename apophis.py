"""Apophis language utilities combining Python and Malbolge.

This module provides helper functions to execute Malbolge code and to
apply Malbolge's instruction encryption algorithm.  It relies on the
`malbolge` Python package for the underlying interpreter.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import malbolge


def run_malbolge(code: str) -> str:
    """Execute *code* written in Malbolge and return its output.

    Parameters
    ----------
    code:
        A string containing a Malbolge program.
    """
    if not isinstance(code, str):
        raise TypeError("code must be a string")
    return malbolge.eval(code)


def apophis_malbolge(path: Path | str = "malbolge.mal") -> str:
    """Execute a Malbolge program stored in *path*.

    By default, the file ``malbolge.mal`` in the current working directory
    is loaded and executed.  The output of the program is returned as a
    string.
    """
    file_path = Path(path)
    code = file_path.read_text(encoding="utf-8")
    return run_malbolge(code)


def malbolge_encode(text: str) -> str:
    """Encode *text* using Malbolge's encryption algorithm.

    Each printable ASCII character (33-126) is substituted using the
    encryption table defined by the language.  Other characters are left
    unchanged.
    """
    encoded_chars: list[str] = []
    for ch in text:
        o = ord(ch)
        if 33 <= o <= 126:
            encoded_chars.append(chr(malbolge.ENCRYPT[o - 33]))
        else:
            encoded_chars.append(ch)
    return "".join(encoded_chars)
