"""User-defined types."""
from typing import NewType, Union

TypeClock = NewType("Clock", int)
TypeTemperature = NewType("Temperature", float)
TypeVoltage = NewType("Voltage", float)
# AnyValue = Union[TypeClock, TypeTemperature, TypeVoltage]
AnyValue = Union[int, float]
