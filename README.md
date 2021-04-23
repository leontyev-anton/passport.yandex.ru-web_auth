# passport.yandex.ru-auth
Authorization on Yandex via a regular web form with the help of Python’s script. It is necessary in order to parse data from Yandex service, that doesn’t have an API. Example work with PyQuery.

Go to the page https://passport.yandex.ru/auth in browser, open the browser’s Inspect (Network -> Preserve log -> All | XHR).

First, enter the login - as you can see, a request has gone to the 'start' url. Then enter a password - a request has gone to the 'commit_password' url.

Learn carefully what goes where (Inspector: Headers, Preview) and implement a similar behavior in the script (there are additional comments in the code).

RUS: Авторизация через обычную веб-форму на Яндексе через Python-скрипт. Это нужно для того, что распарсить данные с Яндекс-сервиса, у которого нет API. Пример работы с PyQuery.

Заходим в браузере на страницу https://passport.yandex.ru/auth, открываем отладчик в браузере (Network -> Preserve log -> All | XHR).

Сначала вводим логин - видим что ушел запрос на страницу start. Потом вводим пароль - ушел запрос на страницу commit_password.

Изучаем внимательно что куда отправляется (в отладчике Headers, Preview) и реализуем подобное поведение в скрипте (в коде есть дополнительные комментарии).
