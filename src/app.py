from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd

import sys
sys.path.append("/app/")
from boxplot import generate_box_plot
from line_plot import generate_line_plot
from bar_chart import generate_bar_chart
from map_plot import generate_map

alt.data_transformers.disable_max_rows()
alt.renderers.set_embed_options(actions=False)
data = pd.read_feather("../data/imdb_2011-2020.feather")
country_codes = pd.read_csv("../data/country_codes.csv")

data = pd.merge(data, country_codes, left_on="region", right_on="alpha_2")

# Setup app and layout/frontend
app = Dash(external_stylesheets=[dbc.themes.DARKLY])
app.title = "IMDB Dashboard"
server = app.server
app.layout = dbc.Container([
    dcc.Store(id="filtered-data"),  # Used to store the data as it is filtered
    
    # First row containing only the title
    dbc.Row([
        dbc.Col([
            html.H1("IMDb Dashboard", style={'color': "#DBA506"}),
        ])
    ]),

    # Second row containing filters towards left and charts toward right
    dbc.Row([
        # First column containing filters separated by dividers
        dbc.Col([
            html.Div([
                # Genre Checklist
                html.H6(
                    "Select Genre(s):",
                    style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                ),
                dbc.Checklist(
                    id="genres-checklist",
                    options=[
                        {"label": genre, "value": genre} for genre in sorted(
                            data.genres.unique().astype(str)
                            ) if genre != "nan"
                        ],
                    value=["Action", "Horror", "Romance"],
                    style={'width': "150px", 'height': "100%"}
                ),
                html.Br(),
                html.Br(),
                # Top N actors
                html.H6(
                    "Top N (actors):",
                    style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                ),
                dcc.Slider(
                    id="top_n",
                    min=1,
                    max=15,
                    step=1,
                    value=10,
                    marks=None,
                    included=False,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Br(),
                # Years
                html.H6(
                    "Years:",
                    style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                ),
                dcc.RangeSlider(
                    id="years-range",
                    marks={
                        2011: '2011',
                        2020: '2020'
                    },
                    min=2011,
                    max=2020,
                    step=1,
                    value=[2011, 2020],
                    dots=True,
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
                # Region dropdown
                html.H6(
                    "Select Region(s):",
                    style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                ),
                dcc.Dropdown(
                    id="region-checklist",
                    options=[
                        {"label": name, "value": name} for name in sorted(
                            data.name.unique().astype(str)
                            ) if name != "nan"
                        ],
                    multi=True,
                    clearable=False,
                    placeholder="Select Region(s)",
                    value=["United States of America", "India"],
                    style={'width': "150px", 'height': "100px", 'color': "#DBA506", 'background': "#222222"}
                ),
            ])
        ],
        width="auto"
        ),
        # Second column containing charts separated by title boxes
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    # KPI Total Movies
                    dbc.Row([
                        html.Div([
                            html.H6(
                                "Total Movies",
                                style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                            )
                        ])
                    ]),
                    dbc.Row([
                        html.Div([
                            dcc.Loading(
                                type="circle",
                                children=html.H2(
                                    children=[html.Div(id='total_movies', style={'display': 'inline'})],
                                    style={'width': "150px", 'height': "60px", 'text-align': "center", 'vertical-align': "middle", 'color': "#DBA506", 'border': "1px solid gold"}
                                )
                            )
                        ]),
                    ]),
                    # Total Actors
                    dbc.Row([
                        html.Div([
                            html.H6(
                                "Total Actors",
                                style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                            )
                        ])
                    ]),
                    dbc.Row([
                        html.Div([
                            dcc.Loading(
                                type="circle",
                                children=html.H2(
                                    children=[html.Div(id='total_actors', style={'display': 'inline'})],
                                    style={'width': "150px", 'height': "60px", 'text-align': "center", 'vertical-align': "middle", 'color': "#DBA506", 'border': "1px solid gold"}
                                )
                            )
                        ])
                    ]),
                    # KPI Average Runtime
                    dbc.Row([
                        html.Div([
                            html.H6(
                                "Average Runtime",
                                style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                            )
                        ])
                    ]),
                    dbc.Row([
                        html.Div([
                            dcc.Loading(
                                type="circle",
                                children=html.H2(
                                    children=[
                                        html.Div(id='avg_runtime', style={'display': 'inline'}),
                                        html.Div("mins", style={'display': 'inline', 'font-size': "15px"})
                                    ],
                                    style={'width': "150px", 'height': "60px", 'text-align': "center", 'vertical-align': "middle", 'color': "#DBA506", 'border': "1px solid gold"}
                                )
                            )
                        ])
                    ]),
                    # KPI Average Rating
                    dbc.Row([
                        html.Div([
                            html.H6(
                                "Average Rating",
                                style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                            )
                        ])
                    ]),
                    dbc.Row([
                        html.Div([
                            dcc.Loading(
                                type="circle",
                                children=html.H2(
                                    children=[html.Div(id='avg_rating', style={'display': 'inline'})],
                                    style={'width': "150px", 'height': "60px", 'text-align': "center", 'vertical-align': "middle", 'color': "#DBA506", 'border': "1px solid gold"}
                                )
                            )
                        ])
                    ])  
                ],
                width="auto"
                ),
                dbc.Col([
                    # Distribution of movies by Genre
                    dbc.Row([
                        html.Div([
                            html.H6(
                                "Distribution of movies by Genre",
                                style={'width': "500px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                            )
                        ])
                    ]),
                    dbc.Row([
                        html.Div([
                            dcc.Loading(
                                type="circle",
                                children=html.Iframe(
                                    id='box',
                                    style={'width': "500px", 'height': "350px", 'border': "1px solid gold"}
                                )
                            )
                        ])
                    ])
                ],
                width="auto"
                ),
                dbc.Col([
                    # Average Revenue/Runtime by Genre over Time
                    dbc.Row([
                        html.Div([
                            html.H6(
                                "Average Rating by Genre over Time",
                                style={'width': "420px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                            )
                        ])
                    ]),
                    dbc.Row([
                        html.Div([
                            dcc.Loading(
                                type="circle",
                                children=html.Iframe(
                                    id='line',
                                    style={'width': "420px", 'height': "320px", 'border': "1px solid gold"}
                                )
                            )
                        ])
                    ]),
                    dbc.Row([
                    # Y-axis of line chart
                        dbc.Col([
                            html.H6(
                                "Select Y-axis:",
                                style={'width': "100px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                                ),
                        ],
                        width="auto"
                        ),
                        dbc.Col([
                            dcc.RadioItems(
                                id='ycol',
                                style={'width': "300px", 'height': "20px"},
                                value='averageRating',
                                inline=True,
                                inputStyle={'margin-right': "10px", 'margin-left': "10px"},
                                options=[
                                    {'label': "Average Rating", 'value': "averageRating"},
                                    {'label': "Average Runtime", 'value': "runtimeMinutes"}
                                ]
                            )
                        ],
                        width="auto"
                        )
                    ]),
                ],
                width={'size': "auto", 'offset': 0}
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6(children=[
                            "Top ",
                            html.Div(id='top_n_val', style={'display': 'inline'}),
                            " Actors from the best rated movies"
                        ],
                            style={'width': "340px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                        ),
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        html.H6(
                            "Top rated movie in each region",
                            style={'width': "750px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                        ),
                    ])
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Loading(
                            type="circle",
                            children=html.Iframe(
                                id='bar',
                                style={'width': "340px", 'height': "350px", 'border': "1px solid gold"}
                            )
                        )
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        dcc.Loading(
                            type="circle",
                            color="#DBA506",
                            children=html.Iframe(
                                id='map',
                                style={'width': "750px", 'height': "350px", 'border': "1px solid gold"}
                            )
                        )
                    ])
                ])
            ])
        ],
        width="auto"
        )
    ])
])

# Callback to filter data based on filter values
@app.callback(
    Output("filtered-data", "data"),
    Input("genres-checklist", "value"),
    Input("region-checklist", "value"),
    Input("years-range", "value")
)
def update_data(genres: list, regions: list, years: list):
    filtered_data = data[data.genres.isin(genres)]
    filtered_data = filtered_data[filtered_data.name.isin(regions)]
    filtered_data = filtered_data[(filtered_data.startYear >= years[0]) & (filtered_data.startYear <= years[1])]
    return filtered_data.to_json()

# Box Plot
@app.callback(
    Output('box', 'srcDoc'),
    Input('filtered-data', 'data')
)
def serve_box_plot(df):
    df = pd.read_json(df)  # Convert the filtered data from a json string to a df
    chart = generate_box_plot(df)
    return chart

# Line Plot
@app.callback(
    Output('line', 'srcDoc'),
    Input('filtered-data', 'data'),
    Input('ycol', 'value')
)
def serve_line_plot(df, ycol):
    df = pd.read_json(df)  # Convert the filtered data from a json string to a df
    chart = generate_line_plot(df, ycol)
    return chart

# Map Plot
@app.callback(
    Output('map', 'srcDoc'),
    Input('filtered-data', 'data'),
)
def serve_map(df):
    df = pd.read_json(df)  # Convert the filtered data from a json string to a df
    print(df.name)
    chart = generate_map(df)  # TODO: the map shouldn't receive filtered data!!
    return chart

# Bar Chart
@app.callback(
    Output('bar', 'srcDoc'),
    Input('filtered-data', 'data'),
    Input('top_n', 'value')
)
def serve_bar_chart(df, top_n):
    df = pd.read_json(df)  # Convert the filtered data from a json string to a df
    chart = generate_bar_chart(df, top_n)
    return chart

@app.callback(
    Output('top_n_val', 'children'),
    Input('top_n', 'value')
)
def update_ticker_header(top_n_val):
    return [f'{top_n_val}']

# Total Movies
@app.callback(
    Output('total_movies', 'children'),
    Input('filtered-data', 'data')
)
def total_movies_count(df):
    df = pd.read_json(df)  # Convert the filtered data from a json string to a df
    movies = df["primaryTitle"].nunique()
    return movies

# Total Actors
@app.callback(
    Output('total_actors', 'children'),
    Input('filtered-data', 'data')
)
def total_movies_count(df):
    df = pd.read_json(df)  # Convert the filtered data from a json string to a df
    actors = df["primaryName"].nunique()
    return actors

# Average Runtime
@app.callback(
    Output('avg_runtime', 'children'),
    Input('filtered-data', 'data')
)
def total_movies_count(df):
    df = pd.read_json(df)  # Convert the filtered data from a json string to a df
    avg_runtime = df["runtimeMinutes"].mean().round(0)
    return avg_runtime

# Average Rating
@app.callback(
    Output('avg_rating', 'children'),
    Input('filtered-data', 'data')
)
def total_movies_count(df):
    df = pd.read_json(df)  # Convert the filtered data from a json string to a df
    avg_rating = df["averageRating"].mean().round(1)
    return avg_rating

if __name__ == '__main__':
    app.run_server(debug=True)
