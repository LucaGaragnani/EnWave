import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
from dash import Dash
from dash import dcc
from dash import html
from dash import html, dcc, callback, Input, Output, register_page
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np
from datetime import datetime

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import plotly.graph_objects as go
import plotly.io as pio

import base64

import mysql.connector

from PIL import Image
import io
# from io import BytesIO #from io import StringIO.
from io import StringIO
import PIL.Image
import dash_bootstrap_components as dbc
import base64

# from create_database import import_db_data
import plotly.graph_objs as go






# opne the page

dash.register_page(__name__)





############################         Import data sets from database          ############################################

###################################    TREND Data

#######  IMPORT DATA FROM DB

cable_config = '/Users/marianasouzaoliveira/Desktop/InWave_EHV_CableHI/database/cable_config.xlsx'
risk_index = '/Users/marianasouzaoliveira/Desktop/InWave_EHV_CableHI/database/risk_index_trend.xlsx'

file_list = [risk_index,cable_config]
# db_list = import_db_data(file_list)
#
# risk_index_data = db_list[0]
# cable_details = db_list[1]

datetime_list =[]
risk_trend = []
criticality_index =[]
health_index = []
component_health_index_dict = []
#
# for item in risk_index_data['risk_index_trend']:
#     datetime_list.append(item[0])
#     risk_trend.append(item[1])
#     criticality_index.append(item[2])
#     health_index.append(item[3])

#
# cable_details_list = []
# for item in cable_details['cable_characteristics']:
#     cable_details_list.append(item)

# print(cable_details_list)



############################################################################################################################################3
######################## blank graph

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template='plotly_dark')
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig


##################################################################################################################################################
#######################     card

# card_PD_analysis_request = dbc.Card(
#     dbc.CardBody(
#         [
#
#             html.A(
#             html.Button('Request data analysis', id='submit-val', n_clicks=0, style={'backgroundColor': 'RGB(20,54,214)', 'color':'white','width':'100%' , 'border':'1.5px black solid','height': '50px','text-align':'center',  'marginTop': 20}),
#             # href="http://demowebapplication-572cbf089b33.herokuapp.com/request-analysis-form"
#             href="https://demowebapplication-572cbf089b33.herokuapp.com/request-analysis-form"
#             # href = "request-analysis-form"
#
#             ),
#
#
#         ], className="border-start border-success border-5"
#     ),
#     className="text-center m-4"
# )



##################################################################################################################################################################################

################### plot the app
# Layout of Dash App

layout = html.Div(
# Interval component to trigger callback periodically
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.A(
                            html.Img(
                                className="logo",
                                src=dash.get_asset_url("dash-logo-new.png"),
                                style={"width": "200px", "height": "auto", "border-radius": "8%"}
                            ), style={"display": "flex", "justify-content": "center", "align-items": "center"},

                            href="home",
                        ),
                        # html.H2("InWave"),

                        html.Br(),
                        html.Br(),

                        html.H3("Asset Information"),
                        # html.P(id="AssetTag"),
                        # # html.Br(),
                        # html.P(id='RatedVoltage'),
                        # # html.Br(),
                        # # html.P(id="Lenght"),
                        # # html.Br(),
                        # html.P(id="Manufactor"),
                        # # html.Br(),
                        # html.P(id="YOM"),
                        # # html.Br(),
                        # html.P(id='YOI'),
                        # html.Br(),
                        # html.P(id='YOM'),
                        # html.Br(),

                        html.Br(),
                        html.Br(),
                        # html.P(id="recomendation"),
                        # html.Br(),
                        # dbc.Container([dbc.Col(card_PD_analysis_request)], fluid=True,),
                        # html.Div(id='dummy', style={'display':'none'}),
                        # html.P(id="LADate"),
                        html.Br(),
                        html.Br(),

                        dcc.Markdown(
                            """
                            Powered By: [Lutur Group](home)

                            """
                            # Links: [Source Code](https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-uber-rides-demo) | [Enterprise Demo](https://plotly.com/get-demo/)
                        ),
                        # # Change to side-by-side for mobile layout
                        # html.Div(
                        #     className="row",
                        #
                        # ),
                        # html.P(id="total-rides"),
                        # html.P(id="total-rides-selection"),
                        html.Br(),
                        html.Br(),

                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # #
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # dcc.Markdown(
                        #     """
                        #     Powered By: [Lutur](https://google.com)
                        #
                        #     """
                        #     # Links: [Source Code](https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-uber-rides-demo) | [Enterprise Demo](https://plotly.com/get-demo/)
                        # ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        # dcc.Graph(id="Map")  , #plot the map

                        html.Br(),
                        html.Br(),
                        html.H4("Risk Index", style={'text-align':'center'}),
                        #
                        dcc.Graph(id="Trend", figure=blank_fig(),
                                  config={
                                      "displaylogo": False,
                                      'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines', 'hoverClosestCartesian', 'hoverCompareCartesian']
                                  },  # remove ploty botton
                                  ),   #plot the line chart
                        #show Pd Pattern of the pulse selected
                        html.Br(),
                        html.Br(),
                        html.P(id='Lastmeasurementdate', style={'backgroundColor': 'black', 'color':'white','width':'400px' , 'border':'1.5px black solid','height': '50px','text-align':'center', 'display': 'flex','justifyContent': 'center', 'alignItems': 'center','margin': 'auto','marginTop': 20,'marginBottom': 20}),
                        # dbc.Row([
                        #     dbc.Col(html.Img(id='image', src='', height=500, width=500)),
                        #     dbc.Col(html.Img(id='image', src='', height=500, width=500)),
                        #     dbc.Col(html.Img(id='image', src='', height=500, width=500)),]),
                        #single picture
                        html.Img(id='image', src='',  style={'marginTop': 20,'marginBottom': 20, 'max-width':' 100%', 'max-height': '100%', 'display':'block'})

                    ],
                ),
            ],)
    ],

)


