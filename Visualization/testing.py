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

controls = sidebar.make_testing_sidebar()

def make_layout(app):
	# Columns for side panel and the outputted graphs and tables
	layout = dbc.Row(
		[
			html.Spacer(),
			dbc.Col(html.Div(controls), width=2),
			dbc.Col(id="testing-delta-table", width=8),
		]
	)

	@app.callback(
		Output(component_id="testing-delta-table", component_property="children"),
		[
			Input(component_id="dataset_name", component_property="value"),
		],
	)
	def make_table(dataset_name):

		df = sd.get_data(dataset_name, 'Testing')		# Get a figure for each passed parameter
			
		return dcc.Graph(id='avg_price_table', figure=vls.testing_average_state_table(dataset_name, df))
	return layout