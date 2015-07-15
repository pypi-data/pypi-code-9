import os
import os.path
import shutil
import codecs
import logging
import yaml
from piecrust.app import CONFIG_PATH
from piecrust.commands.base import ChefCommand


logger = logging.getLogger(__name__)


class InitCommand(ChefCommand):
    def __init__(self):
        super(InitCommand, self).__init__()
        self.name = 'init'
        self.description = "Creates a new empty PieCrust website."
        self.requires_website = False

    def setupParser(self, parser, app):
        parser.add_argument('destination',
                help="The destination directory in which to create the website.")

    def run(self, ctx):
        destination = ctx.args.destination
        if destination is None:
            destination = os.getcwd()

        if not os.path.isdir(destination):
            os.makedirs(destination, 0o755)

        config_path = os.path.join(destination, CONFIG_PATH)
        if not os.path.isdir(os.path.dirname(config_path)):
            os.makedirs(os.path.dirname(config_path), 0o755)

        config_text = yaml.dump({
                'site': {
                    'title': "My New Website",
                    'description': "A website recently generated with PieCrust",
                    'pretty_urls': True
                    },
                'smartypants': {
                    'enable': True
                    }
                },
                default_flow_style=False)
        with codecs.open(config_path, 'w', 'utf-8') as fp:
            fp.write(config_text)


class PurgeCommand(ChefCommand):
    def __init__(self):
        super(PurgeCommand, self).__init__()
        self.name = 'purge'
        self.description = "Purges the website's cache."

    def setupParser(self, parser, app):
        pass

    def run(self, ctx):
        cache_dir = ctx.app.sub_cache_dir
        if cache_dir and os.path.isdir(cache_dir):
            logger.info("Purging cache: %s" % cache_dir)
            shutil.rmtree(cache_dir)


class ImportCommand(ChefCommand):
    def __init__(self):
        super(ImportCommand, self).__init__()
        self.name = 'import'
        self.description = "Imports content from another CMS into PieCrust."

    def setupParser(self, parser, app):
        subparsers = parser.add_subparsers()
        for i in app.plugin_loader.getImporters():
            if not i.__class__.name:
                raise Exception("Importer '%s' has no name set." % type(i))
            p = subparsers.add_parser(i.name, help=i.description)
            i.setupParser(p, app)
            p.set_defaults(sub_func=i.checkedImportWebsite)
            p.set_defaults(sub_requires_website=i.requires_website)

    def checkedRun(self, ctx):
        if not hasattr(ctx.args, 'sub_func'):
            ctx.parser.parse_args(['import', '--help'])
            return
        ctx.args.sub_func(ctx)

