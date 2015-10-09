from django.core.exceptions import ValidationError as BaseValidationError


class ValidationError(BaseValidationError):
    def __init__(self, message, fieldName=None):
        if not fieldName:
            fieldName = "general"
        super().__init__({fieldName: message})
