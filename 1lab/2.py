from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()

driver.get("https://www.saucedemo.com/")

LOGIN_ = "locked_out_user"
PASSWORD_ = "secret_sauce"
FALLBACK_LOGIN_ = "standard_user"


def login(username, password):
    username_input = driver.find_element(By.XPATH, '//input[@placeholder="Username"]')

    password_input = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')

    error_div = driver.find_element(By.CLASS_NAME, 'error-message-container')

    username_input.clear()
    username_input.send_keys(username)
    
    time.sleep(1)
    password_input.clear()
    password_input.send_keys(password)

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    try:
        wait = WebDriverWait(driver, 10)
        error_div = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'error-message-container')))

        if error_div.text == "":
            return True
        return False
    except:
        return True

if not login(LOGIN_, PASSWORD_):
    print("пробуем fallback...")
    if login(FALLBACK_LOGIN_, PASSWORD_):
        print("fallback!")
    else:
        print("fallback не сработал!")
        driver.quit()
        exit()
else:
    print("вход с первого раза")

wait = WebDriverWait(driver, 10)

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

sort_select = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container")))
select = Select(sort_select)
select.select_by_value("lohi")

print("Сортировка по цене (low to high) применена.")

time.sleep(1)

items = driver.find_elements(By.CLASS_NAME, "inventory_item")

last_item = items[-1]

add_to_cart_button = last_item.find_element(By.CSS_SELECTOR, ".btn_primary")

add_to_cart_button.click()

input('press to stop')
driver.quit()