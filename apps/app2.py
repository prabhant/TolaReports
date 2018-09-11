import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
import os
import flask
from plotly import tools
from app import app
# app = dash.Dash(__name__)
# server = app.server
# app.title = 'Partner Progress Report'
a = ['January','February','March','April','May','June','July','August','September','October','November','December']
activity_arr = ['Contracted seed growth', 'Pre season', 'Mid Season', 'PHH',
                'Demo Establishment','Certification','Seed Distribution']


def print_button():
    printButton = html.A(['Print PDF'],className="button no-print print",style={'position': "absolute", 'top': '-40', 'right': '0'})
    return printButton

def get_menu():
    menu = html.Div([

        dcc.Link('Overview   ', href='/apps/landingapp', className="tab first"),

        dcc.Link('NECPA', href='/apps/app1', className="tab"),
        dcc.Link('EQUATOR', href='/apps/app2', className="tab")
    ], className="row ")
    return menu

def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='https://www.toladata.com/wp-content/uploads/2017/11/logo-colors-large.png', height='100', width='120')
        ], className="ten columns padded"),

        html.Div([
            dcc.Link('Full View   ', href='/full-view')
        ], className="two columns page-view no-print")

    ], className="row gs-header")
    return logo

def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                'TolaData Custom Report')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header

layout = html.Div([
    print_button(),
    html.Div([

        # Header
        get_logo(),
        get_header(),
        html.Br([]),
        get_menu(),
    ]),
    html.H1('Partner Progress Report: EQUATOR SEEDS'),
    html.H5('Please select Year'),

    dcc.Dropdown(
        value='2017',
        options=[{'label': i, 'value': i} for i in ['2017', '2018']],
        multi=False,
        id='dropdown-year',
        placeholder="Select Year",
    ),
    html.H5('Please select Month'),
    dcc.Dropdown(
        value='December',
        options=[{'label': i, 'value': i} for i in list(a)],
        placeholder="Select Month",
        multi=False,
        id='dropdown-month',

    ),

    html.H2('Indicator actual results against target'),
    dcc.Graph(id = 'eq-graph'),# bar graph
    html.H2('Indicator actual results by location, sex, age'),
    html.H3('Aggregated by indicators'),
    dcc.Graph(id = 'eq-table-1-1'),
    html.H3('Disaggregated by indicators'),
    dcc.Graph(id = 'eq-table-1-2'),
    html.H5('Please select Activity'),
    dcc.Dropdown(
        value='id mob',
        options=[{'label': i, 'value': i} for i in list(activity_arr)],
        multi=False,
        id='dropdown-activity',
        placeholder="Select Activity",
    ),
    html.H2('Overall beneficiary reached by location, sex and age'),
    html.H3('Aggregated reach data'),
    dcc.Graph(id='eq-table-2-2'),  # Table 2
    html.H3('Disaggregated reach data'),
    dcc.Graph(id='eq-table-2-1'),# eq-table 1
    html.Div(id='intermediate-value-eq', style={'display': 'none'}),
    html.Div(id='intermediate-value-eq-1', style={'display': 'none'})




])

