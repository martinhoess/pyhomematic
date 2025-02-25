import logging
from pyhomematic.devicetypes.generic import HMDevice
from pyhomematic.devicetypes.misc import HMEvent, Remote
from pyhomematic.devicetypes.helper import (HelperLowBat, HelperSabotage,
                                            HelperLowBatIP, HelperSabotageIP,
                                            HelperOperatingVoltageIP,
                                            HelperBinaryState,
                                            HelperSensorState,
                                            HelperWired, HelperEventRemote, HelperRssiPeer, HelperRssiDevice,
                                            HelperValveState)

LOG = logging.getLogger(__name__)


class HMSensor(HMDevice):
    """This class helps to resolve class inheritance order problems."""


class SensorHmW(HMSensor):
    """Homematic Wired sensors"""


class SensorHmNLB(HMSensor, HelperRssiDevice, HelperRssiPeer):
    """Homematic sensors always have
         - strength of the signal received by the device (HelperRssiDevice).
           Be aware that standard HM devices have a reversed understanding of PEER
           and DEVICE compared to HMIP devices.
         - strength of the signal received by the CCU (HelperRssiPeer).
           Be aware that standard HM devices have a reversed understanding of PEER
           and DEVICE compared to HMIP devices."""


class SensorHm(HMSensor, HelperRssiDevice, HelperRssiPeer, HelperLowBat):
    """Homematic sensors always have
         - strength of the signal received by the device (HelperRssiDevice).
           Be aware that standard HM devices have a reversed understanding of PEER
           and DEVICE compared to HMIP devices.
         - strength of the signal received by the CCU (HelperRssiPeer).
           Be aware that standard HM devices have a reversed understanding of PEER
           and DEVICE compared to HMIP devices.
         - low battery status (HelperLowBat)"""


class SensorHmIP(HMSensor, HelperRssiDevice, HelperLowBatIP, HelperOperatingVoltageIP):
    """Homematic IP sensors always have
         - strength of the signal received by the CCU (HelperRssiDevice).
           Be aware that HMIP devices have a reversed understanding of PEER
           and DEVICE compared to standard HM devices.
         - strength of the signal received by the device (HelperRssiPeer).
           Be aware that standard HMIP devices have a reversed understanding of PEER
           and DEVICE compared to standard HM devices.
         - low battery status (HelperLowBatIP)
         - voltage of the batteries (HelperOperatingVoltageIP)"""


class SensorHmIPW(HMSensor, HelperWired):
    """Homematic IP Wired sensors"""


class SensorHmIPNoVoltage(HMSensor, HelperRssiDevice, HelperLowBatIP):
    """Some Homematic IP sensors have
         - strength of the signal received by the CCU (HelperRssiDevice).
           Be aware that HMIP devices have a reversed understanding of PEER
           and DEVICE compared to standard HM devices.
         - strength of the signal received by the device (HelperRssiPeer).
           Be aware that standard HMIP devices have a reversed understanding of PEER
           and DEVICE compared to standard HM devices.
         - low battery status (HelperLowBatIP)
         - but no voltage of batteries"""


class SensorHmIPNoLowbat(HMSensor, HelperRssiDevice, HelperOperatingVoltageIP):
    """Homematic IP sensors always have
         - strength of the signal received by the CCU (HelperRssiDevice).
           Be aware that HMIP devices have a reversed understanding of PEER
           and DEVICE compared to standard HM devices.
         - strength of the signal received by the device (HelperRssiPeer).
           Be aware that standard HMIP devices have a reversed understanding of PEER
           and DEVICE compared to standard HM devices.
         - but no low battery status (HelperLowBatIP)
         - voltage of the batteries (HelperOperatingVoltageIP)"""


class SensorHmIPNoBattery(HMSensor, HelperRssiDevice):
    """Some Homematic IP sensors have
         - strength of the signal received by the CCU (HelperRssiDevice).
           Be aware that HMIP devices have a reversed understanding of PEER
           and DEVICE compared to standard HM devices.
         - strength of the signal received by the device (HelperRssiPeer).
           Be aware that standard HMIP devices have a reversed understanding of PEER
           and DEVICE compared to standard HM devices.
         - but no low battery status (HelperLowBatIP)
         - but no voltage of batteries"""


class ShutterContact(SensorHm, HelperBinaryState, HelperSabotage):
    """Door / Window contact that emits its open/closed state.
       This is a binary sensor."""

    def is_open(self, channel=None):
        """ Returns True if the contact is open. """
        return self.get_state(channel)

    def is_closed(self, channel=None):
        """ Returns True if the contact is closed. """
        return not self.get_state(channel)

    @property
    def ELEMENT(self):
        if "HM-SCI-3-FM" in self._TYPE:
            return [1, 2, 3]
        return [1]


class IPShutterContact(SensorHmIP, HelperBinaryState):
    """Door / Window contact that emits its open/closed state.
       This is a binary sensor."""

    def is_open(self, channel=None):
        """ Returns True if the contact is open. """
        return self.get_state(channel)

    def is_closed(self, channel=None):
        """ Returns True if the contact is closed. """
        return not self.get_state(channel)


