from okapi.settings import settings


class Test(object):
    def __init__(self, test):
        """
        :param test: String to be asserted (eg. `status_code == 200`)
        :type test: str
        """
        self.test = test
        self.result = True
        self.message = None
        self.log = ''

    def __repr__(self):
        return '"{}"'.format(str(self))

    def __str__(self):
        if self.message:
            return '{} -- {}'.format(self.test, self.message)
        return self.test

    def run(self, variables):
        """
        Execute assertion for a test.

        :param variables: Dictionary of with variables passed to exec.
        :type variables: dict

        :return: Result of assertion
        :rtype: bool
        """
        try:
            exec('assert ' + self.test, variables)
        except Exception as e:
            self.message = str(e)
            self.result = False

            self.log += '\t\t[FAIL] ' + str(self) + '\n'

            if settings.debug:
                self.debug(variables)
            return False

        self.log += '\t\t[OK] ' + str(self) + '\n'
        return True

    @staticmethod
    def debug(variables):
        """
        Starts pdb debugger with given variables.

        :param variables: Variables passed to debugger.
        :type variables: dict
        """
        settings.log.write('\nVariables:')
        settings.log.write('\n' + ', '.join(sorted(variables.keys())))
        settings.log.write('\nPress `c` to continue or `q` to quit.\n')
        exec('import pdb; pdb.set_trace()', variables)
