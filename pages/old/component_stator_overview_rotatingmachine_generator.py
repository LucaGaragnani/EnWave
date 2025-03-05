import time

import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
from dash import Dash
from dash import callback_context
from dash import dcc
from dash import html
from dash import html, dcc, callback, Input, Output, register_page, ctx
from dash.exceptions import PreventUpdate
from dash import dash_table
import os

import pandas as pd
import numpy as np

from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import plotly.graph_objects as go
import plotly.io as pio


import base64
from datetime import datetime

import mysql.connector

from PIL import Image
import io
# from io import BytesIO #from io import StringIO.
from io import StringIO
import PIL.Image
import dash_bootstrap_components as dbc


from connectors.db_connectors_mysql import get_asset_analysis, get_failure_mechanism_single_asset_list, \
    get_failure_mechanism_subcomponent, get_online_pd_patter_rm, get_online_pd_patter_identification_polarity
from connectors.db_connectors_mysql import get_component_analysis
from connectors.db_connectors_mysql import get_failure_mechanism_list
from connectors.db_connectors_mysql import get_failure_mechanisms_analysis
from connectors.db_connectors_mysql import get_subcomponent_analysis
from connectors.db_connectors_mysql import get_component_list
from connectors.db_connectors_mysql import get_subcomponent_list
from connectors.db_connectors_mysql import get_subcomponent_details
from connectors.db_connectors_mysql import get_online_test_analysis_data
from connectors.db_connectors_mysql import get_offline_test_analysis_data

from connectors.db_connectors_mysql import get_online_test_data
from connectors.db_connectors_mysql import get_online_pd_test_data
from connectors.db_connectors_mysql import get_rfa_test_data
from connectors.db_connectors_mysql import get_online_ew_test_data
from connectors.db_connectors_mysql import get_online_va_test_data
from connectors.db_connectors_mysql import get_offline_test_data
from connectors.db_connectors_mysql import get_offline_pd_test_data
from connectors.db_connectors_mysql import get_ir_test_data, get_pi_test_data, get_wr_test_data, get_ddf_test_data
from connectors.db_connectors_mysql import get_elcid_test_data, get_bump_test_data, get_coreflux_test_data, get_inspection_test_data


from connectors.db_connectors_mysql import update_subcomponent_factors_details
from connectors.db_connectors_mysql import upload_test_data

from functions.analyse_data_mysql import analyse_data
from functions.assess_condition_mysql import assess_condition


from functions.global_variables import asset_selected_details

import math


# opne the page

dash.register_page(__name__, external_stylesheets=[dbc.themes.SPACELAB,dbc.icons.BOOTSTRAP],)


############################         Import data sets from database          ############################################
failure_mechanisms_dict={}
failure_mechanisms_diagnostic_test={}
failure_mechanisms_diagnostic_test_latest_result={}
failure_mechanisms_subcomponent={}
failure_mechanisms_weights={}
def read_inwave_file(file_path):
            """
            Opens and reads a .InWave file as CSV.

            Args:
            - file_path (str): Path to the .InWave file

            Returns:
            - pandas DataFrame: DataFrame containing the data from the .InWave file
            """
            try:
                df = pd.read_csv(file_path)
                return df
            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
                return None
            except Exception as e:
                print(f"Error reading file '{file_path}': {str(e)}")
                return None



# Determine the path of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))


file_dictory = current_directory.replace('pages', 'database')


# Construct the path to the database file
file_path = os.path.join(file_dictory, 'failure_mechanisms_list.csv')




# file_path = '/Users/marianasouzaoliveira/Desktop/InWave_EHV_RMHI/database/failure_mechanisms_list.csv'


subcomponent_list = get_subcomponent_list()


stator_subcomponent_list = []
rotor_subcomponnet_list = []
aux_subcomponent_list = []
for subs in subcomponent_list:
    if subs[3]==1:
        stator_subcomponent_list.append(subs)
    if subs[3]==2:
        rotor_subcomponnet_list.append(subs)
    if subs[3]==3:
        aux_subcomponent_list.append(subs)

data = []
for items in stator_subcomponent_list:
    sub = {}
    sub['id'] = items[0]
    sub['name'] = items[1]
    sub['age_factor'] = 1
    sub['maintenance_factor'] = 1
    sub['failure_factor'] = 1

    data.append(sub)

#insert data form initialization
initial_columns = []
initial_data = []


# Function to fetch online and offline data trends
def fetch_online_data():
    # Simulated online data
    data = {
        'Date': [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3),
                 datetime(2023, 1, 4), datetime(2023, 1, 5)],
        'Red': [10, 15, 7, 12, 9],
        'Yellow': [8, 10, 6, 11, 13],
        'Blue': [12, 11, 9, 13, 8]
    }
    return pd.DataFrame(data)

def fetch_offline_data():
    # Simulated offline data
    data = {
        'Date': [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3),
                 datetime(2023, 1, 4), datetime(2023, 1, 5)],
        'Red': [7, 12, 9, 10, 15],
        'Yellow': [6, 11, 13, 8, 10],
        'Blue': [9, 13, 8, 11, 11]
    }
    return pd.DataFrame(data)




# Example data for charts (replace with your actual data)
x_data = []
y_data1 = []
y_data2 = []

# Chart 1
trace1 = go.Scatter(
    x=x_data,
    y=y_data1,
    mode='lines+markers',
    name='Chart 1',
    marker=dict(color='blue')
)
graph1_layout = go.Layout(
    title = 'Health index trend',
    titlefont=dict(color='#FFFFFF'),  # Title text color (white)
    xaxis=dict(
        title='X Axis',
        titlefont=dict(color='#FFFFFF'),  # X-axis title text color (white)
        tickfont=dict(color='#FFFFFF')  # X-axis tick labels color (white)
    ),
    yaxis=dict(
        title='Y Axis',
        titlefont=dict(color='#FFFFFF'),  # Y-axis title text color (white)
        tickfont=dict(color='#FFFFFF')  # Y-axis tick labels color (white)
    ),
    plot_bgcolor='#232323',  # Background color
    paper_bgcolor='#232323',  # Background color
    # showlegend=True,  # Show legend
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    margin=dict(l=40, r=20, t=30, b=30),  # Adjust margins
    hovermode='closest'
)

# Remove mode bar icons
config = {'displayModeBar': False}

graph1 = dcc.Graph(
    id='graph1_stator',
    figure=dict(data=[trace1], layout=graph1_layout),
    config=config,
    style={'width': '95%', 'height': 'auto','z-index': 2}
)

normalized_values = [(float(i) - min(y_data2)) / (max(y_data2) - min(y_data2)) for i in y_data2]

# Define color scale from green to red
color_scale = [
    [0, '#00FF00'],  # Green color at 0% value
    [0.5, '#FFA500'],  # Orange color at 50% value
    [1, '#FF0000']   # Red color at 100% value
]


# Map normalized values to colors based on color scale
colors = [color_scale[int(round(normalized_value * (len(color_scale) - 1)))] for normalized_value in normalized_values]
# print(colors)
# Chart 2 as Bar chart with color gradient
trace2 = go.Bar(
    x=x_data,
    y=y_data2,
    marker=dict(
        color=normalized_values,
        colorscale=color_scale,

    ),
    name='Chart 2'
)

# Layout for graph2
graph2_layout = go.Layout(
    title='Stator Failure Mechanisms',  # Title
    titlefont=dict(color='#FFFFFF'),  # Title text color (white)
    xaxis=dict(
        title='X Axis',
        titlefont=dict(color='#FFFFFF'),  # X-axis title text color (white)
        tickfont=dict(color='#FFFFFF')  # X-axis tick labels color (white)
    ),
    yaxis=dict(
        title='Y Axis',
        titlefont=dict(color='#FFFFFF'),  # Y-axis title text color (white)
        tickfont=dict(color='#FFFFFF')  # Y-axis tick labels color (white)
    ),
    plot_bgcolor='#232323',  # Background color
    paper_bgcolor='#232323',  # Background color
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    margin=dict(l=40, r=20, t=30, b=30),  # Margins
    hovermode='closest'
)

# Remove mode bar icons
config = {'displayModeBar': False}

# Create dcc.Graph for graph2
graph2 = dcc.Graph(
    id='graph2_stator',
    figure=dict(data=[trace2], layout=graph2_layout),
    config=config,
    style={'width': '95%', 'height': 'auto','z-index': 2}
)


######## failure mode table:

failure_mechanisms_list = get_failure_mechanism_list()




data_for_table = [
    {
        'Failure Mechanism': item[1],
        'Component Affected': item[2],
        'Local effect': item[3],
    }
    for item in failure_mechanisms_list
]


##################################################################################################################################################################################


############################################ custom function



def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template='plotly_dark')
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig




################### plot the app
# Layout of Dash App

