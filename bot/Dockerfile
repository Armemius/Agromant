FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .

RUN apt-get update -y && apt-get install build-essential g++ libgl1-mesa-glx libglib2.0-0 -y
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8443
ENTRYPOINT ["python", "main.py"]
