
#Welche Newcomer haben in den letzten Jahren an Einfluss im Software-Engineering gewonnen, und wie entwickeln sich ihre Karrieren über die Zeit?

#Voraussetzung: Anzahl der Zitationen -> Forschungsfrage 1. Top 10 Paper
#Beispiel für die Auswertung: Ermittlung von Forschern, die in den letzten 5–10 Jahren stark an Einfluss gewonnen haben. K
#riterien könnten sein: Anzahl der Zitationen, wachsende Publikationsrate und Innovationskraft. Dabei kann untersucht werden, ob diese Forscher 
#dauerhaft aktiv bleiben ("Dauerbrenner") oder nach kurzer Zeit wieder verschwinden ("Eintagsfliegen").
import pandas as pd
import numpy as np
import altair as alt
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

# Visualisierung mit Altair
chart = alt.Chart(top_10_works).mark_bar(color='lightcoral').encode(
    x=alt.X('Article Citation Count:Q', title='Zitationsanzahl'),
    y=alt.Y('Authors:N', sort='-x', title='Autor(en)')
).properties(
    title='Top 10 bekannteste Werke nach Zitationen',
    width=600,
    height=400
)

# Speichern des Diagramms als HTML-Datei
chart.save('(Lea)_Autoren\\top_10_works.html')
