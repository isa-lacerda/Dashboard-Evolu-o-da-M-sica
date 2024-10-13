import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output  

def create_year_vibe_layout(music_df):
    year_vibe = html.Div(children=[
        html.H1("Temas Populares (1950-2019)", style={'textAlign': 'center'}),
        
        dcc.RangeSlider(
            id='year-slider',
            min=music_df['release_year'].min() if music_df is not None else 0,
            max=music_df['release_year'].max() if music_df is not None else 0,
            value=[music_df['release_year'].min(), music_df['release_year'].max()] if music_df is not None else [0, 0],
            marks={str(year): str(year) if year % 10 == 0 else '|' for year in music_df['release_year'].unique()} if music_df is not None else {},
            step=1,
            allowCross=False,
            updatemode='drag',
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        
        dcc.Graph(id='topic-graph')
    ], style={'maxWidth': '105%', 'margin': 'auto', 'padding': '20px'})

    return year_vibe

def register_callbacks(app, music_df):
    @app.callback(
        Output('topic-graph', 'figure'),
        Input('year-slider', 'value')
    )
    def update_graph(selected_years):
        topic_counts = music_df.groupby(['release_year', 'topic']).size().reset_index(name='count')
        
        if topic_counts.empty:
            return px.line(title="Nenhum dado disponível para exibir.")  

        year_gap = topic_counts[
            (topic_counts['release_year'] >= selected_years[0]) & 
            (topic_counts['release_year'] <= selected_years[1])
        ]

        fig = px.line(
            year_gap, 
            x='release_year', 
            y='count', 
            color='topic',
            labels={'count': 'Quantidade de Músicas', 'release_year': 'Ano Lançamento'},
            markers=True
        )

        fig.update_traces(mode='lines+markers')
        fig.update_layout(xaxis=dict(tickmode='linear', dtick=10))

        return fig
