import pytest

from vulsy.common.text.normalization import (
    _remove_hyphenation,
    _remove_punctuation,
    _remove_quotations,
    _remove_whitespace,
    _to_ascii,
)


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # Basic ASCII
        ("hello", "hello"),
        # Accented characters
        ("café", "cafe"),
        ("naïve", "naive"),
        ("résumé", "resume"),
        # Special characters
        ("über", "uber"),
        ("piñata", "pinata"),
        ("søster", "sster"),
        # Mixed case preservation
        ("CaFé", "CaFe"),
        ("ÜBER", "UBER"),
        # Edge cases
        ("", ""),
    ],
)
def test_to_ascii(input_text: str, expected: str) -> None:
    assert _to_ascii(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # Basic hyphenation cases
        ("word-\nbreak", "wordbreak"),
        ("multi-\r\nline", "multiline"),
        # Multiple hyphenations
        ("first-\nbreak-\nsecond", "firstbreaksecond"),
        ("com-\r\nplex-\r\nword", "complexword"),
        # No hyphenation cases
        ("regular text", "regular text"),
        ("hyphen-word", "hyphen-word"),
        ("new\nline", "new\nline"),
        # Edge cases
        ("", ""),  # Empty string
        ("-\n", ""),  # Just hyphenation
        ("text-\n-\nmore", "textmore"),  # Consecutive hyphenation
        ("end-\n", "end"),  # Hyphenation at end
    ],
)
def test_remove_hyphenation(input_text: str, expected: str) -> None:
    assert _remove_hyphenation(input_text) == expected


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ('Hello "World"', "Hello World"),
        ("It's a test.", "Its a test."),
        ("Quotes `should` be removed.", "Quotes should be removed."),
        ("No quotes here!", "No quotes here!"),
        ("'Single' and \"double\" quotes.", "Single and double quotes."),
        ("Mixed 'quotes' and `backticks`.", "Mixed quotes and backticks."),
    ],
)
def test_remove_quotations(input_text: str, expected_output: str) -> None:
    assert _remove_quotations(input_text) == expected_output


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("Hello! World@", "Hello World"),  # Remove exclamation and at sign
        ("This #is a test$", "This is a test"),  # Remove hash and dollar sign
        (
            "Remove % and ^ from & this * text.",
            "Remove  and  from  this  text.",
        ),  # Remove percent, caret, ampersand, and asterisk
        (
            "(Parentheses) and {braces} should be gone.",
            "Parentheses and braces should be gone.",
        ),  # Remove parentheses and braces
        ("<HTML> tags should be removed.", "HTML tags should be removed."),  # Remove angle brackets
        ("'Single' and \"double\" quotes.", "Single and double quotes."),  # Quotes removed
        ("Mixed punctuation: !@#$%^&*()_+-={}[]\\|:;<>?", "Mixed punctuation "),  # Remove all specified punctuation
        ("This is a test: does it work?", "This is a test does it work"),  # Colon removed
        ("Keep 1.0 and 2.5, but remove others!", "Keep 1.0 and 2.5 but remove others"),  # Comma removed
        ("Quotes: 'single' and \"double\".", "Quotes single and double."),  # Quotes removed
        (
            "Punctuation! Should be removed; except for: commas, periods.",
            "Punctuation Should be removed except for commas periods.",  # Expects commas and periods to remain
        ),
        ("This is a test. It works.", "This is a test It works."),  # Period at end should remain
        (
            "Numbers 1.0, 2.5, and 3.0 are valid.",
            "Numbers 1.0 2.5 and 3.0 are valid.",
        ),  # Periods in numbers should remain
    ],
)
def test_remove_punctuation(input_text: str, expected_output: str) -> None:
    assert _remove_punctuation(input_text) == expected_output


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("Hello World", "HelloWorld"),  # Simple case
        ("  Hello   World  ", "HelloWorld"),  # Multiple spaces
        ("\tHello\nWorld\t", "HelloWorld"),  # Tabs and newlines
        ("Hello\r\nWorld", "HelloWorld"),  # Carriage returns
        ("Hello \n \t World", "HelloWorld"),  # Mixed whitespace
        ("", ""),  # Empty string
        ("   \t   ", ""),  # Only whitespace
    ],
)
def test_remove_whitespace(input_text: str, expected_output: str) -> None:
    assert _remove_whitespace(input_text) == expected_output
