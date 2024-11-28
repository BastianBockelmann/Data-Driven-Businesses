import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

# Datei laden
file_path = 'Data/Transactions_on_SE_1994-2024.csv' 
data = pd.read_csv(file_path)

# **1. Zeitreihenanalyse: Anzahl der Artikel pro Jahr**
def plot_articles_per_year(data):
    if 'Publication Year' in data.columns:
        yearly_counts = data['Publication Year'].value_counts().sort_index()
        plt.figure(figsize=(10, 6))
        plt.plot(yearly_counts.index, yearly_counts.values, marker='o', linestyle='-', linewidth=2)
        plt.title("Anzahl der veröffentlichten Artikel pro Jahr", fontsize=16)
        plt.xlabel("Jahr", fontsize=12)
        plt.ylabel("Anzahl der Artikel", fontsize=12)
        plt.xticks(yearly_counts.index, rotation=45)
        plt.grid(visible=True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
    else:
        print("Spalte 'Publication Year' nicht gefunden.")

# **2. Top-Themen pro Jahrzehnt (Top 5 statt Top 10)**
def plot_top_words_by_decade(data):
    if 'Document Title' in data.columns and 'Publication Year' in data.columns:
        data['Decade'] = (data['Publication Year'] // 10) * 10
        all_decades = data['Decade'].dropna().unique()

        for decade in sorted(all_decades):
            titles = data[data['Decade'] == decade]['Document Title'].dropna().str.cat(sep=' ')
            words = [word.lower() for word in titles.split() if len(word) > 3]
            most_common = Counter(words).most_common(5)  # Top 5 statt Top 10

            words, counts = zip(*most_common)
            plt.figure(figsize=(10, 6))
            plt.bar(words, counts, color='skyblue', edgecolor='black')
            plt.title(f"Top 5 Begriffe in Artikel-Titeln der {int(decade)}er Jahre", fontsize=16)
            plt.xlabel("Wörter", fontsize=12)
            plt.ylabel("Häufigkeit", fontsize=12)
            plt.tight_layout()
            plt.show()
    else:
        print("Spalten 'Document Title' oder 'Publication Year' nicht gefunden.")

# **3. Aufkommende und abnehmende Trends**
def plot_trend_of_keywords(data, keywords):
    if 'Document Title' in data.columns and 'Publication Year' in data.columns:
        keyword_trends = {keyword: [] for keyword in keywords}
        years = sorted(data['Publication Year'].dropna().unique())

        for year in years:
            titles = data[data['Publication Year'] == year]['Document Title'].dropna().str.cat(sep=' ')
            for keyword in keywords:
                keyword_trends[keyword].append(titles.lower().count(keyword.lower()))

        plt.figure(figsize=(10, 6))
        for keyword, counts in keyword_trends.items():
            plt.plot(years, counts, marker='o', label=keyword, linewidth=2)
        plt.title("Trends von Schlüsselwörtern in Artikel-Titeln", fontsize=16)
        plt.xlabel("Jahr", fontsize=12)
        plt.ylabel("Häufigkeit", fontsize=12)
        plt.legend(title="Schlüsselwörter", fontsize=10)
        plt.grid(visible=True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
    else:
        print("Spalten 'Document Title' oder 'Publication Year' nicht gefunden.")

# **4. Clusteranalyse: Gruppierung von Themen**
def plot_cluster_analysis(data, num_clusters=5):
    if 'Document Title' in data.columns:
        # TF-IDF-Vektorisierung
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(data['Document Title'].dropna())

        # K-Means-Clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        clusters = kmeans.fit_predict(tfidf_matrix)

        # Daten mit Clustern verbinden
        data['Cluster'] = clusters

        # Cluster-Visualisierung
        cluster_counts = data['Cluster'].value_counts().sort_index()
        plt.figure(figsize=(10, 6))
        plt.bar(range(num_clusters), cluster_counts.values, color='lightgreen', edgecolor='black')
        plt.title("Verteilung der Artikel in Cluster", fontsize=16)
        plt.xlabel("Cluster", fontsize=12)
        plt.ylabel("Anzahl der Artikel", fontsize=12)
        plt.xticks(range(num_clusters))
        plt.tight_layout()
        plt.show()

        print("Top-Themen pro Cluster:")
        for cluster_id in range(num_clusters):
            titles = data[data['Cluster'] == cluster_id]['Document Title']
            print(f"\nCluster {cluster_id}:")
            print(titles.head(5).tolist())
    else:
        print("Spalte 'Document Title' nicht gefunden.")

# Funktionen ausführen
plot_articles_per_year(data)  # Zeitreihenanalyse
plot_top_words_by_decade(data)  # Top-Themen pro Jahrzehnt (Top 5)
plot_trend_of_keywords(data, keywords=["agile", "cloud", "machine learning"])  # Schlüsselwörter-Trends
plot_cluster_analysis(data, num_clusters=5)  # Clusteranalyse

