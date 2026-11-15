"""Validation for one fest registration row."""


class InvalidRegistration(ValueError):
    """Raised for a malformed or invalid registration row."""


def validate_row(row):
    if len(row) != 5:
        raise InvalidRegistration(f"expected 5 fields, found {len(row)}")
    register, name, department, email, events_text = (value.strip() for value in row)
    if not all((register, name, department, email, events_text)):
        raise InvalidRegistration("required field is empty")
    if "@" not in email or email.count("@") != 1:
        raise InvalidRegistration(f"invalid email {email!r}")
    local, domain = email.split("@")
    if not local or "." not in domain or domain.startswith(".") or domain.endswith(".") or any(c.isspace() for c in email):
        raise InvalidRegistration(f"invalid email {email!r}")
    events = [event.strip() for event in events_text.split(";") if event.strip()]
    if not events:
        raise InvalidRegistration("at least one event is required")
    return {"register_number": register, "name": name, "department": department,
            "email": email, "events": events}
