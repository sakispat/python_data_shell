# Python Data Shell

A terminal application for managing courses, trainers, students,
and assignments, built with Python and Rich.

## Features

- Colored banner and interactive menu
- Record counters for each category
- Tables for wide terminals and cards for narrow terminals
- Input validation for required fields, dates, fees, and marks
- Case-insensitive search across all records
- Automatic local JSON storage
- Form cancellation with `/cancel`

## Requirements

- Python 3.10 or newer
- pip
- Git, if cloning the repository

An internet connection is needed to download the project and install
dependencies. Once installed, the application runs locally.

## Download the project

Run these commands in PowerShell on Windows or Terminal on Linux/macOS:

```bash
git clone https://github.com/sakispat/python_data_shell.git
cd python_data_shell
```

Alternatively, download the ZIP from GitHub using **Code → Download ZIP**,
extract it, and open a terminal in the folder containing `app.py`.

If you already have the project locally, open its existing folder.

## Windows installation

Check your Python version:

```powershell
py --version
```

Create a virtual environment:

```powershell
py -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the application:

```powershell
.\.venv\Scripts\python.exe app.py
```

These commands do not require virtual-environment activation or
changes to the PowerShell execution policy.

If `py` is unavailable but `python` points to Python 3.10 or newer,
use `python` instead of `py` to create the environment.

## Linux installation

Check your Python version:

```bash
python3 --version
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Install dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Run the application:

```bash
.venv/bin/python app.py
```

If creating the virtual environment fails because `venv` or
`ensurepip` is missing, install your distribution's venv support
package for the selected Python version, then retry.

Use the virtual environment for dependencies; do not install them
with `sudo pip`.

## macOS installation

Check your Python version:

```bash
python3 --version
```

If Python is missing or older than 3.10, install a supported Python 3
release from https://www.python.org/downloads/macos/ and reopen Terminal.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Install dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Run the application:

```bash
.venv/bin/python app.py
```

## Run the project again

Open a terminal in the project folder and run the command for your OS.

**Windows:**

```powershell
.\.venv\Scripts\python.exe app.py
```

**Linux / macOS:**

```bash
.venv/bin/python app.py
```

You do not need to recreate the virtual environment each time.
Reinstall dependencies when `requirements.txt` changes.

## Usage

| Option |      Action         |
|--------|---------------------|
| `1`    | Add a course        |
| `2`    | Add a trainer       |
| `3`    | Add a student       |
| `4`    | Add an assignment   |
| `5`    | View all records    |
| `6`    | Search records      |
| `0`    | Exit                |

Type `/cancel` while filling in a form to return to the main menu.

Pressing `Ctrl+C` exits the application. Any unfinished entry is
discarded; previously saved records remain available.

### Input rules

- Required text fields cannot be blank.
- Dates must use `YYYY-MM-DD`.
- Birth dates cannot be in the future.
- Study mode must be `full-time` or `part-time`.
- Tuition fees must be nonnegative amounts, not installment counts.
- Use a decimal point for amounts, for example `1500.50`.
- Written and oral marks must be between `0` and `100`.
- The average is calculated without rounding down.
- The original pass rule is preserved: average must be greater than `50`.

## Data storage

Completed entries are saved automatically in:

```text
data/records.json
```

The path is relative to the application folder, regardless of the
directory from which you launch Python.

The application creates the `data` folder when saving the first entry.
Records are loaded again on the next startup.

To use a different data file:

**Windows:**

```powershell
.\.venv\Scripts\python.exe app.py --data-file "data/demo.json"
```

**Linux / macOS:**

```bash
.venv/bin/python app.py --data-file "data/demo.json"
```

Use only one running application instance per data file.

Data is stored as plain JSON and is not encrypted. Keep backups of
your data folder. The default `data/` folder is excluded from Git.

If the existing data file is malformed, startup stops without
overwriting it.

## Project structure

|       File            |               Responsibility                      |
|-----------------------|---------------------------------------------------|
| `app.py`              | Menu, forms, and application flow                 |
| `ui.py`               | Banner, colors, tables, and cards                 |
| `validators.py`       | Input validation and grade calculation            |
| `storage.py`          | JSON loading, structure validation, and saving    |
| `requirements.txt`    | Application dependencies                          |
| `tests/test_app.py`   | Automated tests                                   |
| `.gitignore`          | Files excluded from Git                           |

## Run tests

Run the following command from the project folder.

**Windows:**

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**Linux / macOS:**

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Tests cover input validation, grade calculation, persistent storage,
failed saves, and application flows.

## Troubleshooting

### Python command not found

Install Python 3.10 or newer and reopen your terminal.

On Windows, try `py --version`.
On Linux/macOS, try `python3 --version`.

### No module named rich

Install dependencies with the same virtual-environment interpreter
used to run the application. Follow the installation command for your OS.

### Cannot find app.py or requirements.txt

Navigate to the project folder before running the commands.

### Cannot load data

Read the error message and check the data file's permissions and content.
If it is damaged, preserve a copy and restore a valid backup.

### Entry NOT saved

Check available disk space and write permissions.
After fixing the issue, enter the record again.

## Current scope

Records are stored independently. Course enrollment relationships,
editing, deletion, and installment tracking are not implemented
in this version.