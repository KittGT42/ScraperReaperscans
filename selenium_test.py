import os.path

from selenium import webdriver
import time


from selenium.webdriver.common.by import By


def get_cookies():
    extension_path = os.path.abspath('cloudflare_buy_buy')
    options = webdriver.ChromeOptions()
    options.add_argument(f'--load-extension={extension_path}')
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-gpu')
    with webdriver.Chrome(options=options) as driver:
        driver.get('https://reaperscans.fr/serie/')
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element(By.ID, 'connect').click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(20)
        result_cookies = {}
        cookies_value = driver.get_cookies()
        for cookie in cookies_value:
            result_cookies[cookie['name']] = cookie['value']
        return result_cookies['cf_clearance']