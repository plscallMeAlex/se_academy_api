FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["bash", "-c", "alembic revision --autogenerate -m 'Initialize migration' && alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