layout = html.Div(



    children=[
        dcc.Store(id='store', storage_type='session'),
        # dcc.Location(id='url', refresh=False),
        html.Div(id='content-gen-sta'),

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
                                src=dash.get_asset_url("dash-logo-new-removebg-preview.png"),
                                style={"width": "150px", "height": "auto", "border-radius": "8%"}
                            ), style={"display": "flex", "justify-content": "center", "align-items": "center"},

                            href="home",
                        ),

                        html.Br(),
                        html.Br(),

                        html.H3("Stator Information"),
                        html.P(id='StatorWinding_type'),
                        html.P(id='StatorWinding_thermalClass'),
                        html.P(id='StatorWinding_Impregnation'),
                        html.P(id='NumberOfSlot'),
                        html.P(id="AssetTag", style={'display':'none'}),
                        html.P(id='Type', style={'display':'none'}),
                        html.P(id="RatedVoltage", style={'display':'none'}),
                        html.P(id="Manufactor", style={'display':'none'}),
                        html.P(id="YOM", style={'display':'none'}),
                        html.P(id='YOI', style={'display':'none'}),

                        html.Div(id='dummy1'),
                        html.Br(),
                        html.P(id='Stator Health Index',style={'fontSize': 16}),
                        html.P(id='Latest Assessment Stator'),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            id='button-container1',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Insert new test record', id='open_modal_btn1', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),
                        html.Br(),
                        html.Div(
                            id='button-container',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Update subcomponents details', id='open_modal_btn', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),

                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dcc.Markdown(
                            """
                            Powered By: [InWave](https://www.inwave.au)

                            """
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    style={'height': '100%'},
                    children=[


                        html.Br(),
                        html.Br(),


                        html.Div(className='image-container', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100%','z-index': 1, 'margin-top':'150px'},
                                 children=[
                                html.Img(
                                    src=dash.get_asset_url('stator_picture.jpeg'),  # Replace with your image path
                                    style={'border-radius': '15px','max-width': '50%', 'height': '50%', 'position': 'absolute', 'top':'0',"object-fit": "cover", 'margin-top':'50px'}
                                    # style={'max-width': '100%', 'height': 'auto', 'position': 'relative'}
                                ),
                                html.Div(id='circle1_core', className='circle', children=[
                                    html.Span(id='circle1number_core',children="", className="circle-number", style={"color": "white"},
                                              title="Stator Core Health Index"),
                                ], style={

                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "transparent",  # Custom color
                                        "border-radius": "50%",
                                        "display": "block",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "margin-top": "10px",  # Adjust vertical position
                                        "margin-bottom": "10px",
                                        'opacity': 0.6,
                                        'top':'160px',
                                        'left': '130px',
                                        'position': "absolute",
                                        'cursor':'pointer'
                                    }),

                                html.Div(id='circle2_wind', className='circle',
                                         children=[html.Span(id='circle2number_wind', children="", className="circle-number", style={"color": "white"},
                                              title="Stator Winding Health Index"),
                                ], style={
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "transparent",  # Custom color
                                        "border-radius": "50%",
                                        "display": "block",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "margin-top": "10px",  # Adjust vertical position
                                        "margin-bottom": "10px",
                                        'opacity': 0.6,
                                        'top': '80px',
                                        'left': '-250px',
                                        "position": "relative",
                                        'cursor':'pointer'
                                    }),



                                html.Div(id='circle3_saux', className='circle', children=[
                                    html.Span(id='circle3number_saux',children="", className="circle-number", style={"color": "white"},
                                              title="Stator winding auxiliaries Health Index"),
                                ], style={
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "transparent",  # Custom color
                                        "border-radius": "50%",
                                        "display": "block",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "margin-top": "10px",  # Adjust vertical position
                                        "margin-bottom": "10px",
                                        'opacity': 0.6,
                                        'top': '-150px',
                                        'left': '-190px',
                                        "position": "absolute",
                                        'cursor':'pointer'
                                    }),

                        ]),

                        html.Br(),
                        #
                        html.Br(),

                        #plot the line chart
                        html.Br(),



                        html.Br(),
                        html.Br(),
                        html.Div(
                            id='container-frame',
                            className='graph-container-frame',
                            style={
                                'display': 'flex',
                                'flex-direction': 'column',  # Stack children vertically
                                'align-items': 'stretch',  # Ensure children take full width
                                'padding': '10px',
                                'border-radius': '5px',
                                'margin-top': '50px',
                                'width': '100%',

                            },
                            children=[
                                html.Div(
                                            children=graph1,
                                            style={'margin-bottom': '50px', 'width': '100%'}  # Add some space between the graphs
                                        ),
                                        html.Div(
                                            children=graph2,
                                            style={ 'width': '100%'}
                                        )


                            ]
                        ),
                        #model for legen of Hi
                        html.Div(
                                    id='hi-legend-modal_stator',
                                    style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                                           'transform': 'translate(-50%, -50%)', 'z-index': 1000,},
                                    children=[
                                        html.Div(
                                            id='hi_legend_content_stator',
                                            style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                                                   'border-radius': '5px','max-height': '400px', 'overflow-y': 'auto'},
                                            children=[
                                                html.H5('Health Index Legend',
                                                        id='hi_title',
                                                        style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                                                html.H3(
                                                    'The Health Indexing technique works on the principle of combining a number of different parameters to\n'
                                                    'gain a comprehensive indicator of the asset and its components health.\n'
                                                    'The overall methodology used is visualised below.\n',
                                                    style={'color': 'black', 'font-size': 10, "text-align": "justified"}),


                                                # hi meaning
                                                html.Img(
                                                    src='/assets/hi_meaning.png',  # Replace with the actual path to your image
                                                    style={'width': '100%', 'margin-top': '10px', 'border-radius': '5px'}
                                                ),
                                                html.H3(

                                                    'The overall methodology utilized as per Cigree TB 912 is visualised below.\n',
                                                    style={'color': 'black', 'font-size': 10, "text-align": "justified"}),
                                                # hi calculation
                                                html.Img(
                                                    src='/assets/healthindex_calculation.png',  # Replace with the actual path to your image
                                                    style={'width': '100%', 'margin-top': '10px', 'border-radius': '5px'}
                                                ),


                                                html.Div(
                                                    children=[
                                                        html.Button('Ok', id='confirm-hi-legend_stator', disabled=False,
                                                                    style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                                           'background-color': 'grey', 'border-color': 'black','font-weight': 'bold',
                                                                           'text-align': 'center', 'margin-right': '40px'}),
                                                    ],
                                                    style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                        #  Hidden div to capture right-click event
                        html.Div(id='right-click-data-hi', style={'display': 'none'}),
                        #model for legen of Failure mechanisms
                        html.Div(
                                    id='fm-legend-modal_stator',
                                    style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                                           'transform': 'translate(-50%, -50%)', 'z-index': 1000,},
                                    children=[
                                        html.Div(
                                            id='fm_legend_content_stator',
                                            style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                                                   'border-radius': '5px','max-height': '400px', 'overflow-y': 'auto'},
                                            children=[
                                                html.H5('Failure Mechanisms Legend',
                                                        id='fm_title',
                                                        style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                                                html.H3(
                                                    'A failure mechanism is a specific process that leads to the degradation of a component of the asset and could lead to its failure.'
                                                    'The failure mechanism percentage represents the likelihood of its presence based on the diagnostic test results.',
                                                    style={'color': 'black', 'font-size': 10, "text-align": "justified"}),

                                                html.H3(
                                                    'Each failure mechanisms analysed is described below:',
                                                    style={'color': 'black', 'font-size': 10, "text-align": "justified"}),

                                                dash_table.DataTable(
                                                                        columns=[
                                                                            {'name': 'Failure Mechanism', 'id': 'Failure Mechanism'},
                                                                            {'name': 'Component Affected', 'id': 'Component Affected'},
                                                                            {'name': 'Local effect', 'id': 'Local effect'}
                                                                        ],
                                                                        data=data_for_table,
                                                                        style_table={'overflowX': 'auto'},
                                                                        style_cell={
                                                                            'textAlign': 'left',
                                                                            'padding': '5px',
                                                                            'color': 'black',
                                                                        },
                                                                        style_header={
                                                                            'backgroundColor': 'rgb(230, 230, 230)',
                                                                            'fontWeight': 'bold'
                                                                        },
                                                                        page_size=10
                                                ),


                                                html.Div(
                                                    children=[
                                                        html.Button('Ok', id='confirm-fm-legend_stator', disabled=False,
                                                                    style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                                           'background-color': 'grey', 'border-color': 'black','font-weight': 'bold',
                                                                           'text-align': 'center', 'margin-right': '40px'}),
                                                    ],
                                                    style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                        #  Hidden div to capture right-click event
                        html.Div(id='right-click-data-fm', style={'display': 'none'}),

                        html.Br(),
                        html.Br(),
                        dbc.Container(fluid=True,
                                      style={'backgroundColor': 'transparent', 'color': 'white', 'height': '150vh','textAlign': 'center','margin-bottom':'30px',
                                             'display': 'flex',  # Enable flexbox for centering
                                             'flexDirection': 'column',  # Stack the elements vertically
                                             'alignItems': 'center',  # Horizontally center

                                             },
                                      children=[
                                          # html.H1(children='Data Trends', style={'textAlign': 'center'}),

                                          dbc.Row([
                                              dbc.Col(dbc.Button("Online Results Trend", id="online-button",
                                                                 color="primary", className="mb-3", style ={'width': '300px', 'background-color': 'darkgrey', 'border-color': 'grey', 'color': 'black',
                                                                'font-weight': 'bold'}), width=10, style={'margin-bottom':'20px'}),
                                              dbc.Col(dbc.Button("Offline Results Trend", id="offline-button",
                                                                 color="primary", className="mb-3",style ={'width': '300px', 'background-color': 'darkgrey', 'border-color': 'grey', 'color': 'black',
                                                                'font-weight': 'bold'}), width=10, style={'margin-bottom':'0px'}),

                                          ]),

                                          dbc.Row([
                                              dbc.Col(id='online-container', width=12, style={'margin-bottom':'20px'}),
                                              dbc.Col(id='offline-container', width=12, style={'margin-bottom':'20px'}),
                                          ]),
                                      ]),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dbc.Container(
                            id='raw-data-graph-container-stator',
                            style={'display': 'none', 'padding': '10px', 'width': '100%'}  # Initial style can be hidden
                        ),
                        dbc.Container(
                            id='graph_card_rm',
                            children=[
                                dbc.Card(
                                    dbc.CardBody(


                                            html.Div(
                                                style={'display': 'flex', 'alignItems': 'center',
                                                       'justifyContent': 'center'},  # Center contents
                                                children=[
                                                    # Image component
                                                    html.Img(src='assets/pattern_exmple.jpg',
                                                             style={'width': '200px', 'height': 'auto', 'padding':'10px'}),

                                                    # Container for labels
                                                    html.Div(
                                                        style={'marginLeft': '20px'},  # Space between image and labels
                                                        children=[
                                                            html.P('Identification', id='Identification', style={'fontSize': '12px'}),
                                                            # html.P(id='Po'),
                                                        ]
                                                    )
                                                ]
                                            )

                                    ),
                                    style={
                                        'width': '100%',
                                        'borderRadius': '15px',  # Rounded corners
                                        'backgroundColor': 'grey',  # Background color
                                        'borderColor': 'grey',  # Border color
                                        'borderWidth': '1px',  # Border width
                                        'borderStyle': 'solid'  # Solid border style
                                    }  # Card styling
                                )
                            ],
                            style={'padding': '20px', 'display':'none'}  # Container padding
                        ),
                        html.Br(),
                    ],
                ),

            ],),
        html.Div(
            id='modal_factors_stator',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Stator Subcomponent HI Factors', style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dash_table.DataTable(
                            id='editable-table',
                            columns=[{'name': 'Subcomponent', 'id': 'name'},
                                     {'name':'Age Factor', 'id':'age_factor', 'editable': True,'type': 'numeric'},
                                     {'name':'Maintenance Factor', 'id':'maintenance_factor', 'editable': True,'type': 'numeric'},
                                     {'name': 'Failure Factor', 'id':'failure_factor', 'editable':True,'type': 'numeric'},
                                     ],
                            data=data,
                            style_cell={'textAlign': 'center', 'color':'black'},
                        ),

                        html.Div(
                            children=[
                                html.Button('Update', id='save_modal_btn',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right':'40px'}),
                                html.Button('Exit', id='close_modal_btn',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'red', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9}),
                            ],
                            style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
                        ),
                    ]
                )
            ]
        ),
        html.Div(
            id='modal_insert_data1',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Select test type',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dcc.Dropdown(
                            id='dropdown-menu',
                            options=[
                                {'label': 'Online test', 'value': '1'},
                                {'label': 'Offline test', 'value': '2'},
                            ],
                            value='',
                            # style={'backgroundColor': '#000000', 'color': 'white', 'opacity':'1'},

                        ),

                        html.Div(
                            children=[
                                html.Button('Next', id='open_modal_btn2',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_modal_btn1',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'red', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9}),
                            ],
                            style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
                        ),
                    ]
                )
            ]
        ),

        html.Div(
            id='modal_insert_data2',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content2',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Select test from the list',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dcc.Dropdown(
                            id='dropdown-menu2',
                            options=[

                            ],
                            value='',
                            # style={'backgroundColor': 'black', 'color': 'white', 'opacity':'1'},
                        ),

                        html.Div(
                            children=[
                                html.Button('Next', id='open_modal_btn3',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_modal_btn2',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'red', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9}),
                            ],
                            style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
                        ),
                    ]
                )
            ]
        ),
        html.Div(
            id='modal_insert_data3',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content3',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Insert the data below',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dash_table.DataTable(
                            id='editable-table_data',
                            columns=initial_columns,
                            data=initial_data,
                            style_cell={'textAlign': 'center', 'color':'black'},
                            editable=True,  # Enable editing in cells
                            row_deletable=True,

                        ),
                        html.Button('+', id='add_row_btn', n_clicks=0, style={'margin-top': '10px'}),

                        html.Div(
                            children=[
                                html.Button('Confirm', id='save_modal_btn3',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_modal_btn3',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'red', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9}),
                            ],
                            style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'}
                        ),
                    ]
                )
            ]
        )
    ])





#######################################################################################################################
#######################         call back function

asset_selected_details = []


@callback(
    Output('content-gen-sta', 'children'),
    Input('store', 'data'),
    config_prevent_initial_callbacks=True
)
def display_selected_asset(selected_asset):
    # print('stator',selected_asset)
    if selected_asset is not None and len(selected_asset) != 0:
        # asset_selected_details.append(selected_asset['key'])
        # Extract the customdata from the first point
        # global asset_selected_details
        # asset_selected_details.append(selected_asset['key'])
        # custom_data = selected_asset.get('points', [{}])[0].get('customdata', [])
        # print('listaa',asset_selected_details)
        # Format it for display (convert list to string, for example)
        # content = ', '.join(map(str, custom_data))
        global asset_selected_details
        asset_selected_details.insert(0, selected_asset)
        content = ''
    else:
        content = ''

    return content


