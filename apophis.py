"""Apophis language utilities combining Python, Ruby and Malbolge.

This module provides helper functions to execute Malbolge and Ruby code and to
apply Malbolge's instruction encryption algorithm.  It relies on the
`malbolge` Python package for the Malbolge interpreter and the system `ruby`
command for Ruby execution.
"""
from __future__ import annotations

from pathlib import Path

import ast
import contextlib
import io
import json
import subprocess

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


def run_file(
    path: Path | str = "malbolge.apop", py_env: dict[str, object] | None = None
) -> str:
    """Execute an Apophis program stored in *path*.

    The source may contain Python, Ruby and Malbolge segments.

    Parameters
    ----------
    path:
        Location of the source file.
    py_env:
        Optional dictionary used to persist state between Python and Ruby segments.
    """
    file_path = Path(path)
    if file_path.suffix not in {".apop", ".apo"}:
        raise ValueError("Apophis files must use the .apop or .apo extension")
    code = file_path.read_text(encoding="utf-8")
    return run_apophis(code, py_env=py_env)


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


def run_ruby(code: str, env: dict[str, object] | None = None) -> str:
    """Execute *code* written in Ruby and return its output.

    If *env* is provided, it must contain JSON-serialisable values.  Variables
    from the mapping are injected into the Ruby interpreter before *code*
    executes.  After execution, any Ruby variables are written back to ``env`` to
    allow rudimentary state sharing with Python segments.
    """
    if not isinstance(code, str):
        raise TypeError("code must be a string")

    preamble = ""
    postamble = ""
    if env is not None:
        assignments = [f"{name} = {json.dumps(value)}" for name, value in env.items()]
        preamble = "require 'json'\n" + "\n".join(assignments) + "\n"
        postamble = (
            "\n__apophis_env__ = {}\n"
            "(local_variables - [:__apophis_env__]).each do |v|\n"
            "  __apophis_env__[v] = eval(v.to_s)\n"
            "end\n"
            "STDERR.write(JSON.dump(__apophis_env__))\n"
        )

    full_code = preamble + code + postamble
    proc = subprocess.run(
        ["ruby", "-e", full_code],
        check=True,
        text=True,
        capture_output=True,
    )
    if env is not None:
        try:
            env.update(json.loads(proc.stderr or "{}"))
        except json.JSONDecodeError:
            pass
    return proc.stdout


def _ruby_to_python(code: str) -> str:
    """Translate a tiny Ruby-like syntax subset into valid Python code.

    This helper allows ``run_python`` to accept blocks written using Ruby's
    ``end`` keyword and missing colons after ``if``/``while``/``def`` statements.
    The transformation is intentionally minimal and does not aim to be a full
    Ruby-to-Python converter.
    """

    lines: list[str] = []
    for line in code.splitlines():
        stripped = line.strip()
        if stripped == "end":
            continue
        first_word = stripped.split(" ", 1)[0] if stripped else ""
        if first_word == "elsif":
            line = line.replace("elsif", "elif", 1)
            first_word = "elif"
        elif first_word == "unless":
            line = line.replace("unless", "if not", 1)
            first_word = "if"
        elif first_word == "until":
            line = line.replace("until", "while not", 1)
            first_word = "while"
        stripped = line.strip()
        if first_word in {"if", "while", "elif", "else", "def"} and not stripped.endswith(":"):
            line = line.rstrip() + ":"
        lines.append(line)
    return "\n".join(lines)


def run_python(code: str, env: dict[str, object] | None = None) -> str:
    """Execute *code* using the restricted Apophis Python subset.

    This subset supports variable assignments, ``print`` calls, arithmetic
    expressions, ``if`` statements, ``while`` loops and function definitions.  A
    minimal Ruby-like syntax is also recognised: ``if``/``while``/``def`` blocks
    may omit the trailing colon and be terminated with ``end``; ``elsif``,
    ``unless`` and ``until`` are accepted as aliases for ``elif``, ``if not`` and
    ``while not`` respectively.  Only a curated selection of Python's AST nodes
    is permitted to keep the interpreter intentionally small and safe.

    Parameters
    ----------
    code:
        Python source code to execute.
    env:
        Optional dictionary that stores variables between calls.
    """

    if not isinstance(code, str):
        raise TypeError("code must be a string")

    code = _ruby_to_python(code)
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
        ast.If,
        ast.While,
        ast.FunctionDef,
        ast.arguments,
        ast.arg,
        ast.Return,
        ast.Compare,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.BoolOp,
        ast.And,
        ast.Or,
        ast.UnaryOp,
        ast.UAdd,
        ast.USub,
        ast.Not,
        ast.Break,
        ast.Continue,
        ast.Pass,
    )
    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            raise ValueError(f"Unsupported syntax: {type(node).__name__}")

    if env is None:
        env = {}
    buf = io.StringIO()
    globals_dict = {"__builtins__": {"print": print, "puts": print}}
    with contextlib.redirect_stdout(buf):
        exec(compile(tree, "<apophis>", "exec"), globals_dict, env)
    return buf.getvalue()


def run_apophis(code: str, py_env: dict[str, object] | None = None) -> str:
    """Execute mixed Apophis *code* containing Python, Ruby and Malbolge segments.

    Parameters
    ----------
    code:
        Hybrid Apophis source combining Python (prefixed with ``:``), Ruby
        (prefixed with ``;``) and Malbolge lines.  Blank lines and those
        starting with ``#`` are treated as comments and ignored.
    py_env:
        Optional environment dictionary shared by Python and Ruby segments.
    """

    if not isinstance(code, str):
        raise TypeError("code must be a string")

    segments: list[tuple[str, str]] = []
    current_type: str | None = None
    buffer: list[str] = []
    for raw_line in code.splitlines():
        stripped = raw_line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if raw_line.startswith(":"):
            seg_type = "py"
            line = raw_line[1:]
        elif raw_line.startswith(";"):
            seg_type = "rb"
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

    if py_env is None:
        py_env = {}

    outputs: list[str] = []
    for seg_type, seg_code in segments:
        if not seg_code.strip():
            continue
        if seg_type == "py":
            outputs.append(run_python(seg_code, env=py_env))
        elif seg_type == "rb":
            outputs.append(run_ruby(seg_code, env=py_env))
        else:
            outputs.append(run_malbolge(seg_code))
    return "".join(outputs)


def repl(input_func=input, output_func=print) -> None:
    """Start an interactive Apophis session.

    Lines are read from ``input_func`` and executed immediately.  Python lines
    must begin with ``:``, Ruby lines with ``;`` while all other lines are
    treated as Malbolge.  State from Python code persists across inputs via a
    shared environment.  The ``output_func`` is used for displaying results and
    defaults to :func:`print`.
    """

    env: dict[str, object] = {}
    while True:
        try:
            line = input_func(">>> ")
        except EOFError:
            break
        if line == "":
            break
        result = run_apophis(line, py_env=env)
        if result:
            output_func(result, end="")


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
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Start an interactive REPL instead of running a file",
    )
    args = parser.parse_args()
    if args.interactive:
        repl()
        return
    output = run_file(args.path)
    if output:
        print(output)


if __name__ == "__main__":  # pragma: no cover - CLI utility
    main()
