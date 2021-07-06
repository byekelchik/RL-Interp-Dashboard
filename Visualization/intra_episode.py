'''Creates visual under respective tab'''

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import visuals as vls

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
                                id="intra_vis",
                                options=[
                                    {"label": 'State Delta Table', "value": 'state-delta-table'},
                                    {"label": 'State Delta Graphs', "value": 'state-delta-graph'},
                                    {"label": 'Heatmap', "value": 'heatmap'},
                                ],
                                value='state-delta-table',
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
            dbc.Col(id="intra-visual-output", width=9),
            
        ]
    )

def register_callbacks(app):
    """Takes input from frontend and send back the updated visual"""
    @app.callback(
        Output(component_id="intra-visual-output", component_property="children"),
        [
            Input(component_id="episode", component_property="value"),
            Input(component_id="t2_dataset_name", component_property="value"),
            Input(component_id="intra_vis", component_property="value"),

        ],
    )
    def make_graphs(episode, dataset_name, visual):
        output = []
        i = 0
        df = sd.get_data(dataset_name, 'Training')
        # Add figures to output
        if visual == 'state-delta-table':
            output.append(dcc.Graph(id='average-state-table', figure=vls.average_state_table([episode], df)[0]))
            output.append(dcc.Graph(id='greedy-pie-chart', figure = vls.random_action_plot(episode, df)))
        elif visual == 'state-delta-graph':
            for vis in vls.intra_state_delta_graph(episode, df):
                output.append(dcc.Graph(id='average-state-graph'+str(i), figure = vis))
                i+=1
        elif visual == 'heatmap':
            output.append(dcc.Graph(id='heatmap', figure = vls.heatmap(episode, df)))
        return output
