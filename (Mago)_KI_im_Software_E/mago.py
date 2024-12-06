import pandas as pd
import altair as alt
import os

# Den Pfad zur CSV-Datei definieren (angenommen, sie liegt im 'data'-Ordner des Projekts)
csv_file_path = os.path.join(os.getcwd(), 'data', 'Dataset.csv')

# CSV-Datei einlesen
df = pd.read_csv(csv_file_path)

# Zeige die ersten Zeilen des DataFrames an
print(df.head())

# Überblick über die Daten: Spaltennamen, Datentypen und Speicherplatz
print(df.info())

# Statistische Zusammenfassung der numerischen Daten
print(df.describe())

# Überprüfe, ob es fehlende Werte gibt
print(df.isnull().sum())
