from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from class_logger import get_logger

logger = get_logger('class_like')

class Like:
    sol_sufx = '?thread=solutions'

    def __init__(self, like: WebElement):
        self.like = like
        self.is_comment = like.get_attribute('data-action') == 'replied'
        like_from = like.find_element(By.CLASS_NAME, 'notification__title').find_element(By.TAG_NAME, 'a')
        self.like_info = like.find_element(By.CLASS_NAME, 'notification__title-action').text
        self.user_name = like_from.text     # имя лайкнувшего
        *_, self.user_id, _ = like_from.get_attribute('href').split('/')   # stepik-id лайкнувшего
        _, what_was_liked = like.find_element(By.CLASS_NAME, 'notification__context-content').find_elements(By.TAG_NAME, 'a')
        self.what_was_liked_name = what_was_liked.text
        self.what_was_liked_url = what_was_liked.get_attribute('href')
        self.__mark_read_btn = like.find_element(By.CLASS_NAME, 'notification__icon-action')


    def mark_read(self) -> None:
        """
        Если лайк, а не коммент (который надо бы прочитать самому) -
        смело помечаем прочитанным
        """
        if not self.is_comment:
            try:
                self.__mark_read_btn.click()
            except Exception as e:
                logger.error("Like mark read failed")
                logger.error(str(self))
                logger.error(e)


    def get_info(self) -> tuple[str, str]:
        """получаем url того, что было лайкнуто и id лайкнувшего"""
        solution_url = self.what_was_liked_url + self.sol_sufx
        return solution_url, self.user_id

    def get_statistic_info(self) -> tuple[str, str, int, int]:
        like_from = 1
        like_to = 0
        return self.user_id, self.user_name, like_from, like_to

    @property
    def is_good(self) -> bool:
        """ Если это решение, а не комментарий, и его лайкнули, а не прокомментировали
        - объект подходит для обработки """
        sol_text = self.like.find_element(By.CLASS_NAME, 'show-more__content').text
        return 'Решение' in sol_text and not self.is_comment


    def __str__(self):
        like_name = f'liker_name: {self.user_name}'
        liker_id = f'liker_id: {self.user_id}'
        what_was_liked_name = f'what_was_liked_name: {self.what_was_liked_name}'
        what_was_liked_url = f'what_was_liked_url: {self.what_was_liked_url}'
        comment_or_like = f'comment_or_like: {"comment" if self.is_comment else "like"}'
        on_work = f'take_to_work: {self.is_good}'
        return (f'{on_work}, {comment_or_like}\n'
                f'{like_name}, {liker_id}\n'
                f'{self.like_info}\n'
                f'{what_was_liked_name}\n'
                f'{what_was_liked_url}')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.get_info()})'

