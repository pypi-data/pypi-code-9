class Activity(object):
    """Base class for any custom activity."""

    def __init__(self, target=None):
        """Activity constructor
        
        Args:
            target: optional target class for the activity
        """
        self._target = target

    @property
    def target(self):
        return self._target


class Container(object):
    """Base class for any custom container of activities."""

    def __init__(self, activities):
        """Activity container constructor
        
        Args:
            activities: list of activities in the container
        """
        self._activities = activities

    @property
    def activities(self):
        return self._activities


class Create(Activity):
    """Activity of type Create"""
    pass


class Read(Activity):
    """Activity of type Read"""
    pass


class Update(Activity):
    """Activity of type Update"""
    pass


class Patch(Activity):
    """Activity of type Patch"""
    pass


class Delete(Activity):
    """Activity of type Delete"""
    pass


class CRUD(Container):
    """Activity container that holds Create, Read, Update, Delete activities."""

    def __init__(self, target=None):
        activities = [Create(target), Read(target), Update(target), Delete(target)]
        super().__init__(activities)


class CRUDP(Container):
    """Activity container that holds CRUD and Patch activities."""

    def __init__(self, target=None):
        activities = [CRUD(target), Patch(target)]
        super().__init__(activities)
