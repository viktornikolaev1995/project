## Инструкция по развертыванию проекта

Склонировать репозиторий: 
```bash
git clone https://github.com/viktornikolaev1995/project.git
```

### Настройка проекта

Внесите при необходимости корректировки в переменные окружения, находящиеся в файле `.env`

### Сборка образов и запуск контейнеров

В корне репозитория выполните команду:

```bash
docker-compose up --build
```

При первом запуске данный процесс может занять несколько минут.

Миграции таблиц базы данных и загрузка фикстур выполняются bash скриптом.

При загрузке фикстур создается суперпользователь с логином: `SuperUser` и паролем: `s!_uerDFdaffsre`.

При необходимости создать своего суперпользователя в запущенном контейнере приложения воспользуетесь командой:

```bash
docker-compose exec app python manage.py createsuperuser
```

Проект доступен по адресу http://127.0.0.1:8000

### Для просмотра запущенных контейнеров

```bash
docker-compose ps
```

### Для просмотра списка образов

```bash
docker-compose images
```

### Для просмотра журнала сервисов

```bash
docker-compose logs -f app
```

### Остановка контейнеров

Для остановки контейнеров выполните команду:

```bash
docker-compose stop
```

### Остановка контейнеров с последующим их удалением

Для остановки и удаления контейнеров выполните команду:

```bash
docker-compose down
```
