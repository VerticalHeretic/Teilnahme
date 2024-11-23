from dataclasses import dataclass

from rich.console import Console
from rich.table import Table

from src.common.errors import NotFoundError
from src.common.models import Classroom
from src.modules.classrooms_operations import ClassroomsOperations


@dataclass
class ClassroomsParser:
    classrooms_operations: ClassroomsOperations
    console = Console()
    error_console = Console(stderr=True)

    def _display_classroom(self, classroom):
        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Subject ID", style="green")
        table.add_column(
            "Students", style="magenta", no_wrap=False
        )  # Allow wrapping for student list

        # Format students list as comma-separated names
        students_str = ", ".join(sorted(student.name for student in classroom.students))

        table.add_row(
            str(classroom.id),
            str(classroom.subject_id),
            f"{len(classroom.students)} students: {students_str}",
        )
        self.console.print(table)

    def _display_classrooms(self, classrooms):
        if len(classrooms) == 0:
            self.error_console.print("[red]No classrooms found[/red]")
            return

        table = Table(show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Subject ID", style="green")
        table.add_column("Students", style="magenta")
        for classroom in classrooms:
            table.add_row(
                str(classroom.id),
                str(classroom.subject_id),
                str(len(classroom.students)),
            )
        self.console.print(table)

    def handle_classrooms_get(self, args):
        if args.id is not None:
            try:
                classroom = self.classrooms_operations.get_classroom(args.id)
                self._display_classroom(classroom)
            except NotFoundError as e:
                self.error_console.print(f"[red]{e}[/red]")
            return

        if args.subject_id is not None:
            classrooms = self.classrooms_operations.get_classrooms_for_subject(
                args.subject_id
            )

            if len(classrooms) == 0:
                self.error_console.print(
                    f"[red]No classrooms found for subject with id: {args.subject_id}[/red]"
                )
                return
        elif args.student_id is not None:
            classrooms = self.classrooms_operations.get_classrooms_where_student(
                args.student_id
            )

            if len(classrooms) == 0:
                self.error_console.print(
                    f"[red]No classrooms found for student with id: {args.student_id}[/red]"
                )
                return
        else:
            classrooms = self.classrooms_operations.get_classrooms()

        self._display_classrooms(classrooms)

    def handle_classrooms_add(self, args):
        classroom = Classroom(subject_id=args.subject_id)
        result = self.classrooms_operations.add_classroom(classroom)
        self.console.print(f"[green]Added classroom: {result}[/green]")

    def handle_classrooms_delete(self, args):
        try:
            self.classrooms_operations.delete_classroom(args.id)
            self.console.print(f"[green]Deleted classroom with id: {args.id}[/green]")
        except NotFoundError as e:
            self.error_console.print(f"[red]{e}[/red]")

    def handle_classrooms_update(self, args):
        update_data = {}
        if args.subject_id is not None:
            update_data["subject_id"] = args.subject_id

        if update_data:
            try:
                self.classrooms_operations.update_classroom(
                    args.id, Classroom(**update_data)
                )
            except NotFoundError as e:
                self.error_console.print(f"[red]{e}[/red]")

    def add_student_to_classroom(self, args):
        try:
            self.classrooms_operations.add_student_to_classroom(
                args.classroom_id, args.student_id
            )
            self.console.print(
                f"[green]Added student with id: {args.student_id} to classroom with id: {args.classroom_id}[/green]"
            )
        except NotFoundError as e:
            self.error_console.print(f"[red]{e}[/red]")

    def delete_student_from_classroom(self, args):
        try:
            self.classrooms_operations.delete_student_from_classroom(
                args.classroom_id, args.student_id
            )
            self.console.print(
                f"[green]Deleted student with id: {args.student_id} from classroom with id: {args.classroom_id}[/green]"
            )
        except NotFoundError as e:
            self.error_console.print(f"[red]{e}[/red]")

    def setup_classrooms_parsers(self, subparser):
        classrooms_parser = subparser.add_parser("classrooms", help="Manage classrooms")
        classrooms_subparser = classrooms_parser.add_subparsers(
            title="Classrooms Commands",
            help="Commands for managing classrooms",
            dest="classrooms_command",
        )

        # Get classrooms
        classrooms_get_parser = classrooms_subparser.add_parser(
            "get", help="Get all classrooms"
        )
        classrooms_get_parser.add_argument("--id", type=int, help="Classroom ID")
        classrooms_get_parser.add_argument(
            "--subject-id", type=int, help="Get classrooms for subject"
        )
        classrooms_get_parser.add_argument(
            "--student-id", type=int, help="Get classrooms containing student"
        )
        classrooms_get_parser.set_defaults(
            func=lambda args: self.handle_classrooms_get(args)
        )

        # Add classroom
        classrooms_add_parser = classrooms_subparser.add_parser(
            "add", help="Add a classroom"
        )
        classrooms_add_parser.add_argument(
            "--subject-id", required=True, type=int, help="Subject ID"
        )
        classrooms_add_parser.set_defaults(
            func=lambda args: self.handle_classrooms_add(args)
        )

        # Delete classroom
        classrooms_delete_parser = classrooms_subparser.add_parser(
            "delete", help="Delete a classroom"
        )
        classrooms_delete_parser.add_argument(
            "--id", required=True, type=int, help="Classroom ID"
        )
        classrooms_delete_parser.set_defaults(
            func=lambda args: self.handle_classrooms_delete(args)
        )

        # Update classroom
        classrooms_update_parser = classrooms_subparser.add_parser(
            "update", help="Update a classroom"
        )
        classrooms_update_parser.add_argument(
            "--id", required=True, type=int, help="Classroom ID"
        )
        classrooms_update_parser.add_argument(
            "--subject-id", type=int, help="New subject ID"
        )
        classrooms_update_parser.set_defaults(
            func=lambda args: self.handle_classrooms_update(args)
        )

        # Add student to classroom
        add_student_parser = classrooms_subparser.add_parser(
            "add-student", help="Add student to classroom"
        )
        add_student_parser.add_argument(
            "--classroom-id", required=True, type=int, help="Classroom ID"
        )
        add_student_parser.add_argument(
            "--student-id", required=True, type=int, help="Student ID"
        )
        add_student_parser.set_defaults(
            func=lambda args: self.add_student_to_classroom(args)
        )

        # Delete student from classroom
        delete_student_parser = classrooms_subparser.add_parser(
            "delete-student", help="Delete student from classroom"
        )
        delete_student_parser.add_argument(
            "--classroom-id", required=True, type=int, help="Classroom ID"
        )
        delete_student_parser.add_argument(
            "--student-id", required=True, type=int, help="Student ID"
        )
        delete_student_parser.set_defaults(
            func=lambda args: self.delete_student_from_classroom(args)
        )
