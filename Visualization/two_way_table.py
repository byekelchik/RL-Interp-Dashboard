'''Creates visual under respective tab'''

from random import randint
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import visuals as vls

def make_layout():
    """Creates layout for visualization"""
    # Columns for side panel and the outputted graphs and tables
    return dbc.Row(
        [
            dbc.Col(dbc.Card(
        [
                    dbc.FormGroup(
                        [
                            dbc.Label("Dataset"),
                            dcc.Dropdown(
                                id="t1_dataset_name",
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
                                dbc.Label("Train or Test"),
                                dcc.Dropdown(
                                    id="t1_train_test",
                                    options=[
                                        {"label": 'Train', "value": 'Training'},
                                        {"label": 'Test', "value": 'Testing'}
                                    ],
                                    value="Training",
                                ),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Select two episodes to compare:"),
                            dcc.Slider(
                                id="episode1",
                                min=0,
                                max=10,
                                step=None,
                                marks={i:str(i) for i in range(11)} ,
                                value=1
                            ),
                            dcc.Slider(
                                id="episode2",
                                min=0,
                                max=10,
                                step=None,
                                marks= {i:str(i) for i in range(11)},
                                value=2
                            )
                    ]),
        ],
        body=True,
    )),
            dbc.Col(id="two-way-table", width=8),
        ]
    )
def register_callbacks(app):
    """Takes input from frontend and send back the updated visual"""
    @app.callback(
        Output(component_id="two-way-table", component_property="children"),
        [
            Input(component_id="episode1", component_property="value"),
            Input(component_id="episode2", component_property="value"),
            Input(component_id="t1_dataset_name", component_property="value"),
            Input(component_id="t1_train_test", component_property="value"),
        ],
    )
    def make_two_way_table(episode1, episode2, dataset_name, train_test):

        df = sd.get_data(dataset_name, train_test) # Never run with Testing
        # Get a figure for each passed parameter
        episodes = [episode1, episode2]
        return dcc.Graph(id=str(randint(10000, 99999)), figure=vls.two_way_table(episodes, df))
