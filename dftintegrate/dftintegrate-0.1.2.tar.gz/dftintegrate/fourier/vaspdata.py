"""
Classes::
  VASPData -- A collection of function that wrap bash code to extract
    data from VASP output into managable .dat (.txt) files.
"""
import numpy as np

from subprocess import call, check_output
from ast import literal_eval


class VASPData(object):
    """
    A collection of function that wrap bash code to extract
    data from VASP output into managable .dat (.txt) files.

    Variables::
      name -- A string containing the path to the
        VASP data.

    Funtions::
      extract_symops_trans -- Get symmetry operations and translations
        from OUTCAR -> symops_trans.dat.

      extract_kpts_eigenvals -- Get k-points, weights, and eigenvalues
        from EIGENVAL -> kpts_eigenvals.dat.

      extract_kmax -- Get kmax from KPOINTS -> kmax.dat (details about
        what kmax is are given in readdata.py).
    """

    def __init__(self, name_of_data_directory, kpts_eigenvals=True,
                 symops_trans=True, kmax=True):
        """
        Arguments::
          name_of_data_directory -- See Variables::name.

        Keyword Arguments::
          kpts_eigenvals, symops_trans, kmax -- All are booleans that
            specify if that bit of data should be extracted from the
            VASP output files. One may use False if the corresponding
            .dat file already exists or is hand made. Default is True for
            all three.
        """
        self.name = name_of_data_directory
        if kpts_eigenvals:
            self.extract_kpts_eigenvals()
        if symops_trans:
            self.extract_symops_trans()
        if kmax:
            self.extract_kmax()

    def extract_symops_trans(self):
        """
        Use some bash code to look inside OUTCAR and grab out the
        symmetry operators and translations and then right them to a
        file called symops_trans.dat. File is written to the same folder
        the OUTCAR is in.
        """
        name = self.name
        call("grep -A 4 -E 'isymop' " + name + "/OUTCAR | cut -c 11-50 > " +
             name + "/symops_trans.dat; echo '' >> " + name +
             "/symops_trans.dat", shell=True)

    def extract_kpts_eigenvals(self):
        """"
        Use some bash code to look inside EIGENVAL and grab out the
        k-points, weights, and eigenvalues associated with each band at
        each k-point. Write them to a file called kpts_eigenvals.dat.
        File is written to the same folder the EIGENVAL is in.
        """
        name = self.name
        length = check_output('less ' + name + '/EIGENVAL | wc -l', shell=True)
        num = str([int(s) for s in length.split() if s.isdigit()][0] - 7)
        call('tail -n' + num + ' ' + name +
             '/EIGENVAL | cut -c 1-60 > ' + name + '/kpts_eigenvals.dat',
             shell=True)

    def extract_kmax(self):
        """
        Look inside KPOINTS and grab out the number of kpoints used in
        one direction. If the grid is not cubic i.e. 12 12 5 it will
        take the smallest. Also assumes the KPOINTS has this format:
            nxmxp! comment line
             0
            Monkhorst
             12 12 12
            0 0 0
        at least as far as what line the 12 12 12 is on. To be concrete
        the only requirement is that the grid is specified on
        the fourth line. If one wishes to use a different format for the
        KPOINTS file they can set the kmax bool to False and genterate
        their own kmax.dat in the same directory as the VASP data to be
        used by readdata.py. GRID SIZE ON FOURTH LINE.
        """
        name = self.name
        with open(name+'/KPOINTS', 'r') as inf:
            line = [literal_eval(x) for x in
                    inf.readlines()[3].strip().split()]
        k = min(line)
        kmax = np.ceil(k/(2*np.sqrt(3)))
        with open(name+'/kmax.dat', 'w') as outf:
            outf.write(str(kmax))
