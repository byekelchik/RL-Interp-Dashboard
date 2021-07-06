'''Get functions for accessing colors'''

def get_colors(data):
	colors_id = {'Hold': '#F2BE4A',
					'Buy': '#01A6A4',
					'Sell': '#EC6355'}

	return colors_id

def get_labels(data):
	label_id = {'0': 'Hold',
				'1': 'Buy', 
				'2': 'Sell'}
	labels = data['Choice'].map(label_id)

	return labels

def get_colorscale():

	# specifies values for gradient scale
	colorscale = [[0, '#D3D3D3'], # null values
					[.5, '#ffdb58'], # hold
					[.75, '#66CDAA'], # buy
					[1, '#f88379']] # sell

	return colorscale



	
	
				
	
	

	