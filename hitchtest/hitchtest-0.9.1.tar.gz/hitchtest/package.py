from os import path, makedirs
import sys

class HitchPackageException(Exception):
    pass


class PackageVerificationFailure(HitchPackageException):
    pass


class InvalidPackageVersion(HitchPackageException):
    pass


class PackageBuildFailure(HitchPackageException):
    pass


class HitchPackage(object):
    NAME = None

    RAISE_ISSUE = None

    VERSIONS = None

    SPECIFIED_VERSIONS = {
        "version": 'VERSIONS',
    }

    def __init__(self):
        """Initialize a hitch package."""

        # 3 directories above virtualenv python binary is the hitchdir
        self.hitch_package_directory = path.abspath(
            path.join(path.expanduser("~"), ".hitchpkg")
        )

        if self.NAME is None:
            raise PackageVerificationFailure("This package does not have self.NAME set!")

        if self.RAISE_ISSUE is None:
            raise PackageVerificationFailure("This package does not have self.RAISE_ISSUE set!")

    @property
    def download_url(self):
        return self.DOWNLOAD_URL.format(self.version)

    @property
    def download_package_filename(self):
        return join(
            self.get_downloads_directory(), "{}-{}.tar.gz".format(
                self.NAME.lower(), self.version
            )
        )

    def download_package(self):
        utils.download_file(
            self.download_package_filename,
            self.download_url,
        )

    def get_build_directory(self):
        if not path.exists(self.hitch_package_directory):
            makedirs(self.hitch_package_directory)
        return self.hitch_package_directory

    def get_downloads_directory(self):
        if not path.exists(self.hitch_package_directory):
            makedirs(self.hitch_package_directory)
        return self.hitch_package_directory

    def get_output(self, command):
        return check_output(command).decode('utf8')

    def run_cmd(self, command):
        try:
            check_call(command)
        except CalledProcessException:
            raise PackageBuildFailure((
                "A problem occurred when attempting to build {}.\n"
                "The command '{}' in directory '{}' failed\n"
                "It is likely to be a bug in this hitch plugin.\n"
                "Try copying and pasting the output above to {}\n"
            ).format(self.name, ' '.join(command), os.getcwd(), self.RAISE_ISSUE))
        except OSError:
            raise PackageBuildFailure((
                "A problem occurred when attempting to build {}.\n"
                "The command '{}' in directory '{}' failed because it does not exist.\n"
                "It is likely to be a bug in this hitch plugin.\n"
                "Try copying and pasting the output above to {}\n"
            ).format(self.name, ' '.join(command), os.getcwd(), self.RAISE_ISSUE))


    def check_version(self, version, versions_list, issues_url, name=None):
        package_name = self.name if name is None else name
        if str(version) not in versions_list:
            raise InvalidPackageVersion(
                "{} version {} not in list of approved versions: \n{}\n"
                "Raise a ticket at {} "
                "if you think it should be.".format(
                    package_name, version, versions_list, issues_url
                )
            )
        return version

    def download_file(self, name, url):
        pass

    def extract_archive(self, filename, destination):
        pass

    def build(self):
        pass

    def verify(self):
        pass
