FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn pydantic openai requests python-dotenv

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]