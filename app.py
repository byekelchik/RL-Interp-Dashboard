"""This is the main frontend module"""
# 1. List the proper number or episodes on sidebar, ulan
# 5. Whole numbers only, ulan
# 8. keep B/S/H constant colors, use color.py(maybe)


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Visualization import inter_episode, intra_episode, testing

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],suppress_callback_exceptions=True)

tab_layout = dbc.Container(
    [
        html.Hr(),
        html.H1("Interpretability Dashboard", style={'text-align': 'center'}), # Header
        html.Hr(),
        # Columns for side panel and the outputted graphs and tables
        html.Div(id="hidden-div", style={"display": "none"}),
        dcc.Tabs(
            children=[
                    dcc.Tab(testing.make_layout(),
                    label='Testing',
                ),
                    dcc.Tab(intra_episode.make_layout(),
                    label='Intra-Episode'
                ),
                    dcc.Tab(inter_episode.make_layout(),
                    label='Inter-Episode',
                ),
            ],
        ),

    ],
    fluid=True,
)

app.layout = html.Div(children=[tab_layout])

testing.register_callbacks(app)
intra_episode.register_callbacks(app)
inter_episode.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
