import pandas as pd
import matplotlib.pyplot as plt

# Datei einlesen (Passe den Dateipfad an, falls notwendig)
file_path = 'Transactions_on_SE_1994-2024.csv'
data = pd.read_csv(file_path)

# Sicherstellen, dass die Spalte "Publication Year" numerisch ist
data['Publication Year'] = pd.to_numeric(data['Publication Year'], errors='coerce')

# Nur gültige Jahre verwenden
data = data.dropna(subset=['Publication Year'])
data['Publication Year'] = data['Publication Year'].astype(int)

# Artikel pro Jahr zählen
articles_per_year = data['Publication Year'].value_counts().sort_index()

# Plot erstellen
plt.figure(figsize=(10, 6))
plt.plot(articles_per_year.index, articles_per_year.values, marker='o', linestyle='-')
plt.title('Artikelveröffentlichungen im Software Engineering (1994-2024)', fontsize=14)
plt.xlabel('Jahr', fontsize=12)
plt.ylabel('Anzahl der Artikel', fontsize=12)
plt.grid(True)
plt.tight_layout()

# Plot anzeigen
plt.show()
