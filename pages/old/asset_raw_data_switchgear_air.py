import time

import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
from dash import Dash, clientside_callback
from dash import dcc
from dash import html
import dash.dependencies as dd
from dash.dash_table import DataTable


#speach recognition - google api

import threading
# from functions.voice_to_text import transcribe_voice_to_text
# import speech_recognition as sr

# text to speach
from gtts import gTTS
import os
# from playsound import playsound  # Optional



from dash import html, dcc, callback, Input, Output, register_page, ctx
from dash.exceptions import PreventUpdate
from dash import dash_table
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

from connectors.db_connectors_mysql import get_component_analysis, get_component_single_asset_list, \
    get_asset_sw_layout_individual_sw, upload_test_data_sw, get_offline_test_analysis_data_full_asset, \
    get_online_test_analysis_data_full_asset, get_offline_latest_IR_value_for_summary_table_sw, \
    get_offline_latest_PI_value_for_summary_table_sw
from connectors.db_connectors_mysql import get_failure_mechanism_single_asset_list
from connectors.db_connectors_mysql import get_failure_mechanisms_analysis
from connectors.db_connectors_mysql import get_subcomponent_analysis

from connectors.db_connectors_mysql import update_asset_criticality
from connectors.db_connectors_mysql import get_asset_analysis
from connectors.db_connectors_mysql import export_asset_summary
from connectors.db_connectors_mysql import get_criticality_list
from connectors.db_connectors_mysql import get_maintenance_action

from functions.analyse_data_mysql import analyse_data
from functions.assess_condition_mysql import assess_condition
from functions.global_variables import asset_selected_details


import math


# opne the page

dash.register_page(__name__, external_stylesheets=[dbc.themes.SPACELAB,dbc.icons.BOOTSTRAP,dbc.themes.BOOTSTRAP])





############################         Import data sets from database          ############################################



############################         Pop up    ##################


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
    titlefont=dict(color='#FFFFFF', size=14),  # Title text color (white)
    xaxis=dict(
        title='X Axis',
        titlefont=dict(color='#FFFFFF'),  # X-axis title text color (white)
        tickfont=dict(color='#FFFFFF', size=8)  # X-axis tick labels color (white)
    ),
    yaxis=dict(
        title='Y Axis',
        titlefont=dict(color='#FFFFFF'),  # Y-axis title text color (white)
        tickfont=dict(color='#FFFFFF')  # Y-axis tick labels color (white)
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
    hovermode='closest'
)

# Remove mode bar icons
config = {'displayModeBar': False}

graph1 = dcc.Graph(
    id='graph1',
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
    title='Failure Mechanisms Analysis',  # Title
    titlefont=dict(color='#FFFFFF', size=14),  # Title text color (white)
    xaxis=dict(
        title='X Axis',
        titlefont=dict(color='#FFFFFF'),  # X-axis title text color (white)
        tickfont=dict(color='#FFFFFF',size=8)  # X-axis tick labels color (white)
    ),
    yaxis=dict(
        title='Y Axis',
        titlefont=dict(color='#FFFFFF'),  # Y-axis title text color (white)
        tickfont=dict(color='#FFFFFF')  # Y-axis tick labels color (white)
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
    hovermode='closest'
)

# Remove mode bar icons
config = {'displayModeBar': False}

# Create dcc.Graph for graph2
graph2 = dcc.Graph(
    id='graph2',
    figure=dict(data=[trace2], layout=graph2_layout),
    config=config,
    style={'width': '95%', 'height': 'auto','z-index': 2}

)





######## failure mode table:

failure_mechanisms_list = get_failure_mechanism_single_asset_list(3)




data_for_table = [
    {
        'Failure Mechanism': item[1],
        'Component Affected': item[2],
        'Local effect': item[3],
    }
    for item in failure_mechanisms_list
]

#### criticality list

criticality_list = get_criticality_list()


data_for_table_criticality = [{
    'Class':item[1],
    'Safety consequences': item[2],
    'Environmental consequences': item[5],
    'Financial consequences':item[3],
    'Reliability consequences': item[4],
    }
    for item in criticality_list
]


# Maintenance action table

# Sample data for the table

data_complete_asset_sw = [
    {"Phase": "","Component": "", "Latest update":"", "Insulation Resistance [GΩ]":"", "Polarization Index":""},

]

data_complete_asset_pd_sw = [
    {"Panel": "","Panel tag": "", "Latest update":"", "Partial Discharge":""},

]

#insert data form initialization
initial_columns = []
initial_data = []
##################################################################################################################################################################################

def convert_to_datetime(date_str):
    # Define the date format
    date_format = "%d-%m-%Y %H:%M"
    return datetime.strptime(date_str, date_format)
############################################ blank graph risk index

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template='plotly_dark')
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig

