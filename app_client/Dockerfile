FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# CMD ["gunicorn", "-b", "0.0.0.0:8001",  "main:app"]
CMD ["uvicorn", "main:asgi_app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
