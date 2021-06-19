# encoding: utf-8

"""
Công cụ [EVN] hiển thị thông tin về tình hình sử dụng điện, dữ liệu lấy từ EVN. 
Author: exlab247@gmail.com
Version 1.0 20 April 2020 - EVN Hanoi
Version 1.1 11 May 2020   - Add EVN HoChiMinh
Version 1.2 18 May 2020   - Add EVN MienTrung
Version 1.3 30 May 2020   - Add EVN MienBac

# [your_config]/custom_components/evn
.homeassistant/
|-- custom_components/
|   |-- evn/
|       |-- __init__.py
|       |-- sensor.py
|       |-- evnapi.py
|       |-- evnapi.so
|       |-- manifest.json

# Config in configuration.yaml file for Home Assistant
sensor:
  - platform: evn
    user: user_name
    password: password
    location: HaNoi 
    # select: HaNoi, HoChiMinh, MienTrung, MienBac 
"""
import datetime
import logging
from . import evnapi
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

_LOGGER       = logging.getLogger(__name__)
SCAN_INTERVAL = datetime.timedelta(hours=4)
CONF_USER     = 'user'
CONF_PASSWORD = 'password'
CONF_LOCATION = 'location'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the system monitor sensors."""
    user = config.get(CONF_USER)
    password = config.get(CONF_PASSWORD)
    location = config.get(CONF_LOCATION)
    dev = []
    for sensor_type in list(evnapi.get(location).conf_types.keys()):
        dev.append(evn_class(user, password, sensor_type, location))
    add_entities(dev, True)

class evn_class(Entity):

    def __init__(self, user_, password_, sensor_type_, location_):
        self._user     = user_
        self._password = password_
        self._type     = sensor_type_
        self._location = location_
        self._name     = None
        self._state    = None
        self._icon     = None
        self._unit     = None
        self._attr     = None
        self.update()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state
		
    @property
    def icon(self):
        return self._icon

    @property
    def unit_of_measurement(self):
        return self._unit
    
    @property
    def device_state_attributes(self):
        return self._attr 

    @Throttle(SCAN_INTERVAL)
    def update(self):
        evn = evnapi.get(self._location)
        sensor_prop = evn.conf_types[self._type]
        self._name  = sensor_prop[0]
        self._icon  = sensor_prop[1]
        self._unit  = sensor_prop[2]
        data_evn = evn.get_data(self._user, self._password)
        self._attr = data_evn[1]
        self._state = data_evn[0][self._type]
