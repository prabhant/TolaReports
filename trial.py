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
activity_arr = ['id mob', 'nursery management', 'demo', 'phh', 'marketing', 'crop management', 'seed distribution']


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
        value=[],
        options=[{'label': i, 'value': i} for i in list(a)],
        multi=False,
        id='dropdown-month'
    ),
    dcc.Dropdown(
        value=['2017'],
        options=[{'label': i, 'value': i} for i in ['2017','2018']],
        multi=False,
        id='dropdown-year'
    ),
    dcc.Dropdown(
        value=['id mob'],
        options=[{'label': i, 'value': i} for i in list(activity_arr)],
        multi=False,
        id='dropdown-activity'
    ),
    dcc.Graph(id = 'my-graph'),
    dcc.Graph(id = 'my-table'),
    dcc.Graph(id = 'new-table')

    ])

@app.callback(Output('my-graph', 'figure'), [Input('dropdown-month', 'value')])
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

@app.callback(Output('my-table', 'figure'), [Input('dropdown-month', 'value')])
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




@app.callback(Output('new-table', 'figure'), [Input('dropdown-year', 'value'),Input('dropdown-month', 'value'), Input('dropdown-activity', 'value')])
def update_new_tab(year, month, activity):
    year = int(year)
    df = pd.read_csv('new_report.csv')
    df = df.drop(df.columns[31], axis=1)
    df = df.drop(df.columns[31], axis=1)
    df = df.drop(df.columns[31], axis=1)
    month_arr = ['Month_ID_Mob', 'Month_N_Mgt', 'Month_Demo', 'Month_PHH',
                 'Month_Mrk_Sales', 'Month_C_Mgt', 'Month_Seed_Dist']
    year_arr = ['Year_ID_Mob', 'Year_N_Mgt', 'Year_Demo', 'Year_PHH',
                'Year_Mrk_Sales', 'Year_C_Mgt', 'Year_Seed_Dist']
    activity_arr = ['id mob', 'nursery management', 'demo', 'phh', 'marketing', 'crop management', 'seed distribution']
    count_arr = []
    df_arr = []
    index = 10

    val = month
    valy = year
    for i in range(len(month_arr)):
        index = index + 3
        df_tmp = df[df[month_arr[i]] == val]
        df_tmp = df_tmp[df_tmp[year_arr[i]] == valy]
        count_tmp = df_tmp.iloc[:, index].value_counts()
        count_arr.append(count_tmp)
        df_arr.append(df_tmp)
    df_final = pd.DataFrame()
    for i in range(len(activity_arr)):
        dfc = df_arr[i]
        dfc = dfc.groupby(['Gender', 'Age cohorts','District']).size()
        dfc = pd.DataFrame(dfc)
        dfc.insert(loc=0, column='Activity', value=activity_arr[i])
        df_final = df_final.append(dfc)
    df_final.to_csv('tmp.csv')
    df_display = pd.read_csv('tmp.csv')
    df_display = df_display[['Activity', 'Gender', 'Age cohorts','District', '0']]
    df_display = df_display[df_display['Activity'] == activity]
    df_display = df_display[['Gender', 'Age cohorts', 'District', '0']]
    tab = ff.create_table(df_display)
    return  tab


if __name__ == '__main__':
    app.run_server(debug=True, port=8560)