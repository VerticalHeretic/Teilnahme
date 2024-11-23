from dataclasses import dataclass
from datetime import datetime

from rich.console import Console
from rich.table import Table

from src.common.errors import NotFoundError
from src.common.models import AttendenceRecord
from src.modules.attendence_operations import AttendenceOperations


@dataclass
class AttendenceParser:
    attendence_operations: AttendenceOperations
    console = Console()
    error_console = Console(stderr=True)

    def _display_attendence_record(self, attendence_record):
        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Date", style="green")
        table.add_column("Classroom ID", style="yellow")
        table.add_column("Student ID", style="magenta")

        table.add_row(
            str(attendence_record.id),
            str(attendence_record.date),
            str(attendence_record.classroom_id),
            str(attendence_record.student_id),
        )
        self.console.print(table)

    def _display_attendence_records(self, attendence_records):
        if len(attendence_records) == 0:
            self.error_console.print("[red]No attendence records found[/red]")
            return

        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Date", style="green")
        table.add_column("Classroom ID", style="yellow")
        table.add_column("Student ID", style="magenta")

        for attendence_record in attendence_records:
            table.add_row(
                str(attendence_record.id),
                str(attendence_record.date),
                str(attendence_record.classroom_id),
                str(attendence_record.student_id),
            )
        self.console.print(table)

    def handle_attendence_records_get(self, args):
        if args.classroom_id is None and args.student_id is None and args.date is None:
            self.console.print(
                "[green] You must pass one of the following arguments: --classroom-id, --student-id, --date[/green]"
            )
            return

        if args.classroom_id is not None:
            attendence_records = (
                self.attendence_operations.get_attendence_records_by_classroom(
                    args.classroom_id
                )
            )

            if len(attendence_records) == 0:
                self.error_console.print(
                    f"[red]No attendence records found for classroom with ID: {args.classroom_id}[/red]"
                )
            else:
                self._display_attendence_records(attendence_records)
            return

        if args.student_id is not None:
            attendence_records = (
                self.attendence_operations.get_attendence_records_by_student(
                    args.student_id
                )
            )

            if len(attendence_records) == 0:
                self.error_console.print(
                    f"[red]No attendence records found for student with ID: {args.student_id}[/red]"
                )
            else:
                self._display_attendence_records(attendence_records)
            return

        if args.date is not None:
            attendence_records = (
                self.attendence_operations.get_attendence_records_by_date(args.date)
            )

            if len(attendence_records) == 0:
                self.error_console.print(
                    f"[red]No attendence records found for date {args.date}[/red]"
                )
            else:
                self._display_attendence_records(attendence_records)

    def handle_attendence_records_add(self, args):
        attendence_record = AttendenceRecord(
            date=args.date if args.date is not None else datetime.now(),
            classroom_id=args.classroom_id,
            student_id=args.student_id,
        )

        self.attendence_operations.add_attendence_record(attendence_record)
        self.console.print(
            f"[green]Attendence record with ID {attendence_record.id} added[/green]"
        )

        self._display_attendence_record(attendence_record)

    def handle_attendence_records_delete(self, args):
        try:
            self.attendence_operations.delete_attendence_record(args.id)
            self.console.print(
                f"[green]Attendence record with ID {args.id} deleted[/green]"
            )
        except NotFoundError:
            self.error_console.print(
                f"[red]Attendence record with ID {args.id} not found[/red]"
            )

    def setup_attendence_parsers(self, subparser):
        attendence_parser = subparser.add_parser(
            "attendance", help="Manage attendance records"
        )
        attendence_subparser = attendence_parser.add_subparsers(
            title="Attendance Commands",
            help="Commands for managing attendance records",
            dest="attendance_command",
        )

        # Get attendance records
        attendence_get_parser = attendence_subparser.add_parser(
            "get", help="Get attendance records"
        )
        attendence_get_parser.add_argument(
            "--classroom-id", type=int, help="Get records for classroom"
        )
        attendence_get_parser.add_argument(
            "--student-id", type=int, help="Get records for student"
        )
        attendence_get_parser.add_argument(
            "--date",
            type=lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S"),
            help="Get records for date (format: YYYY-MM-DD HH:MM:SS)",
        )
        attendence_get_parser.set_defaults(
            func=lambda args: self.handle_attendence_records_get(args)
        )

        # Add attendance record
        attendence_add_parser = attendence_subparser.add_parser(
            "add", help="Add an attendance record"
        )
        attendence_add_parser.add_argument(
            "--date",
            type=lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S"),
            help="Date of attendance (format: YYYY-MM-DD HH:MM:SS)",
        )
        attendence_add_parser.add_argument(
            "--classroom-id", required=True, type=int, help="Classroom ID"
        )
        attendence_add_parser.add_argument(
            "--student-id", required=True, type=int, help="Student ID"
        )
        attendence_add_parser.set_defaults(
            func=lambda args: self.handle_attendence_records_add(args)
        )

        # Delete attendance record
        attendence_delete_parser = attendence_subparser.add_parser(
            "delete", help="Delete an attendance record"
        )
        attendence_delete_parser.add_argument(
            "--id", required=True, type=int, help="Attendance record ID"
        )
        attendence_delete_parser.set_defaults(
            func=lambda args: self.handle_attendence_records_delete(args)
        )
