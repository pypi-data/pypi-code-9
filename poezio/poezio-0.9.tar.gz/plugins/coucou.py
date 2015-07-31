from plugin import BasePlugin
import tracemalloc
import cProfile, pstats, io

class Plugin(BasePlugin):
    def init(self):
        self.api.add_command('snapshot', self.command_snapshot, 'Test command')
        self.pr = cProfile.Profile()
        self.pr.enable()
        tracemalloc.start()

    def command_snapshot(self, args):
        import gc
        gc.collect()

        s = io.StringIO()
        ps = pstats.Stats(self.pr, stream=s).sort_stats('cumulative')
        ps.print_stats()

        args = '/tmp/profile'

        with open(args, 'w') as fd:
            fd.write(s.getvalue())

        self.api.information("Profile written to %s" % args, "Info")

        args = '/tmp/malloc'

        snapshot = tracemalloc.take_snapshot()
        stats = snapshot.statistics('filename', cumulative=True)
        with open(args, 'w') as fd:
            for stat in stats:
                fd.write('%s\n' % stat)

        self.api.information("Snapshot written to %s" % args, "Info")
