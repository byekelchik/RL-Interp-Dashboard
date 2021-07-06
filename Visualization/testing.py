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
                                dbc.Label("Dataset", style={'font-weight': 'bold','color': '#ffd369', 'font': 'San Francisco font'}),
                                dcc.Dropdown(
                                    
                                    id="test_dataset_name",
                                    options=[
                                        {"label": '2018', "value": '2018'},
                                        {"label": 'COVID', "value": 'covid'}
                                    ],
                                    value='2018',
                                ),
                            ],style={'backgroundColor': '#222831', 'height':'100vh'},#, 'height':'100vh'
                        
                    ), style={'width': '19%', 'display': 'inline-block', 'vertical-align': 'top', 'padding':'20px'}),
                html.Div([
                    dbc.Row(dbc.Col(id="testing-delta-table", width=13), style={'padding':'15px'}),
                    dbc.Row([dbc.Col(id="qvalues-plot", width=6), 
                            dbc.Col(id="testing-price-volume", width=6),]
                        )], style={'width': '79%', 'display': 'inline-block'})
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
        style_table = {
            'borderBottom': '1px solid #222831',
            'borderTop': '1px solid #222831',
            'padding': '6px',
            'borderRadius': '15px',
            'overflow': 'hidden',
            # 'fontWeight': 'bold'
        }
        df = sd.get_data(dataset_name, 'Testing')
        output, i = [], 0

        for vis in t_vls.get(df):
            output.append(html.Div(dcc.Graph(id='avg_price_table' + str(i), figure=vis, style={'margin':5}), style={'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#393E46'}))
            i += 0
        return output[0], output[1], output[2]
