# Description: This file is creating navigation bar present at top of all pages

from dash import Dash, dcc, html, Input, Output 
import dash_bootstrap_components as dbc


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

def create_navigation_bar():
    """
    Creates a navigation bar for the Market Watch Analytics website.

    Returns:
    dbc.Navbar: The navigation bar component.
    """
    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Market Watch Analytics", className="ml-2")),
                    ],
                    align="center"
                ),
                href="/overview",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Markets Overview", href="/overview")),
                    dbc.NavItem(dbc.NavLink("Manificent 7", href="/page-2")),
                    dbc.NavItem(
                        dbc.InputGroup(
                            [
                                dbc.Input(id="search_bar",type="text", placeholder="Company search"),
                                dbc.InputGroupText(dbc.Button("Search", id="search-button")),
                            ]
                        )
                    ),
                    dbc.NavItem(
                        dcc.Dropdown(id='search_dropdown', style={'display': 'none'})
                    )
                ]
            ),
        ], 
        color="dark",
        dark=True,
    )

    return navbar
