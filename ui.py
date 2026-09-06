"""Banner, χρώματα, μενού και παρουσίαση εγγραφών."""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from storage import FIELDS


console = Console()


def banner():
    title = Text(
        ">_  PYTHON DATA SHELL",
        style="bold cyan",
        justify="center",
    )

    title.append(
        "\nACADEMY MANAGER  /  v2.0",
        style="bold white",
    )

    title.append(
        "\nCourses  |  Trainers  |  Students  |  Assignments",
        style="dim",
    )

    console.print(
        Panel(
            title,
            border_style="cyan",
            padding=(1, 2),
            subtitle="sakispat / local workspace",
        )
    )


def dashboard(data):
    """Εμφανίζει μετρητές και επιλογές."""
    stats = Table(
        box=box.SIMPLE,
        expand=True,
        border_style="cyan",
    )

    for key in FIELDS:
        stats.add_column(
            key.upper(),
            justify="center",
            style="bold cyan",
        )

    stats.add_row(
        *(str(len(data[key])) for key in FIELDS)
    )

    console.print(stats)

    menu = Table(
        box=None,
        show_header=False,
        padding=(0, 2),
    )

    options = [
        ("1", "Add course"),
        ("2", "Add trainer"),
        ("3", "Add student"),
        ("4", "Add assignment"),
        ("5", "View records"),
        ("6", "Search records"),
        ("0", "Exit"),
    ]

    for key, label in options:
        menu.add_row(
            Text(key, style="bold cyan"),
            Text(label),
        )

    console.print(
        Panel(
            menu,
            title="MAIN MENU",
            border_style="blue",
        )
    )

    console.print(
        "Saved after each entry. "
        "Type /cancel in a form to go back.",
        style="dim",
    )


def show_records(key, rows):
    """Πίνακες σε μεγάλο terminal, κάρτες σε μικρό."""
    if not rows:
        console.print(
            f"{key.title()}: no records.",
            style="yellow",
        )
        return

    if console.width < 100:
        for index, row in enumerate(rows, 1):
            table = Table.grid(padding=(0, 2))

            for field in FIELDS[key]:
                table.add_row(
                    Text(field, style="cyan"),
                    Text(row[field]),
                )

            console.print(
                Panel(
                    table,
                    title=f"{key.title()} #{index}",
                    border_style="blue",
                )
            )

        return

    table = Table(
        title=key.title(),
        box=box.ROUNDED,
        header_style="bold cyan",
        border_style="blue",
        show_lines=True,
    )

    table.add_column("#", style="dim")

    for field in FIELDS[key]:
        table.add_column(field, overflow="fold")

    for index, row in enumerate(rows, 1):
        table.add_row(
            str(index),
            *(Text(row[field]) for field in FIELDS[key]),
        )

    console.print(table)