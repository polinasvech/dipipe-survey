1. Создать .env файлы по шаблону и заполнить данные
```commandline
cp app_manager/app/config/.env.template app_manager/app/config/.env
cp app_client/app/config/.env.template app_client/app/config/.env
```

2. В папку app_manager/app/data положить недостающие файлы

3. Выполнить
```commandline
docker compose up --build
```

4. Когда все контейнеры поднимутся, необходимо выполнить следующие шаги для заполнения БД данными из excel:

   1. Находим id контейнера app_manager с помощью
      ```
      docker ps
      ```
   
   2. Подключаемся к контейнеру
      ```
      docker exec -it <conteiner_id> bash
      ```
   
   3. Внутри контейнера выполняем
      ```
      chmod +x parse_excel.sh
      ./parse_excel.sh
      exit
      ```

- Swagger доступен по http://localhost:8002/api/openapi#/
- Интерфейс pgadmin доступен по http://localhost:5050/