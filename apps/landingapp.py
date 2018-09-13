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
                'TolaData Custom Report')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = html.Div([

        html.H5(dcc.Link('Overview   ', href='/apps/landingapp', className="tab first")),
        dcc.Link('NECPA', href='/apps/app1', className="tab",style={"color": "red", "text-decoration": "none","size": "20"}),
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


                     html.H2('Total beneficiaries reached by Districts'),
                     html.Div([
                         html.Div([dcc.Graph(id = 'piechart-1',
                                             figure ={
                                                 'data':[
                                                     go.Pie(labels=list(dis_eq), values=[int(dis_eq.Pader)+int(dis_nec.Pader), int(dis_eq.Omoro)+int(dis_nec.Omoro), int(dis_eq.Gulu)+int(dis_nec.Gulu)],
                                                            marker = dict(colors = ['#07d7a7', '#ff9f00', '#ff1d29']))
                                                 ]
                                             }
                                             )], className="six columns"),

                     ], className="row"),
                     html.H2('Total beneficiaries reached by Gender'),
                     html.Div([
                         html.Div([dcc.Graph(id = 'piechart',
                                             figure ={
                                                 'data':[
                                                     go.Pie(labels=list(gender_eq), values=[int(gender_eq.Male)+int(gender_nec.Male), int(gender_eq.Female)+int(gender_nec.Female)],
                                                            marker=dict(
                                                                colors=['#07d7a7', '#ff9f00']))
                                                 ]
                                             }
                                             )], className="six columns"),

                     ], className="row"),
                     ])


if __name__ == '__main__':
    app.run_server(debug=True)