import dash
import dash_html_components
import dash_core_components as dcc
import dash_bootstrap_components
import dash_html_components as html


message = """

### Welcome to our Reinforcement Learning Interpertation Dash App

This app provides insights into the decisions and actions of an RL trading agent

Throughout this app, trading actions are encoded as follows:

- If the action is 1, then agent buys the stock

- If the action is 2, the agent sells the stocks and removes it from the inventory.

- If the action is 0, then there is no trade. The state can be called holding during that period.

## Tabs:

1. Testing (Interperting the agent outside of its training enviornment):

- Average State Table by Action

- Price Change vs Volumne Change color coded w/ respective action

- B/S/H Q-values over testing horizon

2. Intra-Episode (Interperting the agent within a specific episode):

- State Delta Table

- State Delta Graph

- Heatmap

3. Inter-Episode (Interperting the agent evolving over episodes):

- State Delta Graph

- Two-way Table between the min and max of the selected range

- Price Change vs Volumne Change color coded w/ respective action for the range of episodes chosen

"""
def make_layout():

    style_table = {
            'borderBottom': '1px solid #222831',
            'borderTop': '1px solid #222831',
            'padding': '6px',
            'borderRadius': '15px',
            'overflow': 'hidden',
            # 'fontWeight': 'bold'
        }
        
    return html.Div(dcc.Markdown(message), style={'color': '#ffd369', 'font': 'San Francisco font'})