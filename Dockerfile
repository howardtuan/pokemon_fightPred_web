# 使用 python:3.10-slim-buster 作為基礎映像檔
FROM python:3.10-slim-buster

# 安裝系統級依賴項
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libhdf5-dev

# 設置工作目錄
WORKDIR /app

# 複製當前目錄下的所有文件到映像檔中的 /app 目錄
COPY . .

# 安裝應用程序所需的依賴
RUN pip install --no-cache-dir -r requirements.txt

# 暴露應用程序使用的埠
EXPOSE 5000

# 使用 Gunicorn 運行 Flask 應用程序
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

