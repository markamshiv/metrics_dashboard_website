import pandas as pd
import plotly.express as px

import dash
from dash import Dash, dcc, html, Input, Output 
import dash_bootstrap_components as dbc

import graphUtilities

import overview_homepage
import navigationBar

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=False)

# ------------------------------------------------------------------------------
# App layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navigationBar.create_navigation_bar(),
    html.Div(id='page-content')
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='S&P 500 Graph', component_property='figure'),
     Output(component_id='S&P 500 Graph relative', component_property='figure'),
     Output(component_id='Top Gainers Graph', component_property='figure'),
     Output(component_id='Top Losers Graph', component_property='figure')],
    Input(component_id='S&P 500 Graph timebar', component_property='value')
)
def homePage_graphs_updates(option_selected):
    """
    Generates and returns four graphs for the home page based on the selected option.

    Parameters:
    option_selected (str): The selected option for generating the graphs.

    Returns:
    tuple: A tuple containing four graphs (fig_1, fig_2, fig_3, fig_4) generated based on the selected option.
    """

    fig_1, fig_2, fig_3, fig_4 = graphUtilities.get_graphs_homePage(option_selected)

    return fig_1, fig_2, fig_3, fig_4


@app.callback(
    Output(component_id = 'search_dropdown',component_property= 'options'),
    Input(component_id = 'search_bar',component_property='value')
)
def update_dropdown(value):
    if value is not None:
        return [{'label': value, 'value': value},{'label': '1', 'value': '1'}]
    else:
        return []

@app.callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def urlcontent_updates(pathname):
    if pathname == '/overview':
        return overview_homepage.snp_overview_content
    else:
        pass

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)