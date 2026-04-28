import re

from myapp import generate_password


SPECIALS = "#[]().,!@&^%*"


def is_valid(pw: str) -> bool:
    if not (8 <= len(pw) <= 16):
        return False
    if not re.search(r"[0-9]", pw):
        return False
    if not re.search(r"[a-z]", pw):
        return False
    if not re.search(r"[A-Z]", pw):
        return False
    if not any(ch in SPECIALS for ch in pw):
        return False
    return True


def main() -> None:
    for _ in range(200):
        pw = generate_password()
        assert is_valid(pw), pw
    print("OK")


if __name__ == "__main__":
    main()

