import dash_html_components as html
import dash_bootstrap_components as dbc
import app
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import visuals as vls
from Visualization import sidebar
from random import randint

controls = sidebar.make_twt_sidebar()

def make_layout(app):
	# Columns for side panel and the outputted graphs and tables
	layout = dbc.Row(
		[
			html.Spacer(),
			dbc.Col(html.Div(controls), width=2),
			dbc.Col(id="two-way-table", width=8),
		]
	)
	
	#Callback for updating graph based on sidebar input
	@app.callback(
		Output(component_id="two-way-table", component_property="children"),
		[
			Input(component_id="episode1", component_property="value"),
			Input(component_id="episode2", component_property="value"),
			Input(component_id="dataset_name", component_property="value"),
			Input(component_id="train_test", component_property="value"),
		],
	)
	def make_two_way_table(episode1, episode2, dataset_name, train_test):

		df = sd.get_data(dataset_name, train_test) # Never run with Testing
		# Get a figure for each passed parameter
		episodes = [episode1, episode2]
		return dcc.Graph(id=str(randint(10000, 99999)), figure=vls.two_way_table(episodes, df))
	return layout