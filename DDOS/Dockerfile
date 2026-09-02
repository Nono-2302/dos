FROM python:3.10-slim
RUN pip install --no-cache-dir requests
WORKDIR /app
COPY attack.py .
CMD ["python", "attack.py"]
