from random import randint
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import structure_data as sd
import visuals as vls
import plotly.express as px
import plotly.graph_objects as go


def make_visuals(episode1, episode2, dataset_name, train_test, visual):
        graphs = []
        i = 0
        df = sd.get_data(dataset_name, train_test) # Never run with Testing
        # Get a figure for each passed parameter
        episodes = [episode1, episode2]
        graph_episodes = list(range(episode1, episode2+1))
        
        if visual == 'state-delta-graph':
            # Get a figure for each passed parameter
            for vis in vls.average_price_graph(graph_episodes, df):
                vis.show()

        else:
            return [dcc.Graph(id=str(randint(10000, 99999)), figure=vls.two_way_table(episodes, df))]
make_visuals(1, 2, '2018', 'Training','state-delta-graph' )