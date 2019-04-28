import hashlib

ALICE_USERNAME = "alice@wonderland.org"
ALICE_PASSWORD = "IntoTheLookingGlass"
ALICE_HASH = hashlib.md5(ALICE_PASSWORD.encode()).hexdigest()

MADHATTER_USERNAME = "mad.hatter@wonderland.org"
MADHATTER_PASSWORD = "madhatter"
MADHATTER_HASH = hashlib.md5(MADHATTER_PASSWORD.encode()).hexdigest()

PASSWORD_DB = [
    (MADHATTER_USERNAME, MADHATTER_PASSWORD, MADHATTER_HASH),
    (ALICE_USERNAME, ALICE_PASSWORD, ALICE_HASH),
    # Use alice's password for bill too, because I need an example of two users
    # with the same password for the conversation on salting.
    ("bill.the.lizard@wonderland.org", ALICE_PASSWORD, ALICE_HASH),
]

PASSWORD_DB_USERS = [row[0] for row in PASSWORD_DB]

HASH_LIST = [
    ("544842c3b9a0d0c1562f555bc12444cd", "pentiumm"),
    ("544894d3b1f5b4ed3ebebc3c0a59bc25", "thisisit"),
    ("54489653fb9e8da76c4dbd03bda11ac2", "just4fun"),
    ("5448c1f319e45c44e2f8b602f899500c", "sibila"),
    ("5449175df9f6179154fa26f238c36e54", "ruairid"),
    ("54491de8a3f2b61da65a7322228d79c7", "madhatter"),
    ("54499e18a660b0d5a978dcf06bb8acec", "crxesi"),
    ("544a0180deb641dc1ca70169dd2a6cbc", "lespaul1"),
    ("544aab8af92829deb945d9f8cd4d5ad4", "7532789"),
    ("544b3befd3b2964fa66cea518c5b3bd7", "g00fy"),
    ("544babc97987d460e6b696a95bf8f7b5", "phpbbmystix"),
    ("544c358ceaf975db88198563ffe2510f", "xp0dxrh"),
]