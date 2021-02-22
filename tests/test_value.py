import pytest

from rpidiag.value import Clock, Temperature, Value, Voltage
from tests.utils import utils


def test_temperature_get(mocker):
    utils.mock_cmd_output("58.9'C", mocker)
    assert pytest.approx(Temperature().get(), abs=0.001) == 58.9


def test_voltage_get(mocker):
    utils.mock_cmd_output("0.8438V", mocker)
    assert pytest.approx(Voltage().get(), abs=0.0001) == 0.8438


def test_clock_get(mocker):
    utils.mock_cmd_output("600117184", mocker)
    assert Clock().get() == 600


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ([10, 20], 15.0),
        ([52.6, 53.9, 54.1], 53.533),
        ([0.001, 0], 0.0),
    ],
)
def test_value_get_avg(test_input, expected):
    value = Value(Temperature.get)  # any getter is fine
    value.all = test_input
    assert pytest.approx(value.get_avg(), abs=0.001) == expected


@pytest.mark.parametrize(
    "initial_min, initial_max, test_input, expected_min, expected_max",
    [
        (15, 15, 20, 15, 20),
        (15, 15, 10, 10, 15),
        (15, 15, 15, 15, 15),
        (10, 20, 15, 10, 20),
        (10, 20, 30, 10, 30),
        (10, 20, 5, 5, 20),
    ],
)
def test_update(
    initial_min, initial_max, test_input, expected_min, expected_max, mocker
):
    mocker.patch("rpidiag.value.Clock.get", return_value=test_input)
    clock = Clock()
    clock.min = initial_min
    clock.max = initial_max
    clock.update()

    assert clock.min == expected_min
    assert clock.get_summary()["clock_min"] == str(expected_min)

    assert clock.max == expected_max
    assert clock.get_summary()["clock_max"] == str(expected_max)


def test_temperature_get_summary(mocker):
    mocker.patch(
        "rpidiag.value.Value._get_summary",
        return_value={"min": 5, "avg": 7.5, "max": 10},
    )
    temperature = Temperature()
    assert temperature.get_summary() == {
        "temp_min": "5.0",
        "temp_avg": "7.5",
        "temp_max": "10.0",
    }


def test_voltage_get_summary(mocker):
    mocker.patch(
        "rpidiag.value.Value._get_summary",
        return_value={"min": 5, "avg": 7.5, "max": 10},
    )
    voltage = Voltage()
    assert voltage.get_summary() == {
        "voltage_min": "5.00",
        "voltage_avg": "7.50",
        "voltage_max": "10.00",
    }


def test_clock_get_summary(mocker):
    mocker.patch(
        "rpidiag.value.Value._get_summary",
        return_value={"min": 5, "avg": 7.5, "max": 10},
    )
    clock = Clock()
    assert clock.get_summary() == {
        "clock_min": "5",
        "clock_avg": "7",
        "clock_max": "10",
    }
