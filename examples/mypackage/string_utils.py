"""String utility functions for testing smart-test."""

def reverse_string(text):
    """Reverse a string."""
    return text[::-1]
    
def count_words(text):
    """Count words in a string."""
    if not text:
        return 0
    return len(text.split())