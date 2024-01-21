import time
import unittest

from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
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

    def test_clock_add_city_then_remove_it(self) -> None:
        add_button = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.deskclock:id/fab')
        add_button.click()
        search_field = self.driver.find_element(
            by=AppiumBy.ID, value='com.google.android.deskclock:id/open_search_view_edit_text')
        search_field.send_keys('New York')
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
        self.driver.swipe(900, 900, 0, 900, 250)
        time.sleep(1)
        new_york_widget_displayed = len(self.driver.find_elements(
            by=AppiumBy.ID, value='com.google.android.deskclock:id/city_name'))
        assert new_york_widget_displayed == 0

    def test_set_alarm_and_delete_it(self) -> None:
        alarm_button = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.deskclock:id/tab_menu_alarm')
        alarm_button.click()
        add_button = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.deskclock:id/fab')
        add_button.click()
        number_6 = self.driver.find_element(
            by=AppiumBy.XPATH, value='//*[@content-desc="6 o\'clock"]')
        number_6.click()
        keyboard = self.driver.find_element(
            by=AppiumBy.ID, value='com.google.android.deskclock:id/material_timepicker_mode_button')
        keyboard.click()
        minutes_text_field = self.driver.find_element(
            by=AppiumBy.CLASS_NAME, value='android.widget.EditText')
        minutes_text_field.clear().send_keys('29')
        ok_button = self.driver.find_element(
            by=AppiumBy.ID, value='com.google.android.deskclock:id/material_timepicker_ok_button')
        ok_button.click()
        alarm_check = len(self.driver.find_elements(
            by=AppiumBy.XPATH, value='//*[@content-desc="6:29 AM"]'))
        assert alarm_check == 1
        delete_alarm_button = self.driver.find_element(by=AppiumBy.ID, value='com.google.android.deskclock:id/delete')
        delete_alarm_button.click()
        alarm_check = len(self.driver.find_elements(
            by=AppiumBy.XPATH, value='//*[@content-desc="6:29 AM"]'))
        assert alarm_check == 0


if __name__ == '__main__':
    unittest.main()
