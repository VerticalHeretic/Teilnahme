class NotFoundError(Exception):
    """Raised when a object is not found"""

    pass


class SemesterError(Exception):
    """Exception raised when a student's semester number is invalid.

    This includes cases where:
    - Bachelor semester is greater than 6
    - Master semester is greater than 4
    - Semester is less than or equal to 0
    """

    pass
