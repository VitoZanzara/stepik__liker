from class_logger import get_logger

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

logger = get_logger('class_solution')

class Solution:
    def __init__(self, sol: WebElement):
        self.sol = sol
        user = sol.find_element(By.CLASS_NAME, 'comments-user-badge__name')
        self.user_name = user.text
        self.user_id = user.get_attribute('href').split('/')[-1].strip()
        self.voted = bool(sol.find_elements(By.CSS_SELECTOR, "[data-is-epic]"))
        self.like_btn, self.dislike_btn = sol.find_elements(By.CLASS_NAME, 'ui-vote__like')
        self.n_likes = int('0' + sol.find_element(By.CSS_SELECTOR, "[data-type='like']").text)
        self.n_dislikes = int('0' + sol.find_element(By.CSS_SELECTOR, "[data-type='dislike']").text)

    def like(self):
        try:
            self.like_btn.click()
        except Exception as e:
            logger.error(e)
            logger.error(str(self))

    def get_statistic_info(self):
        like_from = 0
        like_to = 1
        return self.user_id, self.user_name, like_from, like_to

    def __str__(self):
        return (f'{self.user_name}, {self.user_id}\n'
                f'likes: {self.n_likes}, dislikes: {self.n_dislikes}')