class IPShutterContactSabotage(IPShutterContact, HelperSabotageIP):
    """Same as IPShutterContact, but with sabotage detection."""


class MaxShutterContact(HelperBinaryState, HelperLowBat):
    """Door / Window contact that emits its open/closed state.
       This is a binary sensor."""


class TiltSensor(SensorHm, HelperBinaryState):
    """Sensor that emits its tilted state.
       This is a binary sensor."""

    def is_tilted(self, channel=None):
        """ Returns True if the contact is tilted. """
        return self.get_state(channel)

    def is_not_tilted(self, channel=None):
        """ Returns True if the contact is not tilted. """
        return not self.get_state(channel)


class RotaryHandleSensor(SensorHm, HelperSensorState, HelperSabotage):
    """Window handle contact."""

    def is_open(self, channel=None):
        """ Returns True if the handle is set to open. """
        return self.get_state(channel) == 2

    def is_closed(self, channel=None):
        """ Returns True if the handle is set to closed. """
        return self.get_state(channel) == 0

    def is_tilted(self, channel=None):
        """ Returns True if the handle is set to tilted. """
        return self.get_state(channel) == 1


class RotaryHandleSensorIP(SensorHmIP, HelperSensorState, HelperSabotageIP):
    """Window handle contact."""

    def is_open(self, channel=None):
        """ Returns True if the handle is set to open. """
        return self.get_state(channel) == 2

    def is_closed(self, channel=None):
        """ Returns True if the handle is set to closed. """
        return self.get_state(channel) == 0

    def is_tilted(self, channel=None):
        """ Returns True if the handle is set to tilted. """
        return self.get_state(channel) == 1


class CO2Sensor(SensorHm, HelperSensorState):
    """CO2 Sensor"""

    def is_normal(self, channel=None):
        """ Returns True if CO2 state is normal. """
        return self.get_state(channel) == 0

    def is_added(self, channel=None):
        """ Returns True if CO2 state is added. """
        return self.get_state(channel) == 1

    def is_added_strong(self, channel=None):
        """ Returns True if CO2 state is added strong. """
        return self.get_state(channel) == 2


class CO2SensorIP(SensorHmIPNoBattery):
    """CO2 Sensor
        partial support for HmIP-SCTH230
        missing relay state and actions
    """

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)
        self.SENSORNODE.update({"CONCENTRATION": [1],
                                "CONCENTRATION_STATUS": [1],
                                "HUMIDITY": [4],
                                "ACTUAL_TEMPERATURE": [4]
                                })

class ParticulateMatterSensorIP(SensorHmIPNoBattery):
    """Particulate matter sensor"""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)
        self.SENSORNODE.update({"ACTUAL_TEMPERATURE": [1],
                                "HUMIDITY": [1],
                                "MASS_CONCENTRATION_PM_1": [1],
                                "MASS_CONCENTRATION_PM_2_5": [1],
                                "MASS_CONCENTRATION_PM_10": [1],
                                "MASS_CONCENTRATION_PM_1_24H_AVERAGE": [1],
                                "MASS_CONCENTRATION_PM_2_5_24H_AVERAGE": [1],
                                "MASS_CONCENTRATION_PM_10_24H_AVERAGE": [1]
                                })

class WaterSensor(SensorHm, HelperSensorState):
    """Watter detect sensor."""

    def is_dry(self, channel=None):
        """Return True if the state is DRY"""
        return self.get_state(channel) == 0

    def is_wet(self, channel=None):
        """Return True if the state is WET"""
        return self.get_state(channel) == 1

    def is_water(self, channel=None):
        """Return True if the state is WATER"""
        return self.get_state(channel) == 2


class PowermeterGas(SensorHm):
    """Powermeter for Gas and energy."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.SENSORNODE.update({"GAS_ENERGY_COUNTER": [1],
                                "GAS_POWER": [1],
                                "ENERGY_COUNTER": [1],
                                "POWER": [1],
                                "IEC_ENERGY_COUNTER": [1,2],
                                "IEC_POWER": [1,2]})

    def get_gas_counter(self, channel=None):
        """Return gas counter."""
        return float(self.getSensorData("GAS_ENERGY_COUNTER", channel))

    def get_gas_power(self, channel=None):
        """Return gas power."""
        return float(self.getSensorData("GAS_POWER", channel))

    def get_energy(self, channel=None):
        """Return energy counter."""
        return float(self.getSensorData("ENERGY_COUNTER", channel))

    def get_power(self, channel=None):
        """Return power counter."""
        return float(self.getSensorData("POWER", channel))

    def get_iec_energy(self, channel=None):
        """Return iec energy counter."""
        return float(self.getSensorData("IEC_ENERGY_COUNTER", channel))

    def get_iec_power(self, channel=None):
        """Return iec power counter."""
        return float(self.getSensorData("IEC_POWER", channel))


class Smoke(SensorHm, HelperBinaryState):
    """Smoke alarm.
       This is a binary sensor."""

    def is_smoke(self, channel=None):
        """ Return True if smoke is detected """
        return self.get_state(channel)


class SmokeV2(SensorHm, HelperBinaryState):
    """Smoke alarm with Battery.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.ATTRIBUTENODE.update({"ERROR_ALARM_TEST": self.ELEMENT,
                                   "ERROR_SMOKE_CHAMBER": self.ELEMENT})

    def is_smoke(self, channel=None):
        """ Return True if smoke is detected """
        return self.get_state(channel)

