# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết (nếu có, ví dụ build-essential cho một số lib)
# RUN apt-get update && apt-get install -y ...

# Copy và cài đặt requirements trước để tận dụng Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào
COPY ./app /app