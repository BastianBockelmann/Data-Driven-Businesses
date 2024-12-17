import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

# Datei laden
file_path = 'Data/Dataset.csv' 
data = pd.read_csv(file_path)

# **1. Häufigste Begriffe automatisch extrahieren**
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

# **2. Daten vorbereiten: Häufigkeit von Schlüsselwörtern pro Jahr**
def prepare_keyword_trends(data, keyword):
    if 'Document Title' in data.columns and 'Publication Year' in data.columns:
        # Konvertiere 'Publication Year' in numerische Werte
        data['Publication Year'] = pd.to_numeric(data['Publication Year'], errors='coerce')
        data = data.dropna(subset=['Publication Year', 'Document Title'])
        data['Publication Year'] = data['Publication Year'].astype(int)

        years = sorted(data['Publication Year'].unique())
        keyword_counts = []

        for year in years:
            titles = data[data['Publication Year'] == year]['Document Title'].dropna().str.cat(sep=' ')
            keyword_counts.append(titles.lower().count(keyword.lower()))

        # Warnung, wenn das Schlüsselwort in keinem Jahr vorkommt
        if sum(keyword_counts) == 0:
            print(f"Warnung: Das Schlüsselwort '{keyword}' wurde in den Daten nicht gefunden.")
            return pd.DataFrame()

        # Validierung: Entferne Jahre ohne Häufigkeiten
        trends = pd.DataFrame({'Year': years, 'Count': keyword_counts})
        trends = trends[trends['Count'] > 0]  # Entferne Jahre mit 0 Häufigkeit
        return trends
    else:
        print("Spalten 'Document Title' oder 'Publication Year' nicht gefunden.")
        return pd.DataFrame()

# **3. Fehlerbewertung**
def evaluate_model_performance(y_true, y_pred, method_name):
    error = np.mean(np.abs(y_true - y_pred))
    print(f"Durchschnittlicher Fehler ({method_name}): {error:.2f}")
    return error

# **4. Kombinierte Vorhersagevisualisierung**
def combined_forecast_visualization(data, keywords, years_ahead=5):
    # Daten für Holt-Winters-Analysen
    plt.figure(figsize=(12, 8))
    for keyword in keywords:
        trends = prepare_keyword_trends(data, keyword)
        if trends.empty or len(trends) < 5:
            print(f"Nicht genügend Daten für '{keyword}' für Holt-Winters.")
            continue

        # Holt-Winters-Modell anpassen
        model = ExponentialSmoothing(trends['Count'], trend="add", seasonal=None).fit()

        # Vorhersage für zukünftige Jahre
        future_predictions = model.forecast(years_ahead)

        # Visualisieren der beobachteten Werte und Vorhersagen
        plt.plot(trends['Year'], trends['Count'], marker='o', label=f"Beobachtete Werte ({keyword})", linewidth=2)
        future_years = np.arange(trends['Year'].iloc[-1] + 1, trends['Year'].iloc[-1] + 1 + years_ahead)
        plt.plot(future_years, future_predictions, marker='o', linestyle='--', label=f"Vorhersagen (Holt-Winters) ({keyword})", linewidth=2)

    plt.title("Holt-Winters-Analysen für Top 3 Schlüsselwörter", fontsize=16)
    plt.xlabel("Jahr", fontsize=12)
    plt.ylabel("Häufigkeit", fontsize=12)
    plt.legend()
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Daten für Lineare Regressions-Analysen
    plt.figure(figsize=(12, 8))
    for keyword in keywords:
        trends = prepare_keyword_trends(data, keyword)
        if trends.empty or len(trends) < 5:
            print(f"Nicht genügend Daten für '{keyword}' für Lineare Regression.")
            continue

        X = trends['Year'].values.reshape(-1, 1)
        y = trends['Count'].values

        # Lineares Modell anpassen
        model = LinearRegression()
        model.fit(X, y)

        # Vorhersage für zukünftige Jahre
        future_years = np.arange(trends['Year'].iloc[-1] + 1, trends['Year'].iloc[-1] + 1 + years_ahead).reshape(-1, 1)
        future_predictions = model.predict(future_years)

        # Visualisieren der beobachteten Werte und Vorhersagen
        plt.plot(trends['Year'], trends['Count'], marker='o', label=f"Beobachtete Werte ({keyword})", linewidth=2)
        plt.plot(future_years, future_predictions, marker='o', linestyle='--', label=f"Vorhersagen (Linear) ({keyword})", linewidth=2)

    plt.title("Lineare Regressionsanalysen für Top 3 Schlüsselwörter", fontsize=16)
    plt.xlabel("Jahr", fontsize=12)
    plt.ylabel("Häufigkeit", fontsize=12)
    plt.legend()
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# **Top 3 häufigste Begriffe extrahieren und kombinierte Visualisierung erstellen**
keywords = extract_top_keywords(data, n_keywords=3)  # Automatische Keyword-Extraktion
combined_forecast_visualization(data, keywords, years_ahead=15)