class SmokeV2Team(HMSensor, HelperBinaryState):
    """This is a group of smoke sensors. In such a configuration only the
       virtual team device will emit a smoke detected event."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.BINARYNODE.update({"STATE": [1]})

        self.ATTRIBUTENODE.update({"SENDERADDRESS": [1],
                                   "SENDERID": [1]})

    def is_smoke(self, channel=None):
        """ Return True if smoke is detected """
        return self.get_state(channel)

class IPSmoke(SensorHmIPNoVoltage):
    """HomeMatic IP Smoke sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"SMOKE_DETECTOR_ALARM_STATUS": self.ELEMENT})

    @property
    def ELEMENT(self):
        return [1]


class GongSensor(SensorHm):
    """Wireless Gong Sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.EVENTNODE.update({"PRESS_SHORT": self.ELEMENT})


class WiredSensor(SensorHmW, HelperWired):
    """Wired binary Sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.BINARYNODE.update({"SENSOR": self.ELEMENT})

    @property
    def ELEMENT(self):
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def get_state(self, channel=None):
        """ Returns current state of sensor """
        return bool(self.getBinaryData("SENSOR", channel))


class FillingLevel(SensorHm):
    """Filling level sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"FILLING_LEVEL": self.ELEMENT})

    def get_level(self, channel=None):
        """ Return filling level from 0 to 100 % """
        return int(self.getSensorData("FILLING_LEVEL", channel))

    @property
    def ELEMENT(self):
        return [1]


class ValveDrive(SensorHm):
    """Valve drive HM-CC-VD."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"VALVE_STATE": self.ELEMENT})

    def get_level(self, channel=None):
        """ Return valve state from 0% to 99% """
        return int(self.getSensorData("VALVE_STATE", channel))

    @property
    def ELEMENT(self):
        return [1]


class Motion(SensorHmNLB):
    """Motion detection.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION": self.ELEMENT})
        self.SENSORNODE.update({"BRIGHTNESS": self.ELEMENT})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    def get_brightness(self, channel=None):
        """ Return brightness from 0 (dark ) to 255 (bright) """
        return int(self.getSensorData("BRIGHTNESS", channel))


class SmartwareMotion(HMSensor, HelperRssiDevice):
    """Motion detection.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"STATE": self.ELEMENT})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("STATE", channel))

    @property
    def ELEMENT(self):
        return [1]


class MotionV2(SensorHm, HelperSabotage):
    """Motion detection version 2.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION": self.ELEMENT})
        self.SENSORNODE.update({"BRIGHTNESS": self.ELEMENT})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    def get_brightness(self, channel=None):
        """ Return brightness from 0 (dark ) to 255 (bright) """
        return int(self.getSensorData("BRIGHTNESS", channel))


class MotionIP(SensorHmIP):
    """Motion detection indoor (rf ip)
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION_DETECTION_ACTIVE": [1], "MOTION": [1]})
        self.SENSORNODE.update({"ILLUMINATION": [1]})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0]})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    def is_motion_detection_active(self, channel=None):
        return bool(self.getBinaryData("MOTION_DETECTION_ACTIVE", channel))

    def get_brightness(self, channel=None):
        """ Return brightness from 0 (dark) to 163830 (bright) """
        return float(self.getSensorData("ILLUMINATION", channel))

    @property
    def ELEMENT(self):
        return [0, 1]


class MotionIPContactSabotage(SensorHmIP, HelperSabotageIP):
    """Motion detection indoor (rf ip)
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION_DETECTION_ACTIVE": [1], "MOTION": [1]})
        self.SENSORNODE.update({"ILLUMINATION": [1]})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0]})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    def is_motion_detection_active(self, channel=None):
        return bool(self.getBinaryData("MOTION_DETECTION_ACTIVE", channel))

    def get_brightness(self, channel=None):
        """ Return brightness from 0 (dark) to 163830 (bright) """
        return float(self.getSensorData("ILLUMINATION", channel))

    @property
    def ELEMENT(self):
        return [0, 1]


class MotionIPV2(SensorHmIP):
    """Motion detection indoor 55 (rf ip)
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION_DETECTION_ACTIVE": [3], "MOTION": [3]})
        self.SENSORNODE.update({"ILLUMINATION": [3]})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0]})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    def is_motion_detection_active(self, channel=None):
        return bool(self.getBinaryData("MOTION_DETECTION_ACTIVE", channel))

    def get_brightness(self, channel=None):
        """ Return brightness from 0 (dark) to 163830 (bright) """
        return float(self.getSensorData("ILLUMINATION", channel))

    @property
    def ELEMENT(self):
        return [0, 1, 2, 3]


