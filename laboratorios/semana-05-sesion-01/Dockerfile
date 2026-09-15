FROM python:3.9-slim
WORKDIR /app
COPY requirements.py .
RUN pip install requirements.txt
COPY ..
CMD ["python", "test_singleton.py"]