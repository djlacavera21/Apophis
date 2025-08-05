import apophis_ide


def test_exports():
    assert hasattr(apophis_ide, 'ApophisIDE')
    assert callable(apophis_ide.launch)
