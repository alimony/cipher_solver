from string import ascii_lowercase, ascii_uppercase

from cipher_solver.consts import ENGLISH_LETTERS_BY_FREQUENCY, STANDARD_ALPHABET_SIZE


def common_to_alphabetical_key(common_key):
    """Convert a common key to an alphabetical key.

    Convert a key ordered by most common letter to a key ordered by most common
    letter at indices determined by the English alphabet, i.e. the most common letter
    will be at index 4, second most common at index 18, and so on.

    Parameters
    ----------
    common_key : str
        The common key to convert to an alphabetical key.

    Returns
    -------
    alphabetical_key : str
        The alphabetical key.
    """

    alphabetical_key = [""] * STANDARD_ALPHABET_SIZE

    for key_letter, english_letter in zip(common_key, ENGLISH_LETTERS_BY_FREQUENCY):
        index = ascii_lowercase.index(english_letter)
        alphabetical_key[index] = key_letter

    return "".join(alphabetical_key)


def alphabetical_to_common_key(alphabetical_key):
    """Convert an alphabetical key to a common key.

    Convert a key ordered by most common letters at indices determined by the English
    alphabet to a key ordered by most common letter, i.e. the most common letter will
    be at index 0, second most common at index 1, and so on.

    Parameters
    ----------
    alphabetical_key : str
        The alphabetical key to convert to a common key.

    Returns
    -------
    common_key : str
        The common key.
    """

    indices = [ascii_lowercase.index(letter) for letter in ENGLISH_LETTERS_BY_FREQUENCY]

    return "".join([alphabetical_key[index] for index in indices])


def encrypt(plaintext, alphabetical_key):
    """Create a ciphertext from the passed plaintext, using an alphabetical key.

    Case and special chars are preserved.

    Parameters
    ----------
    plaintext : str
        The plaintext to encrypt.
    alphabetical_key : str
        The alphabetical key to use when creating the ciphertext.

    Returns
    -------
    ciphertext : str
        The encrypted text.
    """

    translation_table = {}

    for plain_letter, key_letter in zip(ascii_lowercase, alphabetical_key):
        translation_table[plain_letter] = key_letter

    ciphertext = ""

    for c in plaintext:
        is_upper = c in ascii_uppercase
        letter = translation_table.get(c.lower(), c)
        if is_upper:
            letter = letter.upper()
        ciphertext += letter

    return ciphertext
