import ipdb
import logging
loggerlevel = logging.DEBUG
logger      = logging.getLogger(__name__)

from ..BDES2K import K2BDES, BDES2K
import numpy as np
energy0    = np.float(20.35)
QS1_length = np.float(1)
QS2_length = np.float(1)

__all__ = ['setQS']


class QS(object):
    def __init__(self, K1, length, energy):
        self.K1     = K1
        self.energy = energy
        self.length = length

    def _get_BDES(self):
        return K2BDES(K=self.K1, quad_length=self.length, energy=self.energy)

    def _set_BDES(self, value):
        return BDES2K(BDES=value, quad_length=self.length, energy=self.energy)
    BDES = property(_get_BDES, _set_BDES)
    

class setQS(object):
    def __init__(self, energy_offset):
        logger.critical('****************************USING HARDCODED FUNCTIONS!!!****************************')
        logger.log(level=loggerlevel, msg='Energy offset: {}'.format(energy_offset))
        self.energy_offset = energy_offset
        
    # ======================================
    # QS1, QS2 class objects
    # ======================================
    def _get_QS1(self):
        out = QS(
            K1     = self._get_QS1_K1(),
            length = QS1_length,
            energy = self.energy
            )
        return out
    QS1 = property(_get_QS1)
        
    def _get_QS2(self):
        out = QS(
            K1     = self._get_QS2_K1(),
            length = QS2_length,
            energy = self.energy
            )
        return out
    QS2 = property(_get_QS2)

    # ======================================
    # Get QS1/2's K1 value
    # ======================================
    def _get_QS1_K1(self):
        QS1_BDES = self._get_QS1_BDES()
        return BDES2K(bdes=QS1_BDES, quad_length = QS1_length, energy=self.energy)

    def _get_QS2_K1(self):
        QS2_BDES = self._get_QS2_BDES()
        return BDES2K(bdes=QS2_BDES, quad_length = QS2_length, energy=self.energy)

    # ======================================
    # Get QS1/2's BDES value
    # ======================================
    def _get_QS1_BDES(self):
        QS1_BDES = (np.float64(1)+self.energy_offset/np.float64(20.35))*np.float64(261.72)
        return QS1_BDES

    def _get_QS2_BDES(self):
        QS2_BDES = -(np.float64(1)+self.energy_offset/np.float64(20.35))*np.float64(167.95)
        return QS2_BDES

    # ======================================
    # Get energy in GeV
    # ======================================
    def _get_energy(self):
        return self.energy_offset + energy0

    def _set_energy(self, value):
        self.energy_offset = value - energy0
    energy = property(_get_energy, _set_energy)

    # ======================================
    # Get ELANEX's y motor position
    # ======================================
    def elanex_y_motor(self):
        ymotor = np.float64(55.)*self.energy_offset/(self.energy_offset+np.float64(20.35))
        logger.critical('Ymotor is: {}'.format(ymotor))

        return ymotor