#update information in the dashboard
@callback(
    Output("AssetTag", "children",allow_duplicate=True),
    Output("Type", "children",allow_duplicate=True),
    Output("RatedVoltage", "children",allow_duplicate=True),
    Output("Manufactor", "children",allow_duplicate=True),
    Output("YOM", "children",allow_duplicate=True),
    Output("YOI", "children",allow_duplicate=True),
    Output('StatorWinding_type', "children",allow_duplicate=True),
    Output('StatorWinding_thermalClass', "children",allow_duplicate=True),
    Output('StatorWinding_Impregnation', "children",allow_duplicate=True),
    Output('NumberOfSlot', 'children',allow_duplicate=True),
    Output('Stator Health Index', 'children',allow_duplicate=True),
    Output('Stator Health Index', 'className',allow_duplicate=True),
    Output('Latest Assessment Stator', 'children',allow_duplicate=True),
    Output('circle1number_core', 'children',allow_duplicate=True),
    Output('circle1_core', 'style',allow_duplicate=True),
    Output('circle2number_wind', 'children',allow_duplicate=True),
    Output('circle2_wind', 'style',allow_duplicate=True),
    Output('circle3number_saux', 'children',allow_duplicate=True),
    Output('circle3_saux', 'style',allow_duplicate=True),
    # Output('circle-number', 'children'),
    # Output('circle-div', 'style'),
    Output('graph1_stator', 'figure'),
    Output('graph2_stator', 'figure'),
    # Input('store', 'data'),
    [Input("dummy1", "children")],
    prevent_initial_call='initial_duplicate'
)
def update_asset_info(store):

    # print('asset_list', asset_selected_details)
    # print(asset_selected_details)
    global asset_selected_details

    if len(asset_selected_details)!=0:

        asset_tag ='Asset: {}'.format(asset_selected_details[0]['points'][0]['customdata'][1])

        type = 'Type: {} - {}'.format(asset_selected_details[0]['points'][0]['customdata'][11], asset_selected_details[0]['points'][0]['customdata'][12])
        rated_voltage = 'Rated Voltage: {}kV'.format(asset_selected_details[0]['points'][0]['customdata'][6])
        manufactor = asset_selected_details[0]['points'][0]['customdata'][3]
        yom = 'YOM {}'.format(asset_selected_details[0]['points'][0]['customdata'][4])
        yoi ='YOI {}'.format(asset_selected_details[0]['points'][0]['customdata'][5])
        stator_winding_type = 'Stator Winding: {}'.format(asset_selected_details[0]['points'][0]['customdata'][14])
        stator_winding_thermal = 'Winding Thermal Class: {}'.format(asset_selected_details[0]['points'][0]['customdata'][17])
        impregnation = '{}'.format(asset_selected_details[0]['points'][0]['customdata'][15])
        numb_slot = 'Number of slot {}'.format(asset_selected_details[0]['points'][0]['customdata'][16])


        #update circles for subcomponent
        analysis_id = get_asset_analysis(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])

        component_list = get_component_list()
        subcomponent_list = get_subcomponent_list()
        subcomponent_details_list = get_subcomponent_details(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        try:
            subcomponent_analysis_list = get_subcomponent_analysis(analysis_id[-1][0])
        except IndexError:
            subcomponent_analysis_list = []

        component_analysis_list = []
        component_analysis_date_list = []
        for analysis in analysis_id:
            component_analysis_date_list.append(analysis[1])
            component_analysis = get_component_analysis(analysis[0])
            component_analysis_list.append(component_analysis)

        # print(component_analysis_date_list)

        stator_hi_trend = []
        rotor_hi_trend = []
        aux_hi_trend = []
        for anal in component_analysis_list:
            for comp in anal:
                if comp[2]==1:
                    stator_hi_trend.append(comp[3])
                if comp[2]==2:
                    rotor_hi_trend.append(comp[3])
                if comp[2]==3:
                    aux_hi_trend.append(comp[3])


        # print('statorhi',stator_hi_trend)
        try:
            latest_stator_health_index = 'Stator Health Index: {} / 5'.format(stator_hi_trend[-1])

            hi_className = ''
            latest_stator_hi_date = 'Date: {}'.format(component_analysis_date_list[-1])
        except IndexError:
            latest_stator_health_index = 'Stator Health Index: NA / 5'

            hi_className = ''
            latest_stator_hi_date = 'Date: NA'
        #update graph 1

        # Update color based on the last health index value
        color = '#FFFFFF'  # Default to white
        try:
            if 4 < stator_hi_trend[-1] <= 5:
                color = '#8B0000'  # Dark red
                hi_className = 'dark-red'
            elif 3 < stator_hi_trend[-1] <= 4:
                color = '#FF0000'  # Red
                hi_className = 'red'

            elif 2 < stator_hi_trend[-1] <= 3:
                color = '#FFA500'  # Orange
                hi_className = 'orange'

            elif 1 < stator_hi_trend[-1] <= 2:
                color = '#FFD700'  # Dark yellow (gold)
                hi_className = 'gold'

            elif 0 < stator_hi_trend[-1] <= 1:
                color = '#006400'  # Dark green
                hi_className = 'dark_green'
        except IndexError:
            color = color
            hi_className= 'grey'
            component_analysis_date_list = [datetime.now()]






        updated_trace1 = go.Scatter(
            x=component_analysis_date_list,
            y=stator_hi_trend,
            mode='lines+markers',
            name='Chart 1',
            marker=dict(color='{}'.format(color))
        )
        graph1_layout = go.Layout(
            title='Stator Health index trend',
            titlefont=dict(color='#FFFFFF', size=14),  # Title text color (white)
            xaxis=dict(
                # title='Date',
                titlefont=dict(color='#FFFFFF',size=10),  # X-axis title text color (white)
                tickfont=dict(color='#FFFFFF',size=6),  # X-axis tick labels color (white)
                showgrid=False,
                tickangle = 45,
                tickvals=component_analysis_date_list[::len(component_analysis_date_list) // 5],
            ),
            yaxis=dict(
                title='HI',
                titlefont=dict(color='#FFFFFF', size=12),  # Y-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                range=[0,5],# Y-axis tick labels color (white)
                showgrid=False
            ),
            plot_bgcolor='rgb(17,17,17)',  # Background color
            paper_bgcolor='rgb(17,17,17)',  # Background color
            # showlegend=True,  # Show legend
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            margin=dict(l=40, r=20, t=40, b=40),  # Adjust margins
            hovermode='closest',
            # width=900,
            height=400
        )

        # Remove mode bar icons
        config = {'displayModeBar': False, 'responsive':True}



        updated_graph1 = dict(data=[updated_trace1], layout=graph1_layout)



        # print(stator_hi_trend)


        #latest component hi
        stator_hi = 0
        try:
            for comp in component_analysis_list[-1]:
                if comp[2]==1:
                    stator_hi=comp[3]
        except IndexError:
            None

        # print(stator_hi)

        #subcomponent analysis
        stator_sub_list = []
        stator_sub_id_list = []
        rotor_sub_list = []
        rotor_sub_id_list = []
        aux_sub_list = []
        aux_sub_id_list = []
        for items in subcomponent_list:
            if items[3]==1:
                stator_sub_list.append(items)
                stator_sub_id_list.append(items[0])
            if items[3]==2:
                rotor_sub_list.append(items)
                rotor_sub_id_list.append(items[0])
            if items[3]==3:
                aux_sub_list.append(items)
                aux_sub_id_list.append(items[0])

        # print(component_list)
        # print(subcomponent_list)
        # print(stator_sub_list)
        # print(subcomponent_analysis_list)

        core_hi = 0
        winding_hi = 0
        winding_aux_hi = 0

        for sunan in subcomponent_analysis_list:
            if sunan[2] in stator_sub_id_list:
                if sunan[2]==1:
                    core_hi=sunan[3]
                if sunan[2]==2:
                    winding_hi=sunan[3]
                if sunan[2]==3:
                    winding_aux_hi=sunan[3]

        # print(core_hi, winding_hi, winding_aux_hi)
        health_index_subcomp_dict = {}
        health_index_subcomp_dict['1'] = 0
        health_index_subcomp_dict['2'] = 0
        health_index_subcomp_dict['3'] = 0

        #update circles of subcomponents
        circle_update_list = []


        circle = 1
        for values in [core_hi, winding_hi, winding_aux_hi]:
            # # Determine color based on condition
            if 0 < values <= 1:
                color = "#006400"
                health_index_subcomp_dict['{}'.format(circle)] = {'value': values, 'color': color}
            elif 1 < values <= 2:
                color = "green"
                health_index_subcomp_dict['{}'.format(circle)] = {'value': values, 'color': color}
            elif 2 < values <= 3:
                color = "orange"
                health_index_subcomp_dict['{}'.format(circle)] = {'value': values, 'color': color}
            elif 3 < values <= 4:

                color = "#BF5700"
                health_index_subcomp_dict['{}'.format(circle)] = {'value': values, 'color': color}
            elif 4 < values <= 5:
                color = "red"
                health_index_subcomp_dict['{}'.format(circle)] = {'value': values, 'color': color}
            else:
                color = "grey"  # Default color if condition is out of expected range
                health_index_subcomp_dict['{}'.format(circle)] = {'value': values, 'color': color}

            # Use condition as circle number

            if circle == 1:
                circle_children = [
                    html.Span(id='circle1number_core', children='Core\n {}'.format(values), className="circle-number",
                              style={"color": "white"})
                ]

                circle_style = {
                    "font-size": "10px",  # Set the font size to 8 pixels
                    "white-space": "pre-line",
                    'align-items': 'center',
                    'display': 'flex',
                    'justify-content': 'center',  # Center content horizontally
                    # 'align-items': 'flex-start',  # Align items at the top
                    "border-radius": "10%",
                    'height': '40px',  # Set a fixed height for the rectangle
                    'width': '100px',  # Set a fixed width for the rectangle
                    'padding': '10px',  # Add some padding
                    'border': '1px solid black',  # Optional: Add a border for visibility
                    'background-color': color,  # Optional: Background color
                    # 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Optional: Shadow for depth
                    'position': 'relative',  # Keep it in the document flow
                    'text-align': 'center',
                    'opacity': 0.9,
                }

                circle_style.update({'top': '30px', 'left': '230px'})

            if circle == 2:
                circle_children = [
                    html.Span(id='circle2number_wind', children='Winding\n {}'.format(values), className="circle-number",
                              style={"color": "white"})
                ]

                circle_style = {
                    "font-size": "10px",  # Set the font size to 8 pixels
                    "white-space": "pre-line",
                    'align-items': 'center',
                    'display': 'flex',
                    'justify-content': 'center',  # Center content horizontally
                    # 'align-items': 'flex-start',  # Align items at the top
                    "border-radius": "10%",
                    'height': '40px',  # Set a fixed height for the rectangle
                    'width': '100px',  # Set a fixed width for the rectangle
                    'padding': '10px',  # Add some padding
                    'border': '1px solid black',  # Optional: Add a border for visibility
                    'background-color': color,  # Optional: Background color
                    # 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Optional: Shadow for depth
                    'position': 'relative',  # Keep it in the document flow
                    'text-align': 'center',
                    'opacity': 0.9,
                }

                circle_style.update({'top': '20px', 'left': '-170px'})

            if circle == 3:
                circle_children = [
                    html.Span(id='circle3number_saux', children='Auxiliaries\n {}'.format(values), className="circle-number",
                              style={"color": "white"})]

                circle_style = {
                    "font-size": "10px",  # Set the font size to 8 pixels
                    "white-space": "pre-line",
                    'align-items': 'center',
                    'display': 'flex',
                    'justify-content': 'center',  # Center content horizontally
                    # 'align-items': 'flex-start',  # Align items at the top
                    "border-radius": "10%",
                    'height': '40px',  # Set a fixed height for the rectangle
                    'width': '100px',  # Set a fixed width for the rectangle
                    'padding': '10px',  # Add some padding
                    'border': '1px solid black',  # Optional: Add a border for visibility
                    'background-color': color,  # Optional: Background color
                    # 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',  # Optional: Shadow for depth
                    'position': 'relative',  # Keep it in the document flow
                    'text-align': 'center',
                    'opacity': 0.9,
                }

                circle_style.update({'top': '-120px', 'left': '50px'})

            circle_update_list.append(circle_children)
            circle_update_list.append(circle_style)

            circle += 1


        # print(stator_sub_id_list)
        # print(subcomponent_details_list)

        #failure mechanisms
        failure_mechanism_list = get_failure_mechanism_single_asset_list(1)
        try:
            failure_mechanism_analysis = get_failure_mechanisms_analysis(analysis_id[-1][0])
        except IndexError:
            failure_mechanism_analysis =[]
            for value in failure_mechanism_list:
                temp = [0,0,value[0],0]
                failure_mechanism_analysis.append(temp)
        # print(failure_mechanism_analysis)
        # print(failure_mechanism_list)

        #filter based on subcomponent
        # filter based on subcomponent stator = 1
        failure_mechanisms_subcomponent = get_failure_mechanism_subcomponent(1)
        stator_fm_id = failure_mechanisms_subcomponent

        fm_label = []
        for labels in failure_mechanism_list:
            if labels[0] in stator_fm_id:
                fm_label.append(labels[1])

        fm_value = []
        for values in failure_mechanism_analysis:
            if values[2] in stator_fm_id:
                fm_value.append(values[3])

        # print(fm_label)
        # print(fm_value)
        # Combine labels and values into a list of tuples
        fm_data = list(zip(fm_label, fm_value))

        # Sort the list of tuples by value in descending order
        fm_data_sorted = sorted(fm_data, key=lambda x: x[1], reverse=True)

        # Unzip the sorted list back into two separate lists
        sorted_fm_label, sorted_fm_value = zip(*fm_data_sorted)

        # Update color based on sorted values
        color = []
        for value in sorted_fm_value:
            if value <= 30:
                color.append("#00FF00")
            elif 30 < value <= 50:
                color.append('#FFFF00')
            elif 50 < value <= 80:
                color.append('#FFA500')
            elif 80 < value <= 90:
                color.append('#FF0000')
            elif value > 90:
                color.append('#8B0000')


        ymin = 0
        ymax = 100
        fm_value_max = max(fm_value)
        if fm_value_max <= 1:
            ymax = 5
        elif 1 < fm_value_max <= 5:
            ymax = 10
        elif 5 < fm_value_max <= 10:
            ymax = 20
        elif 10 < fm_value_max <= 20:
            ymax = 50
        elif 20 < fm_value_max <= 50:
            ymax = 75
        elif fm_value_max > 50:
            ymax = 100
        # Map normalized values to colors based on color scale

        # Chart 2 as Bar chart with color gradient
        updated_trace2 = go.Bar(
            x=sorted_fm_label,  # Use sorted labels
            y=sorted_fm_value,  # Use sorted values

            text=sorted_fm_label,
            textposition='outside',
            textangle=-30,
            textfont=dict(color='white', size=18, family='Cabin'),
            marker=dict(
                color=color,
                cmin=0,
                cmax=100,
            ),
            name='Chart 2'
        )



        # Layout for graph2
        graph2_layout = go.Layout(
            title='Stator Failure Mechanism Analysis',  # Title
            titlefont=dict(color='#FFFFFF', size=14),  # Title text color (white)
            xaxis=dict(
                # title='X Axis',
                titlefont=dict(color='#FFFFFF', family='Cabin', size=8),  # X-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                showticklabels=False, # X-axis tick labels color (white)
                showgrid=False
            ),

            yaxis=dict(
                title='Percentage [%]',
                titlefont=dict(color='#FFFFFF', size=12),  # Y-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                range=[ymin, ymax], # Y-axis tick labels color (white)
                showgrid=False
            ),
            plot_bgcolor='rgb(17,17,17)',  # Background color
            paper_bgcolor='rgb(17,17,17)',  # Background color
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            margin=dict(l=40, r=20, t=40, b=40),  # Margins
            hovermode='closest',
            # width=900,
            height=400
        )

        # Remove mode bar icons
        config = {'displayModeBar': False, 'responsive':True}

        updated_graph2 = dict(data=[updated_trace2], layout=graph2_layout)

    else:
        asset_tag = ''
        type = ''
        rated_voltage = ''
        manufactor= ''
        yom = ''
        yoi = ''
        stator_winding_type = ''
        stator_winding_thermal = ''
        impregnation = ''
        numb_slot = ''

        latest_stator_health_index = ''
        hi_className = ''
        latest_stator_hi_date = ''


        circle_update_list = []

        circle_style1 = {
            "width": "40px",
            "height": "40px",
            "background-color": "grey",  # Custom color
            "border-radius": "50%",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "margin-top": "10px",  # Adjust vertical position
            "margin-bottom": "10px",
            'opacity': 0.6,
            'top':'50px',
            'left': '130px',
            'position': "relative",
            'cursor':'pointer'
        }

        circle_style2 = {
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "grey",  # Custom color
                                        "border-radius": "50%",
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "margin-top": "10px",  # Adjust vertical position
                                        "margin-bottom": "10px",
                                        'opacity': 0.6,
                                        'top': '-100px',
                                        'left': '-250px',
                                        "position": "relative",
                                        'cursor':'pointer'
                                    }

        circle_style3 = {
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "grey",  # Custom color
                                        "border-radius": "50%",
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "margin-top": "10px",  # Adjust vertical position
                                        "margin-bottom": "10px",
                                        'opacity': 0.6,
                                        'top': '-150px',
                                        'left': '-190px',
                                        "position": "relative",
                                        'cursor':'pointer'
                                    }

        circle_children1 = [
            html.Span(id='circle1number_core', children='NA', className="circle-number",
                      style={"color": "white"})
        ]


        circle_children2 = [
                html.Span(id='circle2number_wind', children='NA', className="circle-number",
                          style={"color": "white"})
        ]

        circle_children3 = [
                html.Span(id='circle3number_saux', children='NA', className="circle-number",
                          style={"color": "white"})
        ]


        circle_update_list.append(circle_children1)
        circle_update_list.append(circle_style1)

        circle_update_list.append(circle_children2)
        circle_update_list.append(circle_style2)

        circle_update_list.append(circle_children3)
        circle_update_list.append(circle_style3)

        # update graph 1

        # update graph 1
        component_analysis_date_list=[]
        stator_hi_trend=[]

        updated_trace1 = go.Scatter(
            x=component_analysis_date_list,
            y=stator_hi_trend,
            mode='lines+markers',
            name='Chart 1',
            marker=dict(color='blue')
        )
        graph1_layout = go.Layout(
            title='Stator Health index trend',
            titlefont=dict(color='#FFFFFF'),  # Title text color (white)
            xaxis=dict(
                title='Date',
                titlefont=dict(color='#FFFFFF'),  # X-axis title text color (white)
                tickfont=dict(color='#FFFFFF')  # X-axis tick labels color (white)
            ),
            yaxis=dict(
                title='HI',
                titlefont=dict(color='#FFFFFF'),  # Y-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                range=[0, 5]  # Y-axis tick labels color (white)
            ),
            plot_bgcolor='#232323',  # Background color
            paper_bgcolor='#232323',  # Background color
            # showlegend=True,  # Show legend
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            margin=dict(l=40, r=20, t=30, b=30),  # Adjust margins
            hovermode='closest',
            width=900,
            height=400,
        )

        # Remove mode bar icons
        config = {'displayModeBar': False, 'responsive': True}

        updated_graph1 = dict(data=[updated_trace1], layout=graph1_layout)

        # print(stator_hi_trend)

        fm_label=[]
        fm_value=[]
        color = []
        ymin=0
        ymax=0

        # Chart 2 as Bar chart with color gradient
        updated_trace2 = go.Bar(
            x=fm_label,
            y=fm_value,
            marker=dict(
                color=color,
                # colorscale=color,
                cmin=0,
                cmax=100,

            ),
            name='Chart 2'
        )

        # Layout for graph2
        graph2_layout = go.Layout(
            title='Stator Failure Mechanism Analysis',  # Title
            titlefont=dict(color='#FFFFFF'),  # Title text color (white)
            xaxis=dict(
                # title='X Axis',
                titlefont=dict(color='#FFFFFF'),  # X-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                showticklabels=False  # X-axis tick labels color (white)
            ),

            yaxis=dict(
                title='Percentage [%]',
                titlefont=dict(color='#FFFFFF'),  # Y-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                range=[ymin, ymax]  # Y-axis tick labels color (white)
            ),
            plot_bgcolor='#232323',  # Background color
            paper_bgcolor='#232323',  # Background color
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            margin=dict(l=40, r=20, t=30, b=30),  # Margins
            hovermode='closest',
            width=900,
            height=400,
        )

        # Remove mode bar icons
        config = {'displayModeBar': False, 'responsive':True}

        updated_graph2 = dict(data=[updated_trace2], layout=graph2_layout)



    return asset_tag, type, rated_voltage, manufactor, yom, yoi, stator_winding_type, stator_winding_thermal, impregnation,numb_slot, latest_stator_health_index, hi_className,latest_stator_hi_date, circle_update_list[0], circle_update_list[1], circle_update_list[2], circle_update_list[3], circle_update_list[4], circle_update_list[5], updated_graph1, updated_graph2


#callback for health index factor update
@callback(
    Output('modal_factors_stator', 'style'),
    [Input('open_modal_btn', 'n_clicks'),
     Input('close_modal_btn', 'n_clicks'),
     Input('save_modal_btn', 'n_clicks')],
    [State('modal_factors_stator', 'style'),State('editable-table', 'data')]
)
def toggle_modal(open_clicks, close_clicks, save_clicks, current_style,table_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_style

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'open_modal_btn' and open_clicks:
        current_style['display'] = 'block'
    elif trigger_id == 'close_modal_btn' and close_clicks:
        current_style['display'] = 'none'
    elif trigger_id == 'save_modal_btn' and save_clicks:
        # Process saving to database or any other action needed

        # Save selected_value to database
        asset_id=asset_selected_details[0]['points'][0]['customdata'][0]

        # print(table_data)

        for dicts in table_data:
            subcomponent_id = dicts['id']
            age_factor = dicts['age_factor']
            maintenance_factor = dicts['maintenance_factor']
            failure_factor = dicts['failure_factor']

            if failure_factor > 5:
                failure_factor=5
            if age_factor >5:
                age_factor=5
            if maintenance_factor>5:
                maintenance_factor=5

            update_subcomponent_factors_details(age_factor, maintenance_factor, failure_factor, subcomponent_id, asset_id)
            time.sleep(0.5)
            assess_condition(asset_id)

        # print(table_data_dict)

        current_style['display'] = 'none'



    return current_style



#######callback for data entry

@callback(
    Output('modal_insert_data1', 'style'),
    [Input('open_modal_btn1', 'n_clicks'),
     Input('close_modal_btn1', 'n_clicks'),
     Input('open_modal_btn2', 'n_clicks')],
    [State('modal_insert_data1', 'style'),
     State('dropdown-menu', 'value')]
)
def toggle_modal(open_clicks, close_clicks, next_clicks, current_style, selected_value):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_style

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'open_modal_btn1' and open_clicks:
        current_style['display'] = 'block'
    elif trigger_id == 'close_modal_btn1' and close_clicks:
        current_style['display'] = 'none'
    elif trigger_id == 'open_modal_btn2' and next_clicks:
        current_style['display'] = 'none'

    return current_style


@callback(
    Output('modal_insert_data2', 'style'),
    [Input('open_modal_btn2', 'n_clicks'),
     Input('close_modal_btn2', 'n_clicks'),
     Input('open_modal_btn3', 'n_clicks')],
    [State('modal_insert_data2', 'style'), State('modal_insert_data1', 'style')]
)
def show_modal2(n_clicks, close, next, modal2_style, modal1_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return modal2_style

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'open_modal_btn2' and n_clicks:
        modal1_style['display'] = 'none'
        modal2_style['display'] = 'block'


    if trigger_id == 'close_modal_btn2' and close:
        modal2_style['display'] = 'none'
    elif trigger_id == 'open_modal_btn3' and next:
        modal2_style['display'] = 'none'


    return modal2_style

#update content drop down menu
@callback(
    Output('dropdown-menu2', 'options'),
    [Input('dropdown-menu', 'value')]
)
def update_dropdown_options(selected_value):
    if selected_value == '1':
        return [
            {'label': 'Partial Discharge', 'value': '11'},
            {'label': 'Endwinding Vibration', 'value': '12'},
        ]
    elif selected_value == '2':
        return [
            {'label': 'Insulation Resistance', 'value': '1'},
            {'label': 'Polarization Index', 'value': '2'},
            {'label': 'Winding Resistance', 'value': '3'},
            {'label': 'Dielectric Dissipation Factor', 'value': '4'},
            {'label': 'Partial Discharge', 'value': '5'},
            {'label': 'Inspection', 'value': '6'},
            {'label': 'Core Flux', 'value': '7'},
            {'label': 'Elcid', 'value': '8'},
            {'label': 'Bump Test', 'value': '9'},
        ]
    else:
        return []  # Return empty list or default options



#open insert data form
@callback(
    Output('modal_insert_data3', 'style'),
    [Input('open_modal_btn3', 'n_clicks'),
     Input('close_modal_btn3', 'n_clicks'),
     Input('save_modal_btn3', 'n_clicks')],
    [State('modal_insert_data3', 'style'), State('modal_insert_data2', 'style'),State('editable-table_data', 'data'),State('dropdown-menu2', 'value')]
)
def show_modal2(n_clicks, close, save, modal3_style, modal2_style, inserted_data,diagnostic_test_id):
    ctx = dash.callback_context
    if not ctx.triggered:
        return modal3_style

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'open_modal_btn3' and n_clicks:
        modal3_style['display'] = 'block'
        modal2_style['display'] = 'none'

    if trigger_id == 'close_modal_btn3' and close:
        modal3_style['display'] = 'none'

    if trigger_id == 'save_modal_btn3' and save:

        asset_id = asset_selected_details[0]['points'][0]['customdata'][0]
        today = datetime.today()
        formatted_date = today.strftime('%d/%m/%Y')

        diagnostic_test_id= int(diagnostic_test_id)

        #define the right subcompoent id based on thest carried out
        if diagnostic_test_id in (1,2,3,4,5,11,9,12):

            subcomponent_id = 2
        if diagnostic_test_id in (7,8):
            subcomponent_id = 1

        #create data list

        for set in inserted_data:
            # print(set)
            complete_data_list = [formatted_date,asset_id, subcomponent_id, diagnostic_test_id]
            phase=0
            for values in list(set.values()):

                if phase==0:
                    complete_data_list.append(values.casefold())
                if phase!=0:
                    complete_data_list.append(values)
                phase+=1
            # print(complete_data_list)
            # print(fuck)

            upload_test_data(complete_data_list)

            modal3_style['display'] = 'none'

        #analyse the result combining data of the same date
        analyse_data(asset_id)
        time.sleep(0.5)
        assess_condition(asset_id)

    return modal3_style


#update content insert data form
@callback(
    Output('editable-table_data', 'columns'),
        Output('editable-table_data', 'data', allow_duplicate=True),
    [Input('dropdown-menu2', 'value')],
    [State('editable-table_data', 'columns'),
     State('editable-table_data', 'data')],
    config_prevent_initial_callbacks=True
)
def update_table_field(selected_value, current_columns, current_data):
    # print(_columns)
    if selected_value == '1':
        columns = [{'name': 'Phase tested', 'id': 'phase', 'editable': True},
                   {'name': 'Applied Voltage [kV]', 'id': 'voltage', 'editable': True, 'type': 'numeric'},
                   {'name': 'IR 30s [GΩ]', 'id': 'IR30', 'editable': True, 'type': 'numeric'},
                   {'name': 'IR 60s [GΩ]', 'id': 'IR60', 'editable': True, 'type': 'numeric'},
                   {'name': 'Capacitance [nF]', 'id': 'Capacitance', 'editable': True, 'type': 'numeric'},
                   {'name': 'Ambient Temperature [C]', 'id': 'AmbTemp', 'editable': True, 'type': 'numeric'},
                   {'name': 'Humidity [%]', 'id': 'Humidity', 'editable': True, 'type': 'numeric'},
                   ],
        data = [{'phase': '', 'voltage': '', 'IR30': '', 'IR60': '', 'Capacitance': '',
                 'AmbTemp': '', 'Humidity': ''},
                {'phase': '', 'voltage': '', 'IR30': '', 'IR60': '', 'Capacitance': '',
                 'AmbTemp': '', 'Humidity': ''},
                {'phase': '', 'voltage': '', 'IR30': '', 'IR60': '', 'Capacitance': '',
                 'AmbTemp': '', 'Humidity': ''}]

        return columns[0],data

    elif selected_value == '2':
        columns = [{'name': 'Phase tested', 'id': 'phase', 'editable': True},
                   {'name': 'Applied Voltage [kV]', 'id': 'voltage', 'editable': True, 'type': 'numeric'},
                   {'name': 'IR 30s [GΩ]', 'id': 'IR30', 'editable': True, 'type': 'numeric'},
                   {'name': 'IR 60s [GΩ]', 'id': 'IR60', 'editable': True, 'type': 'numeric'},
                   {'name': 'IR 5 minutes [GΩ]', 'id': 'IR300', 'editable': True, 'type': 'numeric'},
                   {'name': 'IR 10 minutes [GΩ]', 'id': 'IR600', 'editable': True, 'type': 'numeric'},
                   {'name': 'Capacitance [nF]', 'id': 'Capacitance', 'editable': True, 'type': 'numeric'},
                   {'name': 'Ambient Temperature [C]', 'id': 'AmbTemp', 'editable': True, 'type': 'numeric'},
                   {'name': 'Humidity [%]', 'id': 'Humidity', 'editable': True, 'type': 'numeric'},
                   ],
        data = [{'phase': '', 'voltage': '', 'IR30': '', 'IR60': '','IR300': '','IR600': '', 'Capacitance': '', 'AmbTemp': '', 'Humidity': ''},{'phase': '', 'voltage': '', 'IR30': '', 'IR60': '','IR300': '','IR600': '', 'Capacitance': '', 'AmbTemp': '', 'Humidity': ''},
                {'phase': '', 'voltage': '', 'IR30': '', 'IR60': '','IR300': '','IR600': '', 'Capacitance': '', 'AmbTemp': '', 'Humidity': ''}]

        return columns[0], data

    elif selected_value == '3':
        columns = [{'name': 'Phase connection', 'id': 'phase', 'editable': True},
                   {'name': 'Applied Current [A]', 'id': 'current', 'editable': True, 'type': 'numeric'},
                   {'name': 'Resistance [mΩ]', 'id': 'wr', 'editable': True, 'type': 'numeric'},
                   {'name': 'Ambient Temperature [C]', 'id': 'AmbTemp', 'editable': True, 'type': 'numeric'},
                   {'name': 'Humidity [%]', 'id': 'Humidity', 'editable': True, 'type': 'numeric'},
                   ],
        data = [{'phase': '', 'current': '', 'wr': '', 'AmbTemp': '', 'Humidity': ''},{'phase': '', 'current': '', 'wr': '', 'AmbTemp': '', 'Humidity': ''},{'phase': '', 'current': '', 'wr': '', 'AmbTemp': '', 'Humidity': ''}]

        return columns[0], data

    elif selected_value == '4':
        columns = [{'name': 'Phase tested', 'id': 'phase', 'editable': True},
                   {'name': 'DDF at 10%Un', 'id': 'ddf1', 'editable': True, 'type': 'numeric'},
                   {'name': 'DDF at 20%Un', 'id': 'ddf2', 'editable': True, 'type': 'numeric'},
                   {'name': 'DDF at 30%Un', 'id': 'ddf3', 'editable': True, 'type': 'numeric'},
                   {'name': 'DDF at 40%Un', 'id': 'ddf4', 'editable': True, 'type': 'numeric'},
                   {'name': 'DDF at 50%Un', 'id': 'ddf5', 'editable': True, 'type': 'numeric'},
                   {'name': 'DDF at 60%Un', 'id': 'ddf6', 'editable': True, 'type': 'numeric'},
                   {'name': 'DDF at 70%Un', 'id': 'ddf7', 'editable': True, 'type': 'numeric'},
                   {'name': 'DDF at 80%Un', 'id': 'ddf8', 'editable': True, 'type': 'numeric'},
                   {'name': 'DDF at 90%Un', 'id': 'ddf9', 'editable': True, 'type': 'numeric'},
                   {'name': 'DDF at 100%Un', 'id': 'ddf10', 'editable': True, 'type': 'numeric'},
                   {'name': 'Ambient Temperature [C]', 'id': 'AmbTemp', 'editable': True, 'type': 'numeric'},
                   {'name': 'Humidity [%]', 'id': 'Humidity', 'editable': True, 'type': 'numeric'},

                   ],
        data = [{'phase': '', 'ddf1': '', 'ddf2': '', 'ddf3': '', 'ddf4': '','ddf5': '', 'ddf6': '', 'ddf7': '', 'ddf8': '', 'ddf9': '', 'ddf10': '', 'AmbTemp': '', 'Humidity': ''},
                {'phase': '', 'ddf1': '', 'ddf2': '', 'ddf3': '', 'ddf4': '','ddf5': '', 'ddf6': '', 'ddf7': '', 'ddf8': '', 'ddf9': '', 'ddf10': '', 'AmbTemp': '', 'Humidity': ''},
                {'phase': '', 'ddf1': '', 'ddf2': '', 'ddf3': '', 'ddf4': '','ddf5': '', 'ddf6': '', 'ddf7': '', 'ddf8': '', 'ddf9': '', 'ddf10': '', 'AmbTemp': '', 'Humidity': ''}]



        return columns[0], data
    elif selected_value == '5':
        columns = [{'name': 'Phase tested', 'id': 'phase', 'editable': True},
                   {'name': 'Applied Voltage [kV]', 'id': 'voltage', 'editable': True, 'type': 'numeric'},
                   {'name': 'Qm Pos [mV]', 'id': 'qmpos', 'editable': True, 'type': 'numeric'},
                   {'name': 'Qm Neg [mV]', 'id': 'qmneg', 'editable': True, 'type': 'numeric'},
                   {'name': 'Classification', 'id': 'identification', 'editable': True, 'type': 'text'},
                   {'name': 'Ambient Temperature [C]', 'id': 'AmbTemp', 'editable': True, 'type': 'numeric'},
                   {'name': 'Humidity [%]', 'id': 'Humidity', 'editable': True, 'type': 'numeric'},
                   {'name': 'PD Pattern', 'id':'pattern', 'editable':True, 'type': 'text','presentation': 'markdown'}
                   ],
        data = [{'phase': '', 'voltage': '', 'qmpos': '', 'qmneg': '', 'identification': '','AmbTemp': '', 'Humidity': '', 'pattern':''},{'phase': '', 'voltage': '', 'qmpos': '', 'qmneg': '','identification': '', 'AmbTemp': '', 'Humidity': '', 'pattern':''},{'phase': '', 'voltage': '', 'qmpos': '', 'qmneg': '','identification': '', 'AmbTemp': '', 'Humidity': '', 'pattern':''}]

        return columns[0], data
    elif selected_value == '6':
        columns = [{'name': 'Item', 'id': 'item', 'editable': True},
                   {'name': 'Inspection result', 'id': 'Iresult', 'editable': True, 'type': 'numeric'},
                   {'name': 'Picture', 'id': 'picture', 'editable': True, 'type': 'text', 'presentation': 'markdown'}
                   ],
        data = [{'item': '', 'Iresult': '', 'picture': ''}]

        return columns[0], data
    elif selected_value == '7':
        columns = [{'name': 'Applied Flux [%]', 'id': 'flux', 'editable': True},
                   {'name': 'Test duration [min]', 'id': 'duration', 'editable': True, 'type': 'numeric'},
                   {'name': 'Average Temperature [C]', 'id': 'averageT', 'editable': True, 'type': 'numeric'},
                   {'name': 'Number of Hot spot detected', 'id': 'nhotspot', 'editable': True, 'type': 'numeric'},
                   {'name': 'Max Temperature Hot spot', 'id': 'hotspotT', 'editable': True, 'type': 'numeric'},
                   {'name': 'Ambient Temperature [C]', 'id': 'AmbTemp', 'editable': True, 'type': 'numeric'},
                   {'name': 'Humidity [%]', 'id': 'Humidity', 'editable': True, 'type': 'numeric'},
                   {'name': 'Picture', 'id': 'picture', 'editable': True, 'type': 'text', 'presentation': 'markdown'}
                   ],
        data = [{'flux': '', 'duration': '', 'averageT': '', 'nhotspot': '', 'AmbTemp': '', 'Humidity': '','picture': ''}]

        return columns[0], data
    elif selected_value == '8':
        columns = [{'name': 'Applied flux [%]', 'id': 'flux', 'editable': True},
                   {'name': 'Number of Slot above 100mA', 'id': 'nslotfaulty', 'editable': True, 'type': 'numeric'},
                   {'name': 'Ambient Temperature [C]', 'id': 'AmbTemp', 'editable': True, 'type': 'numeric'},
                   {'name': 'Humidity [%]', 'id': 'Humidity', 'editable': True, 'type': 'numeric'},
                   {'name': 'Picture', 'id': 'picture', 'editable': True, 'type': 'text', 'presentation': 'markdown'}

                   ],
        data = [{'flux': '', 'nslotfaulty': '', 'AmbTemp': '', 'Humidity': '','picture': ''}]

        return columns[0], data
    elif selected_value == '9':
        columns = [
                   ],
        data = []

        return columns[0], data
    elif selected_value == '10':
        columns = [],
        data = []

        return columns[0], data
    elif selected_value == '11':
        columns = [{'name': 'Phase tested', 'id': 'phase', 'editable': True},
                   {'name': 'Qm Pos [mV]', 'id': 'qmpos', 'editable': True, 'type': 'numeric'},
                   {'name': 'Qm Neg [mV]', 'id': 'qmneg', 'editable': True, 'type': 'numeric'},
                   {'name': 'Classification', 'id': 'identification', 'editable': True, 'type': 'text'},
                   {'name': 'Winding Temperature [C]', 'id': 'WindTemp', 'editable': True, 'type': 'numeric'},
                   {'name': 'Ambient Temperature [C]', 'id': 'AmbTemp', 'editable': True, 'type': 'numeric'},
                   {'name': 'Humidity [%]', 'id': 'Humidity', 'editable': True, 'type': 'numeric'},
                   {'name': 'Actvie Power [MW]', 'id': 'P', 'editable': True, 'type': 'numeric'},
                   {'name': 'Reactive Power [MVAR]', 'id': 'Q', 'editable': True, 'type': 'numeric'},
                   {'name': 'PD Pattern', 'id':'pattern', 'editable':True, 'type': 'text','presentation': 'markdown'}
                   ],
        data = [{'phase': '', 'qmpos': '', 'qmneg': '','identification': '', 'WindTemp': '','AmbTemp': '', 'Humidity': '','P': '', 'Q': '', 'pattern':''},{'phase': '', 'qmpos': '', 'qmneg': '','identification': '', 'WindTemp': '','AmbTemp': '', 'Humidity': '','P': '', 'Q': '', 'pattern':''},{'phase': '', 'qmpos': '', 'qmneg': '','identification': '', 'WindTemp': '','AmbTemp': '', 'Humidity': '','P': '', 'Q': '', 'pattern':''}]

        return columns[0], data
    elif selected_value == '12':
        columns = [],
        data = []

        return columns[0], data
    elif selected_value == '13':
        columns = [],
        data = []

        return columns[0], data
    else:
        columns =[]
        data = []
        return columns,data  # Return empty list or default options

@callback(
    Output('editable-table_data', 'data'),
    [Input('add_row_btn', 'n_clicks')],
    [State('editable-table_data', 'data')],
    config_prevent_initial_callbacks=True
)
def add_row(n_clicks, current_data):
    if n_clicks > 0:
        new_row = current_data[0]
        #empty the row

        pos=0
        for item in list(current_data[0].values()):
            if item == '':
                None
            if item != '':
                key = list(current_data[0].keys())[pos]
                current_data[0]['{}'.format(key)] = ''
            pos+=1

        current_data.append(new_row)
    return current_data

############ data visualization ####################
# Track visibility state of the graphs
graph_visibility = {
    'online': False,
    'offline': False
}

# Callbacks to update graphs based on button clicks
#online
@callback(
    Output('online-container', 'children'),
    [Input('online-button', 'n_clicks')],
)
def update_online_container(n_clicks):
    global graph_visibility

    if n_clicks:


        graph_visibility['online'] = not graph_visibility['online']  # Toggle visibility
        if graph_visibility['online']:

            subcomponent_list = get_subcomponent_list()

            stator_subcomponent_id = []
            rotor_subcomponet_id = []
            aux_subcomponet_id = []
            for sub in subcomponent_list:
                if sub[3] == 1:
                    stator_subcomponent_id.append(sub[0])
                if sub[3] == 2:
                    rotor_subcomponet_id.append(sub[0])
                if sub[3] == 3:
                    aux_subcomponet_id.append(sub[0])

            #iterate through the subcomponet to get all the data related to stator

            result_dict = {}
            for subcomponent in stator_subcomponent_id:

                data = get_online_test_analysis_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0], subcomponent_id=subcomponent)
                # print(data)

                # Create a DataFrame
                df = pd.DataFrame(data, columns=['Date', 'Test', 'Value'])

                # Group by Date and Test, and keep the row with the maximum Value
                data_cleaned = df.loc[df.groupby(['Date', 'Test'])['Value'].idxmax()]

                # print(type(data_cleaned))
                # Convert cleaned DataFrame back to a list of tuples
                data_cleaned = [tuple(row) for row in data_cleaned.to_numpy()]
                sorted_data = sorted(data_cleaned, key=lambda x: datetime.strptime(x[0], '%d/%m/%Y %H:%M'))


                # Iterate through the data list - online pd for now
                for item in sorted_data:
                    key = item[1]  # Get the value in the second position
                    if key not in result_dict:
                        result_dict[key] = []  # Initialize a new list if key is not already present
                    result_dict[key].append(item)

            # Convert the dictionary values to a list of lists
            result_list = list(result_dict.values())

            # Convert result_list to a flat list of tuples
            flat_data = [item for sublist in result_list for item in sublist]

            # print(flat_data)

            # Convert data to DataFrame
            df = pd.DataFrame(flat_data, columns=['Date', 'Group', 'Value'])

            # Initialize a list to hold the max values data
            max_values_data = []

            # Define a mapping for percentage conversion
            percentage_mapping = {0: None, 1: 20, 2: 40, 3: 60, 4: 80, 5: 100}

            # Map group numbers to labels
            group_labels = {
                11: ('Online PD', 'ONPD'),
                10: ('Rotor Flux', 'RF'),
                12: ('Endwinding Vibration', 'EWV')
            }

            # Iterate through each row in the DataFrame
            for _, row in df.iterrows():
                group = row['Group']
                value = row['Value']

                # Replace value to percentage
                percentage = percentage_mapping.get(value)

                # Get the date from the current row
                date = row['Date']

                # Get the corresponding labels
                test_label, test_data_label = group_labels.get(group, (None, None))

                # Append the data to the list
                max_values_data.append({
                    'Group': test_label,
                    'Date': date,
                    'Max Value': percentage,
                    'Label': test_data_label
                })



            # Create a DataFrame from the max values data
            max_values_df = pd.DataFrame(max_values_data)

            # Check if the DataFrame is empty
            if max_values_df.empty:
                today = datetime.today().strftime('%d/%m/%Y')
                # one_month_ahead = today + timedelta(days=30)
                # fig.update_xaxes(range=[today, one_month_ahead])

                max_values_df = pd.DataFrame({'Date': [today], 'Max Value': [None], 'Group': ['No Data']})


            # Create line plot for each group
            line_fig = px.line(max_values_df, x='Date', y='Max Value', color='Group',
                               labels={'Max Value': 'Severity [%]', 'Group': 'Diagnostic test'},
                               title='Online Results Trend', markers=True)

            # Create scatter plot for the same data
            fig = px.scatter(max_values_df, x='Date', y='Max Value', color='Group',
                                     labels={'Max Value': 'Severity [%]', 'Group': 'Diagnostic test'},
                                     title='Online Results Trend')


            # Update the scatter plot traces to hide markers in the legend
            for trace in fig.data:
                if isinstance(trace, px.scatter().data[0].__class__):  # Check if it's a scatter trace
                    trace.showlegend = False

            # Combine the scatter points with the line traces
            for trace in line_fig.data:
                trace.customdata = max_values_df['Group'].values
                fig.add_trace(trace)

            # Update layout for centering the title and customizing appearance
            fig.update_layout(
                title={
                    'text': 'Online Results Trend',
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 14}
                },
                plot_bgcolor='rgb(17,17,17)',
                paper_bgcolor='rgb(17,17,17)',
                font_color='white',
                xaxis_title='',
                yaxis_title='Severity [%]',
                modebar={'bgcolor': 'rgba(0, 0, 0, 0.5)', 'color': 'white'},
                xaxis=dict(linecolor='grey', linewidth=0.5),
            )

            fig.update_xaxes(showgrid=False)  # Remove x-axis gridlines
            fig.update_xaxes(tickfont=dict(color='#FFFFFF',size=8))
            fig.update_xaxes(tickangle = 45)
            # Adjust tickvals based on merged_df['Date']
            tick_interval = 5  # Reduce this value to display more ticks, or increase it to display fewer
            # tickvals = max_values_df['Group'].values[::tick_interval]
            # print(len(max_values_df.values.tolist()[::len(max_values_df.values.tolist()) // 5]))
            # fig.update_xaxes(tickvals=tickvals)
            fig.update_yaxes(showgrid=False)  # Remove y-axis gridlines
            fig.update_yaxes(range=[0, 100])



            graph = dcc.Graph(figure=fig, id='online-results-trend-stator',  config={'displayModeBar': False}, style={'margin-top':'30px', 'padding':'10px'})  # Hide modebar buttons
            return graph
        else:
            return None
    else:
        return None

#offline
@callback(
    Output('offline-container', 'children'),
    [Input('offline-button', 'n_clicks')]
)
def update_offline_container(n_clicks):
    global graph_visibility
    if n_clicks:
        graph_visibility['offline'] = not graph_visibility['offline']  # Toggle visibility
        if graph_visibility['offline']:

            subcomponent_list = get_subcomponent_list()

            stator_subcomponent_id = []
            rotor_subcomponet_id = []
            aux_subcomponet_id = []
            for sub in subcomponent_list:
                if sub[3]==1:
                    stator_subcomponent_id.append(sub[0])
                if sub[3]==2:
                    rotor_subcomponet_id.append(sub[0])
                if sub[3] == 3:
                    aux_subcomponet_id.append(sub[0])


            #iterate through the subcomponent of the component to get all the offline data

            result_dict = {}

            for subcomponent in stator_subcomponent_id:
                data = get_offline_test_analysis_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0], subcomponent_id=subcomponent)

                #clean the data set to have the worst result of the multiple data for the same test/date
                # Create a DataFrame
                df = pd.DataFrame(data, columns=['Date', 'Test', 'Value'])

                # Group by Date and Test, and keep the row with the maximum Value
                data_cleaned = df.loc[df.groupby(['Date', 'Test'])['Value'].idxmax()]

                # Convert cleaned DataFrame back to a list of tuples
                data_cleaned = [tuple(row) for row in data_cleaned.to_numpy()]
                sorted_data = sorted(data_cleaned, key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))



                # Iterate through the data list
                for item in sorted_data:
                    key = item[1]  # Get the value in the second position
                    if key not in result_dict:
                        result_dict[key] = []  # Initialize a new list if key is not already present
                    result_dict[key].append(item)  # Append the current item to the list corresponding to the key





            # Convert the dictionary values to a list of lists
            result_list = list(result_dict.values())

            # Convert result_list to a flat list of tuples
            flat_data = [item for sublist in result_list for item in sublist]

            # print(flat_data)

            # Convert data to DataFrame
            df = pd.DataFrame(flat_data, columns=['Date', 'Group', 'Value'])


            # Initialize a list to hold the max values data
            max_values_data = []

            # Define a mapping for percentage conversion
            percentage_mapping = {0: None, 1: 20, 2: 40, 3: 60, 4: 80, 5: 100}

            # Map group numbers to labels
            group_labels = {
                1: ('Insulation Resistance', 'IR'),
                2: ('Polarization Index', 'PI'),
                3: ('Winding Resistance', 'WR'),
                4: ('DDF', 'DDF'),
                5: ('Offline PD','OFFPD')
            }

            # Iterate through each row in the DataFrame
            for _, row in df.iterrows():
                group = row['Group']
                value = row['Value']

                # Replace value to percentage
                percentage = percentage_mapping.get(value)

                # Get the date from the current row
                date = row['Date']

                # Get the corresponding labels
                test_label, test_data_label = group_labels.get(group, (None, None))

                # Append the data to the list
                max_values_data.append({
                    'Group': test_label,
                    'Date': date,
                    'Max Value': percentage,
                    'Label': test_data_label
                })

            # print(max_values_data)

            # Create a DataFrame from the max values data
            max_values_df = pd.DataFrame(max_values_data)

            # Check if the DataFrame is empty
            if max_values_df.empty:
                today = datetime.today().strftime('%d/%m/%Y')
                # one_month_ahead = today + timedelta(days=30)
                # fig.update_xaxes(range=[today, one_month_ahead])

                max_values_df = pd.DataFrame({'Date': [today], 'Max Value': [None], 'Group': ['No Data']})

            # Create line plot for each group
            line_fig = px.line(max_values_df, x='Date', y='Max Value', color='Group',
                               labels={'Max Value': 'Severity [%]', 'Group': 'Diagnostic test'},
                               title='Offline Data Trend', markers=True)

            # Create scatter plot for the same data
            fig = px.scatter(max_values_df, x='Date', y='Max Value', color='Group',
                             labels={'Max Value': 'Severity [%]', 'Group': 'Diagnostic test'},
                             title='Offline Data Trend')

            # Update the scatter plot traces to hide markers in the legend
            for trace in fig.data:
                if isinstance(trace, px.scatter().data[0].__class__):  # Check if it's a scatter trace
                    trace.showlegend = False

                    # Combine the scatter points with the line traces
            for trace in line_fig.data:
                trace.customdata = max_values_df['Group'].values
                fig.add_trace(trace)

            # Update layout for centering the title and customizing appearance
            fig.update_layout(
                title={
                    'text': 'Offline Results Trend',
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 14}
                },
                plot_bgcolor='rgb(17,17,17)',
                paper_bgcolor='rgb(17,17,17)',
                font_color='white',
                xaxis_title='',
                yaxis_title='Severity [%]',
                modebar={'bgcolor': 'rgba(0, 0, 0, 0.5)', 'color': 'white'},
                xaxis=dict(linecolor='grey', linewidth=0.5),
            )
            fig.update_xaxes(showgrid=False)  # Remove x-axis gridlines
            fig.update_yaxes(showgrid=False)  # Remove y-axis gridlines
            fig.update_yaxes(range=[0, 100])


            # Create a Dash component to display the graph
            graph = dcc.Graph(figure=fig, config={'displayModeBar': False},style={'margin-top':'30px','padding':'10px'})  # Hide modebar buttons
            return graph
        else:
            return None
    else:
        return None