#### voice recognition + text to speach
# Global variables to control transcription
transcribed_text = ""
is_transcribing = False
transcription_thread = None

#
# def transcribe_voice():
#     global transcribed_text, is_transcribing
#     recognizer = sr.Recognizer()
#
#     with sr.Microphone() as source:
#         print("Listening indefinitely...")
#
#         while is_transcribing:
#             try:
#                 # Adjust for ambient noise, but reduce frequency if not necessary
#                 recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Shorter duration
#                 # Listen for audio with a smaller timeout
#                 audio = recognizer.listen(source, timeout=0.5)  # Shorter timeout
#
#                 print("Transcribing...")
#                 # Use Google Web Speech API to transcribe
#                 text = recognizer.recognize_google(audio)
#                 print("You said: " + text)
#
#                 # Update the transcribed_text variable
#                 transcribed_text += text + '\n'
#
#             except sr.WaitTimeoutError:
#                 continue  # Ignore if no audio detected
#             except sr.UnknownValueError:
#                 continue  # Ignore unrecognized audio
#             except sr.RequestError as e:
#                 print(f"Could not request results from Google Speech Recognition service; {e}")
#             except Exception as e:
#                 print(f"An unexpected error occurred: {e}")
#
# #speach
# def text_to_voice(text, filename='output.mp3', play_audio=False):
#     # Create a gTTS object
#     tts = gTTS(text=text, lang='en')
#
#     # Save the audio file
#     tts.save(filename)
#     print(f"Audio saved as {filename}")
#
#     # Optionally play the audio
#     if play_audio:
#         playsound(filename)


