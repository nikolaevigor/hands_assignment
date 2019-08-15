# Тестовое задание

## Текст задания

Компания делает сайт: стандартный справочник организаций. Клиенты на сайте ищут номера телефонов организаций. Номера телефонов устаревают. Из-за этого компания теряет клиентов.

Для каждой организации в базе хранится ссылка на её сайт и путь к странице контактов. Страниц контактов на одном сайте может быть несколько. Есть модуль, который умеет распознавать неактуальный номер. На вход он получает список номеров в формате 8KKKNNNNNNN.

Вам нужно написать модуль, который скачивает web-страницы, находит в тексте и выводит все распознанные номера телефонов в этом формате.

Номера по формату российские. Если для номера не указан код города — номер московский.

Чем выше доля распознаваемых реальных номеров на странице и чем быстрее работает модуль — тем он лучше. Здесь: https://hands.ru/company/about модуль должен найти номер, здесь: https://repetitors.info тоже. Страниц в базе может быть очень много!

В задании не нужно использовать тяжелые фреймворки, или сохранять найденные номера в базу. Задание ориентировано буквально на несколько часов.

Решение нужно предоставить в виде отдельного репозитория на github.com

## Комментарии соискателя

Данная задача классифицируется как IO bound. Соответственно для эффективного использования процессорного времени я использовал трединг.

Для каждого урла создаем отдельный поток, который сделает запрос (с некоторым таймаутом) и полученный ответ положит в очередь. В основном потоке будем пулить из очереди и обрабатывать все ответы, так как обработку можно назвать CPU bound задачей.

В основном потоке прогоняем полученный html страницы через регулярку, форматируем и получаем телефоны вида 8KKKNNNNNNN. Выбрал эту регулярку так как на мой взгляд она оптимальна между "не мэтчится то, что надо" и "мэтчится то, что не надо (например различные id)".

Из сторонних библиотек исользована только requests.

Альтернативным подходом может являться использование asyncio. Но так как requests написана в синхронном стиле, а aiohttp тащить не хотелось, я его не использовал.

### Допущения

- урлы уже загружены в память (на этом месте могли бы быть коннекторы к базе, либо к брокеру сообщений или любому другому IPC)

- так как это тестовое задание, я завершаю процесс, если в очереди секунду ничего не было