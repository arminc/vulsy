import pytest

from vulsy.common.crypto.sha256 import generate_sha256_hash


def test_generate_sha256_hash():
    """Test the generate_sha256_hash function."""
    # Test case 1: Empty string
    assert generate_sha256_hash("") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    # Test case 2: Simple string
    assert generate_sha256_hash("hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

    # Test case 3: String with special characters
    assert generate_sha256_hash("!@#$%^&*()") == "95ce789c5c9d18490972709838ca3a9719094bca3ac16332cfec0652b0236141"

    # Test case 4: Long string
    long_string = "a" * 1000
    assert len(generate_sha256_hash(long_string)) == 64

    # Test case 5: Unicode string
    assert generate_sha256_hash("こんにちは") == "125aeadf27b0459b8760c13a3d80912dfa8a81a68261906f60d87f4a0268646c"


def test_generate_sha256_hash_type_error():
    """Test that generate_sha256_hash raises a TypeError for non-string input."""
    with pytest.raises(AttributeError):
        generate_sha256_hash(123)  # type: ignore


def test_generate_sha256_hash_consistency():
    """Test that generate_sha256_hash produces consistent results."""
    input_string = "test string"
    hash1 = generate_sha256_hash(input_string)
    hash2 = generate_sha256_hash(input_string)
    assert hash1 == hash2
