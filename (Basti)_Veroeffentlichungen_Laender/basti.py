import pandas as pd
import os

# Den Pfad zur CSV-Datei definieren (angenommen, sie liegt im 'data'-Ordner deines Projekts)
csv_file_path = os.path.join(os.getcwd(), 'data', 'test_dataset.csv')

# CSV-Datei einlesen
df = pd.read_csv(csv_file_path)

# Ausgabe der ersten Zeilen zur Überprüfung
print(df.head())

# In welchen Ländern und Sprachen wurde in den letzten Jahren am meisten veröffentlicht und wie entwickelt sich der Trend?



# Welche 5 Länder sind Spitzenreiter in der Forschung?



# Universitäten (Verteilung)



# Authoren arbeiten zusammen über grenzen hinweg