#raw data graph
@callback(
    Output('raw-data-graph-container-stator', 'children'),
    Output('raw-data-graph-container-stator', 'style', allow_duplicate=True),
    Input('online-results-trend-stator', 'clickData'),
    prevent_initial_call='initial_duplicate'
)
def update_graph_container(clickData):
    if clickData is None:

        return dash.no_update, {'display': 'none'}
    # print(clickData)
    # Extract information from the clicked marker
    clicked_point = clickData['points'][0]

    date = clicked_point['x']  # Get the group name or any relevant info
    group = clicked_point['customdata']

    #convert group label to diagnostic test id
    group_labels = {
        'Insulation Resistance': 1,
        'Polarization Index': 2,
        'Winding Resistance': 3,
        'DDF': 4,
        'Offline PD': 5,
        'Online PD': 11,
        'Rotor Flux': 10,
        'Endwinding Vibration': 12
    }

    diagnostic_test_id = group_labels.get(group)

    data_set = []

    for diagnostic_test_id in (10, 11, 12):
        if diagnostic_test_id==11:
            raw_data = get_online_pd_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
            # Check if raw_data is not empty before appending
            if raw_data:  # Ensure raw_data is not None or empty
                for row in raw_data:
                    data_set.append({
                        'Date': row[23],
                        'Phase': row[5],
                        'QMax95% Amplitude': row[6],
                        'Nw': row[7],
                        'pdpattern_id':row[0],
                    })
            data_df = pd.DataFrame(data_set)
            ##################positive
            # Ensure 'Pos Amplitude' is numeric
            data_df['QMax95% Amplitude'] = pd.to_numeric(data_df['QMax95% Amplitude'], errors='coerce')

            # Drop NaNs in 'Pos Amplitude'
            data_df = data_df.dropna(subset=['QMax95% Amplitude'])

            # Sort DataFrame by 'Date' to ensure chronological order
            data_df = data_df.sort_values(by='Date', ascending=True)

            # Define a fixed color sequence
            color_sequence = ['#B22222', '#FFA500', '#4169E1']

            #################negative
            # Ensure 'Pos Amplitude' is numeric
            data_df['Nw'] = pd.to_numeric(data_df['Nw'], errors='coerce')

            # Drop NaNs in 'Pos Amplitude'
            data_df_n = data_df.dropna(subset=['Nw'])

            # Sort DataFrame by 'Date' to ensure chronological order
            data_df_n = data_df_n.sort_values(by='Date', ascending=True)

            # Define a fixed color sequence
            color_sequence_neg = [
                'rgba(178, 34, 34, 0.6)',  # Semi-transparent Lighter Red
                'rgba(255, 165, 0, 0.6)',  # Semi-transparent Lighter Orange
                'rgba(65, 105, 225, 0.6)'  # Semi-transparent Lighter Blue
            ]



            # Filter the DataFrame for each phase to create three line plots
            df_u = data_df [data_df['Phase'] == 'u']
            df_v = data_df [data_df['Phase'] == 'v']
            df_w = data_df [data_df['Phase'] == 'w']

            df_u_n = data_df_n[data_df_n['Phase'] == 'u']
            df_v_n = data_df_n[data_df_n['Phase'] == 'v']
            df_w_n = data_df_n[data_df_n['Phase'] == 'w']



            # Check if data_df is not empty
            if not df_u.empty and not df_u_n.empty and not df_v.empty and not df_v_n.empty and not df_w.empty and not df_w_n.empty:
                # Merge all three phases (positive data) into one DataFrame for 'QMax95% Amplitude'
                merged_df = pd.merge(df_u[['Date', 'QMax95% Amplitude']], df_v[['Date', 'QMax95% Amplitude']],
                                     on='Date', how='outer', suffixes=('_u', '_v'))
                merged_df = pd.merge(merged_df, df_w[['Date', 'QMax95% Amplitude']], on='Date', how='outer')
                merged_df = merged_df.rename(columns={'QMax95% Amplitude': 'QMax95% Amplitude_w'})  # Rename last column

                # Merge all three phases (negative data) into one DataFrame for 'Nw'
                merged_df_n = pd.merge(df_u_n[['Date', 'Nw']], df_v_n[['Date', 'Nw']], on='Date', how='outer',
                                       suffixes=('_u', '_v'))
                merged_df_n = pd.merge(merged_df_n, df_w_n[['Date', 'Nw']], on='Date', how='outer')
                merged_df_n = merged_df_n.rename(columns={'Nw': 'Nw_w'})  # Rename last column

                # Interpolate the Date column to handle any NaN values (if needed)
                merged_df['Date'] = merged_df['Date'].interpolate()

                # Interpolate the QMax95% Amplitude columns to handle any NaN values in y-axis
                merged_df['QMax95% Amplitude_u'] = merged_df['QMax95% Amplitude_u'].interpolate()
                merged_df['QMax95% Amplitude_v'] = merged_df['QMax95% Amplitude_v'].interpolate()
                merged_df['QMax95% Amplitude_w'] = merged_df['QMax95% Amplitude_w'].interpolate()

                # Interpolate the Nw columns (negative data)
                merged_df_n['Nw_u'] = merged_df_n['Nw_u'].interpolate()
                merged_df_n['Nw_v'] = merged_df_n['Nw_v'].interpolate()
                merged_df_n['Nw_w'] = merged_df_n['Nw_w'].interpolate()


                # Drop rows that still have NaN values after interpolation (if any)
                merged_df = merged_df.dropna()
                merged_df_n = merged_df_n.dropna()

                # Sort merged_df by Date (important for proper plotting)
                merged_df = merged_df.sort_values(by='Date')
                merged_df_n = merged_df_n.sort_values(by='Date')

                # Create fig for positive data (QMax95% Amplitude)
                fig = go.Figure()

                # Add traces for each phase ('u', 'v', 'w') for positive data
                fig.add_trace(go.Scatter(
                    x=merged_df['Date'],
                    y=merged_df['QMax95% Amplitude_u'],
                    mode='lines+markers',
                    name='Phase u',
                    line=dict(color='#B22222', width=0.5),  # Custom color for Phase u
                    marker=dict(size=6)
                ))

                fig.add_trace(go.Scatter(
                    x=merged_df['Date'],
                    y=merged_df['QMax95% Amplitude_v'],
                    mode='lines+markers',
                    name='Phase v',
                    line=dict(color='#FFA500', width=0.5),  # Custom color for Phase v
                    marker=dict(size=6)
                ))

                fig.add_trace(go.Scatter(
                    x=merged_df['Date'],
                    y=merged_df['QMax95% Amplitude_w'],
                    mode='lines+markers',
                    name='Phase w',
                    line=dict(color='#4169E1', width=0.5),  # Custom color for Phase w
                    marker=dict(size=6)
                ))

                # Adjust tickvals based on merged_df['Date']
                tick_interval = 5  # Reduce this value to display more ticks, or increase it to display fewer
                tickvals = merged_df['Date'][::tick_interval]
                # Update layout for positive data
                fig.update_layout(
                    title="Online PD Data Trend - QMax95%",
                    xaxis_title="",
                    yaxis_title="Amplitude [mV]",
                    plot_bgcolor='rgb(17,17,17)',  # Set background color
                    paper_bgcolor='rgb(17,17,17)',  # Set background color for paper
                    font_color='white',
                    modebar={'bgcolor': 'rgba(0, 0, 0, 0.5)', 'color': 'white'},
                    xaxis=dict(
                        linecolor='grey',  # X-axis line color
                        linewidth=0.5,  # X-axis line width
                        showgrid=False, # Remove x-axis gridlines
                        tickfont=dict(color='#FFFFFF', size=8),
                        tickangle=45,
                        tickvals=tickvals
                    ),
                    yaxis=dict(
                        linecolor='grey',  # Y-axis line color
                        linewidth=0.5,  # Y-axis line width
                        showgrid=False  # Remove y-axis gridlines
                    ),
                )

                # Show the plot for the positive data
                # fig.show()

                # Create fig for negative data (Nw)
                fig_neg = go.Figure()

                # Add traces for each phase ('u', 'v', 'w') for negative data
                fig_neg.add_trace(go.Scatter(
                    x=merged_df_n['Date'],
                    y=merged_df_n['Nw_u'],
                    mode='lines+markers',
                    name='Phase u',
                    line=dict(color='rgba(178, 34, 34, 0.6)',width=0.5),  # Semi-transparent Lighter Red
                    marker=dict(size=6)
                ))

                fig_neg.add_trace(go.Scatter(
                    x=merged_df_n['Date'],
                    y=merged_df_n['Nw_v'],
                    mode='lines+markers',
                    name='Phase v',
                    line=dict(color='rgba(255, 165, 0, 0.6)',width=0.5),  # Semi-transparent Lighter Orange
                    marker=dict(size=6)
                ))

                fig_neg.add_trace(go.Scatter(
                    x=merged_df_n['Date'],
                    y=merged_df_n['Nw_w'],
                    mode='lines+markers',
                    name='Phase w',
                    line=dict(color='rgba(65, 105, 225, 0.6)',width=0.5),  # Semi-transparent Lighter Blue
                    marker=dict(size=6)
                ))

                # Update layout for negative data
                fig_neg.update_layout(
                    title="Online PD Data Trend - Nw",
                    xaxis_title="",
                    yaxis_title="Pulse Per Cycle",
                    plot_bgcolor='rgb(17,17,17)',  # Set background color
                    paper_bgcolor='rgb(17,17,17)',  # Set background color for paper
                    font_color='white',
                    modebar={'bgcolor': 'rgba(0, 0, 0, 0.5)', 'color': 'white'},
                    xaxis=dict(
                        linecolor='grey',  # X-axis line color
                        linewidth=0.5,  # X-axis line width
                        showgrid=False , # Remove x-axis gridlines
                        tickfont = dict(color='#FFFFFF', size=8),
                        tickangle = 45,
                        tickvals=tickvals
                    ),
                    yaxis=dict(
                        linecolor='grey',  # Y-axis line color
                        linewidth=0.5,  # Y-axis line width
                        showgrid=False  # Remove y-axis gridlines
                    ),
                )





                # # Create line plot for each group - positive
                # line_fig = px.line(data_df, x='Date', y='QMax95% Amplitude', color='Phase',
                #                    labels={'QMax95% Amplitude': 'Amplitude [mV]', 'Phase': 'Phase'},
                #                    title='Online PD Data Trend - QMax95%',color_discrete_sequence=color_sequence, markers=True,custom_data=['pdpattern_id'])
                #
                # line_fig_u = px.line(df_u, x='Date', y='QMax95% Amplitude', color='Phase',
                #                    labels={'QMax95% Amplitude': 'Amplitude [mV]', 'Phase': 'Phase'},
                #                    title='Online PD Data Trend - QMax95%', color_discrete_sequence=[color_sequence[0]],
                #                    markers=True, custom_data=['pdpattern_id'])
                #
                # line_fig_v = px.line(df_v, x='Date', y='QMax95% Amplitude', color='Phase',
                #                    labels={'QMax95% Amplitude': 'Amplitude [mV]', 'Phase': 'Phase'},
                #                    title='Online PD Data Trend - QMax95%', color_discrete_sequence=[color_sequence[1]],
                #                    markers=True, custom_data=['pdpattern_id'])
                #
                # line_fig_w = px.line(df_w, x='Date', y='QMax95% Amplitude', color='Phase',
                #                    labels={'QMax95% Amplitude': 'Amplitude [mV]', 'Phase': 'Phase'},
                #                    title='Online PD Data Trend - QMax95%', color_discrete_sequence=[color_sequence[2]],
                #                    markers=True, custom_data=['pdpattern_id'])
                #
                # # Create line plot for each group - negative
                # line_fig_neg = px.line(data_df_n, x='Date', y='Nw', color='Phase',
                #                    labels={'Nw': 'Pulse Per Cycle', 'Phase': 'Phase'},
                #                    title='Online PD Data Trend - NW', color_discrete_sequence=color_sequence_neg, markers=True,custom_data=['pdpattern_id'])
                #
                # line_fig_neg_u = px.line(df_u_n, x='Date', y='Nw', color='Phase',
                #                        labels={'Nw': 'Pulse Per Cycle', 'Phase': 'Phase'},
                #                        title='Online PD Data Trend - NW', color_discrete_sequence=[color_sequence_neg[0]],
                #                        markers=True, custom_data=['pdpattern_id'])
                #
                # line_fig_neg_v = px.line(df_v_n, x='Date', y='Nw', color='Phase',
                #                        labels={'Nw': 'Pulse Per Cycle', 'Phase': 'Phase'},
                #                        title='Online PD Data Trend - NW', color_discrete_sequence=[color_sequence_neg[1]],
                #                        markers=True, custom_data=['pdpattern_id'])
                # line_fig_neg_w = px.line(df_w_n, x='Date', y='Nw', color='Phase',
                #                        labels={'Nw': 'Pulse Per Cycle', 'Phase': 'Phase'},
                #                        title='Online PD Data Trend - NW', color_discrete_sequence=[color_sequence_neg[2]],
                #                        markers=True, custom_data=['pdpattern_id'])
                #
                # #scale
                # max_value = data_df['QMax95% Amplitude'].max()
                # max_value_neg = data_df['Nw'].max()
                #
                # full_scale = max(max_value, max_value_neg)*1.2
                # # Create scatter plot for the same data
                # fig = px.scatter(data_df, x='Date', y='QMax95% Amplitude', color='Phase',
                #                  labels={'QMax95% Amplitude': 'Amplitude [mV]', 'Phase': 'Phase'},
                #                  title='Online PD Data Trend - QMax95%',color_discrete_sequence=color_sequence,custom_data=['pdpattern_id'])
                #
                # # Create scatter plot for the same data
                # fig_neg = px.scatter(data_df, x='Date', y='Nw', color='Phase',
                #                  labels={'Nw': 'Pulse Per Cycle', 'Phase': 'Phase'},
                #                  title='Online PD Data Trend - Nw', color_discrete_sequence=color_sequence_neg,custom_data=['pdpattern_id'])
                #
                # # Update the scatter plot traces to hide markers in the legend
                # for trace in fig.data:
                #     if isinstance(trace, px.scatter().data[0].__class__):  # Check if it's a scatter trace
                #         trace.showlegend = False
                #
                # # Combine the scatter points with the line traces
                # for trace in line_fig_u.data:
                #     # trace.customdata = max_values_df['Group'].values
                #     fig.add_trace(trace)
                # for trace in line_fig_v.data:
                #     # trace.customdata = max_values_df['Group'].values
                #     fig.add_trace(trace)
                # for trace in line_fig_w.data:
                #     # trace.customdata = max_values_df['Group'].values
                #     fig.add_trace(trace)
                #
                # # Update the scatter plot traces to hide markers in the legend
                # for trace in fig_neg.data:
                #     if isinstance(trace, px.scatter().data[0].__class__):  # Check if it's a scatter trace
                #         trace.showlegend = False
                #
                # for trace in line_fig_neg_u.data:
                #     # trace.customdata = max_values_df['Group'].values
                #     fig_neg.add_trace(trace)
                # for trace in line_fig_neg_v.data:
                #     # trace.customdata = max_values_df['Group'].values
                #     fig_neg.add_trace(trace)
                # for trace in line_fig_neg_w.data:
                #     # trace.customdata = max_values_df['Group'].values
                #     fig_neg.add_trace(trace)
                #
                #
                #
                # # Update layout for centering the title and customizing appearance
                # fig.update_layout(
                #     title={
                #         'text': 'Online PD Test Trend - QMax95%',
                #         'x': 0.5,
                #         'xanchor': 'center',
                #         'yanchor': 'top',
                #         'font': {'size': 14}
                #     },
                #     plot_bgcolor='rgb(17,17,17)',
                #     paper_bgcolor='rgb(17,17,17)',
                #     font_color='white',
                #     xaxis_title='',
                #     yaxis_title='Amplitude [mV]',
                #     modebar={'bgcolor': 'rgba(0, 0, 0, 0.5)', 'color': 'white'},
                #     xaxis=dict(
                #         linecolor='grey',  # X-axis line color
                #         linewidth=0.5,  # X-axis line width
                #         showgrid=False  # Remove x-axis gridlines
                #     ),
                #     yaxis=dict(
                #         linecolor='grey',  # Y-axis line color
                #         linewidth=0.5,  # Y-axis line width
                #         showgrid=False  # Remove y-axis gridlines
                #     ),
                # )
                # fig.update_xaxes(showgrid=False)  # Remove x-axis gridlines
                # fig.update_yaxes(showgrid=False) # Remove y-axis gridlines
                # fig.update_yaxes(range=[0, full_scale])  # Adjust the upper limit as needed
                #
                # fig_neg.update_layout(
                #     title={
                #         'text': 'Online PD Test Trend - Nw',
                #         'x': 0.5,
                #         'xanchor': 'center',
                #         'yanchor': 'top',
                #         'font': {'size': 14}
                #     },
                #     plot_bgcolor='rgb(17,17,17)',
                #     paper_bgcolor='rgb(17,17,17)',
                #     font_color='white',
                #     xaxis_title='',
                #     yaxis_title='Pulse Per Cycle',
                #     modebar={'bgcolor': 'rgba(0, 0, 0, 0.5)', 'color': 'white'},
                #     xaxis=dict(
                #         linecolor='grey',  # X-axis line color
                #         linewidth=0.5,  # X-axis line width
                #         showgrid=False  # Remove x-axis gridlines
                #     ),
                #     yaxis=dict(
                #         linecolor='grey',  # Y-axis line color
                #         linewidth=0.5,  # Y-axis line width
                #         showgrid=False  # Remove y-axis gridlines
                #     ),
                # )
                # fig_neg.update_xaxes(showgrid=False)  # Remove x-axis gridlines
                # fig_neg.update_yaxes(showgrid=False)  # Remove y-axis gridlines
                # fig_neg.update_yaxes(range=[0, full_scale])  # Adjust the upper limit as needed




        if diagnostic_test_id==10:
            raw_data = get_rfa_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        if diagnostic_test_id==12:
            raw_data = get_online_ew_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])

    for diagnostic_test_id in (1, 2, 3, 4, 5, 6, 7, 8, 9):
        if diagnostic_test_id == 1:
            raw_data = get_ir_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        if diagnostic_test_id == 2:
            raw_data = get_pi_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        if diagnostic_test_id == 3:
            raw_data = get_wr_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        if diagnostic_test_id == 4:
            raw_data = get_ddf_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        if diagnostic_test_id == 5:
            raw_data = get_offline_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        if diagnostic_test_id == 6:
            raw_data = get_inspection_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        if diagnostic_test_id == 7:
            raw_data = get_coreflux_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        if diagnostic_test_id == 8:
            raw_data = get_elcid_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        if diagnostic_test_id == 9:
            raw_data = get_bump_test_data(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])

    graph1 = dcc.Graph(id='pd_trend_pos',figure=fig, style={'padding': '10px'},config={'displayModeBar': False})
    graph2 = dcc.Graph(id='pd_trend_neg',figure=fig_neg, style={'padding': '10px'},config={'displayModeBar': False})

    return dbc.Container([graph1,graph2], fluid=True), {'display': 'block', 'margin-top':'30px', 'width':'100%'}


