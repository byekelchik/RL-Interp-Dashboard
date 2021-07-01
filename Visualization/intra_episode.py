'''Creates visual under respective tab'''

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import visuals as vls
import dash_html_components as html

def make_layout():
    """Creates layout for visualization"""
    return dbc.Row(
        [
            
            dbc.Col(dbc.Card(
                [
                    dbc.FormGroup(
                        [
                            dbc.Label("Visualization"),
                            dcc.Dropdown(
                                id="inter_vis",
                                options=[
                                    {"label": 'State Delta Table', "value": 'delta-table'},
                                ],
                                value='delta-table',
                            ),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Dataset"),
                            dcc.Dropdown(
                                id="t2_dataset_name",
                                options=[
                                    {"label": '2018', "value": '2018'},
                                    {"label": 'COVID', "value": 'covid'}
                                ],
                                value='2018',
                            ),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Select episode:"),
                            dcc.Slider(
                                id="episode",
                                min=0,
                                max=10,
                                step=None,
                                marks={i:str(i) for i in range(11)} ,
                                value=1
                            )
                        ]
                    )
                ],
            body=True,
            )
        ),
            dbc.Col(id="delta-table", width=5),
            dbc.Col(id="pie-chart", width=4),
            
        ]
    )

def register_callbacks(app):
    """Takes input from frontend and send back the updated visual"""
    @app.callback(
        [Output(component_id="delta-table", component_property="children"),
         Output(component_id="pie-chart", component_property="children")],
        [
            Input(component_id="episode", component_property="value"),
            Input(component_id="t2_dataset_name", component_property="value"),
            Input(component_id="inter_vis", component_property="value"),
        ],
    )
    def make_graphs(episode, dataset_name, visual):
        output = []
        df = sd.get_data(dataset_name, 'Training')
        # Add figures to output
        state_table = dcc.Graph(id='average_state_table', figure=vls.average_state_table([episode], df)[0])
        pie_chart = dcc.Graph(id='greedy-pie-chart', figure = vls.random_action_plot(episode, df))
        return state_table, pie_chart
