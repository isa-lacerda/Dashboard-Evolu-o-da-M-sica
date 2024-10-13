import pandas as pd
from dash import dcc, html, Input, Output
import plotly.express as px

def register_callbacks(app, music_df):
    @app.callback(
        Output('genre-topic-horizontal-bar-chart', 'figure'),
        Input('genre-dropdown-2', 'value')
    )
    def update_genre_topic_chart(selected_genre):
        genre_topic_counts = music_df.groupby(['genre', 'topic']).size().reset_index(name='count')

        if selected_genre:
            genre_topic_counts = genre_topic_counts[genre_topic_counts['genre'] == selected_genre]

        if genre_topic_counts.empty:
            return px.bar(title="Nenhum dado disponível para o gênero selecionado.")

        fig = px.bar(
            genre_topic_counts,
            x='count',
            y='topic',
            title=f'Tópicos no Gênero: {selected_genre}',
            labels={'count': 'Número de Músicas', 'topic': 'Tópicos'},
            text='count',
            orientation='h',
            color='topic',  
            color_discrete_sequence=px.colors.qualitative.Set1 
        )

        return fig

def create_genre_topic_layout(music_df):
    return html.Div(children=[
        html.H1("Tópicos x Gênero", style={'textAlign': 'center'}),
        
        dcc.Dropdown(
            id='genre-dropdown-2',
            options=[{'label': genre, 'value': genre} for genre in music_df['genre'].unique()],
            value=music_df['genre'].unique()[0],
            clearable=False
        ),

        dcc.Graph(id='genre-topic-horizontal-bar-chart')
    ])
