from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import base64

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

def canvas_to_png(driver, canvas_xpath, download_path, i):
    canvas = select_with_timeout(driver, canvas_xpath)
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    canvas_png = base64.b64decode(canvas_base64)
    with open(r'{}/page_{}.png'.format(download_path, i), 'wb') as f:
        f.write(canvas_png)
    return i + 1