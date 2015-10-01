import zope.interface


class ICryptographicKeys(zope.interface.Interface):
    """Provides cryptographic keys for different purposes.

    Load a set of public and private keys from disk.

    Init parameters:

    keys_dir: filesystem path to keys directory
    names: iterable of key names known to client code

    For each of the names, a private key file of the same name and a public
    key file (with a .pub suffix) must reside inside the keys_dir.
    """

    def __getitem__(name):
        """Each key can be retrieved by name.

        The name must consist of one of the names configured during
        initialisation, suffixed with either -private or -public.
        If there is no key stored by the given name, KeyError will be raised.
        """