# #show graph picture
@callback(
    Output('graph_card_rm', 'style', allow_duplicate=True),
    Output('graph_card_rm', 'children'),
    [Input('pd_trend_pos', 'clickData'),
    Input('pd_trend_neg', 'clickData')],
    prevent_initial_call='initial_duplicate'
)
def update_graph_container(clickData_pos, clickData_neg):
    def get_image_from_db(pdpattern_id):
        # Fetch your image from MySQL
        image_data = get_online_pd_patter_rm(pdpattern_id)[0]
          # Assuming this returns a binary image
        return base64.b64encode(image_data).decode('utf-8') if image_data else None

    pdpattern_raw = None
    pdpattern_id = None
    if clickData_pos is None and clickData_neg is None:
        return {'display': 'none'}, []  # Hide the graph card if no data is clicked

        # Extract information from the clicked marker
    if clickData_pos is not None  or clickData_neg is not None :

        if clickData_neg ==None:
            pdpattern_id = clickData_pos['points'][0]['customdata'][0]
        if clickData_pos==None:
            pdpattern_id = clickData_neg['points'][0]['customdata'][0]

        if clickData_pos!=None and clickData_neg!=None:
            pdpattern_id = clickData_pos['points'][0]['customdata'][0]

        if pdpattern_id !=None:
            pdpattern_raw = get_image_from_db(pdpattern_id)

    if pdpattern_raw is None:
        return {'display': 'none'}, []

    # Create the image component with the fetched image
    image_component = html.Img(
        src='data:image/jpeg;base64,{}'.format(pdpattern_raw),  # Use the image URL from the database
        style={'width': '200px', 'height': 'auto', 'padding': '10px'}
    )

    label_raw = get_online_pd_patter_identification_polarity(pdpattern_id)
    label = ''

    label = '{}-{}'.format(label_raw[0], label_raw[1])

    # Update the identification label as needed
    identification_label = html.P(f'Identification: {label} polarity', style={'fontSize': '12px'})

    # Create the card content while preserving the original style
    card_content = dbc.CardBody(
        html.Div(
            style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},  # Center contents
            children=[
                image_component,  # Image component
                html.Div(
                    style={'marginLeft': '20px'},  # Space between image and labels
                    children=[
                        identification_label,
                        # You can add more labels here as needed
                    ]
                )
            ]
        )
    )

    # Create the card structure with original styling
    card = dbc.Card(
        card_content,
        style={
            'width': '100%',
            'borderRadius': '15px',  # Rounded corners
            'backgroundColor': 'grey',  # Background color
            'borderColor': 'grey',  # Border color
            'borderWidth': '1px',  # Border width
            'borderStyle': 'solid',  # Solid border style
            'margin-bottom':'30px',
            'margin-top': '30px'
        }
    )


    return {'display': 'block'}, card


