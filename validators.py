"""Input validation independent of the terminal interface."""

from datetime import date
from decimal import Decimal, InvalidOperation


def required(value):
    """Reject empty text and control characters."""
    value = value.strip()

    if not value:
        raise ValueError("This field is required.")

    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError("Control characters are not allowed.")

    return value


def iso_date(value, past=False):
    """Validate dates in YYYY-MM-DD format."""
    value = required(value)

    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise ValueError("Enter a valid date: YYYY-MM-DD.") from None

    if parsed.isoformat() != value:
        raise ValueError("Use the format YYYY-MM-DD.")

    if past and parsed > date.today():
        raise ValueError("Birth date cannot be in the future.")

    return value


def number(value, minimum=0, maximum=None):
    """Validate numeric input and optional bounds."""
    try:
        result = Decimal(value.strip())
    except InvalidOperation:
        raise ValueError("Enter a valid number.") from None

    if not result.is_finite():
        raise ValueError("Enter a finite number.")

    if result < minimum:
        raise ValueError(f"Enter a number greater than or equal to {minimum}.")

    if maximum is not None and result > maximum:
        raise ValueError(f"Enter a number less than or equal to {maximum}.")

    return result


def grade_result(written, oral):
    """Calculate the average without discarding decimal places."""
    written_mark = number(str(written), 0, 100)
    oral_mark = number(str(oral), 0, 100)

    average = (written_mark + oral_mark) / 2

    # Preserve the original project's pass rule: average must exceed 50.
    result = "Passed" if average > 50 else "Failed"

    return str(average), result