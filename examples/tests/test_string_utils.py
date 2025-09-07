# tests/test_string_utils.py
from mypackage.string_utils import reverse_string

def test_reverse_string():
    """Test the reverse_string function."""
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""