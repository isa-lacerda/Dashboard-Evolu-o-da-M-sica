from dash import Dash, html
import pandas as pd

from layouts.year_vibe_layout import create_year_vibe_layout, register_callbacks as register_year_callbacks
from layouts.genre_popularity_layout import create_genre_popularity_layout, register_callbacks as register_genre_popularity_callbacks
from layouts.topic_by_genre_layout import create_genre_topic_layout, register_callbacks as register_genre_topic_callbacks
from layouts.song_recommend_layout import create_song_recommend_layout, register_callbacks as register_song_recommend_callbacks
from layouts.wordcloud_layout import create_wordcloud_layout 

music_df = pd.read_csv('music_df.csv')

app = Dash(__name__)

register_year_callbacks(app, music_df) 
register_genre_popularity_callbacks(app, music_df)
register_genre_topic_callbacks(app, music_df) 
register_song_recommend_callbacks(app, music_df)

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(create_genre_popularity_layout(music_df), style={'flex': '1', 'padding': '10px'}),  
        html.Div(create_genre_topic_layout(music_df), style={'flex': '1', 'padding': '10px'})   
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'flexWrap': 'nowrap'}), 
    
    html.Div(children=[
        html.Div(create_year_vibe_layout(music_df), style={'flex': '3', 'padding': '10px'}),   
        html.Div(create_wordcloud_layout(app, music_df), style={'flex': '1', 'padding': '10px', 'height': '100%', 'overflow': 'hidden'}) 
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px', 'alignItems': 'stretch'}),  

    html.Div(create_song_recommend_layout(music_df), style={'padding': '10px'})   
])

if __name__ == '__main__':
    app.run_server(debug=True)
