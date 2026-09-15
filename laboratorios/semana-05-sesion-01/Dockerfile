FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install requirements.txt
COPY . .
CMD ["python", "test_singleton.py"]