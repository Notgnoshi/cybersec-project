import hashlib


def get_SHA1_digest(text):
    return hashlib.sha1(text.encode()).hexdigest()


def get_SHA2_digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def get_SHA3_digest(text):
    return hashlib.sha3_256(text.encode()).hexdigest()


def get_MD5_digest(text):
    return hashlib.md5(text.encode()).hexdigest()
