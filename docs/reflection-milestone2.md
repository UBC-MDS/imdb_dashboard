# Milestone 2 reflection

Currently, our Dashboard implements 4 different plots. The first plot is a boxplot showing the movie rating distribution by genre. The second plot is a line chart showing how the average rating or runtime has changed over the years for each genre. We also have a bar chart showing the top actors from the best rated movies. Lastly, we have a map showing the top rated movie in each region as well as highlights the currently selected regions. On the lefthand side we have filters for the genre and for the region which affect all of the plots on the dashboard.

There are many features and improvements that could be made to our dashboard. Currently, the summary statistics (total movies, total actors, etc) are static elements that do not reflect the data - these should be implemented to dynamically update based on the current filters. We also want to add in more filters for the year of production, the actors, total runtime, and rating. This would allow users to get a more detailed insight into the data.

The map plot needs some improvements. We would like to make it show the top 3 (or even top n) movies in each region. This should provide more information to the user without being overwhelming. We would also like to completely remove tooltils for unselected regions. The size of the map could also be increased to make better use of the screen-space.

We would also like to make a dynamic title for the line chart that updates with the selected y axis. The line chart could also be made interactive - for example, hovering over a particular year could show the highest rated movies of that year in a tooltip.

The bar chart should also be made interactive by adding a tooltip showing all the movies that this actor has starred in (or the top n rated ones if there are too many).

As far as filters go, our dashboard would be more accessible if the selected regions showed the full country names rather than a two-letter country code.

Lastly, we could create a new tab showing additional plots focused on the actors. For example, we could have a plot that shows an actors average rating over time, a plot that shows an actors rating for different genres, a plot that shows how consistent an actor is with a jitterplot of all of their ratings, and so on.