# Usa una imagen oficial de Python como base
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias al contenedor
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Descarga los datos necesarios para el backtest dentro del contenedor
# Esto evita tener que montar volúmenes solo para los datos de entrada
RUN python -c "import yfinance as yf; yf.download('ORCL', start='2000-01-01', end='2000-12-31').to_csv('oracle.csv')"

# Copia el resto del código de tu aplicación al directorio de trabajo
COPY . .

# Comando que se ejecutará cuando el contenedor se inicie
CMD ["python", "mi_estrategia.py"]