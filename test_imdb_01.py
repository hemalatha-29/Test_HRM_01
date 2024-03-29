import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.username_input = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "oxd-input")))
        self.password_input = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "oxd-input--active")))
        self.login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "orangehrm-login-button")]')))
    def login(self, username, password):
        try:
            self.username_input.clear()
            self.username_input.send_keys("Admin")
            self.password_input.clear()
            self.password_input.send_keys("admin123")
            self.login_button.click()
        except (TimeoutException) as e:
            pytest.fail(f"Exception occurred: {e}")

@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.TC_Login_01
def test_valid_login(chrome_driver):
    login_page = LoginPage(chrome_driver)
    login_page.login("Admin", "admin123")
    try:
        error_message = WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.ID, "spanMessage")))
        print("Login failed! Reason:", error_message.text)
    except TimeoutException:
        print("Login successful!")

@pytest.mark.TC_Login_02
def test_invalid_login(chrome_driver):
    login_page = LoginPage(chrome_driver)
    login_page.login("Admin", "incorrect_password")
    try:
        error_message = WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.ID, "spanMessage")))
        print("Login failed! Reason:", error_message.text)
    except TimeoutException:
        print("Login failed! invalid credential.")

@pytest.mark.TC_PIM_01
def test_add_employee(chrome_driver):
    login_page = LoginPage(chrome_driver)
    login_page.login("Admin", "admin123")
    try:
        pim_module_link = WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[2]/a')))
        pim_module_link.click()

        add_employee_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[3]')))
        add_employee_button.click()

        employee_first_name_input = WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[2]/input')))
        employee_first_name_input.clear()
        employee_first_name_input.send_keys("John")

        employee_middle_name_input = WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div[2]/input')))
        employee_middle_name_input.clear()
        employee_middle_name_input.send_keys("Deo")

        employee_last_name_input = WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[2]/input')))
        employee_last_name_input.clear()
        employee_last_name_input.send_keys("Smith")

        employee_id_input = WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/input')))
        employee_id_input.clear()
        employee_id_input.send_keys("1234")

        save_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[2]/button[2]')))
        save_button.click()

        success_message = WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="oxd-toaster_1"]')))
        print("Successful employee addition:", success_message.text)
    except TimeoutException as e:
        print("TimeoutException:", e)

@pytest.mark.TC_Login_02
def test_edit_employee_information(chrome_driver):
    login_page = LoginPage(chrome_driver)
    login_page.login("Admin", "admin123")

    try:
        pim_module_link = WebDriverWait(chrome_driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[2]/a')))
        pim_module_link.click()
        employee_list_link = WebDriverWait(chrome_driver, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[9]/div/button[2]/i')))
        employee_list_link.click()
        first_employee_checkbox = WebDriverWait(chrome_driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[1]/div/div/div/div[2]/div[1]/div[2]/input')))
        first_employee_checkbox.click()
        edit_button = WebDriverWait(chrome_driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[1]/div/div/div/div[2]/div[1]/div[2]/input')))
        edit_button.click()

        first_name_field = WebDriverWait(chrome_driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#app > div.oxd-layout > div.oxd-layout-container > div.oxd-layout-context > div > div > div > div.orangehrm-edit-employee-content > div.orangehrm-horizontal-padding.orangehrm-vertical-padding > form > div:nth-child(1) > div > div > div > div.--name-grouped-field > div:nth-child(1) > div:nth-child(2) > input')))
        first_name_field.send_keys(Keys.CONTROL + "a")  # Select all text
        first_name_field.send_keys(Keys.DELETE)
        first_name_field.send_keys("JOHN DOE")
        save_button = WebDriverWait(chrome_driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[4]/button|//button[@class="oxd-button oxd-button--medium oxd-button--secondary orangehrm-left-space"]')))
        save_button.click()
        success_message = WebDriverWait(chrome_driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="oxd-toaster_1"]')))
        print("Successful employee details addition Message:", success_message.text)

    except TimeoutException as e:
        print("TimeoutException:", e)

@pytest.mark.TC_PIM_03
def test_delete_employee(chrome_driver):
    login_page = LoginPage(chrome_driver)
    login_page.login("Admin", "admin123")

    try:
        pim_module = WebDriverWait(chrome_driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[2]/a')))
        pim_module.click()

        employee_list_element = WebDriverWait(chrome_driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[2]/a')))
        employee_list_element.click()

        employee_list = chrome_driver.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div')

        if len(employee_list) > 0:
            employee_to_delete = employee_list[0]
            delete_button = employee_to_delete.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[9]/div/button[1]')
            delete_button.click()

            delete_button_confirm = chrome_driver.find_element(By.CLASS_NAME, "oxd-icon.bi-trash")
            delete_button_confirm.click()

            WebDriverWait(chrome_driver, 30).until(EC.visibility_of_element_located((By.ID, "dialogDeleteBtn")))
            confirm_delete_button = chrome_driver.find_element(By.ID, "dialogDeleteBtn")
            confirm_delete_button.click()

            success_message = WebDriverWait(chrome_driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="oxd-toaster_1"]')))
            assert "Successfully Deleted" in success_message.text, "Deletion failed"

    except TimeoutException as e:
        print("TimeoutException:", e)

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html"])

