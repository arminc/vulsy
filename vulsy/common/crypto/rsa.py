"""RSA signing and verification utility."""

import base64
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

from vulsy.settings import Settings, settings


class SignatureError(Exception):
    """Custom exception for signature errors."""


class SignatureVerificationError(Exception):
    """Custom exception for signature verification errors."""


def sign_text(text: str, settings: Settings = settings) -> str:
    """Sign the given text using an RSA private key which is comming from the settings.

    Args:
        text: The text to be signed. Assume utf-8 encoded.
        settings: The settings to use.

    Returns:
        str: The signature as a base64-encoded string, utf-8 encoded.
    """
    return _sign_text(settings.rsa_private_key_path, text, settings.rsa_private_key_password.get_secret_value())


def _sign_text(
    private_key_path: Path,
    text: str,
    password: str | None = None,
) -> str:
    """Sign the given text using an RSA private key.

    Args:
        private_key_path: Path to the private key file (PEM format). It needs to be an RSA private key.
        text: The text to be signed. Assume utf-8 encoded.
        password: Optional password for the private key.

    Returns:
        str: The signature as a base64-encoded string, utf-8 encoded.

    Raises:
        SignatureError: If there's an error during the signing process.
    """
    try:
        with Path.open(private_key_path, "rb") as key_file:
            private_key = load_pem_private_key(key_file.read(), password=password.encode("utf-8") if password else None)

        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise SignatureError("The provided key is not an RSA private key.")

        signature = private_key.sign(
            text.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA512(),
        )
        return base64.b64encode(signature).decode("utf-8")
    except (ValueError, TypeError, OSError) as e:
        raise SignatureError from e


def verify_signature(text: str, signature: str, settings: Settings = settings) -> bool:
    """Verify the signature of the given text using an RSA public key which is comming from the settings.

    Args:
        text: The text to be verified. Assume utf-8 encoded.
        signature: The signature to verify against (as a base64-encoded string).
        settings: The settings to use.

    Returns:
        bool: True if the signature is valid.
    """
    return _verify_signature(settings.rsa_public_key_path, text, signature)


def _verify_signature(
    public_key_path: Path,
    text: str,
    signature: str,
) -> bool:
    """Verify the signature of the given text using an RSA public key.

    Args:
        public_key_path: Path to the public key file (PEM format).
        text: The text to be verified. Assume utf-8 encoded.
        signature: The signature to verify against (as a base64-encoded string).

    Returns:
        bool: True if the signature is valid.

    Raises:
        SignatureVerificationError: If there's an error during verification.
    """
    try:
        with Path.open(public_key_path, "rb") as key_file:
            public_key = load_pem_public_key(key_file.read())

        if not isinstance(public_key, rsa.RSAPublicKey):
            raise SignatureVerificationError("The provided key is not an RSA public key.")

        public_key.verify(
            base64.b64decode(signature),
            text.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA512(),
        )
        return True
    except InvalidSignature:
        return False
    except (ValueError, TypeError, OSError) as e:
        raise SignatureVerificationError from e
