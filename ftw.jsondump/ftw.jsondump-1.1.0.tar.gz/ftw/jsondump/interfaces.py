from zope.interface import Interface


class IJSONRepresentation(Interface):
    """Interface for json representation adaper"""

    def __init__(context, request):
        """Adapts contex and request"""

    def json(only=None, exclude=None, **config):
        """Returns the json representations by iterating over IJSONPartials.
        Params:

            - only: List of included representation steps.
            - exclude: List of excluded representation steps.
            - config: Dict.
        """


class IPartial(Interface):
    """Interface for json partial adapters"""

    def __init__(context, request):
        """Adapts contex and request"""

    def __call__(config):
        """Returns a dict"""


class IFieldExtractor(Interface):
    """Interface for field adapter, which extracts the data."""

    def __init__(context, request, field):
        """Adapts the context, request and the field"""

    def extract(name, data, config):
        """Updates the value of the into the data dict.
        Params:

            - name: String - Name of the field.
            - data: Dict.
            - config: Dict - Holds additional/optional configurations.
        """
