# Python Data Shell

A terminal application for managing courses, trainers,
students and assignments.

## Requirements

- Python 3.10 or newer
- Rich

## Run on Windows

Open PowerShell in the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

## Features

- Colored banner and menu
- Record counters
- Tables and responsive record cards
- Separate forms for each category
- Search across all records
- Automatic JSON persistence
- Input validation
- Form cancellation with /cancel

## Menu

1. Add course
2. Add trainer
3. Add student
4. Add assignment
5. View records
6. Search records
0. Exit

## Data

Completed records are saved in:

data/records.json

Dates use YYYY-MM-DD.

Tuition fees are nonnegative amounts, not installment counts.

Marks must be between 0 and 100.
The average is calculated without rounding down.
The original pass rule is preserved: average > 50.

An unfinished entry is discarded on cancellation or exit.

Use one application instance per data file.
Keep backups of your data directory.

## Project structure

- app.py: application flow and forms
- ui.py: terminal interface
- validators.py: input validation
- storage.py: JSON persistence
- tests/test_app.py: automated tests

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Scope

Records are stored independently.
Course enrollment relationships, editing and deletion
are not implemented in this version.
