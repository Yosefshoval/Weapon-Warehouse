FROM python:3.11-slim

WORKDIR /app

COPY ./app/requerements.txt .

RUN pip install -r requerements.txt

COPY ./app .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]