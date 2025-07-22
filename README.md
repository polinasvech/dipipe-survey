1. Создать .env файлы по шаблону
```commandline
cp app_manager/app/config/.env.template app_manager/app/config/.env2
cp app_client/app/config/.env.template app_client/app/config/.env2
```

2. Заполнить данные

3. Выполнить
```commandline
docker compose up --build
```
