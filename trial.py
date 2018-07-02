import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()
df = pd.read_csv('data.csv')
a = df['periodic_target'].unique()

app.layout = html.Div([
    dcc.Dropdown(
        value=['a'],
        options=[{'label': i, 'value': i} for i in list(a)],
        multi=False,
        id='dropdown'
    ),
    dcc.Graph(id = 'my-graph')

])

@app.callback(Output('my-graph', 'figure'), [Input('dropdown', 'value')])
def update_graph(value):
    df = pd.read_csv('data.csv')
    y1 = []
    y2 = []
    indname = []
    for i in range(len(df)):
        if (df['periodic_target'].iloc[i] == value):
            indname.append(df['name'].iloc[i])
            y1.append(df['achieved'].iloc[i])
            y2.append(df['lop_target'].iloc[i])
    return {
        'data': [go.Bar(
            x = indname,
            y = y1,
            name = 'achieved',
            marker = go.Marker(
                color = 'rgb(55,83,109)'
            )

        ),
        go.Bar(
            x = indname,
            y = y2,
            name = 'target'
        )
        ]
    }

if __name__ == '__main__':
    app.run_server(debug=True, port=8550)