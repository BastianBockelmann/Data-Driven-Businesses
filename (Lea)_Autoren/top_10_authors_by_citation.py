import pandas as pd
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

# Gruppieren der Zitationen pro Autor und Berechnung der Gesamtzitationen
total_citations_per_author = df_exploded.groupby('Authors')['Article Citation Count'].sum().reset_index()

# Sortieren nach Zitationen und Auswahl der Top 10 Autoren
top_10_authors_by_citations = total_citations_per_author.sort_values(by='Article Citation Count', ascending=False).head(10)

# Ausgabe der Top 10 Autoren mit der Gesamtzitationsanzahl
print("Die Top 10 Autoren nach Gesamtzitationen:")
print(top_10_authors_by_citations)

# Balkendiagramm erstellen
bars = alt.Chart(top_10_authors_by_citations).mark_bar(color='slategrey', size=30).encode(
    x=alt.X('Article Citation Count:Q', title='Gesamtanzahl der Zitationen'),
    y=alt.Y('Authors:N', sort='-x', title='Autor(en)')
).properties(
    title='Top 10 Autoren nach Gesamtzitationen',
    width=600,
    height=400
)

# Text am Ende jedes Balkens anzeigen
text = bars.mark_text(
    align='left',       # Text linksbündig ausrichten
    baseline='middle',  # Vertikal in der Mitte des Balkens
    dx=5,               # Leichter Abstand vom Ende des Balkens
    fontSize=10,
    color='black'       # Schwarze Schriftfarbe
).encode(
    text='Article Citation Count:Q'  # Gesamtzitationsanzahl am Ende des Balkens anzeigen
)

# Kombinieren des Diagramms (Balken und Text am Ende)
chart = bars + text

# Speichern des Diagramms als HTML-Datei
chart.save('(Lea)_Autoren\\top_10_authors_by_citations.html')
