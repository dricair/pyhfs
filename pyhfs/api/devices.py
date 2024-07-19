from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .plants import Plant

from .util import data_prop, data_prop_opt


class Device:
    """
    API class for "Device List API"
    """

    DEVICE_TYPES = {
        1: "Inverter",
        2: "SmartLogger",
        8: "STS",
        10: "EMI",
        13: "protocol converter",
        16: "general device",
        17: "grid meter",
        22: "PID",
        37: "Pinnet data logger",
        38: "Residential inverter",
        39: "Battery",
        40: "Backup box",
        41: "ESS",
        45: "PLC",
        46: "Optimizer",
        47: "Power sensor",
        62: "Dongle",
        63: "Distributed SmartLogger",
        70: "Safety box",
        60001: "Mains",
        60003: "Genset",
        60043: "SSU group",
        60044: "SSU",
        60092: "Power converter",
        60014: "Lithium battery rack",
        60010: "AC output power distribution",
        23070: "EMMA",
    }

    UNKNOWN_DEVICE = "Unknown"

    def __init__(self, data: dict, plants: dict[str, "Plant"]):
        """
        Initialize from JSON response

        Args:
            data: response from the API for a Device
            plant: Plant linked to this device, calls add_device to this plant
        """
        self._data = data
        if self.station_code not in plants:
            raise ValueError(f"Plant/Station {self.station_code} not found for device {self}")
        self._plant = plants[self.station_code]
        self._plant.add_device(self)

    @staticmethod
    def from_list(data: list, plants: dict[str, "Plant"]) -> dict[str, "Device"]:
        """
        Create a list of devices from a response

        Args:
          data: list of devices from Api
          plants: dictionary of plants

        Returns:
          dict: dictionary device id -> Device
        """
        devices = [Device(item, plants) for item in data]
        return {device.id: device for device in devices}

    def __str__(self) -> str:
        sw_version = f", SW version {self.software_version}" if self.software_version else ""
        return f"{self.name} ({self.id}): {self.dev_type} ({self.dev_type_id}) {sw_version}"

    id = data_prop("id", "Device ID (int)")
    unique_id = data_prop("devDn", "Unique device ID in the system (str)")
    name = data_prop("devName", "Device name (str)")
    station_code = data_prop("stationCode", "Plant ID (str)")
    serial_number = data_prop("esnCode", "Device SN (str)")
    dev_type_id = data_prop("devTypeId", "Device type as integer (int)")
    software_version = data_prop("softwareVersion", "Software version (str)")
    optimizers = data_prop_opt("optimizerNumber", None, "Quantity of optimizers (int)")
    inverter_type = data_prop("invType", "Inverter model, only applicable to inverters (int)")
    longitude = data_prop("longitude", "Plant longitude (float)")
    latitude = data_prop("latitude", "Plant latitude (float)")

    @property
    def dev_type(self) -> str:
        """
        Device type (as string)
        """
        return Device.DEVICE_TYPES.get(self.dev_type_id, Device.UNKNOWN_DEVICE)

    @property
    def plant(self) -> "Plant":
        """
        Plant/Station containing this device
        """
        return self._plant

    @property
    def data(self) -> dict:
        """
        Raw data for this device
        """
        return self._data
