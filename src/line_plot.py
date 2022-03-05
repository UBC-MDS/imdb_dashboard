import altair as alt
from numpy import row_stack
import pandas as pd


def generate_line_plot(data: pd.DataFrame, ycol: str):
    """"
    Generates the line chart for the dashboard

    Parameters
    ----------
    data : pandas dataframe
        The dataframe that contains the data to plot.
    
    ycol : string
        The column to plot on the y-axis. This must be
        a column from the `data` dataframe.

    Returns
    -------
    chart : html of altair Chart
        The generated line chart converted to html
    """
    # Set up dynamic axis labels
    if ycol == "averageRating":
        label = "Average Rating (/10)"
    if ycol == "runtimeMinutes":
        label = "Average Runtime (minutes)"
    
    ycol = f"mean({ycol})"

    chart = alt.Chart(data).mark_line().encode(
        x=alt.X("startYear",
                axis=alt.Axis(title="Year",
                              grid=False,
                              format='.0f'),
                scale=alt.Scale(domain=(2011, 2020))),
        y=alt.Y(ycol,
                axis=alt.Axis(title=label)),
        color=alt.Color("genres",
                        legend=alt.Legend(title="",
                                          orient='none',
                                          columns=5,
                                          legendX=20,
                                          legendY=240,
                                          direction='horizontal')),
        tooltip=[alt.Tooltip('genres', title="Genre"),
                 alt.Tooltip('startYear', format=".0f" , title="Year"),
                 alt.Tooltip(ycol, format=".1f" , title=label)]
    )
    
    chart = chart + chart.mark_circle()

    chart = chart.interactive()

    return chart.configure_axisLeft(
                labelColor='#DBA506',
                titleColor='#DBA506'
            ).configure_view(
                strokeWidth=0
            ).configure_axisBottom(
                labelColor='#DBA506',
                titleColor='#DBA506'
            ).configure_legend(
                labelColor='#DBA506',
                titleColor='#DBA506'
            ).properties(
                height=200,
                width=315,
                background='#222222'
            ).to_html()