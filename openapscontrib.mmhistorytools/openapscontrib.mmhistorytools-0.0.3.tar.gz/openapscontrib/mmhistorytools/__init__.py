"""
mmhistorytools - tools for cleaning, condensing, and reformatting history data


"""
from .version import __version__

import argparse
from dateutil.parser import parse
import json

from openaps.uses.use import Use

from historytools import TrimHistory, CleanHistory, ReconcileHistory
from historytools import ResolveHistory, NormalizeRecords


# set_config is needed by openaps for all vendors.
# set_config is used by `device add` commands so save any needed
# information.
# See the medtronic builtin module for an example of how to use this
# to save needed information to establish sessions (serial numbers,
# etc).
def set_config(args, device):
    # no special config
    return


# display_device allows our custom vendor implementation to include
# special information when displaying information about a device using
# our plugin as a vendor.
def display_device(device):
    # no special information needed to run
    return ''


# openaps calls get_uses to figure out how how to use a device using
# agp as a vendor.  Return a list of classes which inherit from Use,
# or are compatible with it:
def get_uses(device, config):
    return [trim, clean, reconcile, resolve, normalize]


def _opt_date(timestamp):
    """Parses a date string if defined

    :param timestamp: The date string to parse
    :type timestamp: basestring
    :return: A datetime object if a timestamp was specified
    :rtype: datetime.datetime|NoneType
    """
    if timestamp:
        return parse(timestamp)


def _opt_json_file(filename):
    """Parses a filename as JSON input if defined

    :param filename: The path to the file to parse
    :type filename: basestring
    :return: A decoded JSON object if a filename was specified
    :rtype: dict|list|NoneType
    """
    if filename:
        return json.load(argparse.FileType('r')(filename))


class BaseUse(Use):
    def configure_app(self, app, parser):
        """Define command arguments.

        Only primitive types should be used here to allow for serialization and partial application
        in via openaps-report.
        """
        parser.add_argument(
            'infile',
            nargs=argparse.OPTIONAL,
            default='-',
            help='JSON-encoded history data'
        )

    def get_params(self, args):
        return dict(infile=args.infile)

    def get_program(self, params):
        """Parses params into history parser constructor arguments

        :param params:
        :type params: dict
        :return:
        :rtype: tuple(list, dict)
        """
        return [json.load(argparse.FileType('r')(params['infile']))], dict()


# noinspection PyPep8Naming
class trim(BaseUse):
    """Trims a sequence of pump history to a specified time window"""

    def configure_app(self, app, parser):
        super(trim, self).configure_app(app, parser)

        parser.add_argument(
            '--start',
            default=None,
            help='The initial timestamp of the window to return'
        )
        parser.add_argument(
            '--end',
            default=None,
            help='The final timestamp of the window to return'
        )

    def get_params(self, args):
        params = super(trim, self).get_params(args)

        if 'start' in args and args.start:
            params.update(start=args.start)

        if 'end' in args and args.end:
            params.update(end=args.end)

        return params

    def get_program(self, params):
        args, kwargs = super(trim, self).get_program(params)
        kwargs.update(
            start_datetime=_opt_date(params.get('start')),
            end_datetime=_opt_date(params.get('end'))
        )

        return args, kwargs

    def main(self, args, app):
        args, kwargs = self.get_program(self.get_params(args))

        tool = TrimHistory(*args, **kwargs)

        return tool.trimmed_history


