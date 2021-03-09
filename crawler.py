from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from util import element_present, select_with_timeout, send_keys, canvas_to_png
import time, argparse

# Setup parser
parser = argparse.ArgumentParser(description='对BookWalker用爬虫（伪）')
parser.add_argument('Username', metavar='username', type=str, help='BookWalker 用户名')
parser.add_argument('Password', metavar='password', type=str, help='BookWalker 密码')
parser.add_argument('-w', '--wait', action='store', type=float, default=2, help='Web Driver等待时间（可近似看做翻页时间），默认为2秒，网络不好可适当增加')
parser.add_argument('-l', '--load', action='store', type=float, default=16, help='图书最初加载时间，默认为16秒，网络不好可适当增加')
parser.add_argument('-p', '--path', action='store', type=str, default='Download', help='图片存储路径，默认为项目文件夹下的Download文件夹')
args = parser.parse_args()

# Setup driver
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(args.wait)
driver.get("https://global.bookwalker.jp/")

# Sign in and navigate to books page
select_with_timeout(driver, "//span[text()='Sign In']").click()
select_with_timeout(driver, "//input[@name='j_username']").send_keys(args.Username)
select_with_timeout(driver, "//input[@name='j_password']").send_keys(args.Password)
select_with_timeout(driver, "//span[@class='lt_loginBtn' and text()='Sign-in']").click()
select_with_timeout(driver, "(//a[@class='util-menu-btn'])[2]", timeout=60).click()
select_with_timeout(driver, "//section[contains(@class, 'book-item')]")

# Get list of books
books = driver.find_elements_by_xpath("//section[contains(@class, 'book-item')]//a[@data-action-label='タイトル']")
i = 1
for book in books:
    print('{}. {}'.format(i, book.text))
    i += 1
selection = int(input('选择图书序号：'))

# Open book
select_with_timeout(driver, "(//section[contains(@class, 'book-item')]//span[text()='Read this book'])[{}]".format(selection)).click()
driver.switch_to.window(driver.window_handles[-1])
time.sleep(args.load)

# Deal with special case (first page)
download_path = args.path
Path(download_path).mkdir(parents=True, exist_ok=True)
i = canvas_to_png(driver, "//div[@id='viewport1']/canvas", download_path, 1)
send_keys(driver, Keys.LEFT)

# Download rest of the pages
while(not element_present(driver, "//div[@id='dialog']/div[@style='display: block;']")):
    # viewport0
    i = canvas_to_png(driver, "//div[@id='viewport0']/canvas", download_path, i)
    #viewport1
    i = canvas_to_png(driver, "//div[@id='viewport1']/canvas", download_path, i)

    send_keys(driver, Keys.LEFT)
    send_keys(driver, Keys.LEFT)

driver.close()
driver.quit()