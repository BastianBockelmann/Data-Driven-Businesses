#Wer sind die weltweit aktivsten Autoren im Bereich Software-Engineering?

# Top 10 nach Zitationen
# Top 10 nach Publikationen
# Top 10 nach Publikationen und Zitationen
#
# Ausgabe einer Top-Liste 
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

# Sortiere das DataFrame basierend auf Zitationen und wähle die Top 10 Autoren basierend auf ihren meistzitierten Werken
top_authors_by_citations = df_exploded.groupby('Authors').agg({'Article Citation Count': 'sum'}).reset_index()
top_10_authors = top_authors_by_citations.sort_values(by='Article Citation Count', ascending=False).head(10)

# Ausgabe der Top-10-Autoren mit der Gesamtzitationsanzahl
print("Die Top 10 Autoren basierend auf ihren bekanntesten Werken nach Zitationen:")
print(top_10_authors)

# Visualisierung mit Altair
chart = alt.Chart(top_10_authors).mark_bar(color='lightcoral').encode(
    x=alt.X('Article Citation Count:Q', title='Zitationsanzahl'),
    y=alt.Y('Authors:N', sort='-x', title='Autor(en)')
).properties(
    title='Top 10 Autoren basierend auf ihren bekanntesten Werken nach Zitationen',
    width=600,
    height=400
)

# Speichern des Diagramms als HTML-Datei
chart.save('(Lea)_Autoren\\top_10_authors.html')
