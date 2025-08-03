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


def test_run_python_rejects_import():
    with pytest.raises(ValueError):
        apophis.run_python("import os")


def test_run_apophis_mixed_string():
    code = ":print('A', end='')\n>b\n:print('B', end='')"
    assert apophis.run_apophis(code) == "AsB"


def test_run_apophis_mixed_file(tmp_path):
    file = tmp_path / "hybrid.apop"
    file.write_text(":print('hi', end='')\n>b\n")
    assert apophis.run_file(file) == "his"
