class GeneticAlgorithmError(Exception):
    # TODO TBD
    pass


class InvalidPopulationSizeError(GeneticAlgorithmError):
    """ Raised whenever a population size is invalid. """

    def __init__(self, msg=None):
        """ Initializes the exception with the default values.

        :param msg: The message of the exception. Default to None, which means
            that the message will be the default.
        """
        super().__init__(
            msg or 'Population size must be greater than or equal to 1.'
        )


class InvalidReplacementRateError(GeneticAlgorithmError):
    """ Raised whenever a population size is invalid. """

    def __init__(self, msg=None):
        """ Initializes the exception with the default values.

        :param msg: The message of the exception. Default to None, which means
            that the message will be the default.
        """
        super().__init__(
            msg or 'Population size must be greater than or equal to 1.'
        )


class UnexpectedClassError(GeneticAlgorithmError):
    """ Raised when an instance is not of the expected class. """

    def __init__(self, expected_class):
        """ Initializes the exception.

        :param expected_class: The expected class for that instance.
        """
        super().__init__('Expected class {}'.format(expected_class))
