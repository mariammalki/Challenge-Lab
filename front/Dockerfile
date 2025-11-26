# Utiliser Python slim
FROM python:3.12-slim

# Travailler dans /app
WORKDIR /app

# Copier requirements et installer
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Exposer le port du frontend
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
