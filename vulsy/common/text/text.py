"""Text normalization."""

from vulsy.common.text.normalization import (
    _remove_hyphenation,
    _remove_punctuation,
    _remove_quotations,
    _remove_whitespace,
    _to_ascii,
)


def normalize(text: str) -> str:
    """Normalize text by converting to lowercase, ASCII, and removing special characters.

    Args:
        text: Input text to normalize

    Returns:
        Normalized text in lowercase ASCII without hyphenation or quotation marks
    """
    text = text.lower()
    text = _to_ascii(text)
    text = _remove_hyphenation(text)
    text = _remove_quotations(text)
    text = _remove_punctuation(text)
    return _remove_whitespace(text)