################### plot the app
# Layout of Dash App
layout = html.Div(



    children=[
        dcc.Store(id='store', storage_type='session'),
        # dcc.Location(id='url', refresh=False),
        html.Div(id='content-switchgear-raw-data'),
        dcc.Location(id='url1'),
        dcc.Location(id='url2'),
        dcc.Location(id='url3'),

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



                        html.H3("Asset Information"),
                        html.P(id="AssetTag"),
                        html.P(id='Insulation'),
                        html.P(id='Numberofbus'),
                        html.P(id='Numberofpanels'),
                        html.P(id="RatedVoltage"),
                        html.P(id="Manufactor"),
                        html.P(id="YOM"),
                        html.P(id='YOI'),
                        html.Div(id='dummy_as', style={'display': 'none'}),
                        html.Div(id='dummy_table_raw_data_sw', style={'display': 'none'}),

                        html.Br(),
                        html.P(id='Asset Risk Index',style={'fontSize': 16}),
                        html.P(id='Asset Health Index',style={'fontSize': 16}),
                        html.P(id='Latest Assessment'),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            id='insert_data_sw_air',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Insert new test record', id='open_modal_btn1_sw_air', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),
                        html.Br(),
                        html.Div(
                            id='button-container_analysis_sw',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Update Risk assessment', id='risk_assessment_data_sw', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),
                        html.Br(),
                        html.Div(
                            id='button-container_export',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Export Latest assessment', id='export_assessment_sw', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),
                                dcc.Download(id='download-dataframe-csv')

                            ]
                        ),
                        html.Br(),
                        html.Div(
                            id='button-container',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Update Asset Criticality', id='open_modal_btn', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

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

                        html.Div(id='start-button', style={
                                'position': 'fixed',
                                'top': '20px',  # Adjust as needed
                                'left': '20px',  # Adjust as needed
                                'z-index': 1000,
                                'background': 'linear-gradient(to bottom, #C0C0C0,#D3D3D3)',
                                'border': '1px solid #A9A9A9' ,
                                'border-radius': '50%',  # Circle shape
                                'padding': '15px',
                                'cursor': 'pointer',
                                'box-shadow': '0 4px 15px rgba(0, 0, 0, 0.3)',
                            }, children=[
                                html.Img(src='/assets/microphone_off.png', style={
                                    'width': '50px',
                                    'height': '50px',
                                })
                            ]),
                        #
                        # # Hidden Div for capturing voice input
                        html.Div(id='hidden-div', style={'display': 'none'}),
                        #
                        html.Div(id='voice_control_output-switchgear', style={'display': 'none'}),
                        html.Div(id='dummy-output-switchgear', style={'display': 'none'}), # Dummy output for callback


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
                        html.Div(
                            children=[
                                dcc.Markdown(
                                    """
                                    Powered By: [InWave](https://www.inwave.au)
                                    """,
                                    style={'font-size': '10px'}  # Adjust the font size as needed
                                )
                            ],

                        )
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    style={'height': '100%'},
                    children=[


                        html.Br(),
                        # html.H3("Executive Summary", style={'display': 'flex', 'justify-content': 'center'}),

                        html.Br(),


                        html.Div(className='image-container', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100%','z-index': 1, 'margin-top':'150px'},

                                 children=[
                                html.Img(
                                    src=dash.get_asset_url('air_switchgear_main.png'),  # Replace with your image path
                                    style={'border-radius': '15px','max-width': 'auto', 'height': 'auto', 'position': 'absolute', 'top':'0',"object-fit": "cover", 'margin-top':'50px'}
                                    # style={'max-width': '100%', 'height': 'auto', 'position': 'relative'}
                                ),
                                html.Div(id='circle1_bays', className='circle', children=[
                                    html.Span(id='circle1number_bays',children="1", className="circle-number", style={"color": "white"},
                                              title="Stator Health Index, click to see details"),
                                ], style={
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "red",  # Custom color
                                        "border-radius": "50%",
                                        "display": "None",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "margin-top": "10px",  # Adjust vertical position
                                        "margin-bottom": "10px",
                                        'opacity': 0.6,
                                        'top':'140px',
                                        'left': '130px',
                                        'position': "relative",
                                        'cursor':'pointer'
                                    }),

                                html.Div(id='circle2_bus', className='circle',
                                         children=[html.Span(id='circle2number_bus', children="2", className="circle-number", style={"color": "white"},
                                              title="Rotor Health Index, click to see details"),
                                ], style={
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "red",  # Custom color
                                        "border-radius": "50%",
                                        "display": "None",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "margin-top": "10px",  # Adjust vertical position
                                        "margin-bottom": "10px",
                                        'opacity': 0.6,
                                        'top': '20px',
                                        'left': '170px',
                                        "position": "relative",
                                        'cursor':'pointer'
                                    }),



                                html.Div(id='circle3_mainins', className='circle', children=[
                                    html.Span(id='circle3number_mainins',children="3", className="circle-number", style={"color": "white"},
                                              title="Auxiliaries Health Index, click to see details"),
                                ], style={
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "red",  # Custom color
                                        "border-radius": "50%",
                                        "display": "None",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "margin-top": "10px",  # Adjust vertical position
                                        "margin-bottom": "10px",
                                        'opacity': 0.6,
                                        'top': '-80px',
                                        'left': '-160px',
                                        "position": "relative",
                                        'cursor':'pointer'
                                    }),

                        ]),

                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        html.Div(
                            style={'display': 'flex', 'justifyContent': 'center', 'margin': '20px', 'margin-top':'100px'},
                            children=[
                                DataTable(
                                    id='raw_data_summary_sw',
                                    columns=[
                                        {"name": "Phase", "id": "phase"},
                                        {"name": "Component", "id": "component"},
                                        {"name": "Latest update", "id": "latest_test_date"},
                                        {"name": "Insulation Resistance [GΩ]", "id": "latest_ir"},
                                        {"name": "Polarization Index", "id": "latest_pi"},
                                    ],
                                    data=data_complete_asset_sw,
                                    style_table={'overflowX': 'auto', 'width': '100%'},
                                    style_cell={
                                        'backgroundColor':'grey' ,  # Header background color
                                        'color': 'black',  # Header text color
                                        'textAlign': 'center',
                                        'whiteSpace': 'normal',  # Allow text to wrap
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',  # Handle overflow
                                        'width': '100px',
                                        'height': '50px',
                                    },
                                    style_header={
                                        'backgroundColor': 'rgb(17,17,17)',  # Header background color
                                        'color': 'white',  # Header text color
                                        'textAlign': 'center',  # Center header text
                                    },
                                    page_size=10,  # Adjust as needed
                                ),
                            ]
                        ),

                        html.Br(),

                        html.Div(
                            style={'display': 'flex', 'justifyContent': 'center', 'margin': '20px', 'margin-top':'50px'},
                            children=[
                                DataTable(
                                    id='raw_data_summary_pd_sw',
                                    columns=[
                                        {"name": "Panel", "id": "panel"},
                                        {"name": "Panel tag", "id": "tag"},
                                        {"name": "Latest update", "id": "latest_test_date"},
                                        {"name": "Partial Discharge", "id": "latest_pd"},
                                    ],
                                    data=data_complete_asset_pd_sw,
                                    style_table={'overflowX': 'auto', 'width': '100%'},
                                    style_cell={
                                        'backgroundColor':'grey' ,  # Header background color
                                        'color': 'black',  # Header text color
                                        'textAlign': 'center',
                                        'whiteSpace': 'normal',  # Allow text to wrap
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',  # Handle overflow
                                        'width': '100px',
                                        'height': '50px',
                                    },
                                    style_header={
                                        'backgroundColor': 'rgb(17,17,17)',  # Header background color
                                        'color': 'white',  # Header text color
                                        'textAlign': 'center',  # Center header text
                                    },
                                    style_cell_conditional=[
                                        {
                                            'if': {'column_id': 'latest_pd'},  # Specify the column to target
                                            'width': '200px',  # Set the width for this specific cell
                                        },
                                        ],

                                    page_size=10,  # Adjust as needed
                                ),
                            ]
                        ),

                        html.Br(),
                        html.Div(id='graph1', style={'display':'none'}),
                        html.Div(id='graph2', style={'display': 'none'}),
                        html.Div(id='TrendRisk',style={'display': 'none'} ),
                        html.Div(id='online-button', style={'display': 'none'}),
                        html.Div(id='offline-button', style={'display': 'none'}),
                        html.Div(id='complete_maintenance_table_sw', style={'display': 'none'}),

                        html.Br(),
                        dbc.Container(fluid=True,
                                      style={'backgroundColor': 'clear', 'color': 'white', 'height': '150vh',
                                             'textAlign': 'center', 'margin-bottom': '30px', },
                                      children=[
                                          # html.H1(children='Data Trends', style={'textAlign': 'center'}),

                                          dbc.Row([
                                              dbc.Col(dbc.Button("Online Results Trend", id="online-button-sw",
                                                                 color="primary", className="mb-3"), width=10,
                                                      style={'margin-bottom': '20px'}),
                                              dbc.Col(dbc.Button("Offline Results Trend", id="offline-button-sw",
                                                                 color="primary", className="mb-3"), width=10),

                                          ]),

                                          dbc.Row([
                                              dbc.Col(id='online-container-sw', width=12, style={'margin-bottom': '20px'}),
                                              dbc.Col(id='offline-container-sw', width=12,
                                                      style={'margin-bottom': '20px'}),
                                          ]),
                                      ]),
                        dbc.Container(
                            id='raw-data-graph-container-sw',
                            style={'display': 'block', 'padding': '10px', 'width': '100%'}  # Initial style can be hidden
                        ),

                    ],
                ),
            ],),
