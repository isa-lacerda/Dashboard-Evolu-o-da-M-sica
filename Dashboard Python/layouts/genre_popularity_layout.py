import pandas as pd
import plotly.express as px
from dash import dcc, html, callback_context, no_update
from dash.dependencies import Input, Output

def create_genre_popularity_layout(music_df):
    return html.Div(children=[
        html.H1("Gêneros Populares (1950-2019)", style={'textAlign': 'center'}),
        
        dcc.RangeSlider(
            id='genre-year-slider',
            min=music_df['release_year'].min() if music_df is not None else 0,
            max=music_df['release_year'].max() if music_df is not None else 0,
            value=[music_df['release_year'].min(), music_df['release_year'].max()], 
            
            marks={str(year): str(year) if year % 10 == 0 else '|' for year in music_df['release_year'].unique()} if music_df is not None else {},
            step=1,
            allowCross=False,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        
        dcc.Graph(id='bar-graph'),
        
        html.Button('Play', id='play-button', n_clicks=0),
        html.Button('Stop', id='stop-button', n_clicks=0),
        
        dcc.Interval(
            id='interval-component',
            interval=1000, 
            n_intervals=0,
            disabled=True
        )
    ], style={'maxWidth': '800px', 'margin': 'auto', 'padding': '20px'})

def register_callbacks(app, music_df):
    @app.callback(
        Output('bar-graph', 'figure'),
        Input('genre-year-slider', 'value')
    )
    def update_graph(selected_years):
        if music_df is None or music_df.empty:
            return px.bar(title="Nenhum dado disponível para exibir.")

        filtered_data = music_df[
            (music_df['release_year'] >= selected_years[0]) & 
            (music_df['release_year'] <= selected_years[1])
        ]

        if filtered_data.empty:
            return px.bar(title="Nenhum dado disponível para o intervalo selecionado.")

        genre_counts = filtered_data['genre'].value_counts().nlargest(5).reset_index()
        genre_counts.columns = ['genre', 'count']

        fig = px.bar(
            genre_counts,
            x='genre',
            y='count',
            title='Top 5 Gêneros Mais Populares',
            labels={'count': 'Número de Músicas', 'genre': 'Gênero'},
            color='count',
            color_continuous_scale=px.colors.sequential.Viridis
        )

        return fig
    
    @app.callback(
        Output('genre-year-slider', 'value'),
        Output('interval-component', 'disabled'),
        Input('play-button', 'n_clicks'),
        Input('stop-button', 'n_clicks'),
        Input('interval-component', 'n_intervals'),
        Input('genre-year-slider', 'value'),
        prevent_initial_call=True
    )
    def control_slider_and_interval(play_clicks, stop_clicks, n_intervals, current_value):
        ctx = callback_context
        

        if not ctx.triggered:
            return no_update, no_update
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'play-button':
            return current_value, False 

        elif button_id == 'stop-button':
            return no_update, True  


        if n_intervals > 0:
            new_value = [current_value[0] + 1, current_value[1] + 1]
            if new_value[0] <= music_df['release_year'].max():
                return new_value, False 
            return no_update, True
        
        return no_update, no_update  