#change style button
@callback(
    [Output('online-button', 'style'),
     Output('offline-button', 'style'),
     Output('graph_card_rm', 'style', allow_duplicate=True),
     Output('raw-data-graph-container-stator', 'style', allow_duplicate=True)
     ],
    [Input('online-button', 'n_clicks'),
     Input('offline-button', 'n_clicks')],
    prevent_initial_call=True
)

def update_button_style(online_n_clicks, offline_n_clicks):
    style_online = {'width': '300px', 'background-color': 'grey', 'border-color': 'grey', 'color': 'black',
                    'font-weight': 'bold'}
    style_offline = {'width': '300px', 'background-color': 'grey', 'border-color': 'grey', 'color': 'black',
                     'font-weight': 'bold'}

    pd_card_style = {'display': 'none'}
    onlinepdtrend_style = {'display': 'none'}

    if online_n_clicks is not None and online_n_clicks % 2 == 1:
        style_online['background-color'] = 'darkgrey'
        pd_card_style = {'display': 'none'}
        onlinepdtrend_style = {'display': 'none'}

    if offline_n_clicks is not None and offline_n_clicks % 2 == 1:
        style_offline['background-color'] = 'darkgrey'
        pd_card_style = {'display': 'none'}
        onlinepdtrend_style = {'display': 'none'}

    return style_online, style_offline, pd_card_style, onlinepdtrend_style