# noinspection PyPep8Naming
class clean(BaseUse):
    """Resolve inconsistencies from a sequence of pump history

Tasks performed by this pass:
 - De-duplicates BolusWizard records
 - Creates PumpSuspend and PumpResume records to complete missing pairs
    """
    def configure_app(self, app, parser):
        super(clean, self).configure_app(app, parser)

        parser.add_argument(
            '--start',
            default=None,
            help='The initial timestamp of the known window, used to simulate missing '
                 'suspend/resume events'
        )
        parser.add_argument(
            '--end',
            default=None,
            help='The final timestamp of the history window, used to simulate missing '
                 'suspend/resume events'
        )

    def get_params(self, args):
        params = super(clean, self).get_params(args)

        if 'start' in args and args.start:
            params.update(start=args.start)

        if 'end' in args and args.end:
            params.update(end=args.end)

        return params

    def get_program(self, params):
        args, kwargs = super(clean, self).get_program(params)
        kwargs.update(
            start_datetime=_opt_date(params.get('start')),
            end_datetime=_opt_date(params.get('end'))
        )

        return args, kwargs

    def main(self, args, app):
        args, kwargs = self.get_program(self.get_params(args))

        tool = CleanHistory(*args, **kwargs)

        return tool.clean_history


# noinspection PyPep8Naming
class reconcile(BaseUse):
    """Reconcile record dependencies from a sequence of pump history

Tasks performed by this pass:
 - Modifies temporary basal duration to account for cancelled and overlapping basals
 - Duplicates and modifies temporary basal records to account for delivery pauses when suspended
    """
    def main(self, args, app):
        args, _ = self.get_program(self.get_params(args))

        tool = ReconcileHistory(*args)

        return tool.reconciled_history


# noinspection PyPep8Naming
class resolve(BaseUse):
    """Converts events in a sequence of pump history to generalized record types

Each record is a dictionary representing one of the following types, as denoted by the "type" key:
- `Bolus`: Insulin delivery events in Units, or Units/hour
- `Meal`: Grams of carbohydrate
- `TempBasal`: Paced insulin delivery events in Units/hour, or Percent of scheduled basal
The following history events are parsed:
- TempBasal and TempBasalDuration are combined into TempBasal records
- PumpSuspend and PumpResume are combined into TempBasal records of 0%
- Square Bolus is converted to a Bolus record
- Normal Bolus is converted to a Bolus record
- BolusWizard carb entry is converted to a Meal record
- JournalEntryMealMarker is converted to a Meal record
Events that are not related to the record types or seem to have no effect are dropped.
"""
    def main(self, args, app):
        args, _ = self.get_program(self.get_params(args))

        tool = ResolveHistory(*args)

        return tool.resolved_records


# noinspection PyPep8Naming
class normalize(BaseUse):
    """Adjusts the time and amount of records relative to a basal schedule and a timestamp

If `--basal-profile` is provided, the TempBasal `amount` is replaced with a relative dose in
Units/hour. A single TempBasal record might split into multiple records to account for boundary
crossings in the basal schedule.
If `--zero-at` is provided, the values for the `start_at` and `end_at` keys are replaced with signed
integers representing the number of minutes from `--zero-at`.
"""
    def configure_app(self, app, parser):
        super(normalize, self).configure_app(app, parser)

        parser.add_argument(
            '--basal-profile',
            default=None,
            help='A file containing a basal profile by which to adjust TempBasal records'
        )

        parser.add_argument(
            '--zero-at',
            default=None,
            help='The timestamp by which to adjust record timestamps. This can be either a '
                 'filename to a read_clock report or a timestamp string value.'
        )

    def get_params(self, args):
        params = super(normalize, self).get_params(args)
        if 'basal_profile' in args and args.basal_profile:
            params.update(basal_profile=args.basal_profile)

        if 'zero_at' in args and args.zero_at:
            params.update(zero_at=args.zero_at)

        return params

    def get_program(self, params):
        args, kwargs = super(normalize, self).get_program(params)

        zero_at = params.get('zero_at')

        try:
            zero_at = _opt_json_file(zero_at)
        except argparse.ArgumentTypeError:
            pass

        kwargs.update(
            basal_schedule=_opt_json_file(params.get('basal_profile')),
            zero_datetime=_opt_date(zero_at)
        )

        return args, kwargs

    def main(self, args, app):
        args, kwargs = self.get_program(self.get_params(args))

        tool = NormalizeRecords(*args, **kwargs)

        return tool.normalized_records
