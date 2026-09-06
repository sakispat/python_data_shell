"""Κεντρική εφαρμογή Python Data Shell."""

import argparse
import copy
from pathlib import Path

from storage import DEFAULT_PATH, FIELDS, load, save
from ui import console, banner, dashboard, show_records
from validators import required, iso_date, number, grade_result


class Cancelled(Exception):
    """Ο χρήστης ακύρωσε την καταχώριση."""


def ask(label, validator=required):
    """Επαναλαμβάνει μόνο το πεδίο που περιέχει λάθος."""
    while True:
        value = console.input(
            f"[cyan]{label}[/cyan] > "
        )

        if value.strip().casefold() == "/cancel":
            raise Cancelled

        try:
            return validator(value)

        except ValueError as error:
            console.print(
                str(error),
                style="red",
                markup=False,
            )


def study_mode(value):
    value = required(value).casefold()

    if value not in ("full-time", "part-time"):
        raise ValueError(
            "Choose full-time or part-time."
        )

    return value


def collect(key):
    """Συγκεντρώνει τα πεδία μίας νέας εγγραφής."""
    console.rule(f"NEW {key.upper()}")

    row = {}

    for field in FIELDS[key]:
        # Αυτά υπολογίζονται αυτόματα.
        if field in ("Average", "Result"):
            continue

        validator = required

        if field == "Study mode":
            validator = study_mode

        elif field == "Birth date":
            validator = lambda value: iso_date(
                value,
                past=True,
            )

        elif field == "Submission date":
            validator = iso_date

        elif field == "Tuition fees":
            validator = lambda value: str(number(value))

        elif field in ("Written mark", "Oral mark"):
            validator = lambda value: str(
                number(value, 0, 100)
            )

        row[field] = ask(field, validator)

    if key == "assignments":
        average, result = grade_result(
            row["Written mark"],
            row["Oral mark"],
        )

        row["Average"] = average
        row["Result"] = result

    return row


def run(path):
    banner()

    try:
        data = load(path)

    except (OSError, ValueError) as error:
        console.print(
            f"Cannot load data: {error}",
            style="red",
            markup=False,
        )

        console.print(
            "Existing file preserved. "
            "Restore a valid backup before retrying."
        )

        return 1

    while True:
        dashboard(data)

        choice = console.input(
            "[bold cyan]data-shell[/bold cyan] > "
        ).strip().casefold()

        if choice in ("0", "x", "exit"):
            console.print(
                "Goodbye! Completed entries are saved.",
                style="green",
            )
            return 0

        try:
            if choice in ("1", "2", "3", "4"):
                key = tuple(FIELDS)[int(choice) - 1]

                row = collect(key)

                updated = copy.deepcopy(data)
                updated[key].append(row)

                # Πρώτα αποθήκευση στον δίσκο.
                save(updated, path)

                # Μετά ενημέρωση των δεδομένων στη μνήμη.
                data = updated

                console.print(
                    "Record saved.",
                    style="bold green",
                )

                show_records(key, [row])

            elif choice in ("5", "6"):
                query = (
                    ask("Search").casefold()
                    if choice == "6"
                    else ""
                )

                for key in FIELDS:
                    rows = [
                        row
                        for row in data[key]
                        if not query
                        or any(
                            query in value.casefold()
                            for value in row.values()
                        )
                    ]

                    show_records(key, rows)

            else:
                console.print(
                    "Choose 0 through 6.",
                    style="yellow",
                )

        except Cancelled:
            console.print(
                "Entry cancelled.",
                style="yellow",
            )

        except OSError as error:
            console.print(
                f"Entry NOT saved: {error}",
                style="red",
                markup=False,
            )

            console.print(
                "Fix file permissions or disk space, "
                "then enter the record again."
            )


def main():
    parser = argparse.ArgumentParser(
        description="Python Data Shell - Academy Manager"
    )

    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_PATH,
    )

    args = parser.parse_args()

    try:
        return run(args.data_file)

    except (KeyboardInterrupt, EOFError):
        console.print(
            "\nGoodbye. Any unfinished entry was discarded.",
            style="yellow",
        )

        return 0


if __name__ == "__main__":
    raise SystemExit(main())