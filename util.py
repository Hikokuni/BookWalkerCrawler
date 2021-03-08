from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def select_with_timeout(driver, xpath, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except:
        driver.quit()

def send_keys(driver, keys):
    actions = ActionChains(driver)
    actions.send_keys(keys)
    actions.perform()

def element_present(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False