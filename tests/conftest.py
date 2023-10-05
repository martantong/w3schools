import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.page_load_strategy = 'eager'

    with allure.step("Open browser and get URL"):
        driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

        url = "https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all"
        driver.get(url)

    yield driver

    driver.close()
