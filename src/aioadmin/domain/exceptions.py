class AioadminError(Exception):
    """Base exception for aioadmin."""

class ForeignKeyConstraintError(AioadminError):
    """Raised when a foreign key constraint is violated."""

class TargetAlreadyExistsError(AioadminError):
    """Raised when trying to create a record that already exists."""