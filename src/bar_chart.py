import pandas as pd
import altair as alt

def generate_bar_chart(data, top):
    """
    Generate the horizontal bar chart to show top actors in the top rated movies.

    Parameters
    ----------
    data : pandas dataframe
           Dataframe containing the data to plot.
    top : int
          Number of actors to show. 
    
    Results
    -------
    chart : html of altair Chart
            The generated bar chart converted to html
    """

    alt.renderers.set_embed_options(theme='dark')
    x = 'averageRating'
    y = 'primaryName'

    actors = (data[[x, y]]
            .groupby([y])[x]
            .mean()
            .sort_values(ascending=False)
            .head(top))
    actors = pd.DataFrame.from_dict(actors)
    actors = actors.reset_index()
    actors.columns = [y, x]

    actors = (data[
        data.primaryName.isin(actors.primaryName)
        ][["primaryName", "averageRating", "primaryTitle"]]
        .sort_values("averageRating", ascending=False)
        .head(top))

    chart = alt.Chart(
        data=actors
    ).encode(
        x=alt.X(x,
                title="",
                axis=None),
        y=alt.Y(y,
                title="",
                sort='-x'),
        size=alt.Size(x,
                  legend=None),
        color=alt.Color(x,
                        scale=alt.Scale(scheme="darkgold",
                                        domain=[15, 3]),
                        legend=None),
        tooltip=[alt.Tooltip('primaryTitle', title="Top Movie")]
    ).mark_bar(
    )

    chart_text = alt.Chart(
        data=actors,
        title=""
    ).encode(
        x=alt.X(x,
                axis=None),
        y=alt.Y(y,
                sort='-x')
    ).mark_bar(
    )

    text = chart_text.mark_text(
        align='right',
        baseline='middle',
        dx=-5,
        dy=0
    ).encode(
        text=x,
        color=alt.value('white')
    )

    return (chart + text).configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).configure_axisLeft(
                labelColor='#DBA506',
                titleColor='#DBA506'
            ).configure_axisRight(
                labelColor='#DBA506',
                titleColor='#DBA506'
            ).properties(
                height=300,
                width=180,
                background='#000000'
            ).interactive(
            ).to_html()