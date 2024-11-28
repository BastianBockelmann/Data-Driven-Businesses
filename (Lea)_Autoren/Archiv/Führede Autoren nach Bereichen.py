#Welche Autoren sind die führenden Forscher für spezifische Themen im Software-Engineering?

#Voraussetzung: Input aus Themen -> Forschungsfrage: 4
#Beispiel für die Auswertung: Verknüpfung von Themen mit den dazu führenden Autoren durch Textmining-Techniken. 
# Ein bestimmtes Thema wie "Continuous Integration" oder "Microservices" wird analysiert, um die am meisten publizierenden und zitierten Autoren in 
# diesem Bereich zu identifizieren.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Den Pfad zur CSV-Datei definieren (angenommen, sie liegt im 'data'-Ordner des Projekts)
csv_file_path = os.path.join(os.getcwd(), 'data', 'test_dataset.csv')

# CSV-Datei einlesen
df = pd.read_csv(csv_file_path)

# Aufteilen der Autoren-Spalte für Einträge mit mehreren Autoren, die durch ";" getrennt sind
df_exploded = df.dropna(subset=['Authors']).copy()
df_exploded['Authors'] = df_exploded['Authors'].str.split(';')
df_exploded = df_exploded.explode('Authors')
df_exploded['Authors'] = df_exploded['Authors'].str.strip()

# 1. Die 10 bekanntesten Werke nach Zitationen ermitteln
top_10_works = df.sort_values(by='Article Citation Count', ascending=False).head(10)
top_10_works = top_10_works[['Authors', 'Article Citation Count']]

# Ausgabe der Top-10-Werke mit den Autoren und Zitationsanzahl
print("Die Autoren der 10 bekanntesten Werke nach Zitationen:")
print(top_10_works)

# Visualisierung der Top-10-Werke
plt.figure(figsize=(10, 6))
sns.barplot(data=top_10_works, x='Article Citation Count', y='Authors', color='lightcoral')
plt.title('Top 10 bekannteste Werke nach Zitationen')
plt.xlabel('Zitationsanzahl')
plt.ylabel('Autor(en)')
plt.show()
