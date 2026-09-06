"""Αποθήκευση JSON για μία ενεργή εφαρμογή ανά αρχείο δεδομένων."""

import json
import os
import tempfile
from pathlib import Path


FIELDS = {
    "courses": (
        "Title",
        "Language",
        "Description",
        "Study mode",
    ),
    "trainers": (
        "First name",
        "Last name",
        "Subject",
    ),
    "students": (
        "First name",
        "Last name",
        "Birth date",
        "Tuition fees",
    ),
    "assignments": (
        "Title",
        "Description",
        "Submission date",
        "Written mark",
        "Oral mark",
        "Average",
        "Result",
    ),
}

DEFAULT_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "records.json"
)


def empty_data():
    """Ξεχωριστή λίστα εγγραφών για κάθε κατηγορία."""
    return {key: [] for key in FIELDS}


def validate(data):
    """Ελέγχει τη δομή ενός αποθηκευμένου αρχείου."""
    if not isinstance(data, dict) or set(data) != set(FIELDS):
        raise ValueError(
            "Unexpected data format. The existing file was preserved."
        )

    for key, fields in FIELDS.items():
        if not isinstance(data[key], list):
            raise ValueError(f"Invalid collection: {key}")

        for row in data[key]:
            if not isinstance(row, dict):
                raise ValueError(f"Invalid record in {key}")

            if set(row) != set(fields):
                raise ValueError(f"Invalid fields in {key}")

            if any(not isinstance(value, str) for value in row.values()):
                raise ValueError(f"Invalid values in {key}")

    return data


def load(path=DEFAULT_PATH):
    """Φορτώνει δεδομένα ή δημιουργεί άδειες λίστες."""
    path = Path(path)

    if not path.exists():
        return empty_data()

    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    return validate(data)


def save(data, path=DEFAULT_PATH):
    """Γράφει πρώτα προσωρινό αρχείο και μετά αντικαθιστά το κανονικό."""
    validate(data)

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)

            json.dump(
                data,
                handle,
                ensure_ascii=False,
                indent=2,
                allow_nan=False,
            )

            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temporary, path)

    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)