class MotionIPV2W(SensorHmIPW):
    """Motion detection indoor 55 (rf ip)
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION_DETECTION_ACTIVE": [3], "MOTION": [3]})
        self.SENSORNODE.update({"ILLUMINATION": [3]})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0]})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    def is_motion_detection_active(self, channel=None):
        return bool(self.getBinaryData("MOTION_DETECTION_ACTIVE", channel))

    def get_brightness(self, channel=None):
        """ Return brightness from 0 (dark) to 163830 (bright) """
        return float(self.getSensorData("ILLUMINATION", channel))

    @property
    def ELEMENT(self):
        return [0, 1, 2, 3]


class PresenceIP(SensorHmIP, HelperSabotageIP):
    """Presence detection with HmIP-SPI.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"PRESENCE_DETECTION_STATE": self.ELEMENT,
                                "PRESENCE_DETECTION_ACTIVE": self.ELEMENT})
        self.SENSORNODE.update({"ILLUMINATION": self.ELEMENT,
                                "CURRENT_ILLUMINATION": self.ELEMENT})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0]})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("PRESENCE_DETECTION_STATE", channel))

    def get_brightness(self, channel=None):
        """ Return brightness from 0 (dark) to 163830 (bright) """
        return float(self.getSensorData("ILLUMINATION", channel))

    @property
    def ELEMENT(self):
        return [1]


class PresenceIPW(SensorHmIPW):
    """Presence detection with HmIPW-SPI.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"PRESENCE_DETECTION_STATE": self.ELEMENT,
                                "PRESENCE_DETECTION_ACTIVE": self.ELEMENT,
                                "CURRENT_ILLUMINATION_STATUS": self.ELEMENT,
                                "ILLUMINATION_STATUS": self.ELEMENT})
        self.SENSORNODE.update({"ILLUMINATION": self.ELEMENT,
                                "CURRENT_ILLUMINATION": self.ELEMENT})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0]})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("PRESENCE_DETECTION_STATE", channel))

    def get_brightness(self, channel=None):
        """ Return brightness from 0 (dark) to 163830 (bright) """
        return float(self.getSensorData("ILLUMINATION", channel))

    @property
    def ELEMENT(self):
        return [1]


class TiltIP(SensorHmIP):
    """Tilt detection with HmIP-SAM.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION": [1]})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0]})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    @property
    def ELEMENT(self):
        return [0, 1]


class RemoteMotion(SensorHm, Remote):
    """Motion detection with buttons.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION": [3]})
        self.SENSORNODE.update({"BRIGHTNESS": [3]})

    def is_motion(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    def get_brightness(self, channel=None):
        """ Return brightness from 0 (dark ) to 255 (bright) """
        return int(self.getSensorData("BRIGHTNESS", channel))

    @property
    def ELEMENT(self):
        return [1, 2]


class IPRemoteMotionV2(Remote, MotionIPV2):
    """Motion detection with buttons (hm ip).
       This is a binary sensor."""

    # pylint: disable=useless-super-delegation
    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)


class IPRemoteMotionV2W(Remote, MotionIPV2W):
    """Wired motion detection with buttons (hm ip).
       This is a binary sensor."""

    # pylint: disable=useless-super-delegation
    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)


class LuxSensor(SensorHm):
    """Sensor for messure LUX."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"LUX": [1]})

    def get_lux(self, channel=None):
        """Return messure lux."""
        return float(self.getSensorData("LUX", channel))


class ImpulseSensor(HMEvent):
    """Inpulse sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.EVENTNODE.update({"SEQUENCE_OK": self.ELEMENT})


class AreaThermostat(SensorHmNLB):
    """Wall mount thermostat."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": self.ELEMENT,
                                "HUMIDITY": self.ELEMENT})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_humidity(self, channel=None):
        return int(self.getSensorData("HUMIDITY", channel))


class IPAreaThermostat(SensorHmIP):
    """Wall mount thermostat."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"ACTUAL_TEMPERATURE": [1],
                                "HUMIDITY": [1]})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("ACTUAL_TEMPERATURE", channel))

    def get_humidity(self, channel=None):
        return int(self.getSensorData("HUMIDITY", channel))


class IPAreaThermostatNoBattery(SensorHmIPNoBattery):
    """Wall mount thermostat without battery."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"ACTUAL_TEMPERATURE": [1],
                                "HUMIDITY": [1]})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("ACTUAL_TEMPERATURE", channel))

    def get_humidity(self, channel=None):
        return int(self.getSensorData("HUMIDITY", channel))


