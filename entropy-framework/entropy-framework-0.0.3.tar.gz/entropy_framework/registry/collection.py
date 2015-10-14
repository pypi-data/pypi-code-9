class Collection(object):
    """
    Collection of one type entities
    """

    def __init__(self, entity_cls):
        self._items = {}
        self._entity_cls = entity_cls

    def __call__(self, name=None, *args, **kwargs):
        """
        Calling all items or item by name
        :param name: collection
        :return: called item
        """
        if name:
            return self.get(name)(*args, **kwargs)
        else:
            res = {}
            for name, item in self.get_all().items():
                res[name] = item(*args, **kwargs)

            return res

    def get_entity_cls(self):
        """
        :return: Entity class
        """
        return self._entity_cls

    def get_all(self):
        """
        All items
        """
        return self._items

    def get(self, name):
        """
        :param name: item name
        :return: item value
        """
        return self._items[name]

    def insert(self, __name__, **props):
        """
        Inserting new item into collection
        :param __name__: item name
        :param props: item properties
        """
        if __name__ not in self._items:
            self._items[__name__] = self._entity_cls(**props)
        else:
            raise KeyError("Undefined property '%s'" % (__name__,))

    def update(self, __name__, **props):
        """
        Updating existing item
        :param __name__: item name
        :param props: item properties to update
        """
        self.get(__name__).set(**props)

    def insert_or_update(self, __name__, **props):
        try:
            self.insert(__name__, **props)
        except KeyError:
            self.update(__name__, **props)

    def remove(self, name):
        """
        Removing item from collection
        :param name: name of item
        """
        del self._items[name]
