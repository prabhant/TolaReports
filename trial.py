import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff

app = dash.Dash()

df = pd.read_csv('data.csv')
a = df['periodic_target'].unique()

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



app.layout = html.Div([
    dcc.Dropdown(
        value=['a'],
        options=[{'label': i, 'value': i} for i in list(a)],
        multi=False,
        id='dropdown'
    ),
    dcc.Graph(id = 'my-graph'),
    dcc.Graph(id = 'my-table'),
    dcc.Graph(id = 'groupby-table')

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

@app.callback(Output('my-table', 'figure'), [Input('dropdown', 'value')])
def update_table(value):
    df = pd.read_csv('data.csv')
    y1 = []
    y2 = []
    indname = []
    for i in range(len(df)):
        if (df['periodic_target'].iloc[i] == value):
            indname.append(df['name'].iloc[i])
            y1.append(df['achieved'].iloc[i])
            y2.append(df['lop_target'].iloc[i])

    dff = pd.DataFrame({'Indicator name': indname, 'achieved': y1, 'target': y2})
    df_fig = ff.create_table(dff)
    return df_fig

@app.callback(Output('groupby-table', 'figure'), [Input('dropdown', 'value')])
def update_groupby_table(value):
    df_combine = pd.read_csv('combine.csv')
    df_combine = df_combine[df_combine['Month'] == value]
    dfc = df_combine.groupby(['Gender', 'Age Category', 'Activity']).size()
    dfc = pd.DataFrame(dfc)
    dfc.to_csv('dfc.csv')
    dff = pd.read_csv('dfc.csv')
    new_tab = ff.create_table(dff)
    return new_tab


if __name__ == '__main__':
    app.run_server(debug=True, port=8560)