from class_logger import get_logger
from time import perf_counter
from process_likes import process_likes
from process_solution import process_solution
from class_browser import MyBrowser


logger = get_logger('liker_main')

start_time = perf_counter()
total_liked = total_already_liked = total_processed_solutions = 0

with MyBrowser() as browser:
    likes_data = process_likes(browser)     # собираем лайки

    for i, (solution_url, like_data) in enumerate(likes_data.items(), 1):
        logger.warning(f'process solution link {i} of {len(likes_data)}')
        liked, already_liked, n_solutions = process_solution(browser, solution_url, *like_data.values())
        total_liked += liked
        total_already_liked += already_liked
        total_processed_solutions += n_solutions


end_time = perf_counter()
running_time = end_time - start_time

rest, s = divmod(int(running_time), 60)
h, m = divmod(rest, 60)
spent_time = f'{h}:{m:02d}:{s:02d}'
print()
print(f'Новых лайков {total_liked}, ранее лайкнутых {total_already_liked}')
print(f"Всего обработано: {len(likes_data)} ссылок и {total_processed_solutions} решений")
print(f'Running time {spent_time}')