# Modal Popup
    html.Div(
        id='modal',
        style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)', 'z-index': 1000},
        children=[
            html.Div(
                id='modal_content',
                style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc', 'border-radius': '5px'},
                children=[
                    html.H5('Asset Criticality', style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                    # html.P('This is a modal popup.'),
                    html.H3(
                            'The Criticality Index is assigned to each asset based on the severity of a failure occurring and the impact this failure would have.',
                            style={'color': 'black', 'font-size': 10, "text-align": "justified"}),
                    html.H3(
                            'Please select the desired asset Criticality Index as per the table below',
                            style={'color': 'black', 'font-size': 10, "text-align": "justified"}),
                    dcc.Dropdown(
                        id='dropdown-menu',
                        options=[
                            {'label': 'Class 1', 'value': '5'},
                            {'label': 'Class 2', 'value': '4'},
                            {'label': 'Class 3', 'value': '3'},
                            {'label': 'Class 4', 'value': '2'},
                            {'label': 'Class 5', 'value': '1'}
                        ],
                        value='5'  # Default value
                    ),
                    html.Br(),

                    dash_table.DataTable(
                        id='criticality-table_data',
                        columns=[
                                        {'name': 'Class', 'id': 'Class'},
                                        {'name': 'Safety Consequences', 'id': 'Safety consequences'},
                                        {'name': 'Environmental consequences', 'id': 'Environmental consequences'},
                                        {'name': 'Financial consequences', 'id': 'Financial consequences'},
                                        {'name': 'Reliability consequences', 'id': 'Reliability consequences'}
                                    ],
                        data=data_for_table_criticality,
                        style_table={'overflowX': 'auto',
                                     'width':'800px',
                                     'font-size': 10},
                        style_cell={
                                        'textAlign': 'left',
                                        'padding': '5px',
                                        'color': 'black',
                                     },
                        style_header={
                                        'backgroundColor': 'rgb(230, 230, 230)',
                                        'fontWeight': 'bold'
                                    },
                        ),
                html.Div(
                    style={'display': 'flex', 'justify-content': 'center', 'margin-top': '10px'},
                    children=[
                        html.Button('Update', id='save_modal_btn', style={'color': 'black', 'width': '100px', 'background-color': 'green', 'border-color': 'grey', 'opacity': 0.9}),
                        html.Button('Exit', id='close_modal_btn', style={'color': 'black', 'width': '100px', 'background-color': 'red', 'border-color': 'grey', 'opacity': 0.9, 'margin-left': '10px'})
                    ]
                ),
                ]
            )
        ]
    ),
    html.Div(id='risk_assessment', style={'display': 'none'}),
    html.Div(id='close_risk_assessment', style={'display': 'none'}),
    html.Div(id='complete_risk_assessment', style={'display': 'none'}),
    html.Div(id='complete_risk_assessment_tx', style={'display': 'none'}),
    html.Div(id='risk_assessment_tx', style={'display': 'none'}),
    html.Div(id='close_risk_assessment_tx', style={'display': 'none'}),
    html.Div(id='complete_risk_assessment_ugtl', style={'display': 'none'}),
    html.Div(id='risk_assessment_ugtl', style={'display': 'none'}),
    html.Div(id='close_risk_assessment_ugtl', style={'display': 'none'}),
    html.Div(id='risk_assessment_btn_ugtl', style={'display': 'none'}),
    html.Div(id='risk_assessment_title_ugtl', style={'display': 'none'}),
    html.Div(id='risk_assessment_btn_tx', style={'display': 'none'}),
    html.Div(id='risk_assessment_title_tx', style={'display': 'none'}),
    html.Div(id='risk_assessment_btn_generator', style={'display': 'none'}),
    html.Div(id='risk_assessment_title_generator', style={'display': 'none'}),
    html.Div(id='risk_assessment_bottom_cb', style={'display': 'none'}),
    html.Div(id='risk_assessment_title', style={'display': 'none'}),

    html.Div(id='risk_assessment_title_cb', style={'display': 'none'}),



    html.Div(
            id='risk_assessment_sw',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='risk_assessment_content',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Do you want to update the risk assessment?',
                                id='risk_assessment_title_sw',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        # html.Div(
                        #     id='risk_assessment_message',  # Placeholder for dynamic message
                        #     style={'color': 'black', 'text-align': 'center', 'margin-top': '10px'}
                        # ),

                        html.Div(
                            children=[
                                html.Button('Yes', id='complete_risk_assessment_sw', disabled=False,
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_risk_assessment_sw',
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
            id='Insert_data_sw_air_data1',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content_sw_air',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Select test type',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dcc.Dropdown(
                            id='dropdown-menu_sw_air',
                            options=[
                                {'label': 'Online test', 'value': '1'},
                                {'label': 'Offline test', 'value': '2'},
                            ],
                            value='',
                            # style={'backgroundColor': '#000000', 'color': 'white', 'opacity':'1'},

                        ),

                        html.Div(
                            children=[
                                html.Button('Next', id='open_modal_btn2_sw_air',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_modal_btn1_sw_air',
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
            id='Insert_data_sw_air_data2',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content2_sw_air',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Select test from the list',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dcc.Dropdown(
                            id='dropdown-menu2_sw_air',
                            options=[

                            ],
                            value='',
                            # style={'backgroundColor': 'black', 'color': 'white', 'opacity':'1'},
                        ),

                        html.Div(
                            children=[
                                html.Button('Next', id='open_modal_btn3_sw_air',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_modal_btn2_sw_air',
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
            id='Insert_data_sw_air_data3',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content3_sw_air',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px','overflow-y': 'auto', 'overflow-x': 'auto','max-width': '80vw'},
                    children=[
                        html.H5('Insert the data below',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dash_table.DataTable(
                            id='editable-table_data_sw_air',
                            columns=initial_columns,
                            data=initial_data,
                            style_cell={'textAlign': 'center', 'color':'black'},
                            editable=True,  # Enable editing in cells
                            row_deletable=True,

                        ),
                        html.Button('+', id='add_row_btn_sw_air', n_clicks=0, style={'margin-top': '10px'}),

                        html.Div(
                            children=[
                                html.Button('Confirm', id='save_modal_btn3_sw_air',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_modal_btn3_sw_air',
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
            id='Insert_data_sw_air_data_online_pd1',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content4_sw_air',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Which Panel?',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dcc.Dropdown(
                            id='dropdown-menu3_sw_air',
                            options=[

                            ],
                            value='',
                            # style={'backgroundColor': 'black', 'color': 'white', 'opacity':'1'},
                        ),

                        html.Div(
                            children=[
                                html.Button('Next', id='open_modal_btn_onlinepd2_sw_air',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_modal_btn_onlinepd1_sw_air',
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
            id='Insert_data_sw_air_data_online_pd2',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content5_sw_air',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Which component?',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dcc.Dropdown(
                            id='dropdown-menu4_sw_air',
                            options=[

                            ],
                            value='',
                            # style={'backgroundColor': 'black', 'color': 'white', 'opacity':'1'},
                        ),

                        html.Div(
                            children=[
                                html.Button('Next', id='open_modal_btn_onlinepd3_sw_air',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_modal_onlinepd2_sw_air',
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
            id='Insert_data_sw_air_data_online_pd3',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content6_sw_air',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[

                        html.H5('Connect the sensors as per the picture below and press Start',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        html.Div(
                            style={'display': 'flex', 'justify-content': 'center'},
                            children=[
                            html.Img(
                                src='/assets/sw_air_tev.png',  # Replace with your image path
                                style={'width': '300px', 'height': '200px','margin-top': '10px', 'border-radius': '5px'}
                        )]
                        ),

                        html.Div(
                            children=[
                                html.Button('Start', id='start_online_btn_onlinepd_sw_air',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_modal_onlinepd3_sw_air',
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
            id='Insert_data_sw_air_data_online_progress',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content_progress_sw_air',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Processing...',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        html.Div(
                            [
                                dbc.Spinner(size="lg"),  # Circular spinner
                                html.Div("Please wait while the process is ongoing...", className="mt-3")
                            ],
                            style={'text-align': 'center'}
                        ),
                        html.Div(
                            children=[
                                html.Button('Close', id='close_progress_modal_sw_air',
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


@callback(
    Output('content-switchgear-raw-data', 'children', allow_duplicate=True),
    Input('store', 'data'),
    prevent_initial_call='initial_duplicate'
)
def display_selected_asset(selected_asset):
    if selected_asset:
        global asset_selected_details

        asset_selected_details.insert(0, selected_asset)
        # asset_selected_details.append(selected_asset)
        content = ''

    content=''

    return content

#
#
############ data visualization ####################




@callback(
    Output('raw_data_summary_sw','data'),
    Output('raw_data_summary_pd_sw', 'data'),
    Input('dummy_table_raw_data_sw', 'children'),
    prevent_initial_call='initial_duplicate'
)
def display_selected_asset(selected_asset):
    def populate_data(data_lists):

        data = []

        # Extract the latest update date from the first list
        try:
            latest_update = max(entry[0] for entry in data_lists[0])

            for i in range(len(data_lists[0])):  # Assuming all lists have the same length
                entry = {
                    "phase": data_lists[0][i][1],  # Phase from the first list
                    "component": data_lists[0][i][2],  # Core from the first list
                    "latest_test_date": latest_update,
                    "latest_ir": data_lists[0][i][3],  # Insulation resistance from the second list
                    "latest_pi": data_lists[1][i][3],  # Polarization index from the third list

                }
                data.append(entry)
        except ValueError:
            entry = {
                "phase": 'NA',  # Phase from the first list
                "component": 'NA',  # Core from the first list
                "latest_test_date": 'NA',
                "latest_ir": 'NA',  # Insulation resistance from the second list
                "latest_pi": 'NA',  # Polarization index from the third list

            }
            data.append(entry)
        return data
    def populate_data_pd(data_lists):

        data = []

        # Extract the latest update date from the first list
        # latest_update = max(entry[0] for entry in data_lists[0])

        for i in range(len(data_lists[0])):# Assuming all lists have the same length

            entry = {
                "panel": data_lists[0][i][2],  # Phase from the first list
                "tag": data_lists[0][i][3],  # Core from the first list
                "latest_test_date": 'NA',
                "latest_pd": 'NA',  # Insulation resistance from the second list

            }
            data.append(entry)

        return data

    global asset_selected_details

    data = []
    data_pd = []

    asset_id = asset_selected_details[0]['points'][0]['customdata'][0]
    sw_layout = get_asset_sw_layout_individual_sw(asset_id)

    # # get data
    latest_ir = get_offline_latest_IR_value_for_summary_table_sw(asset_id)
    latest_pi = get_offline_latest_PI_value_for_summary_table_sw(asset_id)
    online_pd_data = []
    #
    # # create the data set
    #
    data_list = [latest_ir, latest_pi]
    #
    data = populate_data(data_list)

    data_pd_list = [sw_layout, online_pd_data]
    data_pd = populate_data_pd(data_pd_list)


    return data, data_pd


# # Track visibility state of the graphs
graph_visibility = {
    'online': True,
    'offline': True
}

# Callbacks to update graphs based on button clicks
#online
@callback(
    Output('online-container-sw', 'children', allow_duplicate=True),
    [Input('online-button-sw', 'n_clicks')],
    prevent_initial_call='initial_duplicate'
)
def update_online_container(n_clicks):
    global graph_visibility
    global asset_selected_details


    if n_clicks:


        graph_visibility['online'] = not graph_visibility['online']  # Toggle visibility
        if graph_visibility['online']:

            asset_id=asset_selected_details[0]['points'][0]['customdata'][0]

            online_data_analysis = get_online_test_analysis_data_full_asset(asset_id)
            result_dict = {}
            # Create a DataFrame
            df = pd.DataFrame(online_data_analysis, columns=['Date', 'Test', 'Value'])

            # Group by Date and Test, and keep the row with the maximum Value
            data_cleaned = df.loc[df.groupby(['Date', 'Test'])['Value'].idxmax()]

            # Convert cleaned DataFrame back to a list of tuples
            data_cleaned = [tuple(row) for row in data_cleaned.to_numpy()]
            sorted_data = sorted(data_cleaned, key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))


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
                30: ('Online PD', 'ONPD'),

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
    Output('offline-container-sw', 'children', allow_duplicate=True),
    [Input('offline-button-sw', 'n_clicks')],
    prevent_initial_call='initial_duplicate'
)
def update_offline_container(n_clicks):
    global graph_visibility
    global asset_selected_details
    if n_clicks:
        graph_visibility['offline'] = not graph_visibility['offline']  # Toggle visibility
        if graph_visibility['offline']:
            asset_id = asset_selected_details[0]['points'][0]['customdata'][0]

            offline_data_analysis = get_offline_test_analysis_data_full_asset(asset_id)


            result_dict = {}


            #clean the data set to have the worst result of the multiple data for the same test/date
            # Create a DataFrame
            df = pd.DataFrame(offline_data_analysis, columns=['Date', 'Test', 'Value'])
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
                23: ('Insulation Resistance', 'IR'),
                24: ('Polarization Index', 'PI'),

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


#change style button
@callback(
    [Output('online-button-sw', 'style'),
     Output('offline-button-sw', 'style')],
    [Input('online-button-sw', 'n_clicks'),
     Input('offline-button-sw', 'n_clicks')]
)

def update_button_style(online_n_clicks, offline_n_clicks):
    style_online = {'width': '300px', 'background-color': 'grey', 'border-color': 'grey', 'color': 'black',
                    'font-weight': 'bold'}
    style_offline = {'width': '300px', 'background-color': 'grey', 'border-color': 'grey', 'color': 'black',
                     'font-weight': 'bold'}

    if online_n_clicks is not None and online_n_clicks % 2 == 1:
        style_online['background-color'] = 'darkgrey'

    if offline_n_clicks is not None and offline_n_clicks % 2 == 1:
        style_offline['background-color'] = 'darkgrey'

    return style_online, style_offline
