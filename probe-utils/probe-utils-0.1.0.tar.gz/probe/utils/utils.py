from __future__ import absolute_import
import os
import csv
import sys
import h5py


class SimCommon(object):
    """
    This is a simple "low-level" class that should contain all general
    functionality for manipulation with hdf5 files.

    It only stores filename as ``self.h5_filename``, then opens and stores
    a handle to hdf5 file as ``self.h5_f``.
    """

    def __init__(self, h5_filename):
        """
        Args:
            h5_filename (str): path to hdf5 file with results
        """

        self.h5_filename = h5_filename

        self.h5_f = h5py.File(self.h5_filename, 'r+')

    def __del__(self):
        self.h5_f.close()

    def get_list_of_groups_as_dict(self, starts_with):
        """
        Args:
            starts_with (str): groups prefix

        Returns:
            dict - key is int of group number, value is group name

        """
        return {int(x.split('_')[1]): x for x in self.h5_f.keys() if x.startswith(starts_with)}


    def get_attrs_as_dict(self, group):
        """
        Returns dict with group's attributes.

        Args:
            group (str) - name of group (assumed group at /)
        Returns:
            dict - {attr_name: value}
        """
        return {a : v[0] for a, v in self.h5_f['/{}'.format(group)].attrs.iteritems()}


def h5_walk(path=".", filename = sys.stdout):
	if filename == sys.stdout:
		writer = csv.writer(filename, delimiter="\t")
	else:
		writer = csv.writer(open(str(filename), "wb"), delimiter="\t")
	writer.writerow(("Name", "Path", "Geometry", "Probe radius", "Domain radius", "Pressure", "Temperature of neutral gas", "Temperature of electrons", "Temperature of ions", "Concentration", "Potencial at probe", "Number of particles", "Number of gridpoints", "Weight of particles"))
	for (root, dirs, files) in os.walk(path, topdown=True):
		for name in files:
			if (name.split("."))[-1]=="h5":
				sc = SimCommon(os.path.join(root,name))
				attrs = sc.get_attrs_as_dict(sc.get_list_of_groups_as_dict("common")[max(sc.get_list_of_groups_as_dict("common").keys())])
				writer.writerow((name, os.path.join(root, name), attrs["geom"], attrs["r_p"], attrs["r_d"], attrs["pressure"], attrs["T_gas"], attrs["T_e"], attrs["T_i"], attrs["n_e"], attrs["phi_p"], attrs["NSP_global"]/1.2, attrs["Ngrid"], attrs["weight_global"]))

