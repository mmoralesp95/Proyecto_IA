# Usa la imagen oficial de Python como base
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias al contenedor
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente de la aplicación al contenedor
COPY . .

# Expón el puerto 5000 (el que usa Flask por defecto)
EXPOSE 5000

# Comando para ejecutar la aplicación Flask desde run.py
CMD ["python", "run.py"]
