import dash
from dash import dcc, html, Input, Output
import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.graph_objects as go

# Datei laden
file_path = 'Data/Dataset.csv'  # Passe den Pfad entsprechend an
data = pd.read_csv(file_path)

# **Daten vorbereiten**
def prepare_data_for_topic_modeling(data):
    if 'Document Title' in data.columns and 'Publication Year' in data.columns:
        # Nur gültige Jahre und Titel verwenden
        data['Publication Year'] = pd.to_numeric(data['Publication Year'], errors='coerce')
        data = data.dropna(subset=['Publication Year', 'Document Title'])
        return data
    else:
        raise ValueError("Spalten 'Document Title' oder 'Publication Year' fehlen in der CSV-Datei.")

# **BERTopic anwenden**
def get_topics_by_year_range(data, start_year, end_year):
    # Daten im angegebenen Zeitraum filtern
    filtered_data = data[(data['Publication Year'] >= start_year) & (data['Publication Year'] <= end_year)]
    titles = filtered_data['Document Title'].tolist()

    # Deutsche Stoppwörter definieren
    german_stop_words = [
        "der", "die", "das", "und", "ist", "in", "zu", "den", "von", "auf", "mit",
        "als", "auch", "für", "des", "im", "dass", "ein", "eine", "an", "sich"
    ]

    # TF-IDF-Vektorisierung
    vectorizer_model = TfidfVectorizer(stop_words=german_stop_words)

    # BERTopic-Modell
    topic_model = BERTopic(vectorizer_model=vectorizer_model, language="multilingual")
    topics, probs = topic_model.fit_transform(titles)

    # Themen-Information abrufen
    topic_info = topic_model.get_topic_info()
    top_10_topics = topic_info[topic_info['Topic'] != -1].head(10)

    # Themen mit Top-Wörtern
    topic_labels = {}
    for topic_id in top_10_topics['Topic']:
        top_words = topic_model.get_topic(topic_id)
        if top_words:
            topic_labels[topic_id] = ", ".join([word for word, _ in top_words[:3]])

    return top_10_topics, topic_labels

# **Dash-App erstellen**
app = dash.Dash(__name__)

# Daten vorbereiten
data = prepare_data_for_topic_modeling(data)
available_years = sorted(data['Publication Year'].unique())

# Layout der App
app.layout = html.Div([
    html.H1("Top 10 Themen in der Softwareentwicklung", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Startjahr"),
        dcc.Dropdown(
            id='start-year-dropdown',
            options=[{'label': str(year), 'value': year} for year in available_years],
            value=min(available_years)
        ),
        html.Label("Endjahr"),
        dcc.Dropdown(
            id='end-year-dropdown',
            options=[{'label': str(year), 'value': year} for year in available_years],
            value=max(available_years)
        )
    ], style={'display': 'flex', 'gap': '20px', 'justifyContent': 'center'}),
    dcc.Graph(id='topic-bar-chart'),
    html.Div(id='topic-details', style={'marginTop': '20px'})
])

# **Callback für den Schieberegler**
@app.callback(
    [Output('topic-bar-chart', 'figure'),
     Output('topic-details', 'children')],
    [Input('start-year-dropdown', 'value'),
     Input('end-year-dropdown', 'value')]
)
def update_topics(start_year, end_year):
    if start_year >= end_year:
        return {}, html.Div("Das Startjahr muss vor dem Endjahr liegen.", style={'color': 'red'})

    # Top-Themen für den gewählten Zeitraum abrufen
    top_10_topics, topic_labels = get_topics_by_year_range(data, start_year, end_year)

    # Balkendiagramm erstellen
    fig = go.Figure()
    for topic_id, count in zip(top_10_topics['Topic'], top_10_topics['Count']):
        fig.add_trace(go.Bar(
            x=[str(topic_id)],
            y=[count],
            text=topic_labels.get(topic_id, ""),
            textposition='inside',
            marker=dict(color='grey'),
            name=f"Topic {topic_id}"
        ))

    fig.update_layout(
        title=f"Top 10 Themen von {start_year} bis {end_year}",
        xaxis_title="Themen-ID",
        yaxis_title="Anzahl der Dokumente",
        xaxis=dict(type="category"),
        height=600
    )

    # Themenbeschreibung
    topic_details = [
        html.H4("Top-Themen Details:"),
        html.Ul([html.Li(f"Topic {tid}: {keywords}") for tid, keywords in topic_labels.items()])
    ]

    return fig, topic_details

# App starten
if __name__ == '__main__':
    app.run_server(debug=True)