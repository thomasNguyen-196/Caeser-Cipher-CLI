"""Core Caesar cipher logic."""

def caesar_encrypt(plaintext: str, key: int) -> str:
    """
    Encrypts plaintext using the Caesar cipher algorithm.

    Args:
        plaintext: The string to encrypt.
        key: The integer shift key.

    Returns:
        The encrypted string.
    """
    result = []
    for char in plaintext:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result.append(chr((ord(char) - shift + key) % 26 + shift))
        else:
            result.append(char)
    return "".join(result)

def caesar_decrypt(ciphertext: str, key: int) -> str:
    """
    Decrypts ciphertext using the Caesar cipher algorithm.

    Args:
        ciphertext: The string to decrypt.
        key: The integer shift key.

    Returns:
        The decrypted string.
    """
    return caesar_encrypt(ciphertext, -key)
