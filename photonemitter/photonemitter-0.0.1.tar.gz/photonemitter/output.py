class Result:
    """
    A single search result.

    Usage:
    >>> res = Result('Firefox', 'firefox')
    >>> res.get_output()
    '{Firefox |firefox }'

    >>> res = Result('Firefox', 'firefox', '/whatever/image.png')
    >>> res.get_output()
    '{%I/whatever/image.png% Firefox |firefox }'
    """

    def __init__(self, title, cmd, img=None):
        """
        Instantiate a Result.

        Positional arguments:
        title -- title of the result
        cmd -- command to execute/stdout output for lighthouse

        Keyword arguments:
        img -- image to display alongside the result
        """
        self.title = title
        self.cmd = cmd
        self.img = img

    def get_output(self):
        """
        Get the output representation for a Result.

        This can be sent to lighthouse.
        """
        if self.img:
            return '{{%I{res.img}% {res.title} |{res.cmd} }}'.format(res=self)
        else:
            return '{{{res.title} |{res.cmd} }}'.format(res=self)

    def __repr__(self):
        title = repr(self.title)
        cmd = repr(self.cmd)
        img = repr(self.img)
        return 'Result({}, {}, img={})'.format(title, cmd, img)


def send(results):
    """
    Send some results to lighthouse

    Positional arguments:
    results -- an iterable of Results

    Examples:
    >>> send([Result('A', 'a'), Result('B', 'b')])
    {A |a }{B |b }
    """
    outputs = [x.get_output() for x in results]
    print(''.join(outputs))

if __name__ == '__main__':
    from . import test
    test._test()