class TemperatureSensor(SensorHm):
    """Temperature Sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata (HB-UNI-Sen-TEMP-DS18B20 has 8 temperature values)
        if "HB-UNI-Sen-TEMP-DS18B20" in self._TYPE:
            self.SENSORNODE.update({"TEMPERATURE": [1, 2, 3, 4, 5, 6, 7, 8]})
        else:
            self.SENSORNODE.update({"TEMPERATURE": self.ELEMENT})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("TEMPERATURE", channel))


class HBUNISenWEA(TemperatureSensor):
    """HB-UNI-Sen-WEA"""
    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.SENSORNODE.update({"AIR_PRESSURE": self.ELEMENT,
                                "HUMIDITY": self.ELEMENT,
                                "LUX": self.ELEMENT,
                                "RAIN_COUNTER": self.ELEMENT,
                                "WIND_SPEED": self.ELEMENT,
                                "WIND_DIRECTION": self.ELEMENT,
                                "WIND_DIRECTION_RANGE": self.ELEMENT,
                                "GUST_SPEED": self.ELEMENT,
                                "UVINDEX": self.ELEMENT,
                                "LIGHTNING_COUNTER": self.ELEMENT,
                                "LIGHNTING_DISTANCE": self.ELEMENT})


class TemperatureDiffSensor(SensorHm):
    """Temperature difference Sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": [1, 2, 3, 4]})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("TEMPERATURE", channel))


class WeatherSensor(SensorHm):
    """Weather sensor.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": self.ELEMENT,
                                "HUMIDITY": self.ELEMENT,
                                "RAIN_COUNTER": self.ELEMENT,
                                "WIND_SPEED": self.ELEMENT,
                                "WIND_DIRECTION": self.ELEMENT,
                                "WIND_DIRECTION_RANGE": self.ELEMENT,
                                "SUNSHINEDURATION": self.ELEMENT,
                                "BRIGHTNESS": self.ELEMENT})
        self.BINARYNODE.update({"RAINING": self.ELEMENT})
        del self.ATTRIBUTENODE["LOWBAT"]

    def get_temperature(self, channel=None):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_humidity(self, channel=None):
        return int(self.getSensorData("HUMIDITY", channel))

    def get_rain_counter(self, channel=None):
        return float(self.getSensorData("RAIN_COUNTER", channel))

    def get_wind_speed(self, channel=None):
        return float(self.getSensorData("WIND_SPEED", channel))

    def get_wind_direction(self, channel=None):
        return int(self.getSensorData("WIND_DIRECTION", channel))

    def get_wind_direction_range(self, channel=None):
        return int(self.getSensorData("WIND_DIRECTION_RANGE", channel))

    def get_sunshineduration(self, channel=None):
        return int(self.getSensorData("SUNSHINEDURATION", channel))

    def get_brightness(self, channel=None):
        return int(self.getSensorData("BRIGHTNESS", channel))

    def is_raining(self, channel=None):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("RAINING", channel))


class IPWeatherSensorPlus(SensorHmIP):
    """HomeMatic IP Weather sensor Plus.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"ACTUAL_TEMPERATURE": [1],
                                "HUMIDITY": [1],
                                "RAIN_COUNTER": [1],
                                "WIND_SPEED": [1],
                                "SUNSHINEDURATION": [1],
                                "ILLUMINATION": [1]})
        self.BINARYNODE.update({"RAINING": [1]})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0],
                                   "TEMPERATURE_OUT_OF_RANGE": [0]})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("ACTUAL_TEMPERATURE", channel))

    def get_humidity(self, channel=None):
        return int(self.getSensorData("HUMIDITY", channel))

    def get_rain_counter(self, channel=None):
        return float(self.getSensorData("RAIN_COUNTER", channel))

    def get_wind_speed(self, channel=None):
        return float(self.getSensorData("WIND_SPEED", channel))

    def get_sunshineduration(self, channel=None):
        return int(self.getSensorData("SUNSHINEDURATION", channel))

    def get_brightness(self, channel=None):
        return int(self.getSensorData("ILLUMINATION", channel))

    def is_raining(self, channel=None):
        return bool(self.getBinaryData("RAINING", channel))

    def is_temperature_out_of_range(self, channel=None):
        return bool(self.getAttributeData("TEMPERATURE_OUT_OF_RANGE", channel))


class IPWeatherSensorBasic(SensorHmIP):
    """HomeMatic IP Weather sensor Basic."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"ACTUAL_TEMPERATURE": [1],
                                "HUMIDITY": [1],
                                "WIND_SPEED": [1],
                                "SUNSHINEDURATION": [1],
                                "ILLUMINATION": [1]})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0],
                                   "TEMPERATURE_OUT_OF_RANGE": [0]})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("ACTUAL_TEMPERATURE", channel))

    def get_humidity(self, channel=None):
        return int(self.getSensorData("HUMIDITY", channel))

    def get_wind_speed(self, channel=None):
        return float(self.getSensorData("WIND_SPEED", channel))

    def get_sunshineduration(self, channel=None):
        return int(self.getSensorData("SUNSHINEDURATION", channel))

    def get_brightness(self, channel=None):
        return int(self.getSensorData("ILLUMINATION", channel))

    def is_temperature_out_of_range(self, channel=None):
        return bool(self.getAttributeData("TEMPERATURE_OUT_OF_RANGE", channel))


class IPRainSensor(SensorHmIPNoLowbat):
    """HomeMatic IP Rain sensor HmIP-SRD."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"ACTUAL_TEMPERATURE": [1]})
        self.BINARYNODE.update({"RAINING": [1],
                                "HEATER_STATE": [1]})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0],
                                   "OPERATING_VOLTAGE": [0]})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("ACTUAL_TEMPERATURE", channel))

    def is_raining(self, channel=None):
        return bool(self.getBinaryData("RAINING", channel))


