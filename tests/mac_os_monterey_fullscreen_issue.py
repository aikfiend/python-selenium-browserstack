import json
from os import getenv
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()

EMBED_FRONTEND_BASE_URL = getenv("EMBED_FRONTEND_BASE_URL")
BROWSERSTACK_WEBDRIVER_URL = getenv("BROWSERSTACK_WEBDRIVER_URL")
BROWSERSTACK_USERNAME = getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = getenv("BROWSERSTACK_ACCESS_KEY")

bstack_options = {
    "os": "OS X",
    "osVersion": "Monterey",
    "browserName": "Safari",
    "browserVersion": "15.6",
    "userName": BROWSERSTACK_USERNAME,
    "accessKey": BROWSERSTACK_ACCESS_KEY,
    "projectName": "Browserstack Issues",
    "buildName": "macOS Monterey Full Screen Issue",
    "sessionName" : "Test Expand Video to Full Screen"
}

safari_options = SafariOptions()
safari_options.set_capability(name="bstack:options", value=bstack_options)
driver = webdriver.Remote(command_executor=BROWSERSTACK_WEBDRIVER_URL, options=safari_options)

try:
    wait = WebDriverWait(driver, 10)
    driver.get(f"{EMBED_FRONTEND_BASE_URL}/clip/8959035?a=19&o=16")
    fullscreen_button = wait.until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, "button[data-title='Full screen (f)']"))
    )
    fullscreen_button.click()
    sleep(5)

    assert (
        driver.execute_script("return document.fullscreenElement") is not None
    ), f"Video was not expanded to full screen"
except Exception as e:
    reason = f"{e.__class__.__name__}: {str(e)}"
    driver.execute_script(
        f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status": "failed", "reason": {json.dumps(reason)}}}}}'
    )
else:
    driver.execute_script(
        f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status": "passed"}}}}'
    )
finally:
    driver.quit()
