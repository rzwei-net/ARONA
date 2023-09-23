from unittest import mock

import pytest
import uiautomator2
from pytest_bdd import scenario, when, then, given
from requests import Response

from src.android.drivers.uiautomator2 import UiAutomator2Driver
from src.interfaces.driver import DriverServerError


@scenario(
    feature_name="uiautomator2.feature",
    scenario_name="Error running a daemon on an Android device because invalid pid",
)
def test_scenario():
    pass


@given("Driver is already connected to the device", target_fixture="driver")
def given1(mocker):
    mocker.patch("uiautomator2.connect_adb_wifi")
    serial = "127.0.0.1:16448"

    driver = UiAutomator2Driver(serial)
    device = mock.Mock(spec=uiautomator2.Device)
    driver.device = device

    return driver


@given("ATX agent return invalid pid")
def given2(driver):
    mock_response = mock.Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    driver.device.http.post.return_value = mock_response


@when("I run a daemon")
def when1(driver: UiAutomator2Driver):
    with pytest.raises(DriverServerError):
        driver.run_daemon("sleep 123")


@then("Driver should raise an server error")
def then1():
    pass
