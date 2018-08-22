import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os

from app import app

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

def print_button():
    printButton = html.A(['Print PDF'],className="button no-print print",style={'position': "absolute", 'top': '-40', 'right': '0'})
    return printButton

def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                'TolaReports: MEL')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = html.Div([

        dcc.Link('Overview   ', href='/apps/landingapp', className="tab first"),

        dcc.Link('NECPA', href='/apps/app1', className="tab"),
        dcc.Link('EQUATOR', href='/apps/app2', className="tab")
    ], className="row ")
    return menu

df_eqt = pd.read_csv('data/equator.csv')
df_nec = pd.read_csv('data/necpa.csv')
dis_eq = df_eqt.District.value_counts()
dis_nec = df_nec.District.value_counts()
dis_eq = pd.DataFrame(dis_eq)
dis_nec = pd.DataFrame(dis_nec)
dis_nec = dis_nec.transpose()
dis_eq = dis_eq.transpose()
gender_eq = df_eqt.Gender.value_counts()
gender_nec = df_nec.Gender.value_counts()
gender_eq = pd.DataFrame(gender_eq)
gender_nec = pd.DataFrame(gender_nec)
gender_eq = gender_eq.transpose()
gender_nec = gender_nec.transpose()


layout = html.Div([  print_button(),# page 1


        html.Div([

            # Header
            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),
            ]),


    html.H2('District'),
    html.H3('Partner Equator'),
html.Div([
    html.Div([dcc.Graph(id = 'summary-table-1',
              figure ={
                  'data':[
                      go.Table(
                          header=dict(values = list(dis_eq),
                          font=dict(family='Roboto', size=16, color='#7f7f7f'),
                          fill=dict(color='C2D4FF')
                      ),
                          cells=dict(values=[dis_eq.Pader, dis_eq.Omoro, dis_eq.Gulu],
                                     fill=dict(color='#F5F8FF'),
                                     font=dict(family='Roboto', size=14, color='#7f7f7f'),
                                     align=['left'] * 5
                                     ))
                  ]
              }
    )], className="six columns"),
    html.Div([dcc.Graph(id = 'piechart-1',
                  figure ={
                      'data':[
                          go.Pie(labels=list(dis_eq), values=[int(dis_eq.Pader), int(dis_eq.Omoro), int(dis_eq.Gulu)])
                      ]
                  }
        )], className="six columns"),

    ], className="row"),
    html.H3('Partner NECPA'),
html.Div([
    html.Div([dcc.Graph(id='summary-table-2',
              figure={
                  'data': [
                      go.Table(
                          header=dict(values=list(dis_nec),
                            font=dict(family='Roboto', size=16, color='#7f7f7f'),
                            fill=dict(color='C2D4FF')),
                          cells=dict(values=[dis_nec.Omoro, dis_nec.Gulu, dis_nec.Pader],
                                     fill=dict(color='#F5F8FF'),
                                     font=dict(family='Roboto', size=14, color='#7f7f7f'),
                                     align=['left'] * 5
                                     ))
                  ]
              }
              )], className="six columns"),
    html.Div([dcc.Graph(id = 'piechart-2',
                  figure ={
                      'data':[
                          go.Pie(labels=list(dis_eq), values=[int(dis_nec.Omoro), int(dis_nec.Gulu), int(dis_nec.Pader)])
                      ]
                  }
        )], className="six columns"),

    ], className="row"),
html.H2('Gender'),
html.H3('Partner Equator'),
html.Div([
    html.Div([dcc.Graph(id = 'summary-table-3',
              figure ={
                  'data':[
                      go.Table(
                          header=dict(values = list(gender_eq),
                            font=dict(family='Roboto', size=16, color='#7f7f7f'),
                            fill=dict(color='C2D4FF')),
                          cells=dict(values=[gender_eq.Male, gender_eq.Female],
                                     fill=dict(color='#F5F8FF'),
                                     font=dict(family='Roboto', size=14, color='#7f7f7f'),
                                     align=['left'] * 5
                                     ))
                  ]
              }
    )], className="six columns"),
    html.Div([dcc.Graph(id = 'piechart',
                  figure ={
                      'data':[
                          go.Pie(labels=list(gender_eq), values=[int(gender_eq.Male), int(gender_eq.Female)])
                      ]
                  }
        )], className="six columns"),

    ], className="row"),
    html.H3('Partner NECPA'),
html.Div([
    html.Div([dcc.Graph(id='summary-table-4',
              figure={
                  'data': [
                      go.Table(
                          header=dict(values=list(gender_nec),
                            font=dict(family='Roboto', size=16, color='#7f7f7f'),
                            fill=dict(color='C2D4FF')),
                          cells=dict(values=[gender_nec.Male, gender_nec.Female],
                                     fill=dict(color='#F5F8FF'),
                                     font=dict(family='Roboto', size=14, color='#7f7f7f'),
                                     align=['left'] * 5
                                     ))
                  ]
              }
              )], className="six columns"),
    html.Div([dcc.Graph(id = 'piechart-4',
                  figure ={
                      'data':[
                          go.Pie(labels=list(gender_nec), values=[int(gender_nec.Male), int(gender_nec.Female)])
                      ]
                  }
        )], className="six columns"),

    ], className="row"),


])
# @app.callback(Output('summary-table'),[Input()])
# def summary_table():





external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(debug=True)