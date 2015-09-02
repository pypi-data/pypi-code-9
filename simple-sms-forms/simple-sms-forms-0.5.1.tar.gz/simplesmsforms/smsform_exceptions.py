class SMSFieldException(Exception):

    def __init__(self, field):
        self.field = field

    def __str__(self):
        return repr(self.field)


class MissingRequiredFieldException(SMSFieldException):

    def __str__(self):
        return "You must specify a {required_field} within your message".format(
            required_field=self.field
        )


class InvalidDateException(SMSFieldException):
    pass


class ChoiceException(SMSFieldException):
    pass

class DuplicateFieldsException(SMSFieldException):
    def __str__(self):
        return ("You have included more than one value for {fields} - please include only one within each message").format(
            fields=self.field)

class UnrecognizedDataFoundException(SMSFieldException):
    def __str__(self):
        return ("'{field}' is not recognised or is not in a standard format. Please remove it or adjust it so that it follows the format in your job aid.").format(field=self.field)
