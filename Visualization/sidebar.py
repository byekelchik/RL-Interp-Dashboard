import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

# Two-way table sidebar
# not yet elegant
def visualization_selector():
    top_control = html.Div([
                    dcc.Tabs(id="vis-picker",
                    children=[
                        dcc.Tab(label='State Delta', value='State Delta'),
                        dcc.Tab(label='Two-way Table', value='Two-way Table'),
                        dcc.Tab(label='Testing Data', value='Testing Data'),

                        
                    ],
                    value='State Delta'
                    )]
                )           
    return top_control
    
def make_twt_sidebar():

    controls = dbc.Card(
        [
            dbc.FormGroup(
                [
                    dbc.Label("Dataset"),
                    dcc.Dropdown(
                        id="dataset_name",
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
                        id="train_test",
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
    )

    return controls
# state delta sidebar
def make_sd_sidebar():

    controls = dbc.Card(
        [
            dbc.FormGroup(
                [
                    dbc.Label("Dataset"),
                    dcc.Dropdown(
                        id="dataset_name",
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
                        id="train_test",
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
                    dbc.Label("Episodes"),
                    dcc.Checklist(id="episodes",
                            options=[
                                {"label": "1", "value": 1},
                                {"label": "2", "value": 2},
                                {"label": "3", "value": 3},
                                # {label:i, value:i } for i in data
                            ],
                            value=[1, 2]
                            )
                ]
            )
        ],
        body=True,
    )

    return controls

    
def make_testing_sidebar():

    controls = dbc.Card(
            dbc.FormGroup(
                [
                    dbc.Label("Dataset"),
                    dcc.Dropdown(
                        id="dataset_name",
                        options=[
                            {"label": '2018', "value": '2018'},
                            {"label": 'COVID', "value": 'covid'}
                        ],
                        value='2018',
                    ),
                ]
            )
    ) 
    return controls



