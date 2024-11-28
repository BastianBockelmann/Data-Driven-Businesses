#Wer sind die weltweit aktivsten Autoren im Bereich Software-Engineering?

# Top 10 nach Zitationen
# Top 10 nach Publikationen
# Top 10 nach Publikationen und Zitationen
#
# Ausgabe einer Top-Liste 
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

# Berechnen der Zitations- und Publikationsanzahl pro Autor
unique_authors, indices = np.unique(df_exploded['Authors'], return_inverse=True)
publication_counts = np.bincount(indices)
citation_counts = np.nan_to_num(df_exploded['Article Citation Count'].values, nan=0)
total_citations = np.bincount(indices, weights=citation_counts)

# Zusammenführen der Ergebnisse in einem DataFrame und Konvertieren der Zitationen in Ganzzahlen
result_df = pd.DataFrame({
    'Authors': unique_authors,
    'publication_count': publication_counts,
    'total_citation_count': total_citations.astype(int)  # Zitationen als Ganzzahl formatieren
})

# 1. Top 10 Autoren nach Zitationen mit Publikationsanzahl
top_by_citations = result_df.sort_values(by='total_citation_count', ascending=False).head(10)
top_by_citations['Authors'] = top_by_citations.apply(
    lambda row: f"{row['Authors']} ({row['publication_count']} Publikationen)", axis=1)

# 2. Top 10 Autoren nach Publikationen mit Zitationsanzahl
top_by_publications = result_df.sort_values(by='publication_count', ascending=False).head(10)
top_by_publications['Authors'] = top_by_publications.apply(
    lambda row: f"{row['Authors']} ({row['total_citation_count']} Zitationen)", axis=1)

# Ausgabe der Ranglisten
print("Top 10 Autoren nach Zitationen (mit Anzahl der Publikationen):")
print(top_by_citations[['Authors', 'total_citation_count', 'publication_count']])

print("\nTop 10 Autoren nach Publikationen (mit Anzahl der Zitationen):")
print(top_by_publications[['Authors', 'publication_count', 'total_citation_count']])

# Einzelne Balkendiagramme mit normaler Breite
fig_width = 10  # Normale Breite für bessere Lesbarkeit

# Balkendiagramm: Top 10 nach Zitationen
plt.figure(figsize=(fig_width, 6))
sns.barplot(data=top_by_citations, x='total_citation_count', y='Authors', color='skyblue')
plt.title('Top 10 Autoren nach Zitationen (mit Anzahl der Publikationen)')
plt.xlabel('Zitationsanzahl')
plt.show()

# Balkendiagramm: Top 10 nach Publikationen
plt.figure(figsize=(fig_width, 6))
sns.barplot(data=top_by_publications, x='publication_count', y='Authors', color='salmon')
plt.title('Top 10 Autoren nach Publikationen (mit Anzahl der Zitationen)')
plt.xlabel('Publikationsanzahl')
plt.show()
