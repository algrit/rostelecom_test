git clone https://github.com/algrit/rostelecom_test.git

Устанавливаем poetry:
curl -sSL https://install.python-poetry.org | python3 -

В проекте устанавливаем зависимости,
активируем виртуальное окружение(если надо):
poetry install --no-root
source $(poetry env info --path)/bin/activate

Сервис-заглушка из задания:
python stub_service/stub_service.py

Запускаем докер контейнеры RabbitMQ (1 для работы, 1 тестовый):
docker-compose up -d

Запускаем основное приложение:
python src/main.py

АПИ ручки по адресу:
http://localhost:8000/docs#/

При обращении к ручке "params_input" в очередь conf_task_queue помещается необходимая таска.

В соседнем терминале запускаем Консюмера (мок сервиса А):
python src/mock_service_a.py

Консюмер обрабатывает задачу и в ответную очередь task_status_queue помещает статус таски

Ручка "params_check" проверяет ответную очередь task_status_queue и меняет статус
задачи в in_memory_db


#--------------------------------------------------------
Для тестов:

запускаем Консюмера (мок сервиса А):
python tests/mock_service_a.py

Запускаем тесты:
pytest -l -s