class IPPassageSensor(SensorHmIP, HelperRssiPeer, HelperEventRemote):
    """HomeMatic IP Passage Sensor. #2 = right to left, #3 = left to right
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"PASSAGE_COUNTER_VALUE": self.ELEMENT})
        self.BINARYNODE.update({"PASSAGE_COUNTER_OVERFLOW": self.ELEMENT,
                                "LAST_PASSAGE_DIRECTION": [2],
                                "CURRENT_PASSAGE_DIRECTION": [2]})

    @property
    def ELEMENT(self):
        return [2, 3]


class IPWeatherSensor(SensorHmIP):
    """HomeMatic IP Weather sensor.
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"ACTUAL_TEMPERATURE": [1],
                                "HUMIDITY": [1],
                                "RAIN_COUNTER": [1],
                                "WIND_SPEED": [1],
                                "WIND_DIR": [1],
                                "WIND_DIR_RANGE": [1],
                                "SUNSHINEDURATION": [1],
                                "ILLUMINATION": [1]})
        self.BINARYNODE.update({"RAINING": [1]})
        self.ATTRIBUTENODE.update({"ERROR_CODE": [0],
                                   "TEMPERATURE_OUT_OF_RANGE": [0]})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("ACTUAL_TEMPERATURE", channel))

    def get_humidity(self, channel=None):
        return int(self.getSensorData("HUMIDITY", channel))

    def get_rain_counter(self, channel=None):
        return float(self.getSensorData("RAIN_COUNTER", channel))

    def get_wind_speed(self, channel=None):
        return float(self.getSensorData("WIND_SPEED", channel))

    def get_wind_direction(self, channel=None):
        return int(self.getSensorData("WIND_DIR", channel))

    def get_wind_direction_range(self, channel=None):
        return int(self.getSensorData("WIND_DIR_RANGE", channel))

    def get_sunshineduration(self, channel=None):
        return int(self.getSensorData("SUNSHINEDURATION", channel))

    def get_brightness(self, channel=None):
        return int(self.getSensorData("ILLUMINATION", channel))

    def is_raining(self, channel=None):
        return bool(self.getBinaryData("RAINING", channel))

    def is_temperature_out_of_range(self, channel=None):
        return bool(self.getAttributeData("TEMPERATURE_OUT_OF_RANGE", channel))


class WeatherStation(SensorHm):
    """Weather station."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": self.ELEMENT,
                                "HUMIDITY": self.ELEMENT,
                                "AIR_PRESSURE": self.ELEMENT})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_humidity(self, channel=None):
        return int(self.getSensorData("HUMIDITY", channel))

    def get_air_pressure(self, channel=None):
        return int(self.getSensorData("AIR_PRESSURE", channel))


class IPBrightnessSensor(SensorHmIP):
    """IP Sensor for outdoor brightness measure"""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"CURRENT_ILLUMINATION": [1],
                                "AVERAGE_ILLUMINATION": [1],
                                "LOWEST_ILLUMINATION": [1],
                                "HIGHEST_ILLUMINATION": [1]})


class UniversalSensor(HMSensor, HelperLowBat, HelperRssiPeer, HelperValveState):
    """Universal sensor. (https://wiki.fhem.de/wiki/Universalsensor)"""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": self.ELEMENT,
                                "HUMIDITY": self.ELEMENT,
                                "AIR_PRESSURE": self.ELEMENT})

        if "HB-UNI-Sensor1" in self._TYPE:
            self.SENSORNODE.update({"OPERATING_VOLTAGE": self.ELEMENT,
                                    "LUX": self.ELEMENT,
                                    "VALVE_STATE": self.ELEMENT})
        else:
            self.SENSORNODE.update({"BatteryVoltage": [1],
                                    "LUMINOSITY": [1]})

    def get_temperature(self, channel=None):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_humidity(self, channel=None):
        return int(self.getSensorData("HUMIDITY", channel))

    def get_air_pressure(self, channel=None):
        return int(self.getSensorData("AIR_PRESSURE", channel))

    def get_luminosity(self, channel=None):
        if "HB-UNI-Sensor1" in self._TYPE:
            return float(self.getSensorData("LUX", channel))
        else:
            return float(self.getSensorData("LUMINOSITY", channel))

    def get_battery_voltage(self, channel=None):
        if "HB-UNI-Sensor1" in self._TYPE:
            return float(self.getSensorData("OPERATING_VOLTAGE", channel))
        else:
            return float(self.getSensorData("BatteryVoltage", channel))


