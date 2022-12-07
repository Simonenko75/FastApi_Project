FROM python:3.10.8

#ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 8080

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8080"]