from src.common.errors import SemesterError
from src.common.models import DegreeName


def validate_semester(degree_name: DegreeName, semester: int):
    """Validate that a semester number is valid for a given degree.

    Args:
        degree_name (DegreeName): Name of the degree program
        semester (int): Semester number to validate

    Raises:
        SemesterError: If semester number is invalid for the degree
    """
    if degree_name == DegreeName.bachelor and semester > 6:
        raise SemesterError("Bachelor degree has only 6 semesters")
    elif degree_name == DegreeName.master and semester > 4:
        raise SemesterError("Master degree has only 4 semesters")
    elif semester <= 0:
        raise SemesterError("Semester number must be greater than 0")