@app.callback(Output('intermediate-value-eq', 'children'), [Input('dropdown-month', 'value'),Input('dropdown-year', 'value')])
def common_table(month, year):
    df = pd.read_csv('data/equator.csv')
    seed_dist = []
    for i in range(len(df)):
        if (df['Seeds_Acre'].iloc[i] > 0):
            seed_dist.append(1)
        else:
            seed_dist.append(None)
    df['Seed_dist'] = seed_dist
    df = df.drop(['Seeds_Acre'], axis=1)

    month_arr = ['Month_Cont', 'Month_Pre', 'Month_Mid', 'Month_PHH',
                 'Month_Demo', 'Month_Ins_Cert', 'Month_Seeds_Dist']
    year_arr = ['Year_Cont', 'Year_Pre', 'Year_Mid', 'Year_PHH',
                'Year_Demo', 'Year_Ins_Cert', 'Year_Seeds_Dist']
    activity_arr = ['Contracted seed growth', 'Pre season', 'Mid Season', 'PHH',
                    'Demo Establishment', 'Certification',
                    'Seed_dist']  # HARDCODING ACTIVITEES FOR NOW    count_arr = []
    df_arr = []
    index = 10
    year = int(year)
    val = month
    valy = year
    for i in range(len(month_arr)):
        index = index + 3  # because all activites are at a difference of 3 cols
        df_tmp = df[df[month_arr[i]] == val]  # filtering by month
        df_tmp = df_tmp[df_tmp[year_arr[i]] == valy]  # filtering by year
        # count_tmp = df_tmp.iloc[:, index].value_counts()#counting
        # count_arr.append(count_tmp)
        df_arr.append(df_tmp)
    df_final = pd.DataFrame()
    for i in range(len(activity_arr)):
        dfc = df_arr[i]
        dfc = dfc.groupby(['District', 'Gender', 'Age cohorts']).size()
        dfc = pd.DataFrame(dfc)
        dfc.insert(loc=0, column='Activity', value=activity_arr[i])
        df_final = df_final.append(dfc)
    df_final.to_csv('data/tmp_equator.csv')  # saving the file as temporary one as the ff does not display the row names
    df_display = pd.read_csv('data/tmp_equator.csv')
    return df_display.to_json(date_format='iso', orient='split')

