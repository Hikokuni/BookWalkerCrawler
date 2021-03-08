from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time, util, base64, os, sys, argparse

# Setup parser
parser = argparse.ArgumentParser(description='对BookWalker用爬虫（伪）')
parser.add_argument('Username', metavar='username', type=str, help='BookWalker Username')
parser.add_argument('Password', metavar='password', type=str, help='BookWalker Password')
args = parser.parse_args()

# Setup driver
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(2)
driver.get("https://global.bookwalker.jp/")

# Sign in and navigate to books page
util.select_with_timeout(driver, "//span[text()='Sign In']").click()
util.select_with_timeout(driver, "//input[@name='j_username']").send_keys(args.Username)
util.select_with_timeout(driver, "//input[@name='j_password']").send_keys(args.Password)
util.select_with_timeout(driver, "//span[@class='lt_loginBtn' and text()='Sign-in']").click()
util.select_with_timeout(driver, "(//a[@class='util-menu-btn'])[2]", timeout=60).click()
util.select_with_timeout(driver, "//section[contains(@class, 'book-item')]")

# Get list of books
books = driver.find_elements_by_xpath("//section[contains(@class, 'book-item')]//a[@data-action-label='タイトル']")
i = 1
for book in books:
    print('{}. {}'.format(i, book.text))
selection = int(input('Select the book to scrape: '))

# Open book
util.select_with_timeout(driver, "(//section[contains(@class, 'book-item')]//span[text()='Read this book'])[{}]".format(selection)).click()
driver.switch_to.window(driver.window_handles[-1])

# Deal with pecial case (first page)
time.sleep(30)
Path('Download/').mkdir(parents=True, exist_ok=True)
i = 1
canvas = util.select_with_timeout(driver, "//div[@id='viewport1']/canvas")
canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
canvas_png = base64.b64decode(canvas_base64)
with open(r'Download/page_{}.png'.format(i), 'wb') as f:
    f.write(canvas_png)
i += 1
util.send_keys(driver, Keys.LEFT)

# Download rest of the pages
while(not util.element_present(driver, "//div[@id='dialog']/div[@style='display: block;']")):
    # viewport0
    canvas = util.select_with_timeout(driver, "//div[@id='viewport0']/canvas")
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    canvas_png = base64.b64decode(canvas_base64)
    with open(r'Download/page_{}.png'.format(i), 'wb') as f:
        f.write(canvas_png)
    i += 1

    #viewport1
    canvas = util.select_with_timeout(driver, "//div[@id='viewport1']/canvas")
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    canvas_png = base64.b64decode(canvas_base64)
    with open(r'Download/page_{}.png'.format(i), 'wb') as f:
        f.write(canvas_png)
    i += 1

    util.send_keys(driver, Keys.LEFT)
    util.send_keys(driver, Keys.LEFT)

driver.close()
driver.quit()