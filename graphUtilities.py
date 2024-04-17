# Description
import pandas as pd 
import plotly.express as px 
import preprocessingUtilities 

#function create graphs required for home page 
# Graphs are S&P Graph along with big winners and losers

def get_graphs_homePage(option_selected):
    """
    Generate and return four different graphs for the home page of a metrics dashboard website.

    Parameters:
    - option_selected (int): The number of previous days to consider for data retrieval.

    Returns:
    - fig_1 (plotly.graph_objects.Figure): A line graph showing the S&P 500 price over time.
    - fig_2 (plotly.graph_objects.Figure): A line graph showing the relative S&P 500 price with respect to the starting price.
    - fig_3 (plotly.graph_objects.Figure): A bar graph showing the top gainers in the stock market.
    - fig_4 (plotly.graph_objects.Figure): A bar graph showing the top losers in the stock market.
    """
    
    #Graph  1 - S&P 500
    # Filter the data
    end_date = preprocessingUtilities.get_default_end_date()
    start_date = preprocessingUtilities.get_n_previos_date(end_date=end_date, n=int(option_selected))
    df_snp_500 = preprocessingUtilities.get_snp_daily_data(start_date, end_date)

    # Plotly Express
    fig_1 = px.line(
        data_frame=df_snp_500,
        x='Date',  # assuming your dataframe has a 'Date' column
        y='Price',  # assuming 'Close' is the column with the closing prices
        title='S&P 500 Price',
        labels={'Price': 'Price'},
        template='plotly_dark'
    )
  
    #Graph  2 - S&P 500

    # Plotly Express
    fig_2 = px.line(
        data_frame=df_snp_500,
        x='Date',  # assuming your dataframe has a 'Date' column
        y='normalized_price',  # assuming 'Close' is the column with the closing prices
        title='S&P 500 % Price Change wrt base',
        labels={'normalized_price': '% Change'},
        template='plotly_dark'
    )

    #Graph  3 - Top Gainers
    df_gainers = preprocessingUtilities.get_biggest_movers(start_date, num_companys=4, type='gainers')
    
    df_gainers = df_gainers.drop_duplicates(subset=['Symbol'])
    fig_3 = px.bar(
        data_frame=df_gainers,
        x='Symbol',
        y='percentage_change',
        title='Top Gainers',
        labels={'percentage_change': '% Gain'},
        template='plotly_dark',
        color='company'
    )

    #Graph  4 - Top Losers
    df_losers = preprocessingUtilities.get_biggest_movers(start_date, num_companys=4, type='losers')
    df_losers = df_losers.drop_duplicates(subset=['Symbol'])
    fig_4 = px.bar(
        data_frame=df_losers,
        x='Symbol',
        y='percentage_change',
        title='Top Losers',
        labels={'percentage_change': '% Loss'},
        template='plotly_dark',
        color='company'
    )

    fig_1.update_layout(
    autosize=False,
    width=500,
    height=300,
    )

    fig_2.update_layout(
    autosize=False,
    width=500,
    height=300,
    )

    fig_3.update_layout(
    autosize=False,
    width=500,
    height=300,
    )

    fig_4.update_layout(
    autosize=False,
    width=500,
    height=300,
    )

    return fig_1, fig_2,fig_3, fig_4
