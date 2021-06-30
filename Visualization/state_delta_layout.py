import dash_html_components as html
import dash_bootstrap_components as dbc
import app
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from Visualization import structure_data as sd
from Visualization import visuals as vls
from Visualization import sidebar

controls = sidebar.make_sd_sidebar()

def make_layout(app):
	layout = dbc.Row(
			[
				dbc.Col(html.Div(controls), width=2),
				dbc.Col(id="delta-table", width=4),
				dbc.Col(id="delta-graph", width=6),
			]
	)

	#Callback for updating graph based on sidebar input
	# TODO: output not correct for graphs, it needs to reset the graph then output a new one rather than appending to current graph
	@app.callback(
		Output(component_id="delta-graph", component_property="children"),
		[
			Input(component_id="episodes", component_property="value"),
			Input(component_id="dataset_name", component_property="value"),
			Input(component_id="train_test", component_property="value"),
		],
	)
	def make_graphs(episodes, dataset_name, train_test):
		output=[]
		i = 0
		df = sd.get_data(dataset_name, train_test)
		# Get a figure for each passed parameter
		for vis in vls.average_price_graph(episodes, str(dataset_name), df):
			output.append(dcc.Graph(id='avg_price_graph'+str(i), figure=vis))
			i += 1
		return output

		#Callback for updating graph based on sidebar input
	# TODO: output not correct for graphs, it needs to reset the graph then output a new one rather than appending to current graph
	@app.callback(
		Output(component_id="delta-table", component_property="children"),
		[
			Input(component_id="episodes", component_property="value"),
			Input(component_id="dataset_name", component_property="value"),
			Input(component_id="train_test", component_property="value"),
		],
	)
	def make_tables(episodes, dataset_name, train_test):
		output=[]
		i = 0
		df = sd.get_data(dataset_name, train_test)
		# Get a figure for each passed parameter
		for vis in vls.average_state_table(episodes, str(dataset_name), df):
			output.append(dcc.Graph(id='average_state_table'+str(i), figure=vis))
			i += 1
		return output

	return layout