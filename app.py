import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import os
from plotly import tools
app = dash.Dash(__name__)
server = app.server
app.title = 'Partner Progress Report'
df = pd.read_csv('data.csv')#reading file to get month names
a = df['periodic_target'].unique()# Month names
activity_arr = ['id mob', 'nursery management', 'demo', 'phh', 'marketing', 'crop management', 'seed distribution']# HARDCODING ACTIVITEES FOR NOW

app.css.append_css({
    "external_url": "https://raw.githubusercontent.com/toladata-ce/TolaReports/master/bWLwgP.css"
})
app.layout = html.Div([
    html.H1('Partner Progress Report',style={'color': '#151F56'}),


    dcc.Dropdown(
        value='2017',
        options=[{'label': i, 'value': i} for i in ['2017', '2018']],
        multi=False,
        id='dropdown-year'
    ),

    dcc.Dropdown(
        value='July',
        options=[{'label': i, 'value': i} for i in list(a)],
        multi=False,
        id='dropdown-month'
    ),

    html.H2('Indicator actual result against target',style={'color': '#151F56'}),
    dcc.Graph(id = 'my-graph'),# bar graph
    html.H2('Indicator actual results by location, sex, age',style={'color': '#151F56'}),
    dcc.Graph(id = 'table-1-1'),
    dcc.Graph(id = 'table-1-2'),
    dcc.Dropdown(
        value='id mob',
        options=[{'label': i, 'value': i} for i in list(activity_arr)],
        multi=False,
        id='dropdown-activity'
    ),
    html.H2('Overall benificiary reached by location, sex and age',style={'color': '#151F56'}),
    html.H3('Table 1'),
    dcc.Graph(id='table-2-1'),# table 1
    html.H3('Table 2'),
    dcc.Graph(id = 'table-2-2')# Table 2


    ])



