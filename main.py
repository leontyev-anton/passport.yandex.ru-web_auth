import sys
import time

import requests
from main_config import ya_login, ya_password
from pyquery import PyQuery

# будем отправлять такой User Agent, чтобы Яндекс не посчитал нас ботом
my_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'

# стартуем сессию: запрашиваем первую обычную страницу авторизации, и выдираем оттуда два параметра, которые будут нужны в будущем
try:
    session = requests.Session()
    r_welcome = session.get('https://passport.yandex.ru/auth', headers={'User-Agent': my_user_agent})
    pyquery_object = PyQuery(r_welcome.text)
    csrf_token = pyquery_object('input[name=csrf_token]').val()
    process_uuid_href = pyquery_object('.Button2_type_link:first').attr('href')
    process_uuid = process_uuid_href[process_uuid_href.find('process_uuid=')+13:]
except Exception as e:
    print(f'Exit script. Error at start session: {e}')
    sys.exit(1)
else:
    pass

time.sleep(2.5)
# отправляем логин на следующую страницу-форму. поля которые нужно указать смотрим в отладчике браузера (Headers -> Form Data)
# забираем из JSON-ответа один параметр
try:
    r_start = session.post('https://passport.yandex.ru/registration-validations/auth/multi_step/start',
                           {'csrf_token': csrf_token, 'login': ya_login, 'process_uuid': process_uuid},
                           headers={'User-Agent': my_user_agent, 'Referer': 'https://passport.yandex.ru/auth',
                                    'X-Requested-With': 'XMLHttpRequest'})
    track_id = r_start.json()['track_id']
except Exception as e:
    print(f'Exit script. Error at multi_step/start: {e}')
    sys.exit(1)
else:
    pass

time.sleep(2.5)
# отправляем пароль на следующую страницу-форму. она ничего не возвращает. если все норм, то устанавливает куки
r_password = session.post('https://passport.yandex.ru/registration-validations/auth/multi_step/commit_password',
                          {'csrf_token': csrf_token, 'track_id': track_id, 'password': ya_password,
                           'retpath': 'https://passport.yandex.ru/profile'},
                          headers={'User-Agent': my_user_agent, 'Referer': 'https://passport.yandex.ru/auth/welcome',
                                   'X-Requested-With': 'XMLHttpRequest'})

if (r_password.json()['status'] == 'ok'):
    time.sleep(1)
    # проверим что все хорошо - обычным образом запросим страницу профиля. должны увидеть свое Имя и Фамилию
    r_profile = session.get('https://passport.yandex.ru/profile', headers={'User-Agent': my_user_agent})
    pyquery_object = PyQuery(r_profile.text)
    first_name = pyquery_object('div.personal-info__first:first').text()
    last_name = pyquery_object('div.personal-info__last:first').text()
    print(f'Profile name: {first_name} {last_name}')
else:
    print(f'Exit script. Error at multi_step/commit_password: {r_password.json()["status"]} {r_password.json()["errors"]}')
    sys.exit(1)
