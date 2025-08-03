import apophis
import malbolge


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
