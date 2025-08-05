import apophis_ide


def test_exports():
    assert hasattr(apophis_ide, 'ApophisIDE')
    assert callable(apophis_ide.launch)


def test_class_methods():
    required = {
        'new_file',
        'open_file',
        'save_file',
        'save_file_as',
        'run_code',
        'undo',
        'redo',
        'clear_output',
        'maybe_save',
        'on_close',
        'update_status_bar',
    }
    for name in required:
        assert hasattr(apophis_ide.ApophisIDE, name)
