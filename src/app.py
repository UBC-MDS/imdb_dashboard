
from dash import Dash, html, dcc, Input, Output, State
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
alt.renderers.set_embed_options(actions=False)
data = pd.read_feather("/app/data/imdb_2011-2020.feather")
country_codes = pd.read_csv("/app/data/country_codes.csv")

data = pd.merge(data, country_codes, left_on="region", right_on="alpha_2")

# Setup app and layout/frontend
app = Dash(external_stylesheets=[dbc.themes.CYBORG])
app.title = "IMDb Dashboard"
server = app.server
app.layout = dbc.Container([
    dcc.Store(id="filtered-data"),  # Used to store the data as it is filtered
    
    # First row containing only the title
    dbc.Row([
        dbc.Col([
            html.Img(
                src="/app/src/assets/projector.gif",
                id="projector",
                style={'width': "120%"}
            )
        ],
        width=1),
        dbc.Col([
            html.Div([
                html.Div(
                    "IMDb Dashboard",
                    style={'font-size': 50, 'display': "inline", 'color': "#DBA506"}
                ),
                html.Div("Plan your next movie.",
                    style={'font-size': 20, 'display': "flex", 'position': "absolute", 'top': 40, 'right': 30, 'color': "#F2DB83"}
                )
            ]),
            html.Div([
                html.I(
                    html.Img(
                        src="/app/src/assets/info-64.png",
                        id="info",
                        style={'width': "100%", 'background': "#000000"}
                    ),
                    id="collapse-button",
                    n_clicks=0,
                    style={'width': "2%", 'position': "absolute", 'top': 38, 'right': 3, 'color': "#DBA506", 'margin': 0}
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody("The IMDb dashboard is primarily targeted towards movie producers to present a consolidated crisp view of the average ratings and runtime for movies by genres and regions with interactive abilities to help them choose and plan their next movie.")),
                    id="collapse",
                    is_open=False,
                    style={'width': "100%", 'position': "absolute", 'top': 72, 'left': 0, 'zIndex': 999, 'color': "#DBA506", 'background': "#000000", 'border': "3px solid gold"},
                )
            ])
        ],
        width=11,
        style={'position': "relative"}
        )
    ],
    style={'height': "70px"}
    ),

    # Second row containing reel image and KPIs
    dbc.Row([
        html.Div([
            # Reel image
            html.Img(
                src="/app/src/assets/reel.png",
                id="reel",
                style={'width': "100%", 'height': "200px", 'background': "#DBA506"}
            ),
            # KPI: Total Movies
            html.Div([
                dbc.Row([
                    html.Strong(
                        html.Div(
                            "Total Movies",
                            style={'fontSize': 20, 'display': "inline-block", 'position': "absolute", 'top': 50, 'left': "9.5%", 'textAlign': "center", 'color': "#000000"}
                        )
                    ),
                    html.Div(
                        html.H2(
                            dcc.Loading(
                                children=[html.Div(id="total_movies")],
                                style={'display': "flex", 'position': "absolute", 'top': 0, 'left': 30}
                            ),
                            style={'display': "flex", 'position': "absolute", 'top': 80, 'left': "10%", 'textAlign': "center", 'color': "#000000"}
                        )
                    )
                ])
            ]),
            # KPI: Total Actors
            html.Div([
                dbc.Row([
                    html.Strong(
                        html.Div(
                            "Total Actors",
                            style={'fontSize': 20, 'display': "flex", 'position': "absolute", 'top': 50, 'left': "34.2%", 'textAlign': "center", 'color': "#000000"}
                        )
                    ),
                    html.Div(
                        html.H2(
                            dcc.Loading(
                                children=[html.Div(id="total_actors")],
                                style={'display': "flex", 'position': "absolute", 'top': 0, 'left': 30}
                            ),
                            style={'display': "flex", 'position': "absolute", 'top': 80, 'left': "34.3%", 'textAlign': "center", 'color': "#000000"}
                        )
                    )
                ])
            ]),
            # KPI: Average Runtime
            html.Div([
                dbc.Row([
                    html.Strong(
                        html.Div(
                            "Average Runtime",
                            style={'fontSize': 20, 'display': "flex", 'position': "absolute", 'top': 50, 'right': "32.8%", 'textAlign': "center", 'color': "#000000"}
                        )
                    ),
                    html.Div(
                        html.H2(
                            dcc.Loading(
                                children=[html.Div(id="avg_runtime")],
                                style={'display': "flex", 'position': "absolute", 'top': 0, 'right': 0}
                            ),
                            style={'display': "flex", 'position': "absolute", 'top': 80, 'right': "37%", 'textAlign': "center", 'color': "#000000"}
                        )
                    )
                ])
            ]),
            # "mins" label
            html.Div([
                dbc.Row([
                    html.Strong(
                        html.Div(
                            "mins",
                            style={'fontSize': 20, 'display': "flex", 'position': "absolute", 'top': 103, 'right': "34%", 'textAlign': "center", 'color': "#000000"}
                        )
                    )
                ])
            ]),
            # KPI: Average Rating
            html.Div([
                dbc.Row([
                    html.Strong(
                        html.Div(
                            "Average Rating",
                            style={'fontSize': 20, 'display': "flex", 'position': "absolute", 'top': 50, 'right': "8.6%", 'textAlign': "center", 'color': "#000000"}
                        )
                    ),
                    html.Div(
                        html.H2(
                            dcc.Loading(
                                children=[html.Div(id="avg_rating")],
                                style={'display': "flex", 'position': "absolute", 'top': 0, 'right': 0}
                            ),
                            style={'display': "flex", 'position': "absolute", 'top': 80, 'right': "11.1%", 'textAlign': "center", 'color': "#000000"}
                        )
                    )
                ])
            ])
        ],
        style={'width': "100%", 'position': "relative", 'border-top': "6px solid gold", 'border-bottom': "6px solid gold"}
        )
    ]),
    
    # Third row containing filters towards left and charts toward right
    dbc.Row([
        # First column containing filters separated by dividers
        dbc.Col([
            html.Div([
                # Genre Checklist
                html.H6(
                    "Select Genre(s):",
                    style={'width': "100%", 'color': "#000000", 'textAlign': "center", 'fontWeight': "bold", 'background': "#DBA506", 'margin-top': "6px"}
                ),
                dbc.Checklist(
                    id="genres-checklist",
                    options=[
                        {"label": genre, "value": genre} for genre in sorted(
                            data.genres.unique().astype(str)
                            ) if genre != "nan"
                        ],
                    value=["Action", "Horror", "Romance"],
                    style={'width': "100%", 'height': "100%", 'color': "#DBA506"}
                ),
                html.Br(),
                # Top N actors
                html.H6(
                    "Top N (actors):",
                    style={'width': "100%", 'color': "#000000", 'textAlign': "center", 'fontWeight': "bold", 'background': "#DBA506"}
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
                # Year Range
                html.H6(
                    "Year Range:",
                    style={'width': "100%", 'color': "#000000", 'textAlign': "center", 'fontWeight': "bold", 'background': "#DBA506"}
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
                html.Br(),
                # Region dropdown
                html.H6(
                    "Select Region(s):",
                    style={'width': "100%", 'color': "#000000", 'textAlign': "center", 'fontWeight': "bold", 'background': "#DBA506"}
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
                    style={'width': "100%", 'height': "100px", 'color': "#DBA506", 'background': "#000000"}
                ),
            ])
        ],
        width=2,
        style={'border-right': "6px solid gold"}
        ),
        # Second column containing charts separated by title boxes
        dbc.Col([
            dbc.Row([
                # Distribution of movies by Genre
                dbc.Col([
                    html.Div([
                        html.H6(
                            "Distribution of movies by Genre",
                            style={'width': "100%", 'color': "#000000", 'textAlign': "center", 'fontWeight': "bold", 'background': "#DBA506", 'margin-top': "6px"}
                        )
                    ]),
                    html.Div([
                        dcc.Loading(
                            type="graph",
                            children=html.Iframe(
                                id='box',
                                style={'width': "100%", 'height': "350px", 'border': "1px solid gold"}
                            )
                        )
                    ])
                ],
                width=6
                ),
                # Average Revenue/Runtime by Genre over Time
                dbc.Col([
                    html.Div([
                        html.H6(
                            children=[
                                html.Div(id='ycol_title', style={'display': 'inline'}),
                                " by Genre over Time"
                            ],
                            style={'width': "100%", 'color': "#000000", 'textAlign': "center", 'fontWeight': "bold", 'background': "#DBA506", 'margin-top': "6px"}
                        )
                    ]),
                    html.Div([
                        dcc.Loading(
                            type="graph",
                            children=html.Iframe(
                                id='line',
                                style={'width': "100%", 'height': "320px", 'border': "1px solid gold"}
                            )
                        )
                    ]),
                    dbc.Row([
                    # Y-axis of line chart
                        dbc.Col([
                            html.H6(
                                "Select Y-axis:",
                                style={'width': "100%", 'color': "#000000", 'textAlign': "center", 'fontWeight': "bold", 'background': "#DBA506"}
                                ),
                        ],
                        width=4
                        ),
                        dbc.Col([
                            dcc.RadioItems(
                                id='ycol',
                                style={'width': "100%", 'height': "20px"},
                                value='averageRating',
                                inline=True,
                                inputStyle={'margin-right': "10px", 'margin-left': "10px"},
                                options=[
                                    {'label': "Average Rating", 'value': "averageRating"},
                                    {'label': "Average Runtime", 'value': "runtimeMinutes"}
                                ]
                            )
                        ],
                        width=8
                        )
                    ]),
                ],
                width=6
                )
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6(
                            children=[
                                "Top ",
                                html.Div(id='top_n_val', style={'display': 'inline'}),
                                " Actors from the best rated movies"
                            ],
                            style={'width': "100%", 'color': "#000000", 'textAlign': "center", 'fontWeight': "bold", 'background': "#DBA506"}
                        ),
                    ]),
                    html.Div([
                        dcc.Loading(
                            type="graph",
                            children=html.Iframe(
                                id='bar',
                                style={'width': "100%", 'height': "350px", 'border': "1px solid gold"}
                            )
                        )
                    ])
                ],
                width=4
                ),
                dbc.Col([
                    html.Div([
                        html.H6(
                            "Top rated movie in each region",
                            style={'width': "100%", 'color': "#000000", 'textAlign': "center", 'fontWeight': "bold", 'background': "#DBA506"}
                        ),
                    ]),
                    html.Div([
                        dcc.Loading(
                            type="graph",
                            color="#DBA506",
                            children=html.Iframe(
                                id='map',
                                style={'width': "100%", 'height': "350px", 'border': "1px solid gold"}
                            )
                        )
                    ])
                ],
                width=8
                ),
            ]),
        ],
        width=10
        )
    ])
],
style={'border': "6px solid gold", 'fontFamily': "Bahnschrift Condensed"}
)

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

# Top N Value
@app.callback(
    Output('top_n_val', 'children'),
    Input('top_n', 'value')
)
def update_ticker_header(top_n_val):
    return [f'{top_n_val}']

# Line Chart Title
@app.callback(
    Output('ycol_title', 'children'),
    Input('ycol', 'value')
)
def update_ycol_title(ycol):
    # Set up dynamic axis labels
    if ycol == "averageRating":
        label = "Average Rating"
    if ycol == "runtimeMinutes":
        label = "Average Runtime"
    return label

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

# Information
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
