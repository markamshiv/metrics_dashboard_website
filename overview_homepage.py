# Description: This file contains the layout and callback functions for the overview homepage.
from dash import Dash, dcc, html, Input, Output 
import graphUtilities


snp_overview_content = html.Div([
        #todo   p0 add background color/box, p2 add a sybolic image, add refrence to home page 
        html.Div(html.H1("S&P 500 Overview", style={'textAlign': 'center','margin': '10px'})),
        html.Br(),
        dcc.Tabs(id="S&P 500 Graph timebar", value='60', children=[
                dcc.Tab(label='7 Days', value='7', style={"background":"lightyellow", 'fontWeight': 'bold'}, selected_style={"background": "lightblue"}),
                dcc.Tab(label='15 Days', value='15', style={"background":"lightyellow", 'fontWeight': 'bold'}, selected_style={"background": "lightblue"}),
                dcc.Tab(label='3 Months', value='90', style={"background":"lightyellow", 'fontWeight': 'bold'}, selected_style={"background": "lightblue"}),
                dcc.Tab(label='6 Months', value='180', style={"background":"lightyellow", 'fontWeight': 'bold'}, selected_style={"background": "lightblue"})
        ],className="timebar"),

        html.Div([

            html.Div([
                dcc.Graph(id='S&P 500 Graph', figure={},style={'margin': '10px'}),
                dcc.Graph(id='Top Gainers Graph', figure={},style={'margin': '10px'})
            ], className="flex-container-1"),

            html.Div([
                dcc.Graph(id='S&P 500 Graph relative', figure={}, style={'margin': '10px'}),
                dcc.Graph(id='Top Losers Graph', figure={},style={'margin': '10px'}) 
            ], className="flex-container-2"),
        ]),
    ], className="flex-container-3n")
