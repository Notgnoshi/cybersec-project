import hashlib


def add_key(text, key):
    return key + text + key


def get_SHA1_digest(text, key=""):
    """Compute the SHA1 hash of the given text."""
    return hashlib.sha1(add_key(text, key).encode()).hexdigest()


def get_SHA2_digest(text, key=""):
    """Compute the SHA2 hash of the given text."""
    return hashlib.sha256(add_key(text, key).encode()).hexdigest()


def get_SHA3_digest(text, key=""):
    """Compute the SHA3 hash of the given text."""
    return hashlib.sha3_256(add_key(text, key).encode()).hexdigest()


def get_MD5_digest(text, key=""):
    """Compute the MD5 hash of the given text."""
    return hashlib.md5(add_key(text, key).encode()).hexdigest()
