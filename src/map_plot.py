from cgitb import lookup
import altair as alt
import pandas as pd
from vega_datasets import data  # Required for the map


def generate_map(df: pd.DataFrame):
    """"
    Generates the map for the dashboard

    Parameters
    ----------
    df : pandas dataframe
        The dataframe that contains the data to plot.

    Returns
    -------
    chart : html of altair Chart
        The generated map converted to html
    """
    world_map = alt.topo_feature(data.world_110m.url, "countries")

    # Get the top rated movie for each country code
    df = df.groupby(["country_code"]).apply(lambda x: x.sort_values(["averageRating"], ascending=False)).reset_index(drop=True)
    df = df[["primaryTitle", "country_code", "averageRating"]].drop_duplicates().groupby(["country_code"]).head(1)
    df["fill"] = 1  # Colour the map only if the country exists

    map = alt.Chart(
        world_map
    ).mark_geoshape(
        stroke='#DBA506',
        strokeWidth=0.3
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(df, "country_code", ["averageRating", "primaryTitle", "fill"])
    ).encode(
        tooltip=[alt.Tooltip('averageRating:O', title="Average Rating"),
                 alt.Tooltip('primaryTitle:N', title="Title")],
        color=alt.Color("fill:N",
                        scale=alt.Scale(domain=[None, 1],
                                        range=["dimgray", "gold"]),
                        legend=None)
    ).project(type="equalEarth").configure(background='#000000')

    return map.configure_view(
                strokeWidth=0
            ).properties(
                height=300,
                width=660,
                background='#000000'
            ).to_html()
