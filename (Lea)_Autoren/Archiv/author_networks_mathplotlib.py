import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# Den Pfad zur CSV-Datei definieren (angenommen, sie liegt im 'data'-Ordner des Projekts)
csv_file_path = os.path.join(os.getcwd(), 'data', 'test_dataset.csv')

# CSV-Datei einlesen
df = pd.read_csv(csv_file_path)

# Aufteilen der Autoren-Spalte für Einträge mit mehreren Autoren, die durch ";" getrennt sind
df['Authors'] = df['Authors'].str.split(';')
df_exploded = df.explode('Authors')
df_exploded['Authors'] = df_exploded['Authors'].str.strip()
df_exploded = df_exploded.dropna(subset=['Authors'])

# Erstellen des Graphen für alle Autoren, die mindestens mit einem weiteren zusammengearbeitet haben
G = nx.Graph()

# Hinzufügen von Knoten und Kanten basierend auf Co-Autorenschaft, nur wenn mindestens zwei Autoren beteiligt sind
for authors in df['Authors']:
    if isinstance(authors, list) and len(authors) > 1:  # Nur Publikationen mit mehr als einem Autor
        authors = [author.strip() for author in authors if pd.notna(author)]
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                G.add_edge(authors[i], authors[j])

# Überprüfen, ob der Graph leer ist
if len(G) == 0:
    print("Der Graph enthält keine Verbindungen zwischen Autoren mit Co-Autorenschaften.")
else:
    # Berechnung der Netzwerkmetriken für das gefilterte Netzwerk
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

    # Visualisierung des Netzwerks mit Matplotlib
    plt.figure(figsize=(14, 14))
    pos = nx.spring_layout(G, k=0.1, seed=42)  # Spring-Layout für bessere Übersicht

    # Zeichnen der Knoten mit Größe basierend auf Degree Centrality
    node_sizes = [1000 * degree_centrality[node] for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue", alpha=0.7)

    # Zeichnen der Kanten
    nx.draw_networkx_edges(G, pos, alpha=0.5)

    # Zeichnen der Knotenlabels
    nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

    # Titel und Anzeige des Graphen
    plt.title("Autoren-Netzwerk basierend auf Co-Autorenschaften (nur Autoren mit mindestens einem Co-Autor)")
    plt.show()
