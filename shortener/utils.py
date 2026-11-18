"""Helpers: code generation and URL validation."""
import re
import secrets
import string
from urllib.parse import urlparse

ALPHABET = string.ascii_letters + string.digits
ALIAS_RE = re.compile(r"^[A-Za-z0-9_-]{3,20}$")


def generate_code(length: int = 6) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def is_valid_alias(alias: str) -> bool:
    return bool(ALIAS_RE.match(alias))