######################################################################################################################################################################################
##################################            call back functions
#
# # #show the data trend of the selected asset
# @callback(
#
#     Output("Trend", "figure"),
#     [Input("dummy", "children")],
#     allow_duplicate=True  # Allow duplicate output
#     # Example input trigger, replace with actual input component and property
# )
# def update_trend_graph(dummy_input):
#     # Replace with your actual data retrieval and processing logic
#     # Sample data generation
#     trace = go.Scatter(x=datetime_list, y=risk_trend, mode='lines+markers', name='Trend Data',line=dict(color='white', width=2))
#     layout = go.Layout(
#         # title='Trend Graph',
#         xaxis={'tickfont': {'color': 'white'}, 'showgrid': False},
#         yaxis={'title': 'Risk Index', 'titlefont': {'color': 'white'}, 'tickfont': {'color': 'white'}, 'showgrid': False},
#
#         paper_bgcolor='rgb(17,17,17)',  # Dark background color
#         plot_bgcolor='rgb(17,17,17)',  # Dark background color for the plot area
#         shapes=[
#             # Green background for y in [1, 4]
#             {
#                 'type': 'rect',
#                 'xref': 'paper',
#                 'yref': 'y',
#                 'x0': 0,
#                 'y0': 1,
#                 'x1': 1,
#                 'y1': 4,
#                 'fillcolor': 'green',
#                 'opacity': 0.5,
#                 'layer': 'below',
#                 'line': {'width': 0},
#             },
#             # Orange background for y in [5, 9]
#             {
#                 'type': 'rect',
#                 'xref': 'paper',
#                 'yref': 'y',
#                 'x0': 0,
#                 'y0': 4,
#                 'x1': 1,
#                 'y1': 9,
#                 'fillcolor': 'orange',
#                 'opacity': 0.5,
#                 'layer': 'below',
#                 'line': {'width': 0},
#             },
#             # Red background for y in [10, 20]
#             {
#                 'type': 'rect',
#                 'xref': 'paper',
#                 'yref': 'y',
#                 'x0': 0,
#                 'y0': 9,
#                 'x1': 1,
#                 'y1': 20,
#                 'fillcolor': 'red',
#                 'opacity': 0.5,
#                 'layer': 'below',
#                 'line': {'width': 0},
#             },
#         ]
#
#     )
#     fig = go.Figure(data=[trace], layout=layout)
#     return fig
#
# #update tag
# @callback(
#     Output("AssetTag", "children", allow_duplicate=True),
#     Output("RatedVoltage", "children", allow_duplicate=True),
#     Output("Lenght", "children", allow_duplicate=True),
#     Output("Manufactor", "children", allow_duplicate=True),
#     Output("YOM", "children", allow_duplicate=True),
#     Output("YOI", "children", allow_duplicate=True),
#     [Input("dummy", "children")],
#     prevent_initial_call='initial_duplicate'
# )
# def update_asset_info(n_intervals):
#     asset_tag = cable_details_list[0][0]
#     rated_voltage = str(cable_details_list[0][1]) + ' kV'
#     lenght = str(cable_details_list[0][2]/1000) +' km'
#     manufactorer = cable_details_list[0][5]
#     YOM = cable_details_list[0][9]
#     YOI = cable_details_list[0][10]
#
#
#     return asset_tag, rated_voltage, lenght, manufactorer, YOM, YOI