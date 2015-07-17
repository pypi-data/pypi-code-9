from jirafs.exceptions import JirafsError
from jirafs.plugin import CommandPlugin


class Command(CommandPlugin):
    """ Get the status of the current ticketfolder """
    TRY_SUBFOLDERS = True
    MIN_VERSION = '1.0a1'
    MAX_VERSION = '1.99.99'

    def handle(self, args, folder, **kwargs):
        return self.field(folder, args.field_name, raw=args.raw)

    def add_arguments(self, parser):
        parser.add_argument(
            '--raw',
            help=(
                'Return the field value without applying '
                'plugin transformations'
            ),
            action='store_true',
            default=False
        )
        parser.add_argument(
            'field_name',
        )

    def field(self, folder, field_name, raw=False):
        fields = folder.get_fields()

        if field_name not in fields:
            raise JirafsError("Field '%s' does not exist." % field_name)

        if raw:
            print(fields[field_name])
        else:
            print(fields.get_transformed(field_name))
