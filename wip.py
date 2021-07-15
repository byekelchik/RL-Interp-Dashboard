# Import libraries and packages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import shapiro
from statsmodels.graphics.gofplots import qqplot
from Visualization import colors
from Visualization import structure_data as sd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
# import numpy as np

def heatmap(data):
    i, j = 0, 0
    x, y, columns = [], [], []
    output = []
    df = data # Never run with Testing

    # get max and min values
    price_min, price_max = min(df['Price Delta']), max(df['Price Delta'])
    volume_min, volume_max = min(df['Volume Delta']), max(df['Volume Delta'])

    # create bins with distribution as close to normal as possible
    x = pd.cut(df['Price Delta'], retbins=True, bins=pd.interval_range(start=price_min, end=price_max, periods = 20))
    y = pd.cut(df['Volume Delta'], retbins=True, bins=pd.interval_range(start=volume_min, end=volume_max, periods = 20))

    # convert intervalindex to tuple for looping
    x = x[1].to_tuples()
    y = y[1].to_tuples()

    # fill df with zeros to initialize 
    new_df = pd.DataFrame(np.zeros(((len(y)-1, len(x)-1))))
    empty_df = pd.DataFrame()
    # iterate through entire df and replace with action for the given price/volume delta
    k=0
    for i in range(1, len(x)):
        for j in range(1, len(y)):
            values = df['Choice'][(df['Price Delta'].astype(float).between(x[i-1][0], x[i][0], inclusive = True)) & (df['Volume Delta'].astype(float).between(y[j-1][0], y[j][0], inclusive = True))]
            new_df[i-1][j-1] = values.median() if len(values) > 0 else -2
            if len(values) <= 0:
                empty_df.loc[k, 'empty_price'] = x[i-1][0]
                empty_df.loc[k, 'empty_volume'] = y[j-1][0]
                empty_df.loc[k, 'adj close'] = 100*(1+(float(x[i-1][0])/100))
                k+=1
    min_max_scaler = MinMaxScaler((0,1))
    empty_df[['empty_price_scaled','empty_volume_scaled']] = min_max_scaler.fit_transform(empty_df[['empty_price', 'empty_volume']])
    print(empty_df)
    empty_df.to_csv(path_or_buf="~/Desktop/IoRLTS/dashapp/empty_df.csv", index=False)
    # create heatmap and return it
    fig = go.Figure(go.Heatmap(z=new_df, x=x[1], y=y[1], colorscale=colors.get_colorscale()))
    
    fig.update_layout(
        title="Price v Volume Heatmap",
        xaxis_title="Price Delta",
        yaxis_title="Volume Delta",
        paper_bgcolor='#393E46',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF'
    )

    return output
heatmap(sd.get_data('2018', 'Testing'))
# np.random.seed(0)
# vals = np.random.random((10, 2))
# min_max_scaler = MinMaxScaler((0,1))
# # min_max_scaler.fit(vals)
# scale_output = min_max_scaler.fit_transform(vals)
# scale_df = pd.DataFrame(scale_output).diff()
# print("Scale df")
# print(scale_df)
# vals_df = pd.DataFrame(vals).diff()

# vals_output = min_max_scaler.fit_transform(vals_df)
# print("Vals df")
# print(vals_df)