@app.callback(Output('intermediate-value-eq-1', 'children'), [Input('intermediate-value-eq', 'children')])
def section_one_table(cleaned_data):
    df_display = pd.read_json(cleaned_data, orient='split')
    if(len(df_display)==0):
        return df_display.to_json(date_format='iso', orient='split')
    df_display = df_display[['Activity', 'Gender', 'Age cohorts', 'District', '0']]
    # df_display = df_display[df_display['Activity'] == activity]
    df_display['Sum'] = df_display['0']
    indilist = pd.read_csv('data/indicators_equator.csv')
    indicator_map = ['PHH','Demo Establishment', 'Certification', 'Seed Sistribution']
    df_tmp = df_display
    arr = []
    arr_i = []
    for i in range(len(df_display)):
        flag = 0
        tmp = df_display.iloc[i, 0]
        for j in range(len(indicator_map)):
            if (tmp == indicator_map[j]):
                arr.append(indilist.iloc[j, 0])
                flag = 1
        if (flag == 0):
            arr_i.append(i)
    df_tmp = df_tmp.drop(df_tmp.index[arr_i])
    df_tmp['Indicators'] = arr
    df_tmp = df_tmp[['Indicators', 'District', 'Gender', 'Age cohorts', 'Sum']]
    df_display = df_tmp
    indi_arr = df_display['Indicators'].unique()
    df_main = pd.DataFrame()
    for i in range(len(indi_arr)):
        df_tmp_2 = df_display[df_display['Indicators'] == indi_arr[i]]
        district_arr = df_tmp_2['District'].unique()
        gender_arr = df_tmp_2['Gender'].unique()
        age_arr = df_tmp_2['Age cohorts'].unique()
        sum_arr = []
        arr = []
        for i in range(len(gender_arr)):
            tmp = df_tmp_2[df_tmp_2['Gender'] == gender_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(gender_arr[i])
        for i in range(len(district_arr)):
            tmp = df_tmp_2[df_tmp_2['District'] == district_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(district_arr[i])
        for i in range(len(age_arr)):
            tmp = df_tmp_2[df_tmp_2['Age cohorts'] == age_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(age_arr[i])
        df_tmp = pd.DataFrame(sum_arr, index=arr)
        df_tmp = df_tmp.transpose()
        df_main = df_main.append(df_tmp)
    df_main['Indicator'] = indi_arr
    df_t = df_main
    cols = df_t.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_t = df_t[cols]
    df_t.loc[:, 'Total Actual'] = df_t['Male']+df_t['Female']
    target_arr = []
    for i in range(len(df_t)):
        for j in range(len(indilist)):
            if (df_t.iloc[i, 0] == list(indilist['Indicators'])[j]):
                target_arr.append(list(indilist['LOP Target'])[j])
    df_t['Total Target'] = target_arr
    return df_t.to_json(date_format='iso', orient='split')


@app.callback(Output('eq-graph', 'figure'), [Input('intermediate-value-eq-1', 'children')])
def update_graph(cleaned_data):
    df_t = pd.read_json(cleaned_data, orient='split')
    print(df_t)
    if(len(df_t)==0):
        return {
            'data':
                [go.Table(
                    header = dict(values = ['Message']),
                    cells = dict(values = [['No data']])
                )]
        }
    y1 = list(df_t['Total Actual'])
    y2 = list(df_t['Total Target'])
    indname = list(df_t['Indicator'])
    return {
        'data': [go.Bar(
            x = indname,
            y = y1,
            name = 'achieved',
            marker = go.Marker(
                color = '#07d7a7'

            )


        ),
            go.Bar(
                x = indname,
                y = y2,
                name = 'target',
                marker=go.Marker(
                    color='#ff9f00'

                )

            )
        ]
    }

@app.callback(Output('eq-table-1-1', 'figure'), [Input('intermediate-value-eq-1', 'children')])
def update_table(cleaned_data):
    df_t = pd.read_json(cleaned_data, orient='split')
    vals = []
    if(len(df_t)==0):
        return {
            'data':
                [go.Table(
                    header = dict(values = ['Message']),
                    cells = dict(values = [['No data']])
                )]
        }
    for i in range(len(list(df_t))):
        vals.append(df_t.iloc[:, i])
    return {
        'data': [
            go.Table(
                columnwidth=[150, 40, 40, 40, 40, 40, 40, 40,40],
                header=dict(values=list(df_t.columns),
                            font=dict(family='Roboto', size=16, color='#ffffff'),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    font=dict(family='Roboto', size=14, color='#333333'),
                    fill=dict(color='#ffffff'),
                    align=['left'] * 5)
            )
        ]
    }


@app.callback(Output('eq-table-1-2', 'figure'), [Input('intermediate-value-eq', 'children')])
def update_table(cleaned_data):
    df_display = pd.read_json(cleaned_data, orient='split')
    if(len(df_display)==0):
        return {
            'data':
                [go.Table(
                    header = dict(values = ['Message']),
                    cells = dict(values = [['No data']])
                )]
        }
    df_display = df_display[['Activity', 'Gender', 'Age cohorts', 'District', '0']]
    # df_display = df_display[df_display['Activity'] == activity]
    df_display['Sum'] = df_display['0']
    indilist = pd.read_csv('data/indicators_equator.csv')
    indicator_map = ['PHH', 'Demo Establishment', 'Certification', 'Seed Sistribution']
    df_tmp = df_display
    arr = []
    arr_i = []
    for i in range(len(df_display)):
        flag = 0
        tmp = df_display.iloc[i, 0]
        for j in range(len(indicator_map)):
            if (tmp == indicator_map[j]):
                arr.append(indilist.iloc[j, 0])
                flag = 1
        if (flag == 0):
            arr_i.append(i)
    df_tmp = df_tmp.drop(df_tmp.index[arr_i])
    df_tmp['Indicators'] = arr
    df_tmp = df_tmp[['Indicators', 'District', 'Gender', 'Age cohorts', 'Sum']]
    df_t = df_tmp
    df_t = df_t.rename(index=str, columns={"Age cohorts": "Age Category","Sum":"Total Actual"})
    cols = ['Indicators', 'District', 'Gender', 'Age Category', 'Total Actual']
    df_t = df_t[cols]
    # df_t['Target'] = target_arr
    vals = []
    for i in range(len(list(df_t))):
        vals.append(df_t.iloc[:, i])
    return {
        'data': [
            go.Table(
                columnwidth=[150, 40, 40, 40, 40],
                header=dict(values=list(df_t.columns),
                            font=dict(family='Roboto', size=16, color='#ffffff'),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#ffffff'),
                    font=dict(family='Roboto', size=14, color='#333333'),
                    align=['left'] * 5)
            )
        ]
    }

# Table 3 uses 2 dropdowns so calling 2 inputs
@app.callback(Output('eq-table-2-1', 'figure'), [Input('intermediate-value-eq', 'children'), Input('dropdown-activity', 'value')])
def update_new_tab(cleaned_data, activity):
    df_display = pd.read_json(cleaned_data, orient='split')
    if(len(df_display)==0):
        return {
            'data':
                [go.Table(
                    header = dict(values = ['Message']),
                    cells = dict(values = [['No data']])
                )]
        }
    df_display = df_display[['Activity', 'Gender', 'Age cohorts','District', '0']]
    df_display = df_display[df_display['Activity'] == activity]
    df_display = df_display[['District','Gender', 'Age cohorts','0']]
    df_display['Sum'] = df_display['0']
    df_display = df_display[['District', 'Gender', 'Age cohorts', 'Sum']]
    df_display = df_display.rename(index=str, columns={"Age cohorts": "Age Category","Sum":"Total Actual"})
    vals = []
    for i in range(len(list(df_display))):
        vals.append(df_display.iloc[:, i])
    return {
        'data': [
            go.Table(
                header=dict(values=list(df_display.columns),
                            font=dict(family='Roboto', size=16, color='#ffffff'),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#ffffff'),
                    font=dict(family='Roboto', size=14, color='#333333'),
                    align=['left'] * 5)
            )
        ]
    }


@app.callback(Output('eq-table-2-2', 'figure'),[Input('intermediate-value-eq', 'children'), Input('dropdown-activity', 'value')])
def update_second_tab(cleaned_data, activity):
    # saving the file as temporary one as the ff does not display the row names
    df_display = pd.read_json(cleaned_data, orient='split')
    if(len(df_display)==0):
        return {
            'data':
                [go.Table(
                    header = dict(values = ['Message']),
                    cells = dict(values = [['No data']])
                )]
        }
    df_display = df_display[['Activity', 'Gender', 'Age cohorts','District', '0']]
    df_display = df_display[df_display['Activity'] == activity]
    df_display = df_display[['District','Gender', 'Age cohorts','0']]
    df_display['Sum'] = df_display['0']
    df_display = df_display[['District', 'Gender', 'Age cohorts', 'Sum']]
    district_arr = df_display['District'].unique()
    gender_arr = df_display['Gender'].unique()
    age_arr = df_display['Age cohorts'].unique()
    sum_arr = []
    arr = []
    for i in range(len(district_arr)):
        tmp = df_display[df_display['District'] == district_arr[i]]
        sum_ = tmp['Sum'].sum()
        sum_arr.append(sum_)
        arr.append(district_arr[i])
    for i in range(len(gender_arr)):
        tmp = df_display[df_display['Gender'] == gender_arr[i]]
        sum_ = tmp['Sum'].sum()
        sum_arr.append(sum_)
        arr.append(gender_arr[i])
    for i in range(len(age_arr)):
        tmp = df_display[df_display['Age cohorts'] == age_arr[i]]
        sum_ = tmp['Sum'].sum()
        sum_arr.append(sum_)
        arr.append(age_arr[i])
    df_tmp = pd.DataFrame(sum_arr, index=arr)
    df_tmp = df_tmp.transpose()
    df2 = df_tmp
    if(len(df2)==0):
        return {
            'data':
                [go.Table(
                    header = dict(values = ['Message']),
                    cells = dict(values = [['No data']])
                )]
        }
    df2['Total Actual'] = df2['Male']+df2['Female']
    vals = []
    for i in range(len(list(df2))):
        vals.append(df2.iloc[:, i])
    return {
        'data': [
            go.Table(
                header=dict(values=list(df2.columns),
                            font=dict(family='Roboto', size=16, color='#7f7f7f'),
                            fill=dict(color='#ffffff')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#ffffff'),
                    font=dict(family='Roboto', size=14, color='#333333'),
                    align=['left'] * 5)
            )
        ]
    }
if __name__ == '__main__':
    app.run_server(debug=True)