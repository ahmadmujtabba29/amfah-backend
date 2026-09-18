import json
from pathlib import Path

USERS_FILE = Path(__file__).resolve().parents[1] / "data" / "users.json"


def get_user_by_email(email: str) -> dict | None:
    """
    Load users from the temporary JSON store and return a matching user.

    Later this can be replaced with a database query without changing auth_service.
    """
    if not USERS_FILE.exists():
        return None

    with USERS_FILE.open("r", encoding="utf-8") as file:
        users = json.load(file)

    if not isinstance(users, list):
        return None

    email_lower = email.lower()
    for user in users:
        if not isinstance(user, dict):
            continue
        stored_email = user.get("email")
        if isinstance(stored_email, str) and stored_email.lower() == email_lower:
            return user

    return None
