from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    return password_hash.verify(
        password,
        hashed_password
    )



# password_hash.verify(
#     "hello123",
#     "$argon2id$..........."
# )

# Conceptually, verify() does something like:

# "hello123"
#      ↓
# hash/check using the information
# contained in the stored hash
#      ↓
# compare with stored hash
#      ↓
#    MATCH?
#    /   \
#  YES    NO
#   ↓      ↓
# True   False

# It does NOT do:

# "$argon2id$..........."
#         ↓
#      decrypt
#         ↓
#    "hello123"    ❌
# Why?

# Password hashing is designed to be one-way:

# Password ───────→ Hash
#    ↑                │
#    │                │
#    └──── can't ─────┘
#           reverse

# So even if someone steals your database and gets:

# $argon2id$...........

# they shouldn't be able to simply "decrypt" it and obtain the password.