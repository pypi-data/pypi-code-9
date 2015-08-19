# -*- coding: utf-8 -*-

"""Mixer that controls volume using dam1021 DAC."""

from __future__ import unicode_literals

import logging
from datetime import datetime,timedelta

from mopidy import mixer
from mopidy.exceptions import MixerError

import pykka

import dam1021


logger = logging.getLogger(__name__)


class Dam1021Mixer(pykka.ThreadingActor, mixer.Mixer):

    name = 'dam1021mixer'

    DEFAULT_CMD_TIMEGAP = 1.5
    
    def __init__(self, config):
        super(Dam1021Mixer, self).__init__(config)

        self.serial = config['dam1021']['serial']

        if config['dam1021']['volume_inf'] in range(dam1021.VOLUME_INF,dam1021.VOLUME_SUP+1):
            self.volume_inf = config['dam1021']['volume_inf']
        else:
            self.volume_inf = dam1021.VOLUME_INF
            
        if config['dam1021']['volume_sup'] in range(dam1021.VOLUME_INF,dam1021.VOLUME_SUP+1):
            self.volume_sup = config['dam1021']['volume_sup'] 
        else: 
            self.volume_sup = dam1021.VOLUME_SUP

        if self.volume_inf > self.volume_sup:
            self.volume_inf = dam1021.VOLUME_INF

        #due to limitation of mopidy config validators that cannot deal with floats timeout is given in milliseconds
        self.timeout = config['dam1021']['timeout']/1000. if config['dam1021']['timeout'] else dam1021.DEFAULT_SERIAL_TIMEOUT

        self.cmd_timegap = timedelta(seconds=self.DEFAULT_CMD_TIMEGAP)
        self.cmd_timestamp = datetime.utcnow() - self.cmd_timegap*2

        self._volume_range = self.volume_sup - self.volume_inf

        self._volume_cache = self.volume_inf-1
        self._mute_cache = False

        #temporary workaround (hopefully) for lousy firmware. see commit log for more details
        levels = [-88,-89,-90]
        while levels:
            try:
                conn = dam1021.Connection(self.serial,self.timeout)
                try:
                    conn.set_current_volume_level(levels.pop())
                    break
                except Exception as e:
                    logger.warn(e)
                    pass
                finally:
                    conn.close()
                break
            except Exception as e:
                logger.warn(e)
                pass
                
        if not levels:
            logger.error("Failed to apply temporary fix")
            raise MixerError("Failed  to communicate with DAC. Try cold restart of the device")

        if not isinstance(config['audio']['mixer_volume'],int):
            try:
                conn = dam1021.Connection(self.serial,self.timeout)
                try:
                    conn.set_current_volume_level(self.volume_inf)
                    self._volume_cache = 0
                except Exception as e:
                    logger.error(e)
                    raise MixerError("Failed  to set volume level. Try cold restart of the device")
                finally:
                    conn.close()
            except Exception as e:
                logger.error(e)
                raise MixerError("Failed  to communicate with DAC. Try cold restart of the device")

    def get_volume(self):
        return self._volume_cache

    def set_volume(self, volume):
        rv = False
        if volume == self._volume_cache:
            rv = True
        else:
            if self.cmd_timestamp + self.cmd_timegap > datetime.utcnow():
                logger.debug('throttling dam1021 command flux.')
                return rv
            try:
                conn = dam1021.Connection(self.serial,self.timeout)
                try:
                    target_volume = self.volume_inf + int(round(volume*self._volume_range/100.0))
                    conn.set_current_volume_level(target_volume)
                    self.cmd_timestamp = datetime.utcnow()
                    self._volume_cache = volume
                    self.trigger_volume_changed(volume)
                    rv = True
                except Exception as e:
                    logger.error(e)
                finally:
                    conn.close()
            except Exception as e:
                logger.error(e)
            
        return rv

    def get_mute(self):
        return self._mute_cache
        
    def set_mute(self, mute):
        rv = False
        if mute == self._mute_cache:
            rv = True
        else:
            if self.cmd_timestamp + self.cmd_timegap > datetime.utcnow():
                logger.debug('throttling dam1021 command flux.')
                return rv
            try:
                conn = dam1021.Connection(self.serial,self.timeout)
                try:
                    if mute:
                        conn.set_current_volume_level(dam1021.VOLUME_INF)
                    elif not mute:
                        target_volume = self.volume_inf + int(round(self._volume_cache*self._volume_range/100.0))
                        conn.set_current_volume_level(target_volume)
                    self.cmd_timestamp = datetime.utcnow()
                    self._mute_cache = mute
                    self.trigger_mute_changed(mute)
                    rv = True
                except Exception as e:
                    logger.error(e)
                finally:
                    conn.close()
            except Exception as e:
                logger.error(e)

        return rv
