"""Text normalization utility functions."""

import unicodedata


def _to_ascii(text: str) -> str:
    """Convert text to ASCII representation.

    Args:
        text: Input text to convert

    Returns:
        ASCII representation of the input text with accents removed
    """
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def _remove_hyphenation(text: str) -> str:
    """Remove hyphenation from text by joining split words.

    Args:
        text: Input text containing potential hyphenation

    Returns:
        Text with hyphenation removed (words joined)
    """
    # Replace hyphenation patterns (hyphen followed by newline) with empty string
    return text.replace("-\n", "").replace("-\r\n", "")


def _remove_quotations(text: str) -> str:
    """Remove all quotation marks from text.

    Args:
        text: Input text containing potential quotation marks

    Returns:
        Text with all quotation marks removed
    """
    return text.replace('"', "").replace("'", "").replace("`", "")


def _remove_punctuation(text: str) -> str:
    """Remove punctuation from text, with special handling for commas and periods.

    Removes all punctuation except:
    - Keeps commas and periods that are not followed by space or end of line
    (e.g., keeps decimal points, numbers within values, and version numbers)

    Args:
        text: Input text containing punctuation

    Returns:
        Text with punctuation removed according to rules
    """
    # First handle commas and periods with lookahead
    # Replace only if followed by space or end of line
    text = text.replace(", ", " ").replace(".\n", "\n").replace(". ", " ")

    # Remove all other punctuation except remaining commas and periods
    chars_to_remove = "!@#$%^&*()_+-={}[]\\|:;<>?\"'-"
    for char in chars_to_remove:
        text = text.replace(char, "")

    return text


def _remove_whitespace(text: str) -> str:
    """Remove all whitespace characters from text.

    Removes:
    - Spaces
    - Tabs
    - Carriage returns (Windows/Mac)
    - Line feeds (Unix/Linux)
    - Form feeds
    - Vertical tabs

    Args:
        text: Input text containing whitespace

    Returns:
        Text with all whitespace characters removed
    """
    return "".join(text.split())
