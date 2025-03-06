import logging
from time import sleep
from class_browser import MyBrowser
import random


def scroll_down(browser: MyBrowser, n: str, logger: logging.Logger):
    """
    Прокрутка простыни с лайками или с решениями до самого дна.
    Сделано несколько криво, но остальные варианты получались еще хуже
    """
    try:
        n = int('0' + n)
    except ValueError:
        n = 1000
    scrolls = max(3, (n // 18))
    for i in range(scrolls):
        logger.debug(f'scrolling down {i + 1} of {scrolls}')
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(random.uniform(2, 5))