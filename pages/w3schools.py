import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from pages.common import CommonPage


class W3schoolsPage(CommonPage):
    RUN_SQL_BUTTON = (By.CSS_SELECTOR, ".ws-btn")
    RESULT_TABLE = (By.XPATH, "//table[contains(@class, 'ws-table-all')]")
    RESULT_TABLE_ROWS = (By.XPATH, "//table[contains(@class, 'ws-table-all')]//tr")
    SQL_INPUT = (By.CLASS_NAME, "CodeMirror-code")
    RESULT_MSG = (By.XPATH, "//div/div[@id='divResultSQL'][count(*)=1]")
    RESTORE_BUTTON = (By.ID, "restoreDBBtn")

    @property
    def restore_button(self):
        return self.find_element(self.RESTORE_BUTTON)

    @property
    def run_sql_button(self):
        return self.find_element(self.RUN_SQL_BUTTON)

    @property
    def sql_input(self):
        return self.find_element(self.SQL_INPUT)

    def run_sql(self, request: str = None):
        if request:
            self.sql_input.click()
            self._action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            self._action.send_keys(request).perform()
        self.run_sql_button.click()

    @property
    def result_table_rows(self):
        self.wait_for(self.RESULT_TABLE)
        return self.find_elements(self.RESULT_TABLE_ROWS)[1:]

    def get_customers(self):
        customers = []
        fields = ["customer_id", "customer_name", "contact_name", "address", "city", "postal_code", "country"]
        for row in self.result_table_rows:
            values = [cell.text for cell in row.find_elements(By.XPATH, "./td")]
            customers.append({k: v for (k, v) in zip(fields, values)})
        return customers

    def check_result_message(self, expected_msg):
        assert self.wait_for(self.RESULT_MSG).text == expected_msg, "Wrong result message"

    def restore_database(self):
        with allure.step("Click 'Restore Database' button"):
            self.restore_button.click()
        with allure.step("Click 'OK' button in alert"):
            self.alert().accept()
