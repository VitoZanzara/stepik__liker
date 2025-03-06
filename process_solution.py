from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
import random

from class_browser import MyBrowser
from class_like import Like
from class_solution import Solution
from scroll_down import scroll_down
from class_logger import get_logger
from class_statistics import Statistics


logger = get_logger('process_solution')
stat = Statistics()


def process_solution(browser: MyBrowser, solution_url: str, ids_list: list[str]| None = None,
                     likes_list: list[Like]| None = None) -> tuple[int, int, int]:
    """

    :param browser: браузер они и в Африке браузер
    :param solution_url: адрес страницы с решениями, которые нужно полайкать
    :param ids_list: опционально. список stepik_id для ответных лайков,
    :param likes_list: опционально. Список лайков для пометки прочитанными
    :return:
    """
    ids_list = ids_list or []
    likes_list = likes_list or []
    STEPIK_SELF_ID = browser.STEPIK_SELF_ID
    friends_data = browser.friends_data

    browser.execute_script(f'window.open("{solution_url}", "_blank1");')     # open url in new tab
    browser.switch_to.window(browser.window_handles[-1])                     # switch to new tab
    try:
        _ = browser.waiter.until(EC.presence_of_element_located((By.CLASS_NAME, "tab__item-counter")))
    except TimeoutException:
        _ = browser.waiter.until(EC.presence_of_element_located((By.CLASS_NAME, "tab__item-counter")))
    sleep(random.uniform(6, 9))

    comments_sols = browser.find_elements(By.CLASS_NAME, "tab__item-counter")
    n_sols = '0'
    if len(comments_sols) == 2:
        comments, sols = comments_sols
        n_sols = sols.get_attribute('data-value')    # количество решений
    logger.debug(f'Общее количество решений: {n_sols}')
    scroll_down(browser, n_sols, logger)

    raw_solutions = browser.find_elements(By.CLASS_NAME, 'comment-widget')  # собираем все решения на странице

    liked = already_liked = 0
    for i, raw_sol in enumerate(raw_solutions, 1):
        if not i % 20:
            logger.debug(f'Обработка решения {i} из {len(raw_solutions)}')
        solution = Solution(raw_sol)
        if solution.user_id == STEPIK_SELF_ID:   # если собственное решение - пропускаем
            continue
        elif solution.voted:                     # если уже лайкали - пропускаем
            already_liked += 1
        elif solution.user_id in friends_data or solution.user_id in ids_list:
            liked += 1
            browser.execute_script("arguments[0].scrollIntoView(true);", solution.sol)
            solution.like()

        stat.set_stat(solution)     # Статистика

    stat.dump_data()

    page_title = browser.execute_script("return document.title;")
    solution_count = len(raw_solutions)
    logger.info(f'{page_title} ({solution_url}). Всего решений {solution_count}')
    logger.info(f'новых лайков: {liked}, старых лайков: {already_liked}')

    browser.switch_to.window(browser.window_handles[0])     # switch to main tab

    for like in likes_list:     # Помечаем лайки прочитанными
        browser.execute_script("arguments[0].scrollIntoView(true);", like.like)
        like.mark_read()
        logger.debug(f'{repr(like)} was marked')

    return liked, already_liked, len(raw_solutions)


if __name__ == '__main__':
    url = 'https://stepik.org/lesson/361657/step/3?thread=solutions'
    list_stepik_ids = []        # список айди, которые будут облайканы (помимо списка друзей)
    browser = MyBrowser()
    process_solution(browser, url, list_stepik_ids)

