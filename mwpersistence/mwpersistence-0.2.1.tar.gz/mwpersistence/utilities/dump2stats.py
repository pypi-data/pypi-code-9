r"""
``$ mwpersistence dump2stats -h``
::

    Full pipeline from MediaWiki XML dumps to content persistence statistics.

    Usage:
        dump2stats (-h|--help)
        dump2stats [<input-file>...] --config=<path> --sunset=<date>
                   [--namespaces=<ids>] [--timeout=<secs>]
                   [--window=<revs>] [--revert-radius=<revs>]
                   [--min-persisted=<num>] [--min-visible=<days>]
                   [--include=<regex>] [--exclude=<regex>]
                   [--keep-text] [--keep-diff] [--keep-tokens]
                   [--threads=<num>] [--output=<path>] [--compress=<type>]
                   [--verbose] [--debug]

    Options:
        -h|--help               Print this documentation
        <input-file>            The path to a MediaWiki XML Dump file
                                [default: <stdin>]
        --config=<path>         The path to a deltas DiffEngine configuration
        --namespaces=<ids>      A comma separated list of namespace IDs to be
                                considered [default: <all>]
        --timeout=<secs>        The maximum number of seconds that a diff will
                                be allowed to run before being stopped
                                [default: 10]
        --sunset=<date>         The date of the database dump we are generating
                                from.  This is used to apply a 'time visible'
                                statistic.  Expects %Y-%m-%dT%H:%M:%SZ".
                                [default: <now>]
        --window=<revs>         The size of the window of revisions from which
                                persistence data will be generated.
                                [default: 50]
        --revert-radius=<revs>  The number of revisions back that a revert can
                                reference. [default: 15]
        --min-persisted=<num>   The minimum number of revisions a token must
                                survive before being considered "persisted"
                                [default: 5]
        --min-visible=<days>    The minimum amount of time a token must survive
                                before being considered "persisted" (in days)
                                [default: 14]
        --include=<regex>       A regex matching tokens to include
                                [default: <all>]
        --exclude=<regex>       A regex matching tokens to exclude
                                [default: <none>]
        --keep-text             If set, the 'text' field will be populated in
                                the output JSON.
        --keep-diff             If set, the 'diff' field will be populated in
                                the output JSON.
        --keep-tokens           If set, the 'tokens' field will be populated in
                                the output JSON.
        --threads=<num>         If a collection of files are provided, how many
                                processor threads should be prepare?
                                [default: <cpu_count>]
        --output=<path>         Write output to a directory with one output
                                file per input path.  [default: <stdout>]
        --compress=<type>       If set, output written to the output-dir will
                                be compressed in this format. [default: bz2]
        --verbose               Print progress information to stderr.
        --debug                 Print debug logging to stderr.
"""
import logging

import mwcli
import mwxml

from .revdocs2stats import process_args as revdocs2stats_args
from .revdocs2stats import revdocs2stats

logger = logging.getLogger(__name__)


def dump2stats(dump, *args, **kwargs):

    rev_docs = mwxml.utilities.dump2revdocs(dump)
    stats_docs = revdocs2stats(rev_docs, *args, **kwargs)

    yield from stats_docs


streamer = mwcli.Streamer(
    __doc__,
    __name__,
    dump2stats,
    revdocs2stats_args,
    file_reader=mwxml.Dump.from_file
)
main = streamer.main
