import argparse

from src.common.storage.csv_storage import CSVStorageHandler, StorageHandler
from src.modules.students_operations import StudentsOperations
from src.cli.students_parser import StudentsParser

def setup_parser(storage_handler: StorageHandler):
    parser = argparse.ArgumentParser(description="Student Management System")
    subparser = parser.add_subparsers(dest="command")
    
    students_parser = StudentsParser(StudentsOperations(storage_handler))
    students_parser.setup_students_parsers(subparser)
    
    return parser

def main():
    # Initialize your operations classes
    storage_handler = CSVStorageHandler("students.csv")  # Initialize your storage
    parser = setup_parser(storage_handler)
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()