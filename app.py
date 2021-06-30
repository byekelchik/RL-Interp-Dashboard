"""This is the main frontend module"""
# 1. List the proper number or episodes on sidebar, ulan
# 2. Fix graph output so that choosing 1->3->2 outputs the correct graph, ulan
# 3. Fix visuals to allow for a dataset change
# 4. Set up visuals.py to call dataset only once rather than per function call
# 5. Whole numbers only, ulan
# 6. Create a tab for each table so we dont have a long list when comparing many episodes

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Visualization import state_delta_layout, two_way_table, testing

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
                dcc.Tab(
                    state_delta_layout.make_layout(),
                    label='State Delta',
                ),
                    dcc.Tab(two_way_table.make_layout(),
                    label='Two-way Table'
                ),
                    dcc.Tab(testing.make_layout(),
                    label='Testing Data',
                ),
            ],
        )

    ],
    fluid=True,
)

app.layout = html.Div(children=[tab_layout])
two_way_table.register_callbacks(app)
state_delta_layout.register_callbacks(app)
testing.register_callbacks(app)
if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
