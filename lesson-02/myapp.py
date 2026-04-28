from __future__ import annotations

import random
import string
import time
from urllib.parse import parse_qs

_SPECIALS = "#[]().,!@&^%*"


def generate_password(min_len: int = 8, max_len: int = 16) -> str:
    min_len = max(8, int(min_len))
    max_len = min(16, int(max_len))
    if min_len > max_len:
        min_len = max_len

    rng = random.SystemRandom()
    length = rng.randint(min_len, max_len)

    required = [
        rng.choice(string.digits),
        rng.choice(string.ascii_lowercase),
        rng.choice(string.ascii_uppercase),
        rng.choice(_SPECIALS),
    ]

    alphabet = string.ascii_letters + string.digits + _SPECIALS
    rest = [rng.choice(alphabet) for _ in range(length - len(required))]

    chars = required + rest
    rng.shuffle(chars)
    return "".join(chars)


def _get_query_param(environ: dict, name: str) -> str | None:
    qs = environ.get("QUERY_STRING", "")
    if not qs:
        return None
    parsed = parse_qs(qs, keep_blank_values=True)
    values = parsed.get(name)
    return values[0] if values else None


def app(environ, start_response):
    min_len_s = _get_query_param(environ, "min")
    max_len_s = _get_query_param(environ, "max")

    try:
        min_len = int(min_len_s) if min_len_s is not None else 8
        max_len = int(max_len_s) if max_len_s is not None else 16
    except ValueError:
        min_len, max_len = 8, 16

    password = generate_password(min_len=min_len, max_len=max_len)
    time.sleep(0.05)

    data = (password + "\n").encode("utf-8")
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(data))),
        ],
    )
    return iter([data])
