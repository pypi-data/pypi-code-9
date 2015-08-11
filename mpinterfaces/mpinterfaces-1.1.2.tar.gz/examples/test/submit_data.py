from __future__ import division, unicode_literals, print_function

from mpinterfaces.database import MPINTVaspToDbTaskDrone
from pymatgen.apps.borg.queen import BorgQueen
#import multiprocessing

additional_fields = {"author":"kiran"}
drone = MPINTVaspToDbTaskDrone(host="10.5.46.101", port=27017,
                               database="vasp", collection="NIST",
                               user="km468", password="km468",
                               additional_fields=additional_fields)
#ncpus = multiprocessing.cpu_count()
queen = BorgQueen(drone)#, number_of_drones=ncpus)
queen.serial_assimilate('/home/matk/Google_Drive/Software/MPInterfaces/examples/test/sol_lpcm')
