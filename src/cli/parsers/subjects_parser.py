from dataclasses import dataclass

from rich.console import Console
from rich.table import Table

from src.common.errors import NotFoundError, SemesterError
from src.common.models import DegreeName, Subject
from src.modules.subjects_operations import SubjectsOperations


@dataclass
class SubjectsParser:
    subjects_operations: SubjectsOperations
    console = Console()
    error_console = Console(stderr=True)

    def _display_subject(self, subject):
        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Semester", style="yellow")
        table.add_column("Degree", style="magenta")

        table.add_row(
            str(subject.id), subject.name, str(subject.semester), subject.degree.value
        )
        self.console.print(table)

    def _display_subjects(self, subjects):
        if len(subjects) == 0:
            self.error_console.print("[red]No subjects found[/red]")
            return

        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Semester", style="yellow")
        table.add_column("Degree", style="magenta")

        for subject in subjects:
            table.add_row(
                str(subject.id),
                subject.name,
                str(subject.semester),
                subject.degree.value,
            )
        self.console.print(table)

    def handle_subjects_get(self, args):
        if args.id is not None:
            try:
                subject = self.subjects_operations.get_subject(args.id)
                self._display_subject(subject)
            except NotFoundError:
                self.error_console.print(
                    f"[red]Subject with id {args.id} doesn't exist[/red]"
                )
            return

        if args.degree is not None and args.semester is not None:
            try:
                subjects = self.subjects_operations.get_subjects_in_degree(
                    args.degree, args.semester
                )
            except SemesterError as e:
                self.error_console.print(f"[red]{e}[/red]")
                return
        elif args.degree is not None:
            subjects = self.subjects_operations.get_subjects_in_degree(args.degree)
        else:
            subjects = self.subjects_operations.get_subjects()

        self._display_subjects(subjects)

    def handle_subjects_add(self, args):
        subject = Subject(name=args.name, semester=args.semester, degree=args.degree)
        result = self.subjects_operations.add_subject(subject)
        self.console.print(f"[green]Added subject: {result}[/green]")

    def handle_subjects_delete(self, args):
        try:
            self.subjects_operations.delete_subject(args.id)
            self.console.print(f"[green]Deleted subject with id: {args.id}[/green]")
        except NotFoundError:
            self.error_console.print(
                f"[red]Subject with id {args.id} doesn't exist[/red]"
            )

    def handle_subjects_update(self, args):
        # Create update dict with only provided fields
        update_data = {}
        if args.name is not None:
            update_data["name"] = args.name
        if args.degree is not None:
            update_data["degree"] = args.degree
        if args.semester is not None:
            update_data["semester"] = args.semester

        if update_data:
            try:
                self.subjects_operations.update_subject(args.id, Subject(**update_data))
                self.console.print(f"[green]Updated subject with id: {args.id}[/green]")
            except Exception as e:
                self.error_console.print(f"[red]{e}[/red]")
        else:
            self.error_console.print("[red]No updates provided[/red]")

    def setup_subjects_parsers(self, subparser):
        subjects_parser = subparser.add_parser("subjects", help="Manage subjects")
        subjects_subparser = subjects_parser.add_subparsers(
            title="Subjects Commands",
            help="Commands for managing subjects",
            dest="subjects_command",
        )

        # Get subjects
        subjects_get_parser = subjects_subparser.add_parser(
            "get", help="Get all subjects"
        )
        subjects_get_parser.add_argument("--id", type=int, help="Subject ID")
        subjects_get_parser.add_argument(
            "--degree", type=DegreeName, help="Subject degree"
        )
        subjects_get_parser.add_argument(
            "--semester", type=int, help="Subject semester"
        )
        subjects_get_parser.set_defaults(
            func=lambda args: self.handle_subjects_get(args)
        )

        # Add subject
        subjects_add_parser = subjects_subparser.add_parser("add", help="Add a subject")
        subjects_add_parser.add_argument(
            "--name", required=True, type=str, help="Subject name"
        )
        subjects_add_parser.add_argument(
            "--degree", required=True, type=DegreeName, help="Subject degree"
        )
        subjects_add_parser.add_argument(
            "--semester", required=True, type=int, help="Subject semester"
        )
        subjects_add_parser.set_defaults(
            func=lambda args: self.handle_subjects_add(args)
        )

        # Delete subject
        subjects_delete_parser = subjects_subparser.add_parser(
            "delete", help="Delete a subject"
        )
        subjects_delete_parser.add_argument(
            "--id", required=True, type=int, help="Subject ID"
        )
        subjects_delete_parser.set_defaults(
            func=lambda args: self.handle_subjects_delete(args)
        )

        # Update subject
        subjects_update_parser = subjects_subparser.add_parser(
            "update", help="Update a subject"
        )
        subjects_update_parser.add_argument(
            "--id", required=True, type=int, help="Subject ID"
        )
        subjects_update_parser.add_argument("--name", type=str, help="Subject name")
        subjects_update_parser.add_argument(
            "--degree", type=DegreeName, help="Subject degree"
        )
        subjects_update_parser.add_argument(
            "--semester", type=int, help="Subject semester"
        )
        subjects_update_parser.set_defaults(
            func=lambda args: self.handle_subjects_update(args)
        )
