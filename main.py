from fastapi import FastAPI, Query
import korrelationsanalyse
import webcrawler
import csvEinlesen
import assoziationsanalyse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/korrelationsanalyse")
async def perform_korrelationsanalyse():
    # Führen Sie die Korrelationsanalyse durch
    result = korrelationsanalyse.perform_korrelationsanalyse()

    # Hier können Sie das Ergebnis anpassen und zurückgeben
    return {"result": result}


@app.get("/assoziationsanalyse")
async def perform_assoziationsanalyse(seed_movie: str = Query(...)):
    # Generiere Vorhersagen für den Seed-Film
    predictions = assoziationsanalyse.generate_predictions(seed_movie)

    if predictions:
        # Wenn Vorhersagen gefunden wurden
        response = {
            "message": "Kunden die den Film '{}' gesehen haben, schauen bestimmt auch:".format(seed_movie),
            "predictions": predictions
        }
    else:
        # Wenn keine Vorhersagen gefunden wurden
        response = {
            "message": "Kunden, die den Film '{}' gesehen haben, konnten wir keine weiteren Empfehlungen finden.".format(seed_movie)
        }

    return response