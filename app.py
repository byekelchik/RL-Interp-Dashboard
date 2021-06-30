"""This is the main frontend module"""
# TODO:
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
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import visuals as vls
from Visualization import state_delta_layout, two_way_table, sidebar, testing


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI],suppress_callback_exceptions=True)

controls = sidebar.visualization_selector()


app.layout = dbc.Container(
      [
        html.Hr(),
        html.H1("Interpretability Dashboard", style={'text-align': 'center'}), # Header
        html.Hr(),
        # Columns for side panel and the outputted graphs and tables
        dbc.Row(dbc.Col(html.Div(controls))),
        html.Spacer(style={"margin-left": "15px"}),
        dbc.Row(dbc.Col(html.Div(id="visualization")))

      ],
      fluid=True,
  )

@app.callback(
    Output(component_id="visualization", component_property="children"),
        [
            Input(component_id="vis-picker", component_property="value"),
        ],
    )
def select_view(view):

    if view == 'State Delta':
        layout = state_delta_layout.make_layout(app)
        return layout
    elif view == 'Two-way Table':
        layout = two_way_table.make_layout(app)
        return layout
    elif view == 'Testing Data':
        layout = testing.make_layout(app)
        return layout
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8888)

