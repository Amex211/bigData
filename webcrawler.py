import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By


def perform_webcrawler():
    # Establish a connection to the MySQL database
    db = pymysql.connect(
        host='some-mysql',
        user='root',
        port= 3306,
        password='',
        database='kundenrezensionen'
    )

    # Cursor erstellen
    cursor = db.cursor()

    # Tabellen erstellen (falls sie noch nicht vorhanden ist)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS bewertungen (
        id INT AUTO_INCREMENT PRIMARY KEY,
        anzahl_bewertungen DECIMAL(10, 3),
        five_stars VARCHAR(50),
        four_stars VARCHAR(50),
        three_stars VARCHAR(50),
        two_stars VARCHAR(50),
        one_star VARCHAR(50)
    )
    """
    cursor.execute(create_table_query)

    browser = webdriver.Chrome()

    JamesBond = "https://www.amazon.de/Sterben-Blu-Ray-Untertitel-Deutsch-Englisch/dp/B09HFS96KL"
    TheBatman = "https://www.amazon.de/Batman-Robert-Pattinson/dp/B09TN1CLRF"
    Titanic = "https://www.amazon.de/Titanic-Blu-ray-Leonardo-DiCaprio/dp/B0087WU3YG"
    arr = [JamesBond, TheBatman, Titanic]
    for x in arr:
        browser.get(x)
        anzahlBewertungen = browser.find_element(By.XPATH, "(//div[@class='a-row a-spacing-medium averageStarRatingNumerical'])[1]")
        anzahlBewertungen = anzahlBewertungen.text.split()[0]
        fiveStars = browser.find_element(By.XPATH, "(//td[@class='a-text-right a-nowrap'])[1]")
        fourStars = browser.find_element(By.XPATH, "(//td[@class='a-text-right a-nowrap'])[2]")
        threeStars = browser.find_element(By.XPATH, "(//td[@class='a-text-right a-nowrap'])[3]")
        twoStars = browser.find_element(By.XPATH, "(//td[@class='a-text-right a-nowrap'])[4]")
        oneStar = browser.find_element(By.XPATH, "(//td[@class='a-text-right a-nowrap'])[5]")
        print("--------------------------------")
        print(anzahlBewertungen)
        print(fiveStars.text)
        print(fourStars.text)
        print(threeStars.text)
        print(twoStars.text)
        print(oneStar.text)
        # Daten in die Tabelle einfügen
        insert_query = "INSERT INTO bewertungen (anzahl_bewertungen, five_stars, four_stars, three_stars, two_stars, one_star) VALUES (%s, %s, %s, %s, %s, %s)"
        # Daten in die Tabelle einfügen

        data = (anzahlBewertungen, fiveStars.text, fourStars.text, threeStars.text, twoStars.text, oneStar.text)
        cursor.execute(insert_query, data)
        db.commit()

    # Verbindung schließen
    db.close()
    print("------------------------------------------")
