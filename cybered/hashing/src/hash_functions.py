import hashlib


def get_SHA1_digest(text):
    """Compute the SHA1 hash of the given text."""
    return hashlib.sha1(text.encode()).hexdigest()


def get_SHA2_digest(text):
    """Compute the SHA2 hash of the given text."""
    return hashlib.sha256(text.encode()).hexdigest()


def get_SHA3_digest(text):
    """Compute the SHA3 hash of the given text."""
    return hashlib.sha3_256(text.encode()).hexdigest()


def get_MD5_digest(text):
    """Compute the MD5 hash of the given text."""
    return hashlib.md5(text.encode()).hexdigest()