class WaterIP(SensorHmIP):
    """Water sensor HmIP-SWD
       This is a binary sensor."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"ALARMSTATE": self.ELEMENT,
                                "MOISTURE_DETECTED": self.ELEMENT,
                                "WATERLEVEL_DETECTED": self.ELEMENT})

    @property
    def ELEMENT(self):
        return [1]


class IPContact(SensorHmIP, HelperBinaryState, HelperEventRemote):
    """Multi purpose contact that emits its open/closed state.
       This is a binary sensor. Supports multiple modes"""

    def is_open(self, channel=None):
        """ Returns True if the contact is open. """
        return self.get_state(channel)

    def is_closed(self, channel=None):
        """ Returns True if the contact is closed. """
        return not self.get_state(channel)

    def is_on(self, channel=None):
        """ Returns True if switch is on. """
        return self.get_state(channel)

    def is_off(self, channel=None):
        """ Returns True if switch is off. """
        return not self.get_state(channel)

    @property
    def ELEMENT(self):
        if "FCI6" in self._TYPE:
            return [1, 2, 3, 4, 5, 6]
        elif "FCI1" in self._TYPE:
            return [1]
        return [1]

class IPAlarmSensor(SensorHmIP, HelperSabotageIP):
    """Alarm Sirene that emits its Acoustic and Optical Alarm Status"""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({
            "OPTICAL_ALARM_ACTIVE": [3],
            "ACOUSTIC_ALARM_ACTIVE": [3]
        })

    def is_optical_alarm_active(self, channel=None):
        return bool(self.getBinaryData("OPTICAL_ALARM_ACTIVE", channel))

    def is_acoustic_alarm_active(self, channel=None):
        return bool(self.getBinaryData("ACOUSTIC_ALARM_ACTIVE", channel))

class ValveBox(SensorHmIP):
    """Valve Box HmIP-FALMOT-C12"""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.SENSORNODE.update({"LEVEL": self.ELEMENT})

    def get_level(self, channel=None):
        """Return valve state from 0% to 99%"""
        return float(self.getSensorData("LEVEL", channel))

    @property
    def ELEMENT(self):
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

class ValveBoxW(SensorHmIPW):
    """Valve Box HmIPW-FALMOT-C12"""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.SENSORNODE.update({"LEVEL": self.ELEMENT})

    def get_level(self, channel=None):
        """Return valve state from 0% to 99%"""
        return float(self.getSensorData("LEVEL", channel))

    @property
    def ELEMENT(self):
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

class IPLanRouter(HMSensor):
    """ HmIP Lan Router HmIP-HAP"""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.SENSORNODE.update({"CARRIER_SENSE_LEVEL": [0],
                                "DUTY_CYCLE_LEVEL": [0]})
        self.BINARYNODE.update({"DUTY_CYCLE": [0]})

    def get_duty_cycle_level(self, channel=None):
        return float(self.getSensorData("DUTY_CYCLE_LEVEL", channel))

    def get_carrier_sense_level(self, channel=None):
        return float(self.getSensorData("CARRIER_SENSE_LEVEL", channel))

class TempModuleSTE2(SensorHmIP):
    """HmIP-STE2-PCB."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"ACTUAL_TEMPERATURE": self.ELEMENT,
                                "ACTUAL_TEMPERATURE_STATUS": self.ELEMENT})

    @property
    def ELEMENT(self):
        return [1, 2, 3]

class IPLockDLD(SensorHmIP):
    """Lock state for HmIP-DLD."""

    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"LOCK_STATE": [1]})

