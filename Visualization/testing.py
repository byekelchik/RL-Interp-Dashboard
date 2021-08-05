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
    
    return html.Div([
            html.Div(
                    dbc.Card(
                            [
                                # Dropdown to select visualization
                                dbc.Label("Visualization", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                                dcc.Dropdown(
                                    id="test_vis",
                                    options=[
                                        {"label": 'Action Graphs', "value": 'action-graphs'},
                                        {"label": 'Heatmap', "value": 'test-heatmap'},
                                        {"label": 'Action Distribution', "value": 'test-action-distribution'},
                                    ],
                                    value='action-graphs', # initial value in dropdown
                                ),
                                dbc.Label("Dataset", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                                dcc.Dropdown(
                                    
                                    id="test_dataset_name",
                                    options=[
                                        {"label": '2018', "value": '2018'},
                                        {"label": 'COVID', "value": 'covid'},
                                        {"label": '2017', "value": '2017'}
                                    ],
                                    value='2018',
                                ),
                                dbc.FormGroup(
                                    [
                                        # slider to change episode range in dataset
                                        dbc.Label("Number of Price Bins:", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                                        dcc.Slider(
                                            id="Price",
                                            min=15,
                                            max=20,
                                            step=None,
                                            marks={i:str(i) for i in range(15, 21)},
                                            value=20
                                        ),
                                        dbc.Label("Number of Volume Bins:", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                                        dcc.Slider(
                                            id="Volume",
                                            min=15,
                                            max=20,
                                            step=None,
                                            marks= {i:str(i) for i in range(15, 21)},
                                            value=20
                                        )
                                    ]
                                ),
                            ],style={'backgroundColor': '#222831', 'height':'120vh','padding': 20},#, 'height':'100vh'
                        
                    ), style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'top', 'padding':'20px'}),

                html.Div(
                    [
                        dbc.Row(dbc.Col(id="test-visual"), style={'padding':'20px'}),
                    ], style={'width': '74%', 'display': 'inline-block'}
                )
            ]
            )

def register_callbacks(app):
    """Takes input from frontend and sends back the updated visual"""
    @app.callback(
        Output(component_id="test-visual", component_property="children"),
        [
        Input(component_id="test_dataset_name", component_property="value"),
        Input(component_id="test_vis", component_property="value"),
        Input(component_id="Price", component_property="value"),
        Input(component_id="Volume", component_property="value"),

        ],
    )
    def make_table(dataset_name, visual, Price, Volume):
        style_table = {
            'border':'1px solid',
            'border-radius': 10, 
            'backgroundColor':'#393E46'
        }
        
        # style={'margin':5}), style={'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#393E46'})
        df = sd.get_data(dataset_name, 'Testing')
        output, i = [], 0
        if visual == 'action-graphs':
            
            output.append(html.Div(dcc.Graph(id='qvalues_plot' + str(i), figure=t_vls.qvalues_plot(df), style={'margin':10}), style=style_table))

        elif visual == 'test-heatmap':
            output.append(html.Div(dcc.Graph(id='heatmap', figure = t_vls.heatmap(df, Price, Volume, dataset_name), style={'margin':10}), style=style_table))
            output.append(html.Div(dcc.Graph(id='median_state_table' + str(i), figure=t_vls.median_state_table(df, dataset_name),style={'margin':10}), style=style_table))

        elif visual == 'test-action-distribution': 
                for i, vis in enumerate(t_vls.action_v_state_histogram(df)):
                    output.append(html.Div(dcc.Graph(id='state_v_action_hist'+str(i), figure=vis, style={'margin':10}), style=style_table))

        return output


