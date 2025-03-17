from collections import defaultdict
from class_browser import MyBrowser
from time import sleep
from class_logger import get_logger
from scroll_down import scroll_down
from class_like import Like
from class_statistics import Statistics


from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = get_logger('process_likes')
stat = Statistics()


def process_likes(browser: MyBrowser):
    """
    Собирает лайки. Возвращает словарь вида
                    {solutions_url: {'ids_list': [stepik_id1, ...], 'likes_list': [Like(), ...]}}
    :param browser: экземплеря браузера
    :return: dict[str: dict]
    """
    notifications_url = 'https://stepik.org/notifications?type=comments'
    browser.get(notifications_url)
    browser.waiter.until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar__profile-toggler')))
    sleep(2)
    # получаем количество событий
    try:
        n_events = browser.waiter.until(EC.presence_of_element_located((By.ID, 'profile-notifications-badge'))).text
    except NoSuchElementException:
        logger.warning('Нет лайков, или количество не прогрузилось')
        n_events = '0'

    logger.info('Number of events: {}'.format(n_events))

    # прокручиваем страницу вниз
    scroll_down(browser, n=n_events, logger=logger)

    # собираем все лайки
    raw_likes_list = browser.find_elements(By.CLASS_NAME, 'notifications__widget')
    logger.info('Total number of likes: {}'.format(len(raw_likes_list)))

    likes_data_vals = lambda: {'ids_list': [], 'likes_list': []}
    likes_data = defaultdict(likes_data_vals)

    # фильтрация, группировка лайков
    for i, raw_like in enumerate(raw_likes_list, 1):
        if not i % 10:
            logger.debug(f'processing raw_like {i} of {len(raw_likes_list)}')
        like = Like(raw_like)
        if like.is_good:
            solution_url, liker_id = like.get_info()
            val = likes_data[solution_url]
            val['ids_list'].append(liker_id)
            val['likes_list'].append(like)
        else:
            browser.execute_script("arguments[0].scrollIntoView(true);", raw_like)
            like.mark_read()    # если не подходит для обработки - помечаем прочитанным
        stat.set_stat(like)  # статистика
    stat.dump_data()
    return likes_data


if __name__ == '__main__':
    browser = MyBrowser()
    likes_data = process_likes(browser)
    print(f'len = {len(likes_data)}')
    for solution_url, likes in likes_data.items():
        print(f'solution_url: {solution_url}')
        print(f'likes: {likes}')
        print('-' * 20)

