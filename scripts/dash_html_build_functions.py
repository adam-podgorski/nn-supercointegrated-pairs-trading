import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


nav_item_names = [
    "LSC Angular Modelling",
    "AI & Statistical Arbitrage",
    "Sustainability Discourse Analysis"
]

nav_items = [
    dbc.NavItem(
        dbc.NavLink(
            name, 
            active=True, 
            href='/page-'+str(idx + 1), 
            className='nav-link'), 
        className='project-nav-item'
    ) 
    for idx, name in enumerate(nav_item_names)]

dropdown = dbc.DropdownMenu(
    children=nav_items,
    nav=True,
    in_navbar=True,
    label="Projects"
)

GREEN_GLACIER_LOGO = "assets/logo.png"

# this example that adds a logo to the navbar brand
logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=GREEN_GLACIER_LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand("Adam M. Podgorski", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=False,
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    className="mb-5"
)


def build_header(app):
    return logo



def build_layout(app, children_to_build):
    return html.Div(
        id='index-page',
        children=[
        build_header(app),
        html.Div(
            className='background',
            style={
                'background-image': 'url("/assets/cv-background.png")'
                },
            children=[
                html.Div(
                    id='content-container',
                    children=children_to_build,
                    style={
                        'max-width': '900px',
                        'margin': 'auto',
                        'border': '15px solid white',
                        'background': 'white'
                    }
                )
            ]
            )
        ]
    )


def waiting_for_layout(app):
    pass