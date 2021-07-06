'''Creates visual under respective tab'''

from random import randint
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import visuals as vls
import dash_html_components as html

inter_range = 0
def make_layout():
    """Creates layout for visualization"""
    # get the range of episodes
    # Columns for side panel and the outputted graphs and tables
    return dbc.Row(
        [
            dbc.Col(dbc.Card(
                [
                    dbc.FormGroup(
                        [
                            # Dropdown to select visualization
                            dbc.Label("Visualization", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                            dcc.Dropdown(
                                id="inter_vis",
                                options=[
                                    {"label": 'Two-way Table', "value": 'tw-table'},
                                    {"label": 'State Delta Graph', "value": 'state-delta-graph'},
                                    {"label": 'B/S/H for Price/Volume Delta', "value": 'price-volume'},
                                ],
                                value='tw-table', # initial value in dropdown
                            ),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            # dropdown for choosing the dataset
                            dbc.Label("Dataset", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                            dcc.Dropdown(
                                id="t1_dataset_name",
                                options=[
                                    {"label": '2018', "value": '2018'},
                                    {"label": 'COVID', "value": 'covid'}
                                ],
                                value='2018', # initial value in dropdown
                            ),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            # slider to change episode range in dataset
                            dbc.Label("Select two episodes to compare:", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                            dcc.Slider(
                                id="episode1",
                                min=0,
                                max=10,
                                step=None,
                                marks={i:str(i) for i in range(11)},
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
                        ]
                    ),
        ],style={'backgroundColor': '#222831', 'height':'100vh'},
        body=True,
    )),
            dbc.Col(id="chosen-visual", width=9),

        ],style={'padding': 20},
    )

def register_callbacks(app):
    """Takes input from frontend and sends back the updated visual"""

    @app.callback(
            Output(component_id="chosen-visual", component_property="children"),
        [
            Input(component_id="episode1", component_property="value"),
            Input(component_id="episode2", component_property="value"),
            Input(component_id="t1_dataset_name", component_property="value"),
            Input(component_id="inter_vis", component_property="value"),
        ],
    )
    def make_visuals(episode1, episode2, dataset_name, visual):
        '''Takes input from the callback and returns the visual for the output'''
        output = []
        i = 0
        df = sd.get_data(dataset_name, 'Training') # Never run with Testing
        # Get a figure for each passed parameter
        episodes = [episode1, episode2]
        graph_episodes = list(range(episode1, episode2+1))

        graph_style = {
            'border':'1px solid', 
            'border-radius': 10, 
            'backgroundColor':'#393E46',
            'padding': 5
            }

        # Get a figure for each passed parameter
        if visual == 'state-delta-graph':
            
            for vis in vls.inter_state_delta_graph(graph_episodes, df):
                output.append(html.Div(dcc.Graph(id='avg_price_graph'+str(i), figure=vis, style={'margin':10}), style=graph_style))
                i += 1
        elif visual == 'tw-table':
            output.append(html.Div(dcc.Graph(id=str(randint(10000, 99999)), figure=vls.two_way_table(episodes, df), style={'margin':10}), style=graph_style))
            for vis in vls.average_state_table(episodes, df):
                output.append(html.Div(dcc.Graph(id='average_state_table'+str(i), figure=vis, style={'margin':10}), style=graph_style))
                i += 1
        elif visual == 'price-volume':
            for vis in vls.price_v_volume(graph_episodes, df):
                output.append(html.Div(dcc.Graph(id='price_v_volume'+str(i), figure=vis, style={'margin':10}), style=graph_style))
                i += 1
                
        return output
