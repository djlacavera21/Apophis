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
        'open_recent_file',
        'run_code',
        'undo',
        'redo',
        'find_text',
        'replace_text',
        'clear_output',
        'maybe_save',
        'on_close',
        'update_status_bar',
    }
    for name in required:
        assert hasattr(apophis_ide.ApophisIDE, name)
