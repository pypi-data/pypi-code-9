# -*- coding: utf-8 -*-
from path import path

from pymip.api import Family


class Institute(object):

    """docstring for Institute"""

    def __init__(self, base_path, cust_id):
        super(Institute, self).__init__()
        self.cust_id = cust_id
        self.base_path = path(base_path)
        self.families = {}

    def load_family(self, family_id):
        """Load a family from the instutute.

        Args:
            family_id (str): id of family

        Returns:
            Family: initialized family object
        """
        family_dir = self.base_path.joinpath(family_id)
        # cache the family in the class
        self.families[family_id] = Family(base_dir=family_dir)

        return self.families[family_id]
