import secrets


def generate_verification_id() -> str:
    return secrets.token_urlsafe(32)
