import pytest

from vulsy.common.text import normalize


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # Basic normalization
        ("Hello World!", "helloworld"),
        # Complex case with multiple normalizations
        ("Café-\nStyle", "cafestyle"),
        # Quotations and punctuation
        ("'Hello, World!' she said.", "helloworldshesaid."),
        # Numbers and decimals preserved
        ("Version 1.0, Price: $2.5", "version1.0price2.5"),
        # Mixed case with special chars
        ("über-\nCAFÉ 'test'", "ubercafetest"),
        # Multiple whitespace types
        ("Hello  \t\nWorld", "helloworld"),
        # Edge cases
        ("", ""),
        (" ", ""),
        # Complex real-world example
        ("My 'café-\nrestaurant' is at 123.5° N, price: $20.00!", "mycaferestaurantisat123.5nprice20.00"),
    ],
)
def test_normalize(input_text: str, expected: str) -> None:
    """Test text normalization with various input cases.

    Tests the complete normalization pipeline including:
    - Lowercase conversion
    - ASCII conversion
    - Hyphenation removal
    - Quotation removal
    - Punctuation removal
    - Whitespace removal
    """
    assert normalize(input_text) == expected
