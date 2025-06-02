FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .

RUN apt-get update -y

# Setup reverse proxy

RUN apt-get install nginx bash -y
COPY nginx.conf /etc/nginx/nginx.conf

# Setup bot

RUN apt-get install build-essential g++ libgl1-mesa-glx libglib2.0-0 -y
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Create wrapper script to run reverse proxy & telegram bot

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8080
ENTRYPOINT ["/start.sh"]
