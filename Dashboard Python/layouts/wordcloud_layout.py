import matplotlib.pyplot as plt
from dash import html, dcc
import base64
from io import BytesIO
from wordcloud import WordCloud
import pandas as pd
from dash import Input, Output

def generate_wordcloud(data, max_words=20):
    wordcloud = WordCloud(width=300, height=300, max_words=max_words, background_color='white').generate(data)
    
    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"

def create_wordcloud_layout(app, df):
    
    decade_options = [
        {'label': '1950s', 'value': 1950},
        {'label': '1960s', 'value': 1960},
        {'label': '1970s', 'value': 1970},
        {'label': '1980s', 'value': 1980},
        {'label': '1990s', 'value': 1990},
        {'label': '2000s', 'value': 2000},
        {'label': '2010s', 'value': 2010}
    ]

    decade_dropdown = dcc.Dropdown(
        id='decade-dropdown',
        options=decade_options,
        value=2010, 
        clearable=False,
        style={'width': '50%'}
    )

    lyrics_text = ' '.join(df['lyrics'])
    wordcloud_image = generate_wordcloud(lyrics_text)

    layout = html.Div(children=[
        html.H2("Word Cloud das Letras das Músicas"),
        decade_dropdown,
        html.Img(id='wordcloud-image', src=wordcloud_image, style={'width': '85%', 'height': 'auto'})
    ])

    
    @app.callback(
        Output('wordcloud-image', 'src'),
        Input('decade-dropdown', 'value')
    )
    def update_wordcloud(selected_decade):
        filtered_df = df[(df['release_year'] >= selected_decade) & 
                         (df['release_year'] < selected_decade + 9)]
        lyrics_text = ' '.join(filtered_df['lyrics'])
        return generate_wordcloud(lyrics_text)

    return layout
