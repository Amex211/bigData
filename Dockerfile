# Verwende das offizielle Python-Base-Image
FROM python:3.9

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Projektanforderungen in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere die Projektabhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Projektinhalt in das Arbeitsverzeichnis
COPY . .

# Exponiere den Port, auf dem die FastAPI-Anwendung ausgeführt wird (Standardmäßig 8000)
EXPOSE 8000

# Starte die FastAPI-Anwendung
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]