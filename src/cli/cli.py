import argparse

from sqlmodel import Session

from src.cli.students_parser import StudentsParser
from src.common.storage.db_storage import DBStorageHandler, create_db_and_tables, engine
from src.common.storage.storage import NewStorageHandler
from src.modules.students_operations import StudentsOperations


def setup_parser(storage_handler: NewStorageHandler):
    parser = argparse.ArgumentParser(description="Student Management System")
    subparser = parser.add_subparsers(dest="command")

    students_parser = StudentsParser(StudentsOperations(storage_handler))
    students_parser.setup_students_parsers(subparser)

    return parser


def main():
    create_db_and_tables()
    session = Session(engine)
    storage_handler = DBStorageHandler(session=session)
    parser = setup_parser(storage_handler)
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
