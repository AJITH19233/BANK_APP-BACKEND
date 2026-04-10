FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "banking.wsgi:application", "--bind", "0.0.0.0:8000"]
