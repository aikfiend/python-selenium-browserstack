from json import dumps
from os import getenv

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

FRONTEND_BASE_URL = getenv("FRONTEND_BASE_URL")
BROWSERSTACK_WEBDRIVER_URL = getenv("BROWSERSTACK_WEBDRIVER_URL")
BROWSERSTACK_USERNAME = getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = getenv("BROWSERSTACK_ACCESS_KEY")

bstack_options = {
    "osVersion": "15.0",
    "deviceName": "Google Pixel 9 Pro XL",
    "userName": BROWSERSTACK_USERNAME,
    "accessKey": BROWSERSTACK_ACCESS_KEY,
    "consoleLogs" : "info",
    "projectName": "Browserstack issues",
    "buildName": "Get window size key error issue",
    "sessionName" : "Test get_window_size() raises KeyError",
}

chrome_options = ChromeOptions()
chrome_options.set_capability(name="browserName", value="chrome")
chrome_options.set_capability(name="bstack:options", value=bstack_options)
driver = webdriver.Remote(command_executor=BROWSERSTACK_WEBDRIVER_URL, options=chrome_options)

try:
    wait = WebDriverWait(driver, 10)
    driver.get(FRONTEND_BASE_URL)
    window_size = driver.get_window_size()

    assert {k in window_size for k in ("width", "height")}
except KeyError as e:
    reason = f"{e.__class__.__name__}: {str(e)}, {e.args[0]}"
    driver.execute_script(
        f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status": "failed", "reason": {dumps(reason)}}}}}'
    )
else:
    driver.execute_script(
        f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status": "passed"}}}}'
    )
finally:
    driver.quit()
