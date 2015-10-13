class Entity(object):
    __PROP_NOT_FOUND__ = "The property '%s' is not found in the '%s' entity"

    def __init__(self, **props):
        """
        Initializing Entity object with setting properties or not
        :param props: property_name=property_value
        """

        self.set(**props)

    def get(self, name):
        """
        Getting property
        :param name: property name
        :return: property value
        """
        return self.__getattribute__(name)

    def single_set(self, name, val):
        """
        :param name:
        :param val:
        :return:
        """
        self._set_val(name, self._get_field(name).validate(val))

    def _set_val(self, name, val):
        self.__setattr__(name, val)

    def _get_field(self, name):
        """
        :param name:
        :return: attr Filed
        """
        if hasattr(self, name):
            return self.__class__.__dict__.get(name)
        else:
            raise AttributeError(self.__PROP_NOT_FOUND__ % (name, self.get_entity_name()))

    def set(self, **props):
        """
        Setting of multiple properties
        :param props: property_name=property_value
        """
        for name, val in props.iteritems():
            self.single_set(name, val)

    def clear(self, *props):
        """
        Setting None to multiple properties
        :param props: property_name=property_value
        """
        for name in props:
            self._set_val(name, self._get_field(name).get_default())

    def __call__(self, *args, **kwargs):
        pass

    @classmethod
    def get_entity_name(cls):
        return cls.__name__
