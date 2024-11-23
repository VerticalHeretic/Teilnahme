import argparse

from sqlmodel import Session

from src.cli.parsers.attendence_parser import AttendenceParser
from src.cli.parsers.classrooms_parser import ClassroomsParser
from src.cli.parsers.students_parser import StudentsParser
from src.cli.parsers.subjects_parser import SubjectsParser
from src.common.storage.db_storage import DBStorageHandler, create_db_and_tables, engine
from src.common.storage.storage import NewStorageHandler
from src.modules.attendence_operations import AttendenceOperations
from src.modules.classrooms_operations import ClassroomsOperations
from src.modules.students_operations import StudentsOperations
from src.modules.subjects_operations import SubjectsOperations


def setup_parsers(storage_handler: NewStorageHandler):
    parser = argparse.ArgumentParser(description="Attendance Management System 🏫")
    subparser = parser.add_subparsers(dest="command")

    students_operations = StudentsOperations(storage_handler)
    students_parser = StudentsParser(students_operations)
    students_parser.setup_students_parsers(subparser)

    subjects_parser = SubjectsParser(SubjectsOperations(storage_handler))
    subjects_parser.setup_subjects_parsers(subparser)

    classrooms_parser = ClassroomsParser(
        ClassroomsOperations(storage_handler, students_operations)
    )
    classrooms_parser.setup_classrooms_parsers(subparser)

    attendence_parser = AttendenceParser(AttendenceOperations(storage_handler))
    attendence_parser.setup_attendence_parsers(subparser)

    return parser


def main():
    create_db_and_tables()
    session = Session(engine)
    storage_handler = DBStorageHandler(session=session)
    parser = setup_parsers(storage_handler)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
