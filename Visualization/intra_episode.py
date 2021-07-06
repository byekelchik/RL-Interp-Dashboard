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
                            # Dropdown to select visualization
                            dbc.Label("Visualization", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                            dcc.Dropdown(
                                id="intra_vis",
                                options=[
                                    {"label": 'State Delta Table', "value": 'state-delta-table'},
                                    {"label": 'State Delta Graphs', "value": 'state-delta-graph'},
                                    {"label": 'Heatmap', "value": 'heatmap'},
                                    {"label": 'Q-Values Plot', "value": 'q-values'},
                                ],
                                value='state-delta-table', # initial value in dropdown
                                
                            ),
                    
                               # dropdown for choosing the dataset
                            dbc.Label("Dataset", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                            dcc.Dropdown(
                                id="t2_dataset_name",
                                options=[
                                    {"label": '2018', "value": '2018'},
                                    {"label": 'COVID', "value": 'covid'}
                                ],
                                value='2018', # initial value in dropdown
                           
                    ),
                            # slider to change episode in dataset
                            dbc.Label("Select episode:", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                            dcc.Slider(
                                id="episode",
                                min=0,
                                max=10,
                                step=None,
                                marks={i:str(i) for i in range(11)},
                                value=1,
                            )
                     
                ],style={'backgroundColor': '#222831', 'height':'100vh'},
            body=True,
            )
        ),
            # structures and displays the chosen output
            dbc.Col(id="intra-visual-output", width=9), 
            
        ],style={'padding': 20},
    )

def register_callbacks(app):
    """Takes input from frontend and send back the updated visual"""
    @app.callback(
        Output(component_id="intra-visual-output", component_property="children"),
        [
            # three input values from the sidebar
            Input(component_id="episode", component_property="value"),
            Input(component_id="t2_dataset_name", component_property="value"),
            Input(component_id="intra_vis", component_property="value"),

        ],
    )
    def make_graphs(episode, dataset_name, visual):
        '''Takes input from the callback and returns the visual for the output'''
        output = []
        i = 0
        df = sd.get_data(dataset_name, 'Training') # get data from database
        graph_style = {
            'border':'1px solid', 
            'border-radius': 10, 
            'backgroundColor':'#393E46',
            'padding': 5
            }
        # Add figures to output
        if visual == 'state-delta-table':
            output.append(html.Div(dcc.Graph(id='average-state-table', figure=vls.average_state_table([episode], df)[0], style={'margin':10}), style=graph_style))
            output.append(html.Div(dcc.Graph(id='greedy-pie-chart', figure = vls.random_action_plot(episode, df), style={'margin':10}), style=graph_style))
        elif visual == 'state-delta-graph':
            for vis in vls.intra_state_delta_graph(episode, df):
                output.append(html.Div(dcc.Graph(id='average-state-graph'+str(i), figure = vis, style={'margin':10}), style=graph_style))
                i+=1
        elif visual == 'heatmap':
            output.append(html.Div(dcc.Graph(id='heatmap', figure = vls.heatmap(episode, df), style={'margin':10}), style=graph_style))
        elif visual == 'q-values':
            output.append(html.Div(dcc.Graph(id='q-values-plot', figure = vls.qvalues_plot(episode, df), style={'margin':10}), style=graph_style))
        return output
