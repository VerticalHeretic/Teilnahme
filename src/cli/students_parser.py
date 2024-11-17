from src.modules.students_operations import StudentsOperations
from src.common.models import BaseStudent, DegreeName


class StudentsParser:
    def __init__(self, students_operations: StudentsOperations):
        self.students_operations = students_operations

    def handle_students_add(self, args):
        student = BaseStudent(
            name=args.name,
            surname=args.surname,
            degree=args.degree,
            semester=args.semester,
        )
        result = self.students_operations.add_student(student)
        print(f"Added student: {result}")

    def handle_students_get(self, args):
        students = self.students_operations.get_students()
        for student in students:
            print(student)

    def handle_students_delete(self, args):
        self.students_operations.delete_student(args.id)
        print(f"Deleted student with id: {args.id}")

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
            self.students_operations.update_student(args.id, BaseStudent(**update_data))
            print(f"Updated student with id: {args.id}")
        else:
            print("No updates provided")

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
