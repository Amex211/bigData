import pandas as pd
import pymysql
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def perform_korrelationsanalyse():
    # Verbindung zur MySQL-Datenbank herstellen
    connection = pymysql.connect(
        host='some-mysql',
        user='root',
        port=3306,
        password='',
        database='kundenrezensionen'
    )

    # SQL-Abfrage zum Abrufen der gewünschten Spalten
    query = "SELECT `Alter`, Aktivitätsindex, Geschlecht, AnzahlFilme FROM csv"

    # Daten aus der Datenbank abrufen und in ein DataFrame laden
    df = pd.read_sql(query, connection)

    # Korrelationsmatrix berechnen
    correlation_matrix = df.corr()

    # Korrelationsmatrix zurückgeben
    return correlation_matrix

# Test der Funktion
result = perform_korrelationsanalyse()
print("Korrelationsmatrix:")
print(result)
