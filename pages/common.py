from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


class CommonPage:

    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 30)
        self._action = ActionChains(self.driver)

    def wait_for(self, locator):
        return self._wait.until(ec.presence_of_element_located(locator))

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, element):
        return self._action.click(element)

    def alert(self):
        return self._wait.until(ec.alert_is_present())
