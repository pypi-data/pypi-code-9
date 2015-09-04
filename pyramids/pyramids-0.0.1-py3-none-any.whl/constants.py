# =========================================================================
# constants.py
# by Aaron Hosford
# 6/27/2011
# =========================================================================
#
# Description:
#   Provides functionality for reserving and retrieving constants by name.
#
# =========================================================================
#
# Contents:
#
#   class Constants
#     Provides functionality for reserving and retrieving constants by 
#     name.
#
# =========================================================================
#
# Modification History:
#
#   6/27/2011:
#     - Created this module.
#
# =========================================================================


class Constants:
    
    def __init__(self):
        self._values = {}
        self._owners = {}

    def reserve(self, name, value, owner):
        if name in self._values:
            # This is for situations where a module has to be reloaded.
            if self._values[name] != value or self._owners[name] != owner:
                raise NameError(
                    "This name has already been reserved by " +
                    repr(self._owners[name]) + "."
                )
        self._values[name] = value
        self._owners[name] = owner

    def get_value(self, name):
        if name not in self._values:
            raise NameError("This name is undefined.")
        return self._values[name]

    def get_owner(self, name):
        if name not in self._owners:
            raise NameError("This name is undefined.")
        return self._owners[name]

    def is_defined(self, name):
        return name in self._values

    def __getitem__(self, name):
        return self.get_value(name)

    def __contains__(self, name):
        return self.is_defined(name)
