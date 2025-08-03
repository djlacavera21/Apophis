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


def test_apophis_malbolge():
    assert apophis.apophis_malbolge() == ''


def test_apophis_malbolge_with_apo(tmp_path):
    file = tmp_path / "sample.apo"
    file.write_text("Q")
    assert apophis.apophis_malbolge(file) == ''


def test_run_apophis_basic():
    code = "x = 1\nprint(x + 2)"
    assert apophis.run_apophis(code) == "3\n"


def test_run_apophis_rejects_import():
    with pytest.raises(ValueError):
        apophis.run_apophis("import os")
