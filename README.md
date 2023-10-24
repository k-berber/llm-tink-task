# llm-tink-task
Веб-сервис, который по базе знаний умеет отвечать на вопросы пользователя

Для успешного запуска нужно положить файл llm-модели в диркеторию /app.

Собрать образ докера: docker build -t llm_username:v1 .
Запустить приложение: docker run -p 8080:8080 llm_username:v1

Проверить работоспособность приложения: pytest tests.py (запускать из корня проекта)

<img width="1204" alt="Снимок экрана 2023-10-25 в 01 53 08" src="https://github.com/k-berber/llm-tink-task/assets/62189074/e4e6cf98-a91d-49b4-90d4-1364e4820a35">

<img width="1208" alt="Снимок экрана 2023-10-25 в 02 06 27" src="https://github.com/k-berber/llm-tink-task/assets/62189074/2702db03-4fcb-41a8-a3eb-ae60b86f8bd6">


