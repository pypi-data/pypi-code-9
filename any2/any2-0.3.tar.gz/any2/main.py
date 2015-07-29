# -*- encoding: utf-8 -*-
import six
import logging
from any2.exceptions import ColumnMappingError

log = logging.getLogger(__name__)


def recursive_getattr(obj, attr, default_value=None):
    if hasattr(obj, attr):
        return getattr(obj, attr)

    if '.' not in attr:
        return default_value

    newattr, tail = attr.split('.', 1)

    # we test the attr presence explicitly because it could exist and be None
    # in which case doing
    # new_obj = getattr(obj, newattr, None)
    # if new_obj:
    #     pass
    #
    # would simple lose the info about the presence or absence of the Attr
    # and if the default value is not None then the result will endup False
    if not hasattr(obj, newattr):
        return default_value

    new_obj = getattr(obj, newattr)
    return recursive_getattr(new_obj, tail, default_value)


class Any2Base(object):

    def __init__(
        self, target_filename, column_mappings, show_first_line=False
    ):
        """Initialize the Any2*.

        :param target_filename: The target csv file name
        :type target_filename: String

        :param column_mappings: Mapping to use
        :type column_mappings: list of dictionary with keys :
            - attr
            - colname
            - renderer (callback function or string)

            The renderer callback must accept one argument the object,
            the result must be unicode type

        :param show_first_line: Show the csv header with all column names,
        default is False
        :type show_first_line: Boolean
        """
        self.target_filename = target_filename
        self.column_mappings = column_mappings
        self.check_column_mappings()
        self.show_first_line = show_first_line

    def check_column_mappings(self):
        attr = None
        renderer = None
        colname = None

        for column_mapping in self.column_mappings:
            attr = column_mapping.get('attr', None)
            renderer = column_mapping.get('renderer', None)
            colname = column_mapping.get('colname', None)

            if colname is None:
                raise ColumnMappingError(
                    'The colname is mandatory on the column mapping'
                )

            if renderer is not None:
                if not (
                    isinstance(renderer, six.string_types) or
                    callable(renderer)
                ):
                    msg = "Renderer definition error from the column_mapping,"
                    msg += " renderer must be only string/unicode or "
                    msg += "callable, not %s" % type(renderer)

                    raise ColumnMappingError(msg)

            if renderer is None and attr is None:
                msg = 'On the column mapping definition,'
                msg += ' you must define at least attr or renderer'
                raise ColumnMappingError(msg)

            if attr is None and callable(renderer):
                msg = (
                    'You cannot use a callable '
                    'renderer if attr is not defined.'
                )
                raise ColumnMappingError(msg)
