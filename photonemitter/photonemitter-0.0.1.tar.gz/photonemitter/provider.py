import abc
from . import util
from . import output


class Provider(metaclass=abc.ABCMeta):
    """
    A provider for search Results.
    """

    def __init__(self, match, **options):
        """
        Instantiate a Provider.

        Keyword arguments:
        Every option for this Provider, probably from the config

        To make an option *required*, simply put it in a positional argument.
        """
        ...

    def query(self, q):
        """Search something, return an iterable of Results"""
        ...


class ProviderSet:
    """
    A set of providers.
    """

    def __init__(self):
        self._providers = []

    def add(self, match: str, klass: str, index: int = None,
            regex_group: int = 0, **options):
        """
        Load a provider with options.

        Positional arguments:
        match -- regex match for this provider. '.*' matches everything and
                 means default provider
        klass -- the class of the module, using module.class notation
                 Ex: google_provider.GoogleProvider

        Keyword arguments:
        index -- place to insert the provider in the list. By default,
                 providers are appended
        regex_group -- the regex match group to pass to the provider
        Any option for the provider.

        Usage:
        >>> import photonemitter.provider
        >>> ps = photonemitter.provider.ProviderSet()
        >>> ps.add(match='.*',\
                   klass='photonemitter.providers.test.TestProvider')
        """

        provider = util.get_module_attr(klass)
        prov = provider(**options)
        prov.match = match
        prov.regex_group = regex_group
        if index is None:
            self._providers.append(prov)
        else:
            self._providers.insert(index, prov)

    def query(self, q: str) -> list:
        """
        Query any providers matching q in the order of the list.

        Positional arguments:
        q -- query

        Examples:
        >>> import photonemitter.provider
        >>> ps = photonemitter.provider.ProviderSet()
        >>> ps.add(match='.*',\
                   klass='photonemitter.providers.test.TestProvider')
        >>> ps.query('whatever') #doctest:+ELLIPSIS
        [Result('This was a triumph', '', img=None), ...]

        Returns:
        A list of Results, None if there are no matching providers, or an
        error message as a Result
        """

        import re
        for p in self._providers:
            match = re.match(p.match, q)
            if match:
                groups = match.groups()
                if len(groups) < 1:
                    return [output.Result('Bad regex! Result must be in a '
                                          'group!', '')]
                return p.query(groups[p.regex_group])
        else:
            return None

    def get_providers(self) -> list:
        """
        Gets a list of providers in preferential order

        Returns:
        A list of Providers
        """

        return self._providers


if __name__ == '__main__':
    from . import test
    test._test()
