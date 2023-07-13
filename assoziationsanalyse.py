import pymysql
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Verbindung zur MySQL-Datenbank herstellen
connection = pymysql.connect(
    host='some-mysql',
    user='root',
    port=3306,
    password='',
    database='kundenrezensionen'
)

# SQL-Abfrage zum Abrufen der Kundendaten
query = "SELECT ErsterFilm, ZweiterFilm, DritterFilm, VierterFilm, FuenfterFilm, SechsterFilm, SiebterFilm, AchterFilm FROM csv"

# Daten aus der Datenbank abrufen und in eine Liste von Transaktionen konvertieren
cursor = connection.cursor()
cursor.execute(query)
rows = cursor.fetchall()

transactions = []
for row in rows:
    transaction = [str(item) for item in row if item != False]
    transactions.append(transaction)

# Schließe die Verbindung zur Datenbank
cursor.close()
connection.close()

# Konvertiere die Transaktionsdaten in ein Dataframe mit One-Hot-Encoding
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)

# Führe die Assoziationsanalyse durch
frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)


# Funktion zur Generierung von Vorhersagen für einen Film
def generate_predictions(seed_movie):
    # Filtere die Assoziationsregeln für den Seed-Film
    filtered_rules = rules[rules['antecedents'].apply(lambda x: seed_movie in x)]

    # Überprüfe, ob Vorhersagen vorhanden sind
    if not filtered_rules.empty:
        # Sortiere die Regeln basierend auf der Confidence oder Lift
        sorted_rules = filtered_rules.sort_values(by='confidence', ascending=False)

        # Erhalte die Vorhersagen (Konsequenzen) aus den am besten bewerteten Regeln
        predictions = sorted_rules['consequents'].explode().unique()

        return predictions.tolist()
    else:
        return []
