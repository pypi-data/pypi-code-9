class Entity(object):
    __PROP_NOT_FOUND__ = "Property '%s' in not found in this entity"

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
        Setting of single property if it exist
        :param name: property name
        :param val: property value
        """
        if hasattr(self, name):
            self.__setattr__(name, val)
        else:
            raise AttributeError(self.__PROP_NOT_FOUND__ % (name,))

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
            self.__setattr__(name, None)

    def __call__(self, *args, **kwargs):
        pass

    @classmethod
    def get_entity_name(cls):
        return cls.__name__
