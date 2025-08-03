import apophis
import malbolge
import pytest


def test_run_malbolge_trivial():
    assert apophis.run_malbolge('Q') == ''


def test_malbolge_encode():
    text = 'Hello!'
    encoded = apophis.malbolge_encode(text)
    expected = ''.join(
        chr(malbolge.ENCRYPT[ord(ch) - 33]) if 33 <= ord(ch) <= 126 else ch
        for ch in text
    )
    assert encoded == expected


def test_run_file_default():
    assert apophis.run_file() == ''


def test_run_file_with_apo(tmp_path):
    file = tmp_path / "sample.apo"
    file.write_text("Q")
    assert apophis.run_file(file) == ''


def test_run_python_basic():
    code = "x = 1\nprint(x + 2)"
    assert apophis.run_python(code) == "3\n"


def test_run_python_puts_alias():
    assert apophis.run_python("puts('hello')") == "hello\n"


def test_run_python_rejects_import():
    with pytest.raises(ValueError):
        apophis.run_python("import os")


def test_run_python_if_statement():
    code = "x = 5\nif x > 3:\n    print('yes')"
    assert apophis.run_python(code) == "yes\n"


def test_run_python_ruby_style_block():
    code = "x = 1\nif x == 1\n    puts('ok')\nend"
    assert apophis.run_python(code) == "ok\n"


def test_run_python_while_loop():
    code = (
        "x = 0\n" "while x < 3:\n" "    print(x)\n" "    x = x + 1"
    )
    assert apophis.run_python(code) == "0\n1\n2\n"


def test_run_apophis_mixed_string():
    code = ":print('A', end='')\n>b\n:print('B', end='')"
    assert apophis.run_apophis(code) == "AsB"


def test_run_ruby_basic():
    assert apophis.run_ruby("print 'hi'") == "hi"


def test_run_apophis_with_ruby():
    code = ":print('A', end='')\n;print 'B'\n:print('C', end='')"
    assert apophis.run_apophis(code) == "ABC"


def test_run_apophis_mixed_file(tmp_path):
    file = tmp_path / "hybrid.apop"
    file.write_text(":print('hi', end='')\n>b\n")
    assert apophis.run_file(file) == "his"


def test_run_apophis_persistent_env():
    code = ":x = 1\n>b\n:print(x, end='')"
    assert apophis.run_apophis(code) == "s1"


def test_run_apophis_comments():
    code = "# comment\n:print('X', end='')\n# another\nQ"
    assert apophis.run_apophis(code) == "X"


def test_repl_persistence():
    inputs = iter([":x = 2", ":print(x)", ""])

    def fake_input(prompt=""):
        try:
            return next(inputs)
        except StopIteration:
            raise EOFError

    outputs: list[str] = []

    def fake_output(s: str, end: str = "\n") -> None:
        outputs.append(s + end)

    apophis.repl(input_func=fake_input, output_func=fake_output)
    assert "".join(outputs) == "2\n"


def test_run_python_ruby_style_function():
    code = "def add(x, y)\n    return x + y\nend\nprint(add(2, 3))"
    assert apophis.run_python(code) == "5\n"


def test_run_python_ruby_style_elsif():
    code = (
        "x = 2\n"
        "if x == 1\n"
        "    puts('one')\n"
        "elsif x == 2\n"
        "    puts('two')\n"
        "end"
    )
    assert apophis.run_python(code) == "two\n"


def test_run_python_ruby_style_unless_until():
    code_unless = "x = 1\nunless x > 1\n    puts('ok')\nend"
    assert apophis.run_python(code_unless) == "ok\n"

    code_until = (
        "x = 0\n"
        "until x == 2\n"
        "    puts(x)\n"
        "    x = x + 1\n"
        "end"
    )
    assert apophis.run_python(code_until) == "0\n1\n"


def test_run_apophis_cross_language_env():
    code = ":x = 5\n;puts x\n;y = x + 1\n:print(y)"
    assert apophis.run_apophis(code) == "5\n6\n"
