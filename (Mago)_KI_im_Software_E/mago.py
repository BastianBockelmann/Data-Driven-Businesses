import pandas as pd
import altair as alt
import os

# Den Pfad zur CSV-Datei definieren (angenommen, sie liegt im 'data'-Ordner des Projekts)
csv_file_path = os.path.join(os.getcwd(), 'data', 'Dataset.csv')

# CSV-Datei einlesen
df = pd.read_csv(csv_file_path)