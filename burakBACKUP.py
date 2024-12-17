#1. Zeitreihenanalyse der Themen
#Wie haben sich die verschiedenen Themen in der Softwareentwicklung über die letzten 30 Jahre zeitlich entwickelt, 
#und welche Trends lassen sich daraus ableiten?

#2. Top-Themen pro Jahrzehnt
#Welche Themen dominierten die Softwareentwicklung in den letzten drei Jahrzehnten, 
#und wie unterscheiden sich die Top-Themen in den Zeiträumen 1990–2000, 2000–2010 und 2010–2020?

#3. Aufkommende und abnehmende Trends
#Welche neuen Themen sind in den letzten drei Jahrzehnten in der Softwareentwicklung entstanden,
#und welche ehemals wichtigen Themen haben an Bedeutung verloren?

#4. Clusteranalyse
#Welche thematischen Cluster können in der Softwareentwicklung identifiziert werden, 
#und wie haben sich diese Cluster im Laufe der Zeit verändert?
# Top 10 häufigste Begriffe extrahieren

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns

# Datei laden
file_path = 'Data/Dataset.csv' 
data = pd.read_csv(file_path)

# **Häufigste Begriffe automatisch extrahieren**
def extract_top_keywords(data, n_keywords=3):
    if 'Document Title' in data.columns:
        titles = data['Document Title'].dropna()

        # CountVectorizer mit integrierten Stoppwörtern
        vectorizer = CountVectorizer(stop_words='english', max_features=1000)
        keyword_matrix = vectorizer.fit_transform(titles)

        # Häufigste Begriffe berechnen
        keywords = vectorizer.get_feature_names_out()
        keyword_counts = keyword_matrix.sum(axis=0).A1
        sorted_keywords = sorted(zip(keywords, keyword_counts), key=lambda x: x[1], reverse=True)

        # Nur die Top-n Schlüsselwörter zurückgeben
        top_keywords = [word for word, _ in sorted_keywords[:n_keywords]]

        # Begriffe und ihre Häufigkeiten ausgeben
        print("Top 3 Begriffe und ihre Häufigkeiten:")
        for word, count in sorted_keywords[:n_keywords]:
            print(f"{word}: {count}")

        return top_keywords
    else:
        print("Spalte 'Document Title' nicht gefunden.")
        return []

# **1. Detaillierte Trends analysieren**
def plot_detailed_trends(data, keywords):
    if 'Document Title' in data.columns and 'Publication Year' in data.columns:
        keyword_trends = {keyword: [] for keyword in keywords}
        years = sorted(data['Publication Year'].dropna().unique())

        for year in years:
            titles = data[data['Publication Year'] == year]['Document Title'].dropna().str.cat(sep=' ')
            for keyword in keywords:
                keyword_trends[keyword].append(titles.lower().count(keyword.lower()))

        plt.figure(figsize=(12, 6))
        for keyword, counts in keyword_trends.items():
            plt.plot(years, counts, marker='o', label=keyword, linewidth=2)

        # Beschriftungen auf der X-Achse: Nur jede zweite Jahreszahl anzeigen
        xticks = years[::2]  # Nur jedes zweite Jahr nehmen
        plt.xticks(ticks=xticks, labels=xticks, rotation=45)

        plt.title("Thementrends in der Softwareentwicklung (1994–2025)", fontsize=16)
        plt.xlabel("Jahr", fontsize=12)
        plt.ylabel("Anzahl der Erwähnungen", fontsize=12)
        plt.legend(title="Schlüsselwörter", fontsize=10)
        plt.grid(visible=True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
    else:
        print("Spalten 'Document Title' oder 'Publication Year' nicht gefunden.")

# **3. Heatmap für Begriffe pro Jahr**
def plot_keyword_heatmap(data, keywords):
    if 'Document Title' in data.columns and 'Publication Year' in data.columns:
        # Jahre extrahieren und sortieren
        years = sorted(data['Publication Year'].dropna().unique())
        keyword_counts = {year: [] for year in years}

        # Häufigkeit der Schlüsselwörter pro Jahr berechnen
        for year in years:
            titles = data[data['Publication Year'] == year]['Document Title'].dropna().str.cat(sep=' ')
            for keyword in keywords:
                keyword_counts[year].append(titles.lower().count(keyword.lower()))

        # DataFrame für die Heatmap erstellen
        heatmap_data = pd.DataFrame(keyword_counts, index=keywords).T.fillna(0)

        # Heatmap erstellen
        plt.figure(figsize=(14, 10))  # Größere Darstellung für mehr Übersicht
        sns.heatmap(
            heatmap_data,
            cmap="coolwarm",  # Farbschema
            annot=True,       # Werte in den Zellen anzeigen
            fmt=".0f",        # Ganze Zahlen anzeigen
            linewidths=.5,    # Trennlinien zwischen Zellen
            cbar_kws={'label': 'Häufigkeit'}  # Farbskalenbeschriftung
        )

        # Titel und Achsentitel hinzufügen
        plt.title("Häufigkeit von Schlüsselwörtern pro Jahr", fontsize=18)
        plt.xlabel("Schlüsselwörter", fontsize=14)
        plt.ylabel("Jahr", fontsize=14)
        plt.xticks(rotation=45, fontsize=12)  # Schlüsselwörter rotieren leicht
        plt.yticks(fontsize=12)  # Jahreswerte vergrößern
        plt.tight_layout()
        plt.show()
    else:
        print("Spalten 'Document Title' oder 'Publication Year' nicht gefunden.")

# **4. Aufkommende und abnehmende Begriffe analysieren**
def identify_emerging_declining_keywords(data, keywords):
    if 'Document Title' in data.columns and 'Publication Year' in data.columns:
        years = sorted(data['Publication Year'].dropna().unique())
        keyword_trends = {keyword: [] for keyword in keywords}

        for year in years:
            titles = data[data['Publication Year'] == year]['Document Title'].dropna().str.cat(sep=' ')
            for keyword in keywords:
                keyword_trends[keyword].append(titles.lower().count(keyword.lower()))

        for keyword, counts in keyword_trends.items():
            plt.figure(figsize=(10, 6))
            plt.plot(years, counts, marker='o', label=keyword, linewidth=2)

            # Beschriftungen auf der X-Achse: Nur jede zweite Jahreszahl anzeigen
            xticks = years[::2]  # Nur jedes zweite Jahr
            plt.xticks(ticks=xticks, labels=xticks, rotation=45)

            plt.title(f"Entwicklung des Begriffs '{keyword}' (1994–2025)", fontsize=16)
            plt.xlabel("Jahr", fontsize=12)
            plt.ylabel("Anzahl der Erwähnungen", fontsize=12)
            plt.grid(visible=True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.legend(title="Begriff", fontsize=10)
            plt.show()
    else:
        print("Spalten 'Document Title' oder 'Publication Year' nicht gefunden.")

# Top 3 häufigste Begriffe extrahieren (ohne Stoppwörter)
keywords = extract_top_keywords(data, n_keywords=3)

# Funktionen ausführen
plot_detailed_trends(data, keywords)  # Detaillierte Trends
plot_keyword_heatmap(data, keywords)  # Heatmap für Begriffe
identify_emerging_declining_keywords(data, keywords)  # Aufkommende und abnehmende Begriffe
