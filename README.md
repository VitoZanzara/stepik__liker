# stepik_liker
### автоматическая раздача лайков на Stepik

в `class_browser.py` можно выбрать чем пользоваться
- Chrome -  `MyBrowser = MyChromeBrowser`, понадобится [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/)
- Firefox -  `MyBrowser = MyFirefoxBrowser`, понадобится [geckodriver](https://github.com/mozilla/geckodriver/releases/)

и Chromedriver и Geckodriver - проще всего положить в папку проекта

C Хромом имел постоянные проблемы - при открытии новой вкладки туда не переносилась авторизация с основной. И на сто процентов этот момент победить не удалось.

Гораздо более стабильно у меня всё работало в Firefox (если нет в установленной - [качаем портативную версию](https://portableapps.com/apps/internet/firefox_portable), кладем в папку проекта в `/firefox_portable`).

---
Для работы надо создать в папке проекта `.env` файл вида
```
STEPIK_USERNAME=your_stepik_id
STEPIK_PASSWORD=your_stepik_password
```
---
Если хочется раздавать лайки по списку друзей - создать в папке проекте файл `friends_list.yml`
```
  "friend_1_stepik_id": friend_1 name
  "friend_2_stepik_id": friend_2 name
   ...
  "friend_n_stepik_id": friend_n name
```
---
Запуск скрипта через `liker_main.py`, и понеслась:
- авторизация
- сбор выданных лайков
- проход по темам с лайкнутыми решениям, там ставим ответные лайки и раздаем лайки друзьям по списку
- отмечаем лайки прочитанными (уведомления о комментариях остаются нетронутыми)

Можно запустить отдельно `process_solution.py`, передав url страницы с решениями. Раздаст лайки на этой странице