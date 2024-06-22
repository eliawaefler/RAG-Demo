import hashlib


def secure_hash(s):
    """
    Generate a secure hash for a given string using SHA-256.

    Args:
    s (str): The string to hash.

    Returns:
    str: The hexadecimal representation of the hash value.
    """
    # Create a sha256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the bytes of the string
    hash_object.update(s.encode('utf-8'))

    # Get the hexadecimal digest of the hash
    hash_digest = hash_object.hexdigest()

    return hash_digest


def sha_dez(any_string):
    return int(secure_hash(any_string), 16)


if __name__ == '__main__':
    # Example usage
    input_string = "John "
    result = secure_hash(input_string)
    print("SHA-256 Hash value:", result)
    print(sha_dez(input_string))