DEVICETYPES = {
    "HM-Sec-SC": ShutterContact,
    "HM-Sec-SC-2": ShutterContact,
    "HM-Sec-SCo": ShutterContact,
    "ZEL STG RM FFK": ShutterContact,
    "BC-SC-Rd-WM-2": MaxShutterContact,
    "BC-SC-Rd-WM": MaxShutterContact,
    "HM-SCI-3-FM": ShutterContact,
    "HmIP-SCI": IPShutterContactSabotage,
    "HMIP-SWDO": IPShutterContactSabotage,
    "HmIP-SWDO": IPShutterContactSabotage,
    "HmIP-SWDO-PL": IPShutterContactSabotage,
    "HmIP-SWDO-I": IPShutterContactSabotage,
    "HmIP-SWDM": IPShutterContact,
    "HmIP-SWDM-B2": IPShutterContact,
    "HmIP-SRH": RotaryHandleSensorIP,
    "HM-Sec-RHS": RotaryHandleSensor,
    "ZEL STG RM FDK": RotaryHandleSensor,
    "HM-Sec-RHS-2": RotaryHandleSensor,
    "HM-Sec-xx": RotaryHandleSensor,
    "HM-Sec-WDS": WaterSensor,
    "HM-Sec-WDS-2": WaterSensor,
    "HM-ES-TX-WM": PowermeterGas,
    "HM-Sen-DB-PCB": GongSensor,
    "HM-Sec-SD": Smoke,
    "HM-Sec-SD-Generic": Smoke,
    "HM-Sec-SD-2": SmokeV2,
    "HM-Sec-SD-2-Generic": SmokeV2,
    "HM-Sec-SD-2-Team": SmokeV2Team,
    "HmIP-SWSD": IPSmoke,
    "HM-Sen-MDIR-WM55": RemoteMotion,
    "HM-Sen-MDIR-SM": Motion,
    "HM-Sen-MDIR-O": Motion,
    "HM-MD": Motion,
    "HM-Sen-MDIR-O-2": Motion,
    "HM-Sen-MDIR-O-3": Motion,
    "HM-Sec-MDIR-3": MotionV2,
    "HM-Sec-MDIR-2": MotionV2,
    "HM-Sec-MDIR": MotionV2,
    "263 162": MotionV2,
    "HM-Sec-MD": MotionV2,
    "HmIP-SMI": MotionIPContactSabotage,
    "HmIP-SMI55": IPRemoteMotionV2,
    "HmIP-SMI55-2": IPRemoteMotionV2,
    "HmIPW-SMI55": IPRemoteMotionV2W,
    "HmIP-SMO": MotionIP,
    "HmIP-SMO-A": MotionIP,
    "HmIP-SMO-A-2": MotionIP,
    "HmIP-SMO-2": MotionIP,
    "HmIP-SPI": PresenceIP,
    "HmIPW-SPI": PresenceIPW,
    "HM-Sen-LI-O": LuxSensor,
    "HM-Sen-EP": ImpulseSensor,
    "HM-Sen-X": ImpulseSensor,
    "ASH550I": AreaThermostat,
    "ASH550": AreaThermostat,
    "HM-WDS10-TH-O": AreaThermostat,
    "HM-WDS20-TH-O": AreaThermostat,
    "HM-WDS40-TH-I": AreaThermostat,
    "HM-WDS40-TH-I-2": AreaThermostat,
    "263 157": AreaThermostat,
    "263 158": AreaThermostat,
    "IS-WDS-TH-OD-S-R3": AreaThermostat,
    "HM-WDS100-C6-O": WeatherSensor,
    "HM-WDS100-C6-O-2": WeatherSensor,
    "KS550": WeatherSensor,
    "KS888": WeatherSensor,
    "KS550Tech": WeatherSensor,
    "KS550LC": WeatherSensor,
    "HmIP-SWO-PR": IPWeatherSensor,
    "HmIP-SWO-PL": IPWeatherSensorPlus,
    "HmIP-SWO-B": IPWeatherSensorBasic,
    "WS550": WeatherStation,
    "WS888": WeatherStation,
    "WS550Tech": WeatherStation,
    "WS550LCB": WeatherStation,
    "WS550LCW": WeatherStation,
    "HM-WDC7000": WeatherStation,
    "HM-Sec-TiS": TiltSensor,
    "HM-CC-SCD": CO2Sensor,
    "263 160": CO2Sensor,
    "HM-WDS30-OT2-SM": TemperatureDiffSensor,
    "HM-WDS30-OT2-SM-2": TemperatureDiffSensor,
    "HM-WDS30-T-O": TemperatureSensor,
    "S550IA": TemperatureSensor,
    "HM-Sen-Wa-Od": FillingLevel,
    "HMW-Sen-SC-12-DR": WiredSensor,
    "HMW-Sen-SC-12-FM": WiredSensor,
    "HM-CC-VD": ValveDrive,
    "ZEL STG RM FSA": ValveDrive,
    "HmIP-SAM": TiltIP,
    "HmIP-STHO": IPAreaThermostat,
    "HmIP-STHO-A": IPAreaThermostat,
    "HmIP-SPDR": IPPassageSensor,
    "IT-Old-Remote-1-Channel": SmartwareMotion,
    "HmIP-SLO": IPBrightnessSensor,
    "HB-UW-Sen-THPL-O": UniversalSensor,
    "HB-UW-Sen-THPL-I": UniversalSensor,
    "HmIP-SWD": WaterIP,
    "HB-UNI-Sensor1": UniversalSensor,
    "HmIP-FCI1": IPContact,
    "HmIP-FCI6": IPContact,
    "HmIP-DSD-PCB": IPContact,
    "HB-UNI-Sen-TEMP-DS18B20": TemperatureSensor,
    "HB-UNI-Sen-WEA": HBUNISenWEA,
    "HmIP-ASIR-B1": IPAlarmSensor,
    "HmIP-ASIR-O": IPAlarmSensor,
    "HmIP-ASIR": IPAlarmSensor,
    "HmIP-ASIR-2": IPAlarmSensor,
    "HmIP-FALMOT-C12": ValveBox,
    "HmIPW-FALMOT-C12": ValveBoxW,
    "HmIP-SRD": IPRainSensor,
    "HmIP-HAP": IPLanRouter,
    "HB-WDS40-THP-O": WeatherStation,
    "HmIP-STE2-PCB": TempModuleSTE2,
    "HmIP-SCTH230": CO2SensorIP,
    "HmIP-DLD": IPLockDLD,
    "HmIP-SFD": ParticulateMatterSensorIP,
}