### legends graphs
#hi graph
@callback(
    Output('hi-legend-modal_stator', 'style',allow_duplicate=True),
    [Input('graph1_stator', 'clickData'), Input( 'confirm-hi-legend_stator', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_modal(clickData, close_btn_click):
    if clickData and ctx.triggered[0]['prop_id'].split('.')[0] == 'graph1_stator':
        return {'display': 'block', 'position': 'fixed', 'top': '50%', 'left': '50%',
                'transform': 'translate(-50%, -50%)', 'z-index': 1000}
    elif close_btn_click:
        return {'display': 'none'}
    return {'display': 'none'}


# External JavaScript for right-click handling
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Dash App</title>
    </head>
    <body>
        <div id="dash-app"></div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const graphDiv = document.getElementById('graph1_stator');
                graphDiv.oncontextmenu = function(event) {
                    event.preventDefault();
                    // Trigger the click event to open the modal
                    Dash.clientsideCallbacks.triggerInput({
                        id: 'graph1_stator',
                        prop: 'clickData',
                        value: { 'points': [{ 'x': event.clientX, 'y': event.clientY }] }
                    });
                };
            });
        </script>
    </body>
</html>
'''


#fm graph
@callback(
    Output('fm-legend-modal_stator', 'style',allow_duplicate=True),
    [Input('graph2_stator', 'clickData'), Input( 'confirm-fm-legend_stator', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_modal(clickData, close_btn_click):
    if clickData and ctx.triggered[0]['prop_id'].split('.')[0] == 'graph2_stator':
        return {'display': 'block', 'position': 'fixed', 'top': '50%', 'left': '50%',
                'transform': 'translate(-50%, -50%)', 'z-index': 1000}
    elif close_btn_click:
        return {'display': 'none'}
    return {'display': 'none'}


# External JavaScript for right-click handling
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Dash App</title>
    </head>
    <body>
        <div id="dash-app"></div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const graphDiv = document.getElementById('graph2_stator');
                graphDiv.oncontextmenu = function(event) {
                    event.preventDefault();
                    // Trigger the click event to open the modal
                    Dash.clientsideCallbacks.triggerInput({
                        id: 'graph2_stator',
                        prop: 'clickData',
                        value: { 'points': [{ 'x': event.clientX, 'y': event.clientY }] }
                    });
                };
            });
        </script>
    </body>
</html>
'''