import pandas as pd
import altair as alt
import os

# Den Pfad zur CSV-Datei definieren (angenommen, sie liegt im 'data'-Ordner des Projekts)
csv_file_path = os.path.join(os.getcwd(), 'data', 'Transactions_on_SE_1994-2024.csv')

# CSV-Datei einlesen
df = pd.read_csv(csv_file_path)

# Aufteilen der Autoren-Spalte für Einträge mit mehreren Autoren, die durch ";" getrennt sind
df['Authors'] = df['Authors'].str.split(';')
df_exploded = df.explode('Authors')
df_exploded['Authors'] = df_exploded['Authors'].str.strip()

# Die 10 bekanntesten Werke nach Zitationen ermitteln
top_10_works = df.sort_values(by='Article Citation Count', ascending=False).head(10)

# Gruppieren der Autoren für jedes Werk
top_10_works['Authors'] = top_10_works['Authors'].apply(lambda authors: ', '.join(authors))
top_10_works = top_10_works[['Document Title', 'Authors', 'Article Citation Count']]

# Balkendiagramm erstellen
bars = alt.Chart(top_10_works).mark_bar(color='slategrey', size=30).encode(
    x=alt.X('Article Citation Count:Q', title='Zitationsanzahl'),
    y=alt.Y('Authors:N', sort='-x', title='Autor(en)')
).properties(
    width=600,
    height=400
)

# Textanzeige für die Anzahl der Zitationen neben dem Balken hinzufügen
text = bars.mark_text(
    align='left',  # Text linksbündig anzeigen
    dx=3,  # Abstand vom Balken
    fontSize=12
).encode(
    text='Article Citation Count:Q'  # Zitationsanzahl als Text
)

# Diagramm kombinieren
chart = bars + text

# Speichern des Diagramms als HTML-Datei
output_path = os.path.join(os.getcwd(), "(Lea)_Autoren\\top_10_authors_by_cited_works.html")
chart.save(output_path)

print(f"Das Diagramm wurde gespeichert und kann unter '{output_path}' angezeigt werden.")
