# Usa una imagen base de Python
FROM python:3.12-slim

# Instala las dependencias necesarias para Chrome y chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator1 \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libcurl4 \
    libvulkan1 \
    xdg-utils \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

ENV TZ=America/Santiago

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN dpkg -i google-chrome-stable_current_amd64.deb

RUN apt-get -fy install


# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu aplicación al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt


# Exponer el puerto
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app", "--timeout", "120", "--workers", "2"]