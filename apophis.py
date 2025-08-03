"""Apophis language utilities combining Python and Malbolge.

This module provides helper functions to execute Malbolge code and to
apply Malbolge's instruction encryption algorithm.  It relies on the
`malbolge` Python package for the underlying interpreter.
"""
from __future__ import annotations

from pathlib import Path

import ast
import contextlib
import io

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


def run_file(path: Path | str = "malbolge.apop") -> str:
    """Execute an Apophis program stored in *path*.

    Apophis source files must end in ``.apop`` or ``.apo``.  By default, the
    file ``malbolge.apop`` in the current working directory is loaded and
    executed.  The output of the program is returned as a string.
    """
    file_path = Path(path)
    if file_path.suffix not in {".apop", ".apo"}:
        raise ValueError("Apophis files must use the .apop or .apo extension")
    code = file_path.read_text(encoding="utf-8")
    return run_apophis(code)


# Backwards compatibility for earlier versions
apophis_malbolge = run_file


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


def run_python(code: str) -> str:
    """Execute *code* using the restricted Apophis Python subset."""

    if not isinstance(code, str):
        raise TypeError("code must be a string")

    tree = ast.parse(code, mode="exec")
    allowed_nodes = (
        ast.Module,
        ast.Assign,
        ast.Expr,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Store,
        ast.keyword,
        ast.Constant,
        ast.BinOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
    )
    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            raise ValueError(f"Unsupported syntax: {type(node).__name__}")

    env: dict[str, object] = {}
    buf = io.StringIO()
    globals_dict = {"__builtins__": {"print": print}}
    with contextlib.redirect_stdout(buf):
        exec(compile(tree, "<apophis>", "exec"), globals_dict, env)
    return buf.getvalue()


def run_apophis(code: str) -> str:
    """Execute mixed Apophis *code* containing Python and Malbolge segments.

    Lines starting with ``:`` are treated as Python and evaluated using
    :func:`run_python`.  Other lines are considered Malbolge and executed via
    :func:`run_malbolge`.  Output from both languages is concatenated and
    returned as a single string.
    """

    if not isinstance(code, str):
        raise TypeError("code must be a string")

    segments: list[tuple[str, str]] = []
    current_type: str | None = None
    buffer: list[str] = []
    for raw_line in code.splitlines():
        if raw_line.startswith(":"):
            seg_type = "py"
            line = raw_line[1:]
        else:
            seg_type = "mb"
            line = raw_line
        if current_type is None:
            current_type = seg_type
        if seg_type != current_type:
            segments.append((current_type, "\n".join(buffer)))
            buffer = []
            current_type = seg_type
        buffer.append(line)
    if buffer:
        segments.append((current_type, "\n".join(buffer)))

    outputs: list[str] = []
    for seg_type, seg_code in segments:
        if not seg_code.strip():
            continue
        if seg_type == "py":
            outputs.append(run_python(seg_code))
        else:
            outputs.append(run_malbolge(seg_code))
    return "".join(outputs)


def main() -> None:
    """Command-line entry point for executing Apophis programs."""
    import argparse

    parser = argparse.ArgumentParser(description="Execute an Apophis program")
    parser.add_argument(
        "path",
        nargs="?",
        default="malbolge.apop",
        help="Path to a .apop/.apo source file",
    )
    args = parser.parse_args()
    output = run_file(args.path)
    if output:
        print(output)


if __name__ == "__main__":  # pragma: no cover - CLI utility
    main()
