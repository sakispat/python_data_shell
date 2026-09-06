import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import run
from storage import load, save, empty_data
from validators import required, iso_date, number, grade_result


class ValidationTests(unittest.TestCase):
    def test_required_rejects_blanks_and_escape(self):
        for value in (" ", "", "\x1b[31m"):
            with self.assertRaises(ValueError):
                required(value)

    def test_numeric_limits(self):
        for value in ("nan", "Infinity", "-1", "101", "abc"):
            with self.assertRaises(ValueError):
                number(value, 0, 100)

    def test_average_and_pass_threshold(self):
        self.assertEqual(
            grade_result("50", "51"),
            ("50.5", "Passed"),
        )

        self.assertEqual(
            grade_result("50", "50"),
            ("50", "Failed"),
        )

    def test_dates(self):
        self.assertEqual(
            iso_date("2024-02-29"),
            "2024-02-29",
        )

        for value in ("2025-02-29", "20240229", "abc"):
            with self.assertRaises(ValueError):
                iso_date(value)

        with self.assertRaises(ValueError):
            iso_date("2999-01-01", past=True)


class StorageTests(unittest.TestCase):
    def test_multiple_entries_survive_reload(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.json"
            data = load(path)

            for name in ("Θανάσης", "Μαρία"):
                data["trainers"].append({
                    "First name": name,
                    "Last name": "Test",
                    "Subject": "Python",
                })

                save(data, path)

            self.assertEqual(load(path), data)

    def test_corrupt_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.json"

            path.write_text("{broken", encoding="utf-8")

            self.assertEqual(run(path), 1)

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "{broken",
            )

    def test_failed_save_preserves_original(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.json"

            save(empty_data(), path)
            original = path.read_bytes()

            with patch(
                "storage.os.replace",
                side_effect=OSError("Disk error"),
            ):
                with self.assertRaises(OSError):
                    save(empty_data(), path)

            self.assertEqual(path.read_bytes(), original)

            self.assertEqual(
                list(Path(folder).glob("*.tmp")),
                [],
            )

    def test_forms_search_cancel_and_restart(self):
        answers = [
            "1", "Python", "Python", "Basics", "full-time",
            "2", "Ada", "Lovelace", "Programming",
            "3", "Alan", "Turing", "1912-06-23", "1500.50",
            "4", "Assignment 1", "Build a CLI",
            "2026-10-01", "50", "51",
            "6", "python",
            "5",
            "1", "/cancel",
            "0",
        ]

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.json"

            with patch("ui.console.input", side_effect=answers):
                self.assertEqual(run(path), 0)

            data = load(path)

            self.assertTrue(
                all(len(rows) == 1 for rows in data.values())
            )

            self.assertEqual(
                data["assignments"][0]["Average"],
                "50.5",
            )

            with patch(
                "ui.console.input",
                side_effect=["5", "0"],
            ):
                self.assertEqual(run(path), 0)

            self.assertEqual(load(path), data)


if __name__ == "__main__":
    unittest.main()