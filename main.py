import requests
import pandas as pd
import time

#10	Calls per second
#200	Calls per day

# Dein IEEE Xplore API-Schlüssel
API_KEY = 'rm72u3q4x5ct6wft3mnbeuyp'

# Der Suchstring
SEARCH_QUERY = '("All Metadata": Software Engineering AND year_range:1994_2024)'

# Basis-URL für die API
BASE_URL = 'http://ieeexploreapi.ieee.org/api/v1/search/articles'

# Anfrageparameter
PARAMS = {
    'apikey': API_KEY,
    'querytext': SEARCH_QUERY,
    'max_records': 100,  # Die API erlaubt bis zu 100 Datensätze pro Anfrage
    'start_record': 1,
    'format': 'json'
}

# Funktion zum Abrufen der Daten von der API
def fetch_results():
    all_results = []
    current_record = 1
    total_records = 100  # Platzhalterwert für die erste Anfrage

    while current_record <= total_records:
        PARAMS['start_record'] = current_record
        response = requests.get(BASE_URL, params=PARAMS)
        
        if response.status_code == 200:
            data = response.json()
            total_records = data.get('total_records', 0)
            articles = data.get('articles', [])
            all_results.extend(articles)

            # Zeige Fortschritt an
            print(f"Fetched {len(all_results)} of {total_records} records...")

            # Setze den Startrekord für die nächste Anfrage
            current_record += len(articles)

            # Wartezeit zwischen Anfragen, um API-Rate-Limits zu vermeiden
            time.sleep(1)
        else:
            print(f"Fehler bei Anfrage: {response.status_code}")
            break

    return all_results

# Funktion zum Speichern der Ergebnisse in einer CSV-Datei
def save_to_csv(results, filename='software_30_years.csv'):
    if results:
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False)
        print(f"Ergebnisse wurden in {filename} gespeichert.")
    else:
        print("Keine Ergebnisse zum Speichern vorhanden.")

# Hauptfunktion
def main():
    print("Daten werden abgerufen...")
    results = fetch_results()
    save_to_csv(results)

if __name__ == "__main__":
    main()
