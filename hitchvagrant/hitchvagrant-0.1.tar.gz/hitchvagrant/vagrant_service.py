from hitchserve import Service
import sys


class VagrantService(Service):
    """Service to run vagrant as a hitch service."""

    def __init__(self, directory=".", **kwargs):
        """Define service to start and stop vagrant.

        Args:
            directory (Optional[str]): Directory that contains Vagrantfile to start.
        """
        self.directory = directory
        kwargs['log_line_ready_checker'] = lambda line: "Vagrant service ready" == line
        kwargs['command'] = [sys.executable, "-u", "-m", "hitchvagrant.vagrant", "-d", directory,]
        super(VagrantService, self).__init__(**kwargs)

    def ssh(self, *args):
        """Run ssh command against your vagrant service.

        Args:
            *args - list of arguments

        Example:
            self.ssh("ls", "-lrt")
        """
        full_command = ["vagrant", "ssh", ] + list(args)
        return self.subcommand(*full_command)
