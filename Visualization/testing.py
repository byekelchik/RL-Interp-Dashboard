'''Creates visual under respective tab'''

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import testing_visuals as t_vls

def make_layout():
    """Creates layout for visualization"""
    # Columns for side panel and the outputted graphs and tables
    return dbc.Row(
        [
        dbc.Col(
            dbc.Card(
                dbc.FormGroup(
                    [
                        dbc.Label("Dataset"),
                        dcc.Dropdown(
                            id="test_dataset_name",
                            options=[
                                {"label": '2018', "value": '2018'},
                                {"label": 'COVID', "value": 'covid'}
                            ],
                            value='2018',
                        ),
                    ]
                )
            )
        ),
        dbc.Col(id="testing-delta-table", width=4),
        dbc.Col(id="testing-price-volume", width=4),
        # dbc.Col(id="heatmap-visual", width=4),
        dbc.Col(id="qvalues-plot", width=8),

        ])

def register_callbacks(app):
    """Takes input from frontend and send back the updated visual"""
    @app.callback(
        [
        Output(component_id="testing-delta-table", component_property="children"),
        Output(component_id="testing-price-volume", component_property="children"),
        # Output(component_id="heatmap-visual", component_property="children"),
        Output(component_id="qvalues-plot", component_property="children"),
        ],
        [
        Input(component_id="test_dataset_name", component_property="value"),
        ],
    )
    def make_table(dataset_name):
        df = sd.get_data(dataset_name, 'Testing')
        output, i = [], 0

        for vis in t_vls.get(df):
            output.append(dcc.Graph(id='avg_price_table' + str(i), figure=vis))
            i += 0
        return output[0], output[1], output[2]
