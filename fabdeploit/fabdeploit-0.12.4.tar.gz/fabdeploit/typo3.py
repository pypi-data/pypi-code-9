from fabdeploit.base import BaseCommandUtil


class Typo3(BaseCommandUtil):
    php_commands = ('php',)
    php_ini_path = None
    typo3_path = None

    def __init__(self, **kwargs):
        super(Typo3, self).__init__(**kwargs)
        if self.typo3_path is None:
            raise RuntimeError('No typo3_path specified (class or constructor)')

    def php_bin(self):
        return self._select_bin(*self.php_commands)

    def cli_dispatch_bin(self):
        php_bin = self.php_bin()
        shell_bin = self._path_join(self._abs_path(self.typo3_path), 'typo3', 'cli_dispatch.phpsh')
        php_ini_path = self._abs_path(self.php_ini_path) if self.php_ini_path else None

        if php_ini_path:
            format_str = '{php_bin} -c {php_ini_path} {shell_bin}'
        else:
            format_str = '{php_bin} {shell_bin}'
        return format_str.format(
            php_bin=php_bin,
            shell_bin=shell_bin,
            php_ini_path=php_ini_path,
        )

    def run(self, cli_command, *options):
        with self._cd(self._abs_path(self.typo3_path)):
            self._run("%s %s %s" % (
                self.cli_dispatch_bin(),
                cli_command,
                ' '.join([o for o in options if not o is None]),
            ))

    def clear_cache(self):
        self.run(
            'cleartypo3cache',
            'all',
        )

    def maintenance_enable(self):
        self._run('touch "%s"' % self._path_join(self._abs_path(self.typo3_path), 'typo3conf', 'maintenance.flag'))

    def maintenance_disable(self):
        self._run('rm -f "%s"' % self._path_join(self._abs_path(self.typo3_path), 'typo3conf', 'maintenance.flag'))
