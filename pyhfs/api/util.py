import datetime

def from_timestamp(timestamp: int):
    """
    Converts fusion solar timestamp to datetime

    Args:
        timestamp: timestamp as an integer

    returns:
        datetime: timestamp converted to datetime, with milliseconds ignored
    """
    return datetime.datetime.fromtimestamp(timestamp // 1000)

def to_timestamp(time: datetime.datetime) -> int:
    """Converts datetime to fusion solar timestamp.

    Args:
        time: time as datetime

    Returns:
        int: time as integer
    """
    return int(time.timestamp() * 1000)

def data_prop(field: str, docstring=None, conv=None) -> property:
    """
    Read-only property for `self._data[field]` with no
    default value. `conv` can specify a conversion function,
    for example `float`

    Args:
        field: name of the field
        docstring: documentation string
        conv: optional conversion function, typically `int` or `float`

    returns:
        property
    """

    def getter(self):
        value = self._data[field]
        if conv is not None:
            value = conv(value)
        return value

    return property(getter, doc=docstring)


def data_prop_opt(field: str, default, docstring=None, conv=None) -> property:
    """
    Read-only property for `self._data[field]` with default value.
    `conv` can specify a conversion function, for example `float`

    Args:
        field: name of the field
        default: default value if field does not exist
        docstring: documentation string
        conv: optional conversion function, typically `int` or `float`

    returns:
        property
    """

    def getter(self):
        value = self._data.get(field, default)
        if conv is not None:
            value = conv(value)
        return value

    return property(getter, doc=docstring)


def data_item_prop(field: str, docstring=None, conv=None) -> property:
    """
    Read-only property for `self._data["dataItemMap"][field]` with no
    default value. `conv` can specify a conversion function,
    for example `float`

    Args:
        field: name of the field
        docstring: documentation string
        conv: optional conversion function, typically `int` or `float`

    returns:
        property
    """

    def getter(self):
        value = self._data["dataItemMap"][field]
        if conv is not None:
            value = conv(value)
        return value

    return property(getter, doc=docstring)


def data_item_prop_opt(field: str, default, docstring=None, conv=None) -> property:
    """
    Read-only property for `self._data["dataItemMap"][field]` with default value.
    `conv` can specify a conversion function, for example `float`

    Args:
        field: name of the field
        default: default value if field does not exist
        docstring: documentation string
        conv: optional conversion function, typically `int` or `float`

    returns:
        property
    """

    def getter(self):
        value = self._data["dataItemMap"].get(field, default)
        if conv is not None:
            value = conv(value)
        return value

    return property(getter, doc=docstring)

def ffmt(value: float) -> str:
    """
    Format a float to 5.2f, compatible with None
    """
    s = "(none)" if value is None else f"{value:5.2f}"
    return f"{s:7s}"