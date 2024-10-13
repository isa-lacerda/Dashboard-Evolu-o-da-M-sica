from dash import dcc, html, Input, Output, State
from dash.dash_table import DataTable

def register_callbacks(app, music_df):
    @app.callback(
        Output('top-songs-table', 'data'),
        Output('top-songs-table', 'columns'),
        Input('search-button', 'n_clicks'),
        State('metric-checkboxes', 'value')
    )
    def update_top_songs(n_clicks, selected_metrics):
        if n_clicks is None or len(selected_metrics) != 2:
            return [], []  

        if len(selected_metrics) == 2:
            metric_1 = selected_metrics[0]
            metric_2 = selected_metrics[1]
            
            music_df['vibe_total'] = music_df[metric_1] + music_df[metric_2]  

            top_songs = music_df.nlargest(10, 'vibe_total')

            columns = [
                {"name": "Track Name", "id": "track_name"},
                {"name": "Artist Name", "id": "artist_name"},
            ] + [{"name": metric.capitalize(), "id": metric} for metric in selected_metrics]

            return top_songs.to_dict('records'), columns 

def create_song_recommend_layout(music_df):
    return html.Div(children=[
        html.Link(
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap", 
            rel="stylesheet"
        ),

        html.Div(style={'fontFamily': 'Poppins, sans-serif', 'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
                        html.H1("Músicas x Vibes (TOP 10)", style={
                'textAlign': 'center', 
                'color': '#333', 
                'fontSize': '36px', 
                'fontWeight': 'bold', 
                'marginBottom': '30px'
            }),

            html.Div(children=[
                html.Label("Selecione duas métricas:", style={'fontSize': '18px', 'fontWeight': '600', 'color': '#333'}),
                dcc.Checklist(
                    id='metric-checkboxes',
                    options=[
                        {'label': 'Danceability', 'value': 'danceability'},
                        {'label': 'Loudness', 'value': 'loudness'},
                        {'label': 'Acousticness', 'value': 'acousticness'},
                        {'label': 'Valence', 'value': 'valence'},
                        {'label': 'Energy', 'value': 'energy'},
                        {'label': 'Sadness', 'value': 'sadness'},
                        {'label': 'Feelings', 'value': 'feelings'},
                        {'label': 'Obscene', 'value': 'obscene'},
                        {'label': 'Romantic', 'value': 'romantic'},
                        {'label': 'Family/Gospel', 'value': 'family/gospel'},
                        {'label': 'World/Life', 'value': 'world/life'},
                        {'label': 'Night/Time', 'value': 'night/time'},
                        {'label': 'Shake the Audience', 'value': 'shake the audience'},
                        {'label': 'Family/Spiritual', 'value': 'family/spiritual'},
                        {'label': 'Violence', 'value': 'violence'},
                    ],
                    value=['danceability', 'obscene'],  
                    inline=True,
                    labelStyle={
                        'display': 'inline-block', 
                        'marginRight': '15px', 
                        'marginBottom': '10px', 
                        'fontSize': '16px', 
                        'color': '#555'
                    },
                    inputStyle={
                        'marginRight': '10px', 
                        'transform': 'scale(1.5)',  
                        'border-radius': '50%',  
                        'cursor': 'pointer'
                    }
                ),
            ], style={'marginBottom': '20px'}),

            html.Div(children=[
                html.Button('Buscar', id='search-button', n_clicks=0, style={
                    'backgroundColor': '#301934', 
                    'color': 'white', 
                    'border': 'none', 
                    'padding': '10px 20px', 
                    'fontSize': '16px', 
                    'borderRadius': '5px', 
                    'cursor': 'pointer',
                    'transition': 'background-color 0.3s ease'
                }),
            ], style={'textAlign': 'center', 'marginBottom': '30px'}),

            DataTable(
                id='top-songs-table',
                columns=[
                    {"name": "Track Name", "id": "track_name"},
                    {"name": "Artist Name", "id": "artist_name"},
                ],
                style_table={'overflowX': 'auto', 'border': '1px solid #ddd'},
                style_header={
                    'backgroundColor': '#f1f1f1', 
                    'fontWeight': 'bold', 
                    'color': '#333',
                    'fontSize': '14px',
                    'textAlign': 'center'
                },
                style_cell={
                    'textAlign': 'center', 
                    'fontSize': '14px',
                    'padding': '10px',
                    'color': '#555'
                },
                page_size=10
            )
        ])
    ])
