# Top 10 Autoren nach Bekanntesten Werk (laut Zitationen)
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
# Sortiere nach Zitationen und wähle die obersten 10 Werke (Originaldaten ohne explodierte Autoren)
top_10_works = df.sort_values(by='Article Citation Count', ascending=False).head(10)

# Filtere das explodierte DataFrame basierend auf den Titeln der Top 10 Werke
top_10_authors_expanded = df_exploded[df_exploded['Document Title'].isin(top_10_works['Document Title'])]
top_10_authors_expanded = top_10_authors_expanded[['Authors', 'Article Citation Count']]

# Ausgabe der Top-10-Werke mit den Autoren und Zitationsanzahl
print("Die Autoren der 10 bekanntesten Werke nach Zitationen:")
print(top_10_authors_expanded)

# Visualisierung mit Altair
chart = alt.Chart(top_10_authors_expanded).mark_bar(color='lightcoral').encode(
    x=alt.X('Article Citation Count:Q', title='Zitationsanzahl'),
    y=alt.Y('Authors:N', sort='-x', title='Autor(en)')
).properties(
    title='Top 10 Autoren nach bekanntesten Werken (laut Zitationen)',
    width=600,
    height=400
)

# Speichern des Diagramms als HTML-Datei
chart.save('(Lea)_Autoren\\top_10_works.html')
