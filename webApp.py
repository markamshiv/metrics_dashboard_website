import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, Input, Output 
import preprocssingUtilities

app = Dash(__name__)

# ------------------------------------------------------------------------------
# App layout

sidebar = html.Div(id = "sidebar" ,children=[
        html.Div(html.H2(dcc.Link("Home", href='/overview')),className="sidebar-header"),
        html.Table([
            html.Tr(html.Td(dcc.Link("S&P 500 Overview", href='/overview', className="rounded-box"))),
            html.Tr(html.Td(dcc.Link("Magnificent 7 Overview", href='/page-2', className="rounded-box")))
        ], className="sidebar-menu")
    ], className="sidebar")

app.layout = html.Div(id='home_layout', children=[
    sidebar,
    html.Div([
        #todo   p0 add background color/box, p2 add a sybolic image, add refrence to home page 
        html.Div(html.H1("Market Watch Analytics", style={'textAlign': 'center','margin': '10px'})),
        html.Br(),
        html.Div([

            dcc.Tabs(id="S&P 500 Graph timebar", value='60', children=[
                dcc.Tab(label='7 days', value='7', style={'background': 'lightyellow'}, selected_style={"background": "lightblue"}),
                dcc.Tab(label='15 days', value='15', style={'background': 'lightyellow'}, selected_style={"background": "lightblue"}),
                dcc.Tab(label='3 Months', value='90', style={'background': 'lightyellow'}, selected_style={"background": "lightblue"}),
                dcc.Tab(label='6 Months', value='180', style={'background': 'lightyellow'}, selected_style={"background": "lightblue"})
            ],style={'margin-left': '300px',"width": "500px","hight":"20px"}),

            html.Div([
                dcc.Graph(id='S&P 500 Graph', figure={},style={'margin': '10px'}),
                dcc.Graph(id='S&P 500 Graph relative', figure={}, style={'margin': '10px'}),
            ], className="flex-container-1"),

            html.Div([
                dcc.Graph(id='Top Gainers Graph', figure={},style={'margin': '10px'}),
                dcc.Graph(id='Top Losers Graph', figure={},style={'margin': '10px'}) 
            ], className="flex-container-2"),
        ]),
    ], className="flex-container-3n")
],className="containerX")

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='S&P 500 Graph', component_property='figure'),
     Output(component_id='S&P 500 Graph relative', component_property='figure'),
     Output(component_id='Top Gainers Graph', component_property='figure'),
     Output(component_id='Top Losers Graph', component_property='figure')],
    Input(component_id='S&P 500 Graph timebar', component_property='value')
)
def update_graph(option_selected):
    

    container = "The year chosen by user was: {}".format(option_selected)
    #Graph  1 - S&P 500
    # Filter the data
    end_date = preprocssingUtilities.get_default_end_date()
    start_date = preprocssingUtilities.get_n_previos_date(end_date=end_date, n=int(option_selected))
    df_snp_500 = preprocssingUtilities.get_snp_daily_data(start_date, end_date)

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
        title='S&P 500 relative Price wrt starting Price',
        labels={'normalized_price': '% normalized Price'},
        template='plotly_dark'
    )

    #Graph  3 - Top Gainers
    df_gainers = preprocssingUtilities.get_biggest_movers(start_date, num_companys=3, type='gainers')
    
    df_gainers = df_gainers.drop_duplicates(subset=['Symbol'])
    fig_3 = px.bar(
        data_frame=df_gainers,
        x='Symbol',
        y='percentage_change',
        title='Top Gainers',
        labels={'Percentage Change': '% Gain'},
        template='plotly_dark'
    )

    #Graph  4 - Top Losers
    df_losers = preprocssingUtilities.get_biggest_movers(start_date, num_companys=3, type='losers')
    df_losers = df_losers.drop_duplicates(subset=['Symbol'])
    fig_4 = px.bar(
        data_frame=df_losers,
        x='Symbol',
        y='percentage_change',
        title='Top Losers',
        labels={'Percentage Change': '% Loss'},
        template='plotly_dark'
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



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)