from pexpect import spawn, EOF
from os import chdir, path


class CommandLineSteps(object):
    def cd(self, directory):
        """Change directory to 'directory'."""
        chdir(directory)

    def run(self, command, args=None):
        """Run application."""
        args = [] if args is None else args
        self.process = spawn(command, args=args)

    def expect(self, text, timeout=60):
        """Expect 'text' to appear."""
        self.process.expect(text, timeout=timeout)

    def send_control(self, letter):
        """Send ctrl-[letter] to the application."""
        self.process.sendcontrol(letter)

    def send_line(self, line):
        """Send a line of text to the application."""
        self.process.sendline(line)

    def exit_with_any_code(self, timeout=180):
        """Expect an exit and don' care what kind of code."""
        self.process.expect(EOF, timeout=timeout)
        self.process.close()

    def exit(self, with_code=0, timeout=180):
        """Exit and expect a code 'with_code' after timeout seconds."""
        self.process.expect(EOF, timeout=timeout)
        self.process.close()
        if with_code != self.process.exitstatus:
            raise RuntimeError(
                """{}\nReturn code should be {}, but is {}.""".format(
                    self.process.before.decode('utf8').replace("\\n", "\n"),
                    with_code,
                    self.process.exitstatus
                ))
        self.process = None
