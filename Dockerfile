FROM python:3.10.8

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "-it", "fastapi_app.main:app"]
