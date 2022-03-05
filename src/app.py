from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd

import sys
sys.path.append("/app/")
from .boxplot import generate_box_plot
from .line_plot import generate_line_plot
from .bar_chart import generate_bar_chart
from .map_plot import generate_map

alt.data_transformers.disable_max_rows()
data = pd.read_csv("/app/data/imdb_2011-2020.csv")
country_codes = pd.read_csv("/app/data/country_codes.csv")
data = pd.merge(data, country_codes, left_on="region", right_on="alpha_2")

# Setup app and layout/frontend
app = Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.layout = dbc.Container([
    dcc.Store(id="filtered-data"),  # Used to store the data as it is filtered
    
    # First row containing only the title
    dbc.Row([
        dbc.Col([
            html.H1("IMDB Dashboard", style={'color': "#DBA506"}),
        ])
    ]),

    # Second row containing filters towards left and charts toward right
    dbc.Row([
        # First column containing filters separated by dividers
        dbc.Col([
            # Genre Checklist
            html.Div([
                html.H6(
                    "Select Genre(s):",
                    style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                ),
                dbc.Checklist(
                    options=[
                        {"label": genre, "value": genre} for genre in sorted(
                            data.genres.unique().astype(str)
                            ) if genre != "nan"
                        ],
                    value=["Action", "Horror", "Romance"],
                    id="genres-checklist",
                    style={'width': "150px", 'height': "100%"}
                ),
                # Region dropdown
                html.H6(
                    "Select Region(s):",
                    style={'width': "150px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                ),
                dcc.Dropdown(
                    options=[
                        {"label": region, "value": region} for region in sorted(
                            data.region.unique().astype(str)
                            ) if region != "nan"
                        ],
                    multi=True,
                    clearable=False,
                    placeholder="Select Region(s)",
                    value=["US", "IN", "UK"],
                    id="region-checklist",
                    style={'width': "150px", 'height': "100px", 'color': "#DBA506", 'background': "#222222"}
                )
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
                            html.H2(
                                "100",
                                style={'width': "150px", 'height': "50px", 'text-align': "center", 'vertical-align': "middle", 'color': "#DBA506"}
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
                            html.H2(
                                "50",
                                style={'width': "150px", 'height': "50px", 'text-align': "center", 'vertical-align': "middle", 'color': "#DBA506"}
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
                            html.H2(
                                "120",
                                style={'width': "150px", 'height': "50px", 'text-align': "center", 'vertical-align': "middle", 'color': "#DBA506"}
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
                            html.H2(
                                "10",
                                style={'width': "150px", 'height': "50px", 'text-align': "center", 'vertical-align': "middle", 'color': "#DBA506"}
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
                            html.Iframe(
                                id='box',
                                style={'width': "500px", 'height': "350px"}
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
                                style={'width': "400px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                            )
                        ])
                    ]),
                    dbc.Row([
                        html.Div([
                            html.Iframe(
                                id='line',
                                style={'width': "400px", 'height': "320px"}
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
                        html.H6(
                            "Top 15 Actors from the best rated movies",
                            style={'width': "500px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                        ),
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        html.H6(
                            "Top rated movie in each region",
                            style={'width': "500px", 'color': "#000000", 'font-weight': "bold", 'background': "#DBA506"}
                        ),
                    ])
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Iframe(
                            id='bar',
                            style={'width': "500px", 'height': "400px"}
                        )
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        html.Iframe(
                            id='map',
                            style={'width': "500px", 'height': "400px"}
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
    Input("region-checklist", "value")
)
def update_data(genres: list, regions: list):
    filtered_data = data[data.genres.isin(genres)]
    filtered_data = filtered_data[filtered_data.region.isin(regions)]
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
    chart = generate_map(df)  # TODO: the map shouldn't receive filtered data!!
    return chart

# Bar Chart
@app.callback(
    Output('bar', 'srcDoc'),
    Input('filtered-data', 'data')
)
def serve_bar_chart(df):
    df = pd.read_json(df)  # Convert the filtered data from a json string to a df
    chart = generate_bar_chart(df)
    return chart

if __name__ == '__main__':
    app.run_server(debug=True)
