import csv
import pymysql



# verbindungsdetails
connection = pymysql.connect(
    host='some-mysql',
    user='root',
    port=3306,
    password='',
    database='kundenrezensionen'
)

# Erstelle den cursor
cursor = connection.cursor()

# Erstelle csv wenn nicht existen tabelle in DB
create_table_query = '''
    CREATE TABLE IF NOT EXISTS csv (
        Kundennummer INT PRIMARY KEY,
        AccountErstellung DATE,
        `Alter` INT,
        Geschlecht INT,
        PLZ INT,
        MonatlicherUmsatz FLOAT,
        Rabatt FLOAT,
        Aktivitätsindex FLOAT,
        ErsterFilm VARCHAR(50),
        ZweiterFilm VARCHAR(50),
        DritterFilm VARCHAR(50),
        VierterFilm VARCHAR(50),
        FuenfterFilm VARCHAR(50),
        SechsterFilm VARCHAR(50),
        SiebterFilm VARCHAR(50),
        AchterFilm VARCHAR(50),
        AnzahlFilme INT
    )
'''
cursor.execute(create_table_query)


with open('recommend.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file, delimiter=';')

    #Überspringe Titel
    next(reader)

    existing_kundennummers = set()
    # Iterate über die CSV
    for row in reader:
        # Speichere jede Zeile in eine Variable
        kundennummer = int(row[0])
        account_erstellung = row[1]
        alter = int(row[2]) if row[2] else None
        geschlecht = row[3]
        plz = int(row[4]) if row[4] else None
        umsatz = float(row[5].replace(',', '.')) if row[5] else None
        rabatt = float(row[6].replace(',', '.')) if row[6] else None
        aktivitaetsindex = float(row[7].replace(',', '.')) if row[7] else None
        erster_film = row[8]
        zweiter_film = row[9]
        dritter_film = row[10]
        vierter_film = row[11]
        fuenfter_film = row[12]
        sechster_film = row[13]
        siebter_film = row[14]
        achter_film = row[15]

        anzahl_filme = sum(1 for film in [erster_film, zweiter_film, dritter_film, vierter_film,
                                         fuenfter_film, sechster_film, siebter_film, achter_film] if film)

        if kundennummer in existing_kundennummers:
            print("Überspringe duplikat Kunde mit Kundennummer " + str(kundennummer) + ".")
            continue
        if any(value is None for value in [alter, plz, umsatz, rabatt, aktivitaetsindex]):
            print("Überspringe missing values gefunden für Kundennummer " + str(kundennummer) + ".")
            continue
        if alter < 18 or alter > 45:
            print("Überspringe Kundennummer " + str(kundennummer) + " wegen alter.")
            continue


        if geschlecht == 'männlich':
            geschlecht = 0
        elif geschlecht == 'weiblich':
            geschlecht = 1
        else:
            geschlecht = None

        # SQL query um alles einzufügen
        insert_query = "INSERT IGNORE INTO csv (Kundennummer, AccountErstellung, `Alter`, Geschlecht, PLZ, " \
                       "MonatlicherUmsatz, Rabatt, Aktivitätsindex, ErsterFilm, ZweiterFilm, DritterFilm, " \
                       "VierterFilm, FuenfterFilm, SechsterFilm, SiebterFilm, AchterFilm, AnzahlFilme) " \
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # füge alles ein
        cursor.execute(insert_query, (kundennummer, account_erstellung, alter, geschlecht, plz, umsatz, rabatt,
                                      aktivitaetsindex, erster_film, zweiter_film, dritter_film, vierter_film,
                                      fuenfter_film, sechster_film, siebter_film, achter_film, anzahl_filme))


        existing_kundennummers.add(kundennummer)

# Commit die änderungen in die Datenbank
connection.commit()

# Schließe die verbindung
cursor.close()
connection.close()
