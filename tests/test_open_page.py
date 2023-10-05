import allure

from pages.w3schools import W3schoolsPage


def test_select_all(browser):
    page = W3schoolsPage(browser)

    with allure.step("Run SQL"):
        page.run_sql()

    with allure.step("Wait for result and get customers"):
        customers = page.get_customers()

    with allure.step("Check that 'Giovanni Rovelli' has Address = 'Via Ludovico il Moro 22'"):
        giovannies = list(filter(lambda d: d["contact_name"] == "Giovanni Rovelli", customers))
        for giovanni in giovannies:
            assert giovanni["address"] == "Via Ludovico il Moro 22", "Wrong address"


def test_select_only_london(browser):
    sql = "SELECT * FROM Customers WHERE City = 'London';"
    page = W3schoolsPage(browser)

    with allure.step("Run SQL"):
        page.run_sql(sql)

    with allure.step("Wait for result and get customers"):
        rows = page.result_table_rows

    with allure.step("Check that table has only 6 records"):
        assert len(rows) == 6, "Wrong number of row in table"


def test_insert_new_record(browser):
    values = ("Anton Martynau", "Victor Hugo", "Isle de Paris", "Paris", "211501", "FR")
    sql = f"INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country) VALUES {values}"
    page = W3schoolsPage(browser)

    with allure.step("Run INSERT SQL"):
        page.run_sql(sql)

    with allure.step("Wait for result and check result message"):
        page.check_result_message("You have made changes to the database. Rows affected: 1")


def test_update_record(browser):
    sql = """UPDATE Customers
             SET CustomerName = 'Robin Bobin', ContactName = 'MR Bean', Address = 'Street',
                 City = 'Limassol', PostalCode = '12345', Country = 'CY'
             WHERE CustomerID = 69;"""
    page = W3schoolsPage(browser)

    with allure.step("Run UPDATE SQL"):
        page.run_sql(sql)

    with allure.step("Wait for result and check result message"):
        page.check_result_message("You have made changes to the database. Rows affected: 1")

    with allure.step("Run SELECT SQL"):
        sql = "SELECT * FROM Customers WHERE CustomerID = 69;"
        page.run_sql(sql)
    with allure.step("Wait for result and get customers"):
        customer = page.get_customers()[0]
    with allure.step("Check that values are updated"):
        assert customer["customer_name"] == "Robin Bobin", "Wrong CustomerName"
        assert customer["contact_name"] == "MR Bean", "Wrong ContactName"
        assert customer["address"] == "Street", "Wrong Address"
        assert customer["city"] == "Limassol", "Wrong City"
        assert customer["postal_code"] == "12345", "Wrong PostalCode"
        assert customer["country"] == "CY", "Wrong Country"


def test_restore_database(browser):
    page = W3schoolsPage(browser)

    with allure.step("Restore Database"):
        page.restore_database()
    with allure.step("Wait for result and check result message"):
        page.check_result_message("The database is fully restored.")
