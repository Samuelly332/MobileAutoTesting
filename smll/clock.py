import unittest
from lib2to3.pgen2 import driver
from telnetlib import EC

from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Pixel',
    appPackage='com.google.android.deskclock',
    appActivity='com.android.deskclock.DeskClock',
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=AppiumOptions.load_capabilities(
            AppiumOptions(), capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_clock_add_city(self) -> None:
        button = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.deskclock:id/fab')
        button.click()
        text_field = self.driver.find_element(
            by=AppiumBy.ID, value='com.google.android.deskclock:id/open_search_view_edit_text')
        text_field.send_keys('New York')
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((
            By.ID, "com.google.android.deskclock:id/city_name")))
        new_york = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.deskclock:id/city_name')
        new_york.click()
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "com.google.android.deskclock:id/city_name")))
        new_york_widget = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.deskclock:id/city_name')
        if new_york_widget is not None and new_york_widget.text == "New York":
            assert True
        else:
            assert False


if __name__ == '__main__':
    unittest.main()