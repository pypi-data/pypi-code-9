import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np

import slactrac as _sltr
import logging
logger = logging.getLogger(__name__)

__all__ = [
    'IP_to_lanex',
    'IP_to_lanex_nobend',
    'IP_to_cherfar'
    ]


gamma_default    = float(39824)
# QS1_K1_default = float(0.077225846087095e-01)
# QS2_K1_default = float(02.337527121004531e-01)
QS1_K1_default   = float(3.8743331090707228e-1)
QS2_K1_default   = float(-2.5439067538354171e-1)
PEXT_Z           = float(1994.97)
QS1_Z            = float(1998.71)
AL_Z             = float(2015.16)
BE_Z             = float(1996.34)
ELANEX_Z         = float(2015.22)
# IP2QS1_length  = float(5.4217)
IP2QS1_length    = QS1_Z-PEXT_Z


def IP_to_lanex(beam_x, beam_y,
        gamma  = gamma_default,
        QS1_K1 = QS1_K1_default,
        QS2_K1 = QS2_K1_default
        ):
    """
    The beamline from the interaction point to CMOS_ELAN, with some default quadrupole settings.
    """
    logger.debug('Using lanex')
    # Beamline elements
    # IP2QS1    = _sltr.Drift(length = IP2QS1_length)
    IP2BE     = _sltr.Drift(   name= 'IP2BE'     , length = IP2QS1_length-_np.float_(2.37))
    BESCATTER = _sltr.Scatter( name= 'BESCATTER' , thickness = _np.float_(75e-6)            , radlength = _np.float_(35.28e-2))
    BE2QS1    = _sltr.Drift(   name= 'BE2QS1'    , length = _np.float_(2.37))
    QS1       = _sltr.Quad(    name= 'QS1'       , length = _np.float_(5.000000000E-01)     , K1 = QS1_K1)
    LQS12QS2  = _sltr.Drift(   name= 'LQS12QS2'  , length = _np.float_(4.00E+00))
    QS2       = _sltr.Quad(    name= 'QS2'       , length = _np.float_(5.000000000E-01)     , K1 = QS2_K1)
    LQS22BEND = _sltr.Drift(   name= 'LQS22BEND' , length = _np.float_(0.7428E+00))
    B5D36     = _sltr.Bend(    name= 'B5D36'     ,
            length = _np.float_(2)*_np.float_(4.889500000E-01),
            angle  = _np.float_(6.0E-03),
            order  = 1,
            rotate = 90
            )
    # LBEND2ELANEX = _sltr.Drift(length = _np.float_(8.792573))
    LBEND2AL  = _sltr.Drift(   name = 'LBEND2AL'  , length    = _np.float_(8.792573)-_np.float_(0.06))
    ALSCATTER = _sltr.Scatter( name = 'ALSCATTER' , thickness = _np.float_(5e-3)                      , radlength = _np.float_(8.897e-2))
    AL2ELANEX = _sltr.Drift(   name = 'AL2ELANEX' , length    = _np.float_(0.06))

    beamline     = _sltr.Beamline(
        element_list=[
            # IP2QS1  ,
            IP2BE     ,
            BESCATTER ,
            BE2QS1    ,
            QS1       ,
            QS1       ,
            LQS12QS2  ,
            QS2       ,
            QS2       ,
            LQS22BEND ,
            B5D36     ,
            # LBEND2ELANEX
            LBEND2AL  ,
            ALSCATTER ,
            AL2ELANEX
            ],
        gamma  = gamma,
        beam_x = beam_x,
        beam_y = beam_y
        )
    return beamline


def IP_to_lanex_nobend(beam_x, beam_y,
        gamma  = gamma_default,
        QS1_K1 = QS1_K1_default,
        QS2_K1 = QS2_K1_default
        ):
    """
    The beamline from the interaction point to CMOS_ELAN, with the bend turned off, with some default quadrupole settings.
    """

    logger.debug('Using lanex_nobend')

    beamline = IP_to_lanex(
        beam_x = beam_x,
        beam_y = beam_y,
        gamma  = gamma,
        QS1_K1 = QS1_K1,
        QS2_K1 = QS2_K1
        )

    # Replace bend with drift
    B5D36_drift = _sltr.Drift(name='B5D36_drift', length= _np.float_(2)*_np.float_(4.889500000E-01))
    beamline.elements[9] = B5D36_drift

    return beamline


def IP_to_cherfar(beam_x, beam_y,
        gamma  = gamma_default,
        QS1_K1 = QS1_K1_default,
        QS2_K1 = QS2_K1_default
        ):
    """
    The beamline from the interaction point to cherfar with some default quadrupole settings.
    """
    logger.debug('Using cherfar')
    beamline = IP_to_lanex(beam_x, beam_y,
        gamma  = gamma,
        QS1_K1 = QS1_K1,
        QS2_K1 = QS2_K1
        )

    # print beamline.elements[12].length
    ind = 12
    logger.critical('Modifying lanex into cherfar by changing length of element: Index {}'.format(ind))
    logger.critical('Beamline elements {ind}: {value}'.format(ind=ind, value=beamline.elements[12].length))
    beamline.elements[12].length = beamline.elements[12].length + _np.float_(0.8198)

    return beamline
