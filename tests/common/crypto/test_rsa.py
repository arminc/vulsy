import base64
from copy import deepcopy
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from vulsy.common.crypto.rsa import SignatureError, SignatureVerificationError, sign_text, verify_signature
from vulsy.settings import settings


@pytest.fixture
def rsa_key_pair():
    private_key_path = Path("tests/data/test-private-key.pem")
    public_key_path = Path("tests/data/test-public-key.pem")
    password = "vulsy"
    return private_key_path, public_key_path, password


def settings_copy():
    return deepcopy(settings)


def test_sign_text_non_existent_key_file():
    settings = settings_copy()
    settings.rsa_private_key_path = Path("non_existent_key.pem")
    with pytest.raises(SignatureError):
        sign_text("Hello, World!", settings)


def test_sign_text_non_rsa_key(tmp_path):
    # Generate a non-RSA key (Ed25519 in this case)
    password = "vulsy"
    private_key = ed25519.Ed25519PrivateKey.generate()
    pem_data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode("utf-8")),
    )
    # Write the key to a temporary file
    key_path = tmp_path / "ed25519_private_key.pem"
    key_path.write_bytes(pem_data)

    settings = settings_copy()
    settings.rsa_private_key_path = key_path

    # Attempt to sign with the non-RSA key
    with pytest.raises(SignatureError, match="The provided key is not an RSA private key."):
        sign_text("Hello, World!", settings)


def test_sign_and_verify_valid_signature(rsa_key_pair):
    private_key_path, public_key_path, password = rsa_key_pair
    text = "Hello, World!"

    signature = sign_text(text, settings)
    assert verify_signature(text, signature, settings)


def test_invalid_signature(rsa_key_pair):
    _, public_key_path, _ = rsa_key_pair
    text = "Hello, World!"
    invalid_signature = base64.b64encode(b"invalid_signature").decode("utf-8")

    settings = settings_copy()
    settings.rsa_public_key_path = public_key_path
    assert not verify_signature(text, invalid_signature, settings)


def test_modified_text(rsa_key_pair):
    private_key_path, public_key_path, _ = rsa_key_pair
    original_text = "Hello, World!"
    modified_text = "Hello, Modified World!"

    settings = settings_copy()
    settings.rsa_private_key_path = private_key_path
    settings.rsa_public_key_path = public_key_path
    signature = sign_text(original_text, settings)
    assert not verify_signature(modified_text, signature, settings)


def test_verify_signature_non_existent_public_key_file(tmp_path):
    settings = settings_copy()
    settings.rsa_public_key_path = Path("non_existent_key.pem")
    with pytest.raises(SignatureVerificationError):
        verify_signature("Hello, World!", "invalid_signature", settings)


def test_verify_signature_non_rsa_public_key(tmp_path):
    # Generate a non-RSA key (Ed25519 in this case)
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Serialize the public key to PEM format
    pem_data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Write the key to a temporary file
    key_path = tmp_path / "ed25519_public_key.pem"
    key_path.write_bytes(pem_data)

    settings = settings_copy()
    settings.rsa_public_key_path = key_path
    # Attempt to verify with the non-RSA public key
    with pytest.raises(SignatureVerificationError, match="The provided key is not an RSA public key."):
        verify_signature("Hello, World!", "invalid_signature", settings)