@app.callback(Output('my-graph', 'figure'), [Input('dropdown-month', 'value'),Input('dropdown-year', 'value')])
def update_graph(month, year):
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
    df_final.to_csv('tmp.csv')  # saving the file as temporary one as the ff does not display the row names
    df_display = pd.read_csv('tmp.csv')
    df_display = df_display[['Activity', 'Gender', 'Age cohorts', 'District', '0']]
    # df_display = df_display[df_display['Activity'] == activity]
    df_display['Sum'] = df_display['0']
    indilist = pd.read_csv('indicators.csv')
    indicator_map = ['nursery management', 'phh', 'marketing', 'crop management', 'seed distribution']
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
        for i in range(len(district_arr)):
            tmp = df_tmp_2[df_tmp_2['District'] == district_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(district_arr[i])
        for i in range(len(gender_arr)):
            tmp = df_tmp_2[df_tmp_2['Gender'] == gender_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(gender_arr[i])
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
    cols = ['Indicator', 'Male', 'Female', 'Gulu', 'Omoro', 'Pader', '15-18', '19-24', '25+']
    df_t = df_t[cols]
    df_t.loc[:, 'Sum'] = df_t['Male']+df_t['Female']
    target_arr = []
    for i in range(len(df_t)):
        for j in range(len(indilist)):
            if (df_t.iloc[i, 0] == list(indilist['Indicators'])[j]):
                target_arr.append(list(indilist['LOP Target'])[j])
    df_t['Target'] = target_arr
    y1 = list(df_t['Sum'])
    y2 = list(df_t['Target'])
    indname = list(df_t['Indicator'])
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

@app.callback(Output('table-1-1', 'figure'), [Input('dropdown-month', 'value'),Input('dropdown-year', 'value')])
def update_table(month, year):
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
    df_final.to_csv('tmp.csv')  # saving the file as temporary one as the ff does not display the row names
    df_display = pd.read_csv('tmp.csv')
    df_display = df_display[['Activity', 'Gender', 'Age cohorts', 'District', '0']]
    # df_display = df_display[df_display['Activity'] == activity]
    df_display['Sum'] = df_display['0']
    indilist = pd.read_csv('indicators.csv')
    indicator_map = ['nursery management', 'phh', 'marketing', 'crop management', 'seed distribution']
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
        for i in range(len(district_arr)):
            tmp = df_tmp_2[df_tmp_2['District'] == district_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(district_arr[i])
        for i in range(len(gender_arr)):
            tmp = df_tmp_2[df_tmp_2['Gender'] == gender_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(gender_arr[i])
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
    cols = ['Indicator', 'Male', 'Female', 'Gulu', 'Omoro', 'Pader', '15-18', '19-24', '25+']
    df_t = df_t[cols]
    df_t.loc[:, 'Sum'] = df_t['Male']+df_t['Female']
    target_arr = []
    for i in range(len(df_t)):
        for j in range(len(indilist)):
            if (df_t.iloc[i, 0] == list(indilist['Indicators'])[j]):
                target_arr.append(list(indilist['LOP Target'])[j])
    df_t['Target'] = target_arr
    table = ff.create_table(df_t, height_constant=60)
    vals = []
    for i in range(len(list(df_t))):
        vals.append(df_t.iloc[:, i])
    return {
        'data': [
            go.Table(
                columnwidth=[150, 40, 40, 40, 40, 40, 40, 40,40],
                header=dict(values=list(df_t.columns),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#F5F8FF'),
                    align=['left'] * 5)
            )
        ]
    }


@app.callback(Output('table-1-2', 'figure'), [Input('dropdown-month', 'value'),Input('dropdown-year', 'value')])
def update_table(month, year):
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
    df_final.to_csv('tmp.csv')  # saving the file as temporary one as the ff does not display the row names
    df_display = pd.read_csv('tmp.csv')
    df_display = df_display[['Activity', 'Gender', 'Age cohorts', 'District', '0']]
    # df_display = df_display[df_display['Activity'] == activity]
    df_display['Sum'] = df_display['0']
    indilist = pd.read_csv('indicators.csv')
    indicator_map = ['nursery management', 'phh', 'marketing', 'crop management', 'seed distribution']
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
    cols = ['Indicators', 'District', 'Gender', 'Age cohorts', 'Sum']
    df_t = df_t[cols]
    # df_t['Target'] = target_arr
    table = ff.create_table(df_t, height_constant=60)
    vals = []
    for i in range(len(list(df_t))):
        vals.append(df_t.iloc[:, i])
    return {
        'data': [
            go.Table(
                columnwidth=[150, 40, 40, 40, 40],
                header=dict(values=list(df_t.columns),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#F5F8FF'),
                    align=['left'] * 5)
            )
        ]
    }

# Table 3 uses 2 dropdowns so calling 2 inputs
@app.callback(Output('table-2-1', 'figure'), [Input('dropdown-year', 'value'),Input('dropdown-month', 'value'), Input('dropdown-activity', 'value')])
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
        dfc = dfc.groupby(['District','Gender', 'Age cohorts']).size()
        dfc = pd.DataFrame(dfc)
        dfc.insert(loc=0, column='Activity', value=activity_arr[i])
        df_final = df_final.append(dfc)
    df_final.to_csv('tmp.csv')# saving the file as temporary one as the ff does not display the row names
    df_display = pd.read_csv('tmp.csv')
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
    df_tmp.to_csv('tmp2.csv', index=False)
    tab = ff.create_table(df_display)
    vals = []
    for i in range(len(list(df_display))):
        vals.append(df_display.iloc[:, i])
    return {
        'data': [
            go.Table(
                header=dict(values=list(df_display.columns),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#F5F8FF'),
                    align=['left'] * 5)
            )
        ]
    }


@app.callback(Output('table-2-2', 'figure'),[Input('dropdown-year', 'value'),Input('dropdown-month', 'value'), Input('dropdown-activity', 'value')])
def update_second_tab(year, month, activity):
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
        dfc = dfc.groupby(['District','Gender', 'Age cohorts']).size()
        dfc = pd.DataFrame(dfc)
        dfc.insert(loc=0, column='Activity', value=activity_arr[i])
        df_final = df_final.append(dfc)
    df_final.to_csv('tmp.csv')# saving the file as temporary one as the ff does not display the row names
    df_display = pd.read_csv('tmp.csv')
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
    df2['Sum'] = df2['Male']+df2['Female']
    tab = ff.create_table(df2)
    print(df2)
    vals = []
    for i in range(len(list(df2))):
        vals.append(df2.iloc[:, i])
    return {
        'data': [
            go.Table(
                header=dict(values=list(df2.columns),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#F5F8FF'),
                    align=['left'] * 5)
            )
        ]
    }
if __name__ == '__main__':
    app.run_server(debug=True, port=8560)