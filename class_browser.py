from time import sleep
import random

from config import load_config
from load_friends_data import load_friends_data
from class_logger import get_logger

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


logger = get_logger('class_browser')

class MyFirefoxBrowser(webdriver.Firefox):
    __instance = None

    firefox_path = 'firefox_portable/firefox.exe'
    options = FirefoxOptions()
    # options.add_argument('-headless')       # отключить показ браузера
    options.binary_location = firefox_path

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, headless=False, timeout=30):
        if headless:
            self.options.add_argument('--headless')
        super().__init__(options=self.options)
        self.waiter = WebDriverWait(self, timeout)
        self.friends_data = load_friends_data()
        self._do_login()

    def _do_login(self):
        user = load_config()
        # DO LOGIN
        self.get('https://stepik.org')
        self.waiter.until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar__auth_login'))).click()

        name_field = self.waiter.until(EC.presence_of_element_located((By.ID, 'id_login_email')))
        pwd_field = self.waiter.until(EC.presence_of_element_located((By.ID, 'id_login_password')))
        enter_btn = self.find_element(By.CLASS_NAME, 'sign-form__btn')

        name_field.send_keys(user.username)
        pwd_field.send_keys(user.password)

        enter_btn.click()
        n = random.uniform(5, 9)
        logger.debug(f'sleep after login {n:.5f} seconds')
        sleep(n)

        # await page loading and open user menu
        self.waiter.until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar__profile-toggler'))).click()
        user_profile = self.find_element(By.CSS_SELECTOR, "[data-qa='menu-item-profile']")
        # get your own stepik_id
        *_, self.STEPIK_SELF_ID, _ = user_profile.find_element(By.TAG_NAME, 'a').get_attribute('href').split('/')
        sleep(3)



class MyChromeBrowser(webdriver.Chrome):
    __instance = None

    options = ChromeOptions()
    options.binary_location = "chrome_portable/chrome.exe"
    # you may need some other options
    options.add_argument('--disable-site-isolation-trials')
    # options.add_argument('--headless')    # отключить показ браузера

    # options.add_argument('--no-sandbox')
    # options.add_argument('--no-default-browser-check')
    # options.add_argument('--no-first-run')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--disable-default-apps')

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, headless=False, timeout=30):
        if headless:
            self.options.add_argument('--headless')
        super().__init__(options=self.options)
        self.waiter = WebDriverWait(self, timeout)
        self.friends_data = load_friends_data()
        self._do_login()

    def _do_login(self):
        user = load_config()
        # DO LOGIN
        self.get('https://stepik.org')
        self.waiter.until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar__auth_login'))).click()

        name_field = self.waiter.until(EC.presence_of_element_located((By.ID, 'id_login_email')))
        pwd_field = self.waiter.until(EC.presence_of_element_located((By.ID, 'id_login_password')))
        enter_btn = self.find_element(By.CLASS_NAME, 'sign-form__btn')

        name_field.send_keys(user.username)
        pwd_field.send_keys(user.password)

        enter_btn.click()
        n = random.uniform(5, 9)
        logger.debug(f'sleep after login {n:.5f} seconds')
        sleep(n)

        # await page loading and open user menu
        self.waiter.until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar__profile-toggler'))).click()
        user_profile = self.find_element(By.CSS_SELECTOR, "[data-qa='menu-item-profile']")
        # get your own stepik_id
        *_, self.STEPIK_SELF_ID, _ = user_profile.find_element(By.TAG_NAME, 'a').get_attribute('href').split('/')
        n = random.uniform(3, 5)
        logger.debug(f'sleep after get self_stepik_id {n:.5f} seconds')
        sleep(n)

        # Костыль. Только так удалось заставить работать авторизация во второй вкладке
        # но и он работает не всегда
        self.execute_script(f'window.open(" ", "_blank1");')  # open url in new tab
        self.switch_to.window(self.window_handles[-1])
        self.switch_to.window(self.window_handles[0])


# можно выбрать Chrome или Firefox
MyBrowser = MyFirefoxBrowser
# MyBrowser = MyChromeBrowser


if __name__ == '__main__':
    browser = MyBrowser()
    # browser = MyFirefoxBrowser()

    print(browser.friends_data)
    print(browser.STEPIK_SELF_ID)
    print(browser.execute_script("return document.title;"))

    urls = ('https://stepik.org/lesson/654056/step/7?thread=solutions',
            'https://stepik.org/lesson/654058/step/5?thread=solutions',
            'https://stepik.org/lesson/332555/step/6?thread=solutions')


    sleep(10)
    cookies = browser.get_cookies()
    print(cookies)
    for i, url in enumerate(urls):
        browser.execute_script(f'window.open("{url}", "_blank1");')
        browser.switch_to.window(browser.window_handles[-1])
        sleep(3)
        print(browser.execute_script("return document.title;"))
        sleep(12)



