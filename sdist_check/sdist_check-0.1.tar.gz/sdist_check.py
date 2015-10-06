import fnmatch
from distutils.command.check import check
from distutils.filelist import FileList


class sdist_check(check):
    description = "To come..."
    user_options = []
    description = ("perform additional checks on sdists")

    user_options = [
        ('metadata', 'm', 'Verify meta-data'),
        ('restructuredtext', 'r', (
            'Checks if long string meta-data syntax '
            'are reStructuredText-compliant')),
        ('strict', 's', 'Will exit with an error if a check fails'),
        ('badfiles=', 'b', 'Check files included in dist for unusual names'),
    ]

    boolean_options = ['metadata', 'restructuredtext', 'strict']

    def initialize_options(self):
        check.initialize_options(self)
        self.badfiles = None

    def finalize_options(self):
        if self.badfiles is None:
            self.badfiles = ["*~", ]
        self.ensure_string_list('badfiles')

    def _get_sdist_filelist(self):
        """Get a filelist as would be contained in sdist.
        """
        sdist = self.distribution.get_command_obj('sdist')
        sdist.ensure_finalized()
        sdist.filelist = FileList()
        sdist.get_file_list()
        self.sdist_files = sdist.filelist
        return sdist.filelist

    def run(self):
        self.check_bad_filenames()
        check.run(self)

    def check_bad_filenames(self):
        """Checks if there are unusual filenames contained in sdist.
        """
        filelist = self._get_sdist_filelist()
        for pattern in self.badfiles:
            matches = fnmatch.filter(filelist.files, pattern)
            for match in matches:
                self.warn("suspicious filename found for distribution: %s"
                          % match)
