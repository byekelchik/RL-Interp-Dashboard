"""This is the main frontend module"""
# 1. List the proper number or episodes on sidebar, ulan
# 8. keep B/S/H constant colors, use color.py(maybe)


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Visualization import inter_episode, intra_episode, testing
import welcome

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],suppress_callback_exceptions=True)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #222831',
    'borderTop': '1px solid #222831',
    'padding': '6px',
    'borderRadius': '30px',
    'overflow': 'hidden',
    'backgroundColor': '#393E46',
    'color': '#ffd369',
    'borderColor': '#393E46',
    "margin-left": "4px"
    # 'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #222831',
    'borderBottom': '1px solid #222831',
    'backgroundColor': '#ffd369',
    'color': '#222831',
    'padding': '6px',
    'borderRadius': '30px',
    'overflow': 'hidden',
    "margin-left": "4px"
}

tab_layout = dbc.Container(
    [
        html.H1("Interpretability Dashboard", style={'color': '#ffd369', 'font': 'San Francisco font'}), # Header
        # Columns for side panel and the outputted graphs and tables
        html.Div(id="hidden-div", style={"display": "none"}),
        dcc.Tabs(
            children=[
                    dcc.Tab(welcome.make_layout(),
                    label='Welcome',
                    style=tab_style, selected_style=tab_selected_style
                ),
                    dcc.Tab(testing.make_layout(),
                    label='Testing',
                    style=tab_style, selected_style=tab_selected_style
                ),
                    dcc.Tab(intra_episode.make_layout(),
                    label='Intra-Episode',
                    style=tab_style, selected_style=tab_selected_style
                ),
                    dcc.Tab(inter_episode.make_layout(),
                    label='Inter-Episode',
                    style=tab_style, selected_style=tab_selected_style
                ),
            ], style=tabs_styles
        ),

    ],
    fluid=True,
)

app.layout = html.Div(children=[tab_layout], style={'backgroundColor':'#222831'},)

testing.register_callbacks(app)
intra_episode.register_callbacks(app)
inter_episode.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
