import altair as alt
import pandas as pd
from .constants import genre_color_map



def generate_box_plot(data: pd.DataFrame):
    """"
    Generates the boxplot for the dashboard

    Parameters
    ----------
    data : pandas dataframe
        The dataframe that contains the data to plot.

    Returns
    -------
    chart : html of altair Chart
        The generated boxplot converted to html
    """

    # Prepare data for boxplot
    data = data.drop(['primaryName','Unnamed: 0'], axis=1)
    data = data.drop_duplicates()
    
    # Filter the colours for the legend
    genre_names = data.genres.unique()
    genre_colors = []
    for genre in genre_names:
        genre_colors.append(genre_color_map[genre])

    # Create Boxplot
    chart = alt.Chart(data).mark_boxplot(size=25, color="gold").encode(
        x=alt.X('genres',
                axis=alt.Axis(title="", labelAngle=-45)),
        y=alt.Y('averageRating',
                title="IMDb Rating"),
        color=alt.Color('genres',
                        scale=alt.Scale(
                            domain=genre_names,
                            range=genre_colors
                        ),
                        title="Genre")
    )

    return chart.configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).configure_axisLeft(
                labelColor='#DBA506',
                titleColor='#DBA506'
            ).configure_axisBottom(
                labelColor='#DBA506',
                titleColor='#DBA506'
            ).configure_legend(
                labelColor='#DBA506',
                titleColor='#DBA506'
            ).properties(
                height=250,
                width=250,
                background='#000000'
            ).to_html()
