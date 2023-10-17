### [Установка](#title1)
### [Логика работы системы](#title2)
### [Права доступа](#title3)
### [Запуск](#title4)

---

---

## <a id="title1">Для корректной работы системы необходимо:</a>

- Запустите виртуальное окружение "poetry shell".
- Установите зависимости "poetry install".
- Создайте в корне файл .env и внесите в него все переменные окружения по образцу из файла .env.sample (по умолчанию в
  системе
  используется база данных PostgreSQL)
- Запустите миграции
```shell
python manage.py migrate
```
- Создайте Суперпользователя, командой
```shell
python manage.py csu
```
- Создайте группу менеджеров с необходимыми разрешениями, командой 
```shell
python manage.py cgm
```
- Установите и запустите сервер redis.

<a id="title2">Логика работы системы</a>
---
После создания новой рассылки, если текущее время больше или равно времени начала,  
выбираются из справочника все клиенты, которые указаны в настройках рассылки,  
и запускается отправка для всех этих клиентов.  

Если создается рассылка со временем старта в будущем, то отправка  
стартует автоматически по наступлению этого времени без дополнительных действий со стороны пользователя системы.  
По ходу отправки сообщений собирается статистика по каждой рассылке для последующего формирования отчетов.

<a id="title3">Права доступа</a>
---

- Для незарегистрированного пользователя открыт доступ только к главной странице и зарыт весь функционал системы  
  за исключением страницы регистрации и страницы авторизации.
- Каждый авторизованный пользователь имеет доступ только к своим клиентам, сообщениям, рассылкам и отчету о своих
  проведенных рассылках.
- Персонал может просматривать списки всех клиентов, сообщений, рассылок, пользователей сервиса и имеет доступ к отчету
  о всех проведенных рассылках.
- Чтобы добавить пользователя в группу менеджеров, в административной панели установите ему статус персонала  
и в разделе групп, выберите группу "manager".

<a id="title4">Запуск</a>
---

- Для запуска приложения, используйте команду 
```shell
python manage.py runserver
```
- Для запуска работы сервиса по расписанию, используйте команду
```shell
python manage.py runapscheduler
```
- Для запуска сервиса вручную, используйте команду
```shell
python manage.py run_mailings
```