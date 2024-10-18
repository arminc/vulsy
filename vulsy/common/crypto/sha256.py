"""SHA256 hashing utility."""

import hashlib


def generate_sha256_hash(data: str) -> str:
    """Generate a SHA256 hash from the data.

    Args:
        data (str): The data to hash.

    Returns:
        str: The hexadecimal representation of the SHA256 hash.
    """
    return hashlib.sha256(data.encode()).hexdigest()
