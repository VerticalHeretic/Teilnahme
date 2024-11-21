from dataclasses import dataclass

from rich.console import Console
from rich.table import Table

from src.common.errors import NotFoundError, SemesterError
from src.common.models import DegreeName, Student
from src.modules.students_operations import StudentsOperations


@dataclass
class StudentsParser:
    students_operations: StudentsOperations
    console = Console()
    error_console = Console(stderr=True)

    def _display_student(self, student):
        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Surname", style="green")
        table.add_column("Degree", style="yellow")
        table.add_column("Semester", style="magenta")

        table.add_row(
            str(student.id),
            student.name,
            student.surname,
            str(student.degree),
            str(student.semester),
        )
        self.console.print(table)

    def _display_students(self, students):
        if len(students) == 0:
            self.error_console.print("[red]No students found[/red]")
            return

        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Surname", style="green")
        table.add_column("Degree", style="yellow")
        table.add_column("Semester", style="magenta")

        for student in students:
            table.add_row(
                str(student.id),
                student.name,
                student.surname,
                student.degree.value,
                str(student.semester),
            )
        self.console.print(table)

    def handle_students_get(self, args):
        if args.id is not None:
            try:
                student = self.students_operations.get_student(args.id)
                self._display_student(student)
            except NotFoundError:
                self.error_console.print(
                    f"[red]Student with id {args.id} doesn't exist[/red]"
                )
            return

        if args.degree is not None and args.semester is not None:
            try:
                students = self.students_operations.get_students_in_degree(
                    args.degree, args.semester
                )
            except SemesterError as e:
                self.error_console.print(f"[red]{e}[/red]")
                return
        elif args.degree is not None:
            students = self.students_operations.get_students_in_degree(args.degree)
        else:
            students = self.students_operations.get_students()

        self._display_students(students)

    def handle_students_add(self, args):
        student = Student(
            name=args.name,
            surname=args.surname,
            degree=args.degree,
            semester=args.semester,
        )
        result = self.students_operations.add_student(student)
        self.console.print(f"[green]Added student: {result}[/green]")

    def handle_students_delete(self, args):
        self.students_operations.delete_student(args.id)
        self.console.print(f"[green]Deleted student with id: {args.id}[/green]")

    def handle_students_update(self, args):
        # Create update dict with only provided fields
        update_data = {}
        if args.name is not None:
            update_data["name"] = args.name
        if args.surname is not None:
            update_data["surname"] = args.surname
        if args.degree is not None:
            update_data["degree"] = args.degree
        if args.semester is not None:
            update_data["semester"] = args.semester

        if update_data:
            try:
                self.students_operations.update_student(args.id, Student(**update_data))
                self.console.print(f"[green]Updated student with id: {args.id}[/green]")
            except Exception as e:
                self.error_console.print(f"[red]{e}[/red]")
        else:
            self.error_console.print("[red]No updates provided[/red]")

    def setup_students_parsers(self, subparser):
        students_parser = subparser.add_parser("students", help="Manage students")
        students_subparser = students_parser.add_subparsers(
            title="Students Commands",
            help="Commands for managing students",
            dest="students_command",
        )

        # Add student
        students_add_parser = students_subparser.add_parser("add", help="Add a student")
        students_add_parser.add_argument(
            "--name", required=True, type=str, help="Student name"
        )
        students_add_parser.add_argument(
            "--surname", required=True, type=str, help="Student surname"
        )
        students_add_parser.add_argument(
            "--degree", required=True, type=DegreeName, help="Student degree"
        )
        students_add_parser.add_argument(
            "--semester", required=True, type=int, help="Student semester"
        )
        students_add_parser.set_defaults(
            func=lambda args: self.handle_students_add(args)
        )

        # Get students
        students_get_parser = students_subparser.add_parser(
            "get", help="Get all students"
        )
        students_get_parser.add_argument("--id", type=int, help="Get student by id")
        students_get_parser.add_argument(
            "--degree", type=DegreeName, help="Get students by degree"
        )
        students_get_parser.add_argument(
            "--semester", type=int, help="Get students by semester"
        )

        students_get_parser.set_defaults(
            func=lambda args: self.handle_students_get(args)
        )

        # Delete student
        students_delete_parser = students_subparser.add_parser(
            "delete", help="Delete a student"
        )
        students_delete_parser.add_argument(
            "--id", required=True, type=int, help="Student id"
        )
        students_delete_parser.set_defaults(
            func=lambda args: self.handle_students_delete(args)
        )

        # Update student
        students_update_parser = students_subparser.add_parser(
            "update", help="Update a student"
        )
        students_update_parser.add_argument(
            "--id", required=True, type=int, help="Student id"
        )
        students_update_parser.add_argument("--name", type=str, help="Student name")
        students_update_parser.add_argument(
            "--surname", type=str, help="Student surname"
        )
        students_update_parser.add_argument(
            "--degree", type=DegreeName, help="Student degree"
        )
        students_update_parser.add_argument(
            "--semester", type=int, help="Student semester"
        )
        students_update_parser.set_defaults(
            func=lambda args: self.handle_students_update(args)
        )
