import itertools



def imapchain(*a, **kwa):
    """ Like itertools.imap but also chains the results. """

    imap_results = itertools.imap( *a, **kwa )
    return itertools.chain( *imap_results )


def iapply(function, *iterables):
    """ Like itertools.imap, but returns the iterable's item/iterables' items instead. """

    iterables = map(iter, iterables)
    while True:
        args = [next(it) for it in iterables]
        if function is None:
            yield tuple(args)
        else:
            function(*args)
            yield args[0]
