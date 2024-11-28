import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

# Den Pfad zur CSV-Datei definieren (angenommen, sie liegt im 'data'-Ordner des Projekts)
csv_file_path = os.path.join(os.getcwd(), 'data', 'Transactions_on_SE_1994-2024.csv')

# CSV-Datei einlesen
df = pd.read_csv(csv_file_path)

# Aufteilen der Autoren-Spalte für Einträge mit mehreren Autoren, die durch ";" getrennt sind
df['Authors'] = df['Authors'].str.split(';')
df_exploded = df.dropna(subset=['Authors']).copy()

# Erstellen des Graphen
G = nx.Graph()

# Hinzufügen von Knoten und Kanten basierend auf Co-Autorenschaft
for authors in df['Authors']:
    if isinstance(authors, list) and len(authors) > 1:  # Nur Publikationen mit mehr als einem Autor
        authors = [author.strip() for author in authors if pd.notna(author)]
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                G.add_edge(authors[i], authors[j])

# Entfernen von isolierten Knoten (Autoren ohne Co-Autoren)
G = G.subgraph([node for node in G if G.degree(node) > 0]).copy()

# Berechnung der Netzwerkmetriken
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)

# Zusammenstellen der Ergebnisse in einem DataFrame
metrics_df = pd.DataFrame({
    'Author': list(G.nodes()),
    'Degree Centrality': [degree_centrality[author] for author in G.nodes()],
    'Betweenness Centrality': [betweenness_centrality[author] for author in G.nodes()],
    'Closeness Centrality': [closeness_centrality[author] for author in G.nodes()],
    'Eigenvector Centrality': [eigenvector_centrality[author] for author in G.nodes()]
})

# Sortieren nach Degree Centrality, um die wichtigsten Autoren anzuzeigen
metrics_df = metrics_df.sort_values(by='Degree Centrality', ascending=False)

# Ausgabe der Top-Autoren nach Degree Centrality
print("Top-Autoren nach Netzwerkmetriken:")
print(metrics_df.head(10))

# Interaktive Visualisierung des Netzwerks mit PyVis
net = Network(notebook=False, width="1000px", height="800px")
net.from_nx(G)

# Speichern der Netzwerkvisualisierung als HTML-Datei
output_path = os.path.join(os.getcwd(), "(Lea)_Autoren\\Co-author_network.html")
net.save_graph(output_path)

print(f"Das Netzwerk wurde gespeichert und kann unter '{output_path}' angezeigt werden.")
