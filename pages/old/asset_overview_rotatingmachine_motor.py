import time

import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
from dash import Dash, clientside_callback
from dash import dcc, callback_context
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

from connectors.db_connectors_mysql import get_component_analysis
from connectors.db_connectors_mysql import get_failure_mechanism_single_asset_list
from connectors.db_connectors_mysql import get_failure_mechanisms_analysis
from connectors.db_connectors_mysql import get_subcomponent_analysis

from connectors.db_connectors_mysql import update_asset_criticality
from connectors.db_connectors_mysql import get_asset_analysis
from connectors.db_connectors_mysql import export_asset_summary
from connectors.db_connectors_mysql import get_criticality_list
from connectors.db_connectors_mysql import get_maintenance_action

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
    style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '20px'}
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
    style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}

)





######## failure mode table:

failure_mechanisms_list = get_failure_mechanism_single_asset_list(1)




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
data_complete_maintenance_action = [
    {"Asset Tag": "", "Open Maintenance Action": "", "Peer Name":"", "Peer review comment":"", "Review date":""},

]

##################################################################################################################################################################################

def convert_to_datetime(date_str):
    # Define the date format
    date_format = "%d-%m-%Y"
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
#

################### plot the app
# Layout of Dash App

layout = html.Div(



    children=[
        # dcc.Store(id='store', storage_type='session'),
        dcc.Location(id='url', refresh=False),
        html.Div(id='content-motor'),
        dcc.Location(id='url1_m'),
        dcc.Location(id='url2_m'),
        dcc.Location(id='url3_m'),

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
                        html.P(id='Function'),
                        html.P(id='Type'),
                        html.P(id="RatedVoltage"),
                        html.P(id="Manufactor"),
                        html.P(id="YOM"),
                        html.P(id='YOI'),
                        html.Div(id='dummy_m', style={'display': 'none'}),
                        html.Br(),
                        html.P(id='Asset Risk Index',style={'fontSize': 16}),
                        html.P(id='Asset Health Index',style={'fontSize': 16}),
                        html.P(id='Latest Assessment'),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        html.Div(
                            id='button-container_analysis_motor',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Update Risk assessment', id='risk_assessment_data', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),
                        html.Br(),
                        html.Div(
                            id='button-container_export',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Export Latest assessment', id='export_assessment_m', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),
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
                        html.Div(id='voice_control_output-motor', style={'display': 'none'}),
                        html.Div(id='dummy-output-motor', style={'display': 'none'}), # Dummy output for callback


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
                            # style={
                            #     'display': 'flex',
                            #     'justify-content': 'left',  # Center horizontally
                            #     'align-items': 'flex-enf',  # Align to the bottom
                            #     # 'height': '100vh',  # Full height of the viewport
                            #     'padding': '10px',  # Add some padding if needed
                            #     'position': 'absolute',  # Use absolute positioning
                            #     # 'bottom': '800',  # Position at the bottom
                            #     'width': '100%',  # Full width
                            #     'text-align': 'center'  # Center text
                            # }
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
                                    src=dash.get_asset_url('rotating_machine_generator_spa.jpg'),  # Replace with your image path
                                    style={'max-width': 'auto', 'height': 'auto', 'position': 'absolute', 'top':'0',"object-fit": "cover", 'margin-top':'50px'}
                                    # style={'max-width': '100%', 'height': 'auto', 'position': 'relative'}
                                ),
                                html.Div(id='circle1_stator_m', className='circle', children=[
                                    html.Span(id='circle1number_stator_m',children="1", className="circle-number", style={"color": "white"},
                                              title="Stator Health Index, click to see details"),
                                ], style={
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "red",  # Custom color
                                        "border-radius": "50%",
                                        "display": "none",
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

                                html.Div(id='circle2_rotor_m', className='circle',
                                         children=[html.Span(id='circle2number_rotor_m', children="2", className="circle-number", style={"color": "white"},
                                              title="Rotor Health Index, click to see details"),
                                ], style={
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "red",  # Custom color
                                        "border-radius": "50%",
                                        "display": "none",
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



                                html.Div(id='circle3_aux_m', className='circle', children=[
                                    html.Span(id='circle3number_aux_m',children="3", className="circle-number", style={"color": "white"},
                                              title="Auxiliaries Health Index, click to see details"),
                                ], style={
                                        "width": "40px",
                                        "height": "40px",
                                        "background-color": "red",  # Custom color
                                        "border-radius": "50%",
                                        "display": "none",
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


                        html.Div(
                            id='container-frame-risk',
                            style={
                                'padding': '10px',
                                'border-radius': '5px',
                                'margin-top': '250px',
                            },
                            children=[
                                # html.H4("Risk Index", style={'text-align':'center'}),
                                #
                                dcc.Graph(id="TrendRisk", figure=blank_fig(),
                                  config={
                                      "displaylogo": False,
                                      'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines', 'hoverClosestCartesian', 'hoverCompareCartesian']
                                  },  # remove ploty botton
                                  ),   #plot the line chart
                        html.Br(),

                            ],

                        ),
                        html.Div(
                                    id='risk-legend-modal',
                                    style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                                           'transform': 'translate(-50%, -50%)', 'z-index': 1000},
                                    children=[
                                        html.Div(
                                            id='risk_legend_content',
                                            style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                                                   'border-radius': '5px'},
                                            children=[
                                                html.H5('Risk Index Legend',
                                                        id='risk_assessment_title',
                                                        style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                                                html.H3(
                                                    'The Risk Index is calculated through multiplication of the Health Index and Criticality Index for each individual asset.\n',
                                                    style={'color': 'black', 'font-size': 10, "text-align": "justified"}),
                                                html.H3(
                                                    'The Risk Index can be used to risk ranking the asset and determine the management strategy',
                                                    style={'color': 'black', 'font-size': 10,
                                                           "text-align": "justified"}),

                                                # Risk meaning
                                                html.Img(
                                                    src='/assets/risk_index_meaning.png',  # Replace with the actual path to your image
                                                    style={'width': '100%', 'margin-top': '10px', 'border-radius': '5px'}
                                                ),


                                                html.Div(
                                                    children=[
                                                        html.Button('Ok', id='confirm-risk-legend', disabled=False,
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
                        html.Div(id='right-click-data', style={'display': 'none'}),
                        # html.Br(),

                        html.Div(
                            id='container-frame',
                            # className='graph-container-frame',
                            style={
                                # 'border': '1px solid black',
                                # 'display': 'flex',
                                'flex-direct': 'column',
                                'justify-content': 'center',  # Center horizontally
                                'align-items': 'center',
                                'padding': '10px',
                                'border-radius': '5px',
                                'margin-top': '10px',
                                'width': '100%',
                                'margin-left': 'auto',  # Center horizontally
                                'margin-right': 'auto',
                                "overflow": "auto",
                            },
                            children=[
                                html.Div(
                                            children=graph1,
                                            style={'margin-bottom': '50px', 'width': '100%', 'height':'auto'}  # Add some space between the graphs
                                        ),
                                html.Div(
                                            children=graph2,
                                            style={ 'width': '100%','height': 'auto'}
                                        )

                                # graph1,  # Display graph1
                                # graph2

                            ]
                        ),
                        #model for legen of Hi
                        html.Div(
                                    id='hi-legend-modal',
                                    style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                                           'transform': 'translate(-50%, -50%)', 'z-index': 1000,},
                                    children=[
                                        html.Div(
                                            id='hi_legend_content',
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
                                                        html.Button('Ok', id='confirm-hi-legend', disabled=False,
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
                                    id='fm-legend-modal',
                                    style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                                           'transform': 'translate(-50%, -50%)', 'z-index': 1000,},
                                    children=[
                                        html.Div(
                                            id='fm_legend_content',
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
                                                        html.Button('Ok', id='confirm-fm-legend', disabled=False,
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
                        html.Div(
                            style={'display': 'flex', 'justifyContent': 'center', 'margin': '20px'},
                            children=[
                                DataTable(
                                    id='complete_maintenance_table_m',
                                    columns=[
                                        {"name": "Asset Tag", "id": "Asset Tag"},
                                        {"name": "Open Maintenance Action", "id": "Open Maintenance Action"},
                                        {"name": "Peer Name", "id": "Peer Name"},
                                        {"name": "Peer review comment", "id": "Peer review comment"},
                                        {"name": "Review date", "id": "Review date"},

                                    ],
                                    data=data_complete_maintenance_action,
                                    style_table={'overflowX': 'auto', 'width': '100%'},
                                    style_cell={
                                        'backgroundColor':'grey' ,  # Header background color
                                        'color': 'black',  # Header text color
                                        'textAlign': 'center',
                                        'whiteSpace': 'normal',  # Allow text to wrap
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',  # Handle overflow
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


                        html.Br(),
                        html.Br(),

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
    html.Div(id='complete_risk_assessment_tx', style={'display': 'none'}),
    html.Div(id='risk_assessment_tx', style={'display': 'none'}),
    html.Div(id='close_risk_assessment_tx', style={'display': 'none'}),
    html.Div(id='complete_risk_assessment_ugtl', style={'display': 'none'}),
    html.Div(id='risk_assessment_ugtl', style={'display': 'none'}),
    html.Div(id='close_risk_assessment_ugtl', style={'display': 'none'}),
    html.Div(id='risk_assessment_bottom_cb', style={'display': 'none'}),
    html.Div(id='risk_assessment_title_cb', style={'display': 'none'}),
    html.Div(id='risk_assessment_btn_tx', style={'display': 'none'}),
    html.Div(id='risk_assessment_title_tx', style={'display': 'none'}),
    html.Div(id='risk_assessment_btn_generator', style={'display': 'none'}),
    html.Div(id='risk_assessment_title_generator', style={'display': 'none'}),
    html.Div(id='risk_assessment_btn_sw', style={'display': 'none'}),
    html.Div(id='risk_assessment_title_sw', style={'display': 'none'}),
    html.Div(id='risk_assessment_btn_ugtl', style={'display': 'none'}),
    html.Div(id='risk_assessment_title_ugtl', style={'display': 'none'}),

    html.Div(
            id='risk_assessment',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='risk_assessment_content',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Do you want to update the risk assessment?',
                                id='risk_assessment_title',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        # html.Div(
                        #     id='risk_assessment_message',  # Placeholder for dynamic message
                        #     style={'color': 'black', 'text-align': 'center', 'margin-top': '10px'}
                        # ),

                        html.Div(
                            children=[
                                html.Button('Yes', id='complete_risk_assessment', disabled=False,
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close_risk_assessment',
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



])





#######################################################################################################################
#######################         call back function

# asset_selected_details = []


@callback(
    Output('content-motor', 'children'),
    Input('store', 'data'),
    prevent_initial_call='initial_duplicate'
)
def display_selected_asset(selected_asset):
    # print('motor',selected_asset)
    if selected_asset:
        global asset_selected_details
        asset_selected_details.insert(0, selected_asset)
        # print(asset_selected_details)
        # print('motor',selected_asset)
        # asset_selected_details.append(selected_asset)
        content = ''

    content=''

    return content



### update data in the dashboard and graphs
@callback(
    Output("AssetTag", "children", allow_duplicate=True),
    Output("Function", "children", allow_duplicate=True),
    Output("Type", "children", allow_duplicate=True),
    Output("RatedVoltage", "children", allow_duplicate=True),
    Output("Manufactor", "children", allow_duplicate=True),
    Output("YOM", "children", allow_duplicate=True),
    Output("YOI", "children", allow_duplicate=True),
    Output("Asset Risk Index", "children", allow_duplicate=True),
    Output('Asset Risk Index', 'className', allow_duplicate=True),
    Output("Asset Health Index", "children", allow_duplicate=True),
    Output("Asset Health Index", "className", allow_duplicate=True),
    Output("Latest Assessment", "children", allow_duplicate=True),
    Output('circle1number_stator_m', 'children', allow_duplicate=True),
    Output('circle1_stator_m', 'style', allow_duplicate=True),
    Output('circle2number_rotor_m', 'children', allow_duplicate=True),
    Output('circle2_rotor_m', 'style', allow_duplicate=True),
    Output('circle3number_aux_m', 'children', allow_duplicate=True),
    Output('circle3_aux_m', 'style', allow_duplicate=True),
    # Output('circle-number', 'children'),
    # Output('circle-div', 'style'),
    Output('graph1', 'figure', allow_duplicate=True),
    Output('graph2', 'figure', allow_duplicate=True),
    Output('TrendRisk', 'figure', allow_duplicate=True),
    Output('complete_maintenance_table_m', 'data', allow_duplicate=True),

    [Input("dummy_m", "children")],
    prevent_initial_call='initial_duplicate',

)
def update_asset_info(store):
    global asset_selected_details

    if len(asset_selected_details)!=0:

        # print(asset_selected_details)

        asset_tag ='Asset: {}'.format(asset_selected_details[0]['points'][0]['customdata'][1])
        function = 'Function: {}'.format(asset_selected_details[0]['points'][0]['customdata'][2])
        type = 'Type: {} - {}'.format(asset_selected_details[0]['points'][0]['customdata'][11], asset_selected_details[0]['points'][0]['customdata'][12])
        rated_voltage = 'Rated Voltage: {}kV'.format(asset_selected_details[0]['points'][0]['customdata'][6])
        manufactor = asset_selected_details[0]['points'][0]['customdata'][3]
        yom = 'YOM {}'.format(asset_selected_details[0]['points'][0]['customdata'][4])
        yoi ='YOI {}'.format(asset_selected_details[0]['points'][0]['customdata'][5])

        asset_category = asset_selected_details[0]['points'][0]['customdata'][24]

        #update circle

        analysis_id = get_asset_analysis(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])



        #take latest analysis
        risk_label = analysis_id[-1][3]
        health_index_label = analysis_id[-1][4]
        latest_analysis = analysis_id[-1][1]

        risk_className = ''
        health_index_className = ''

        #define color risk circle
        if risk_label <=1:
            risk_color = '#006400'
            risk_className = 'normal'
        elif 1 < risk_label <=2:
            risk_color = 'green'
            risk_className = 'normal'
        elif 2 < risk_label <= 3:
            risk_color = "orange"
            risk_className = 'normal'
        elif 3 < risk_label <= 4:
            risk_color = "#BF5700"
            risk_className = 'normal'
        elif 4 < risk_label <=9:
            risk_color = "red"
            risk_className = 'warning'
        elif 9 < risk_label <=20:
            risk_className = 'flashing'
        else:
            risk_color = "grey"

        risk_style = {
            "width": "120px",
            "height": "60px",
            "background-color":risk_color ,  # Custom color
            "border-radius": "8%",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "margin-top": "10px",  # Adjust vertical position
            "margin-bottom": "10px",
            'opacity': 0.6,
            }


        #update label risk , health index, latest date
        latest_risk = 'Asset Risk Index: {} / 25'.format(risk_label)
        latest_health_index = 'Asset Health Index: {} / 5'.format(health_index_label)
        latest_assessment_date = 'Date: {}'.format(latest_analysis)

        component_analysis = get_component_analysis(analysis_id[-1][0])


        # print(component_analysis)
        circle_update_list = []

        health_index_comp_dict = {}
        for item in component_analysis:
            health_index_comp_dict['{}'.format(item[2])] = {'value':item[3]}

        circle=1
        for values in list(health_index_comp_dict.values()):
        # # Determine color based on condition
            if values['value'] <= 1:
                color = "#006400"
                health_index_comp_dict['{}'.format(circle)] = {'value': values['value'], 'color':color}
            elif 1 < values['value'] <= 2:
                color = "green"
                health_index_comp_dict['{}'.format(circle)] = {'value': values['value'], 'color':color}
            elif 2< values['value'] <= 3:
                color = "orange"
                health_index_comp_dict['{}'.format(circle)] = {'value': values['value'], 'color':color}
            elif 3 < values['value'] <= 4:
                color = "dark orange"
                health_index_comp_dict['{}'.format(circle)] = {'value': values['value'], 'color':color}
            elif 4 < values['value'] <= 5:
                color = "red"
                health_index_comp_dict['{}'.format(circle)] = {'value': values['value'], 'color':color}
            else:
                color = "grey"  # Default color if condition is out of expected range
                health_index_comp_dict['{}'.format(circle)] = {'value': values['value'], 'color':color}

          # Use condition as circle number



            if circle==1:

                circle_children = [
                    html.Span(id='circle1number_stator', children='Stator\n {}'.format(values['value']), className="circle-number",
                              style={"color": "white"})
                ]

                circle_style = {
                    "font-size": "12px",  # Set the font size to 8 pixels
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

                circle_style.update({'top': '190px', 'left': '190px'})

            if circle==2:
                circle_children = [
                html.Span(id='circle2number_rotor', children='Rotor\n {}'.format(values['value']), className="circle-number",
                          style={"color": "white"})
            ]

                circle_style = {
                    "font-size": "12px",  # Set the font size to 8 pixels
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

                circle_style.update({'top': '20px', 'left': '160px'})

            if circle==3:
                circle_children = [
                html.Span(id='circle3number_aux', children='Auxiliaries\n {}'.format(values['value']), className="circle-number",
                          style={"color": "white"})]

                circle_style = {
                    "font-size": "12px",  # Set the font size to 8 pixels
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

                circle_style.update({'top': '-100px', 'left': '-160px'})



            circle_update_list.append(circle_children)
            circle_update_list.append(circle_style)

            circle+=1

        #update graph 1

        analysis_date = [date[1] for date in analysis_id]
        asset_hi_data = [hi[4] for hi in analysis_id]

        # Update color based on the last health index value
        color = '#FFFFFF'  # Default to white

        try:

            if asset_hi_data[-1] == 5:
                color = '#8B0000'  # Dark red
                health_index_className = 'dark-red'
            elif asset_hi_data[-1] == 4:
                color = '#FF0000'  # Red
                health_index_className = 'red'
            elif asset_hi_data[-1] == 3:
                color = '#FFA500'  # Orange
                health_index_className = 'orange'
            elif asset_hi_data[-1] == 2:
                color = '#FFD700'  # Dark yellow (gold)
                health_index_className = 'gold'
            elif asset_hi_data[-1] == 1:
                color = '#006400'  # Dark green
                health_index_className = 'dark-green'

        except IndexError:
            color = color
            health_index_className = 'grey'
            analysis_date = [datetime.now()]

        updated_trace1 = go.Scatter(
            x=analysis_date,
            y=asset_hi_data,
            mode='lines+markers',
            name='Chart 1',
            marker=dict(color='{}'.format(color))
        )
        graph1_layout = go.Layout(
            title='Health index trend',
            titlefont=dict(color='#FFFFFF', size=14),  # Title text color (white)
            xaxis=dict(
                # title='Date',
                titlefont=dict(color='#FFFFFF'),  # X-axis title text color (white)
                tickfont=dict(color='#FFFFFF',size=10), # X-axis tick labels color (white)
                showgrid = False
            ),
            yaxis=dict(
                title='HI',
                titlefont=dict(color='#FFFFFF', size=12),  # Y-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                range=[0,5],# Y-axis tick labels color (white)
                showgrid = False
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
            height=400,
            width=900


        )

        # Remove mode bar icons
        config = {'displayModeBar': False, 'responsive': True}

        updated_graph1 = dict(data=[updated_trace1], layout=graph1_layout)

        #update graph 2
        failure_mechanism_list = get_failure_mechanism_single_asset_list(asset_category)
        failure_mechanism_analysis = get_failure_mechanisms_analysis(analysis_id[-1][0])

        fm_label = [label[1] for label in failure_mechanism_list]

        fm_value = [value[3] for value in failure_mechanism_analysis]

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

        # Determine y-axis limits
        ymin = 0
        ymax = 100
        fm_value_max = max(sorted_fm_value)
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
            title='Failure Mechanism Analysis',  # Title
            titlefont=dict(color='#FFFFFF', size=14),  # Title text color (white)
            xaxis=dict(
                titlefont=dict(color='#FFFFFF', family='Cabin', size=8),  # X-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                tickangle=30,
                showticklabels=False,# Show X-axis tick labels
                showgrid= False

            ),
            yaxis=dict(
                title='Percentage [%]',
                titlefont=dict(color='#FFFFFF', size=12),  # Y-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                range=[ymin, ymax],  # Y-axis range
                showgrid= False
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
            width=900,
            height=400,
        )

        # Remove mode bar icons
        config = {'displayModeBar': False, 'responsive':True}

        updated_graph2 = dict(data=[updated_trace2], layout=graph2_layout)


        ###### risk trend

        risk_date_trend = [records[1] for records in analysis_id]
        risk_value_trend = [records[3] for records in analysis_id]

        if len(risk_date_trend) ==0:
            risk_date_trend=[datetime.now()]

        trace = go.Scatter(x=risk_date_trend, y=risk_value_trend, mode='lines+markers', name='Trend Data',
                           line=dict(color='white', width=2))
        layout = go.Layout(
                title={
                        'text': 'Risk Index',
                        'font': {'color': 'white', 'family': 'Cabin', 'size': 18},
                        'x': 0.5,  # Center the title
                        'xanchor': 'center'},
                xaxis={'tickfont': {'color': 'white'}, 'showgrid': False},
                yaxis={'title': 'Risk', 'titlefont': {'color': 'white'}, 'tickfont': {'color': 'white'}, 'showgrid': False},

                paper_bgcolor='rgb(17,17,17)',  # Dark background color
                plot_bgcolor='rgb(17,17,17)',  # Dark background color for the plot area
                shapes=[
                    # Green background for y in [1, 4]
                    {
                        'type': 'rect',
                        'xref': 'paper',
                        'yref': 'y',
                        'x0': 0,
                        'y0': 1,
                        'x1': 1,
                        'y1': 4,
                        'fillcolor': 'green',
                        'opacity': 0.5,
                        'layer': 'below',
                        'line': {'width': 0},
                    },
                    # Orange background for y in [5, 9]
                    {
                        'type': 'rect',
                        'xref': 'paper',
                        'yref': 'y',
                        'x0': 0,
                        'y0': 4,
                        'x1': 1,
                        'y1': 9,
                        'fillcolor': 'orange',
                        'opacity': 0.5,
                        'layer': 'below',
                        'line': {'width': 0},
                    },
                    # Red background for y in [10, 20]
                    {
                        'type': 'rect',
                        'xref': 'paper',
                        'yref': 'y',
                        'x0': 0,
                        'y0': 9,
                        'x1': 1,
                        'y1': 25,
                        'fillcolor': 'red',
                        'opacity': 0.5,
                        'layer': 'below',
                        'line': {'width': 0},
                    },
                ]

            )
        fig = go.Figure(data=[trace], layout=layout)

        #update maintenance data table for the asset selected
        # get open maintenance acitons
        asset_maintenance_action_complete_list = get_maintenance_action(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
        # print(asset_maintenance_action_complete_list)
        maintenance_action_list = []
        for item in asset_maintenance_action_complete_list:
            maintenance_action_list.append(item)

        data_table = []
        for sublist in maintenance_action_list:
            data_table.append({
                    "Asset Tag": sublist[6],
                    "Open Maintenance Action": sublist[2],
                    "Peer Name": sublist[5],
                    "Peer review comment": sublist[4],
                    "Review date": sublist[3],
                })


    else:
        asset_category =1
        asset_tag = ''
        function = ''
        type = ''
        rated_voltage = ''
        manufactor= ''
        yom = ''
        yoi = ''
        risk_label = 'NA'
        risk_style = {
            "width": "120px",
            "height": "60px",
            "background-color": 'grey',  # Custom color
            "border-radius": "8%",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "margin-top": "10px",  # Adjust vertical position
            "margin-bottom": "10px",
            'opacity': 0.6,
        }
        latest_risk = ''
        risk_className = ''
        latest_health_index = ''
        health_index_className = ''
        latest_assessment_date = ''


        circle_update_list = []

        circle_style1 = {
            "width": "40px",
            "height": "40px",
            "background-color": 'grey',
            "border-radius": "50%",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "margin-top": "10px",
            "margin-bottom": "10px",
            'opacity': 0.6,
            'top': '140px',
            'left': '130px',
            'position': 'relative'
        }

        circle_style2 = {
            "width": "40px",
            "height": "40px",
            "background-color": 'grey',
            "border-radius": "50%",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "margin-top": "10px",
            "margin-bottom": "10px",
            'opacity': 0.6,
            'top': '20px',
            'left': '170px',
            'position': 'relative'
        }

        circle_style3 = {
            "width": "40px",
            "height": "40px",
            "background-color": 'grey',
            "border-radius": "50%",
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "margin-top": "10px",
            "margin-bottom": "10px",
            'opacity': 0.6,
            'top': '-80px',
            'left': '-160px',
            'position': 'relative'
        }

        circle_children1 = [
            html.Span(id='circle1number_stator', children='NA', className="circle-number",
                      style={"color": "white"})
        ]


        circle_children2 = [
                html.Span(id='circle2number_rotor', children='NA', className="circle-number",
                          style={"color": "white"})
        ]

        circle_children3 = [
                html.Span(id='circle3number_aux', children='NA', className="circle-number",
                          style={"color": "white"})
        ]


        circle_update_list.append(circle_children1)
        circle_update_list.append(circle_style1)

        circle_update_list.append(circle_children2)
        circle_update_list.append(circle_style2)

        circle_update_list.append(circle_children3)
        circle_update_list.append(circle_style3)

        # update graph 1

        analysis_date = []
        asset_hi_data = []

        updated_trace1 = go.Scatter(
            x=analysis_date,
            y=asset_hi_data,
            mode='lines+markers',
            name='Chart 1',
            marker=dict(color='blue')
        )
        graph1_layout = go.Layout(
            title='Health index trend',
            titlefont=dict(color='#FFFFFF', size=14),  # Title text color (white)
            xaxis=dict(
                title='Date',
                titlefont=dict(color='#FFFFFF'),  # X-axis title text color (white)
                tickfont=dict(color='#FFFFFF', size=10)  # X-axis tick labels color (white)
            ),
            yaxis=dict(
                title='HI',
                titlefont=dict(color='#FFFFFF', size=12),  # Y-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                range=[0, 5]  # Y-axis tick labels color (white)
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

        updated_graph1 = dict(data=[updated_trace1], layout=graph1_layout)

        # update graph 2
        failure_mechanism_list = get_failure_mechanism_single_asset_list(asset_category)

        fm_label = [label[1] for label in failure_mechanism_list]

        fm_value = [0 for value in fm_label]

        color = []

        for values in fm_value:
            if values <= 30:
                color.append("#00FF00")
            elif 30 < values <= 50:
                color.append('#FFFF00')
            elif 50 < values <= 80:
                color.append('#FFA500')
            elif 80 < values <= 90:
                color.append('#FF0000')
            elif values > 90:
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
            title='Failure Mechanism Analysis',  # Title
            titlefont=dict(color='#FFFFFF', size=12),  # Title text color (white)
            xaxis=dict(
                # title='X Axis',
                titlefont=dict(color='#FFFFFF'),  # X-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                showticklabels=False  # X-axis tick labels color (white)
            ),

            yaxis=dict(
                title='Percentage [%]',
                titlefont=dict(color='#FFFFFF', size=12),  # Y-axis title text color (white)
                tickfont=dict(color='#FFFFFF'),
                range=[ymin, ymax]  # Y-axis tick labels color (white)
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

        updated_graph2 = dict(data=[updated_trace2], layout=graph2_layout)


        ##### Risk trend

        risk_date_trend = []
        risk_value_trend = []

        trace = go.Scatter(x=risk_date_trend, y=risk_value_trend, mode='lines+markers', name='Trend Data',
                           line=dict(color='white', width=2))
        layout = go.Layout(
            # title='Trend Graph',
            xaxis={'tickfont': {'color': 'white'}, 'showgrid': False},
            yaxis={'title': 'Risk Index', 'titlefont': {'color': 'white'}, 'tickfont': {'color': 'white'},
                   'showgrid': False},

            paper_bgcolor='rgb(17,17,17)',  # Dark background color
            plot_bgcolor='rgb(17,17,17)',  # Dark background color for the plot area
            shapes=[
                # Green background for y in [1, 4]
                {
                    'type': 'rect',
                    'xref': 'paper',
                    'yref': 'y',
                    'x0': 0,
                    'y0': 1,
                    'x1': 1,
                    'y1': 4,
                    'fillcolor': 'green',
                    'opacity': 0.5,
                    'layer': 'below',
                    'line': {'width': 0},
                },
                # Orange background for y in [5, 9]
                {
                    'type': 'rect',
                    'xref': 'paper',
                    'yref': 'y',
                    'x0': 0,
                    'y0': 4,
                    'x1': 1,
                    'y1': 9,
                    'fillcolor': 'orange',
                    'opacity': 0.5,
                    'layer': 'below',
                    'line': {'width': 0},
                },
                # Red background for y in [10, 20]
                {
                    'type': 'rect',
                    'xref': 'paper',
                    'yref': 'y',
                    'x0': 0,
                    'y0': 9,
                    'x1': 1,
                    'y1': 25,
                    'fillcolor': 'red',
                    'opacity': 0.5,
                    'layer': 'below',
                    'line': {'width': 0},
                },
            ]

        )
        fig = go.Figure(data=[trace], layout=layout)



    return asset_tag, function, type, rated_voltage, manufactor, yom, yoi, latest_risk,risk_className, latest_health_index,health_index_className, latest_assessment_date, circle_update_list[0], circle_update_list[1], circle_update_list[2], circle_update_list[3], circle_update_list[4], circle_update_list[5],updated_graph1,updated_graph2, fig, data_table

#
# #handle clicl on the circle 1
# @callback(
#     Output('url1', 'pathname'),
#     Input('circle1_stator', 'n_clicks')
# )
# def handle_click(n_clicks):
#     if n_clicks is not None:
#         page_url = 'component-stator-overview-rotatingmachine-generator'
#
#         print(f'Clicked on Stator! Number of clicks: {n_clicks}')
#         return page_url
#     else:
#         # If no click, return current pathname
#         return dash.no_update
#
# #handle click on circle 2
# @callback(
#     Output('url2', 'pathname'),
#     Input('circle2_rotor', 'n_clicks')
# )
# def handle_click(n_clicks):
#     if n_clicks is not None:
#
#         page_url = 'component-rotor-overview-rotatingmachine-generator'
#
#         print(f'Clicked on Rotor! Number of clicks: {n_clicks}')
#         return page_url
#     else:
#         # If no click, return current pathname
#         return dash.no_update
#
#
# #handle click on circle 3
# @callback(
#     # Output('output-click-aux', 'children'),
#     Output('url3', 'pathname'),
#     Input('circle3_aux', 'n_clicks'),
# )
# def handle_click(n_clicks):
#     if n_clicks is not None:
#         # Replace with the desired path/route you want to navigate to
#         page_url = 'component-aux-overview-rotatingmachine-generator'
#
#         print(f'Clicked on Aux! Number of clicks: {n_clicks}')
#         return page_url
#     else:
#         # If no click, return current pathname
#         return dash.no_update
#
#
# #form - Asset Criticality
# @callback(
#     Output('modal', 'style'),
#     [Input('open_modal_btn', 'n_clicks'),
#      Input('close_modal_btn', 'n_clicks'),
#      Input('save_modal_btn', 'n_clicks')],
#     [State('modal', 'style'),
#      State('dropdown-menu', 'value')]
# )
# def toggle_modal(open_clicks, close_clicks, save_clicks, current_style, selected_value):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return current_style
#
#     trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
#
#     if trigger_id == 'open_modal_btn' and open_clicks:
#         current_style['display'] = 'block'
#     elif trigger_id == 'close_modal_btn' and close_clicks:
#         current_style['display'] = 'none'
#     elif trigger_id == 'save_modal_btn' and save_clicks:
#         # Save selected_value to database
#         asset_id=asset_selected_details[0]['points'][0]['customdata'][0]
#         today = datetime.today()
#         formatted_date = today.strftime('%d/%m/%Y')
#         criticality_id = selected_value
#
#         update_asset_criticality(criticality_id, formatted_date, asset_id)
#
#         current_style['display'] = 'none'  # Close modal after saving
#
#     return current_style
#
#
#
# ###### Action risk assessment
# @callback(
#     [Output('risk_assessment', 'style'),
#     Output('risk_assessment_title', 'children'),
#     Output('complete_risk_assessment', 'disabled'),
#      Output('complete_risk_assessment', 'style'),
#      Output('close_risk_assessment', 'children')],
#     [Input('button-container_analysis', 'n_clicks'),
#      Input('close_risk_assessment', 'n_clicks'),
#      Input('complete_risk_assessment', 'n_clicks')],
#     [State('risk_assessment', 'style'),
#      State('complete_risk_assessment', 'disabled'),
#      State('complete_risk_assessment', 'style'),
#      State('close_risk_assessment', 'children')]
# )
# def toggle_modal(update_risk_clicks, close_clicks, save_clicks, current_style,button_disabled, complete_risk_style, close_name):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return current_style, '',button_disabled, complete_risk_style, close_name
#
#     trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     message = 'Do you want to update the risk assessment?'
#
#     if trigger_id == 'button-container_analysis' and update_risk_clicks:
#         current_style['display'] = 'block'
#         button_disabled = False
#         complete_risk_style = {'color': 'black', 'width': '100px', 'margin-top': '10px',
#                                'background-color': 'green', 'border-color': 'grey',
#                                'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}
#     elif trigger_id == 'close_risk_assessment' and close_clicks:
#         current_style['display'] = 'none'
#     elif trigger_id == 'complete_risk_assessment' and save_clicks:
#         # Process saving to database or any other action needed
#
#         # Save selected_value to database
#         asset_id=asset_selected_details[0]['points'][0]['customdata'][0]
#
#
#         ### analyse the data with latest test
#
#         message = ''
#
#         #get latest assessment date
#         today = datetime.today()
#         formatted_date_str = today.strftime('%d-%m-%Y')
#
#
#         asset_analysis = get_asset_analysis(asset_id)
#
#         latest_assessment_date_str = asset_analysis[-1][1]
#
#         # Convert the date strings to datetime objects
#         latest_assessment_date = convert_to_datetime(latest_assessment_date_str)
#         formatted_date = convert_to_datetime(formatted_date_str)
#
#
#
#         if latest_assessment_date < formatted_date:
#             assess_condition(asset_id)
#             message = 'Risk assessment updated!'
#
#         else:
#             message = 'The Risk assessment is up to date!'
#
#         current_style['display'] = 'block'
#         # Disable the button after it has been clicked
#         button_disabled = True
#
#         complete_risk_style = {'color': 'black', 'width': '100px', 'margin-top': '10px',
#                  'background-color': 'grey', 'border-color': 'grey',
#                  'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px', 'display':'none'}
#
#         close_name='Close'
#
#
#
#     return current_style, message, button_disabled, complete_risk_style, close_name
#
#
# ###### legend when right click on the graph
# # Callback to toggle modal
#
# #risk graph
# @callback(
#     Output('risk-legend-modal', 'style'),
#     [Input('TrendRisk', 'clickData'), Input( 'confirm-risk-legend', 'n_clicks')],
# )
# def toggle_modal(clickData, close_btn_click):
#     if clickData and ctx.triggered[0]['prop_id'].split('.')[0] == 'TrendRisk':
#         return {'display': 'block', 'position': 'fixed', 'top': '50%', 'left': '50%',
#                 'transform': 'translate(-50%, -50%)', 'z-index': 1000}
#     elif close_btn_click:
#         return {'display': 'none'}
#     return {'display': 'none'}
#
#
# # External JavaScript for right-click handling
# index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Dash App</title>
#     </head>
#     <body>
#         <div id="dash-app"></div>
#         <script>
#             document.addEventListener('DOMContentLoaded', function() {
#                 const graphDiv = document.getElementById('TrendRisk');
#                 graphDiv.oncontextmenu = function(event) {
#                     event.preventDefault();
#                     // Trigger the click event to open the modal
#                     Dash.clientsideCallbacks.triggerInput({
#                         id: 'TrendRisk',
#                         prop: 'clickData',
#                         value: { 'points': [{ 'x': event.clientX, 'y': event.clientY }] }
#                     });
#                 };
#             });
#         </script>
#     </body>
# </html>
# '''
#
# #hi graph
# @callback(
#     Output('hi-legend-modal', 'style'),
#     [Input('graph1', 'clickData'), Input( 'confirm-hi-legend', 'n_clicks')],
# )
# def toggle_modal(clickData, close_btn_click):
#     if clickData and ctx.triggered[0]['prop_id'].split('.')[0] == 'graph1':
#         return {'display': 'block', 'position': 'fixed', 'top': '50%', 'left': '50%',
#                 'transform': 'translate(-50%, -50%)', 'z-index': 1000}
#     elif close_btn_click:
#         return {'display': 'none'}
#     return {'display': 'none'}
#
#
# # External JavaScript for right-click handling
# index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Dash App</title>
#     </head>
#     <body>
#         <div id="dash-app"></div>
#         <script>
#             document.addEventListener('DOMContentLoaded', function() {
#                 const graphDiv = document.getElementById('graph1');
#                 graphDiv.oncontextmenu = function(event) {
#                     event.preventDefault();
#                     // Trigger the click event to open the modal
#                     Dash.clientsideCallbacks.triggerInput({
#                         id: 'graph1',
#                         prop: 'clickData',
#                         value: { 'points': [{ 'x': event.clientX, 'y': event.clientY }] }
#                     });
#                 };
#             });
#         </script>
#     </body>
# </html>
# '''
#
#
# #fm graph
# @callback(
#     Output('fm-legend-modal', 'style'),
#     [Input('graph2', 'clickData'), Input( 'confirm-fm-legend', 'n_clicks')],
# )
# def toggle_modal(clickData, close_btn_click):
#     if clickData and ctx.triggered[0]['prop_id'].split('.')[0] == 'graph2':
#         return {'display': 'block', 'position': 'fixed', 'top': '50%', 'left': '50%',
#                 'transform': 'translate(-50%, -50%)', 'z-index': 1000}
#     elif close_btn_click:
#         return {'display': 'none'}
#     return {'display': 'none'}
#
#
# # External JavaScript for right-click handling
# index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Dash App</title>
#     </head>
#     <body>
#         <div id="dash-app"></div>
#         <script>
#             document.addEventListener('DOMContentLoaded', function() {
#                 const graphDiv = document.getElementById('graph2');
#                 graphDiv.oncontextmenu = function(event) {
#                     event.preventDefault();
#                     // Trigger the click event to open the modal
#                     Dash.clientsideCallbacks.triggerInput({
#                         id: 'graph2',
#                         prop: 'clickData',
#                         value: { 'points': [{ 'x': event.clientX, 'y': event.clientY }] }
#                     });
#                 };
#             });
#         </script>
#     </body>
# </html>
# '''
#
#
# # #voice regnotion for voice control
#
# @callback(
#     Output('voice_control_output', 'children'),
#     Input('start-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def start_stop_voice_recognition(n_clicks):
#     global transcribed_text, is_transcribing, transcription_thread
#
#     if n_clicks % 2 == 1:  # Odd click count: start transcription
#         transcribed_text = ""  # Reset previous transcriptions
#         is_transcribing = True
#
#         # Start the transcription in a separate thread
#         transcription_thread = threading.Thread(target=transcribe_voice)
#         transcription_thread.start()
#
#         return "Voice recognition started. Speak now..."
#     else:  # Even click count: stop transcription
#         is_transcribing = False  # Stop transcription
#         if transcription_thread:
#             transcription_thread.join()  # Wait for the thread to finish
#
#         return "Voice recognition stopped."
#
#
#
# @callback(
#     Output('start-button', 'className'),
#     Input('start-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def toggle_flashing(n_clicks):
#     return 'flashing' if n_clicks % 2 == 1 else ''
#
# @callback(
#     Output('hidden-div', 'children'),
#     Input('voice_control_output', 'children'),
#     prevent_initial_call=True
# )
# def update_transcription_output(_):
#     global transcribed_text
#
#     # print(transcribed_text)
#     # print(transcribed_text.split(' '))
#
#     text = 'Please repeat the command, as I did not understand you.'
#
#     # Perform an action with the transcribed text
#     if transcribed_text.strip():
#         # Example action: print or log the transcribed text
#         for word in transcribed_text.split(' '):
#             print(word)
#             if word =='update' or word == 'condition' or word =='status':
#
#                 # print(asset_selected_details)
#                 if len(asset_selected_details) != 0:
#                     # print(asset_selected_details)
#
#                     asset_tag = '{}'.format(asset_selected_details[0]['points'][0]['customdata'][1])
#                     function = '{}'.format(asset_selected_details[0]['points'][0]['customdata'][2])
#                     type = 'Type: {} - {}'.format(asset_selected_details[0]['points'][0]['customdata'][11],
#                                                   asset_selected_details[0]['points'][0]['customdata'][12])
#                     rated_voltage = 'Rated Voltage: {}kV'.format(
#                         asset_selected_details[0]['points'][0]['customdata'][6])
#                     manufactor = asset_selected_details[0]['points'][0]['customdata'][3]
#                     yom = 'YOM {}'.format(asset_selected_details[0]['points'][0]['customdata'][4])
#                     yoi = 'YOI {}'.format(asset_selected_details[0]['points'][0]['customdata'][5])
#
#                     # update circle
#
#                     analysis_id = get_asset_analysis(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])
#
#                     # take latest analysis
#                     risk_label = analysis_id[-1][3]
#                     health_index_label = analysis_id[-1][4]
#                     latest_analysis = analysis_id[-1][1]
#
#                     failure_mechanism_list = get_failure_mechanism_list()
#                     failure_mechanism_analysis = get_failure_mechanisms_analysis(analysis_id[-1][0])
#
#                     fm_label = [label[1] for label in failure_mechanism_list]
#
#                     fm_value = [value[3] for value in failure_mechanism_analysis]
#
#                     # Combine labels and values into a list of tuples
#                     fm_data = list(zip(fm_label, fm_value))
#
#                     # Sort the list of tuples by value in descending order
#                     fm_data_sorted = sorted(fm_data, key=lambda x: x[1], reverse=True)
#
#                     # Unzip the sorted list back into two separate lists
#                     sorted_fm_label, sorted_fm_value = zip(*fm_data_sorted)
#                     highest_failure_mechanism = sorted_fm_label[0]
#                     highest_failure_mechanism_value = sorted_fm_value[0]
#
#                     text = ('The {} {} has a Risk Index of {} out of 25 as of {}.\n'
#                             'Its Health Index stand at {} out of 5.\n'
#                             'The highest failure mechanisms record is {} with a probability of occurence of {}.\n'
#                             'There are no pending actions for the asset').format(asset_tag, function, risk_label, latest_analysis, health_index_label,highest_failure_mechanism, highest_failure_mechanism_value)
#
#                 if len(asset_selected_details) ==0:
#                     text = ('I`m not able to read the information.\n'
#                             'Please select the asset again from the home page.')
#
#                 print(text)
#
#         text_to_voice(text, play_audio=True)
#
#     # Return the latest transcribed text
#     return transcribed_text
#
# @callback(
#     Output('dummy-output', 'children'),  # Dummy output to trigger the callback
#     Input('url', 'pathname')  # Track the URL changes
# )
# def stop_transcription_on_page_change(pathname):
#     global is_transcribing
#     if is_transcribing:
#         is_transcribing = False  # Stop transcription when the page changes
#         print("Voice recognition stopped due to page change.")
#     return ""
#
#
#
# #export csv with latest assessment
@callback(
    Output('download-dataframe-csv', 'data', allow_duplicate=True),
    Input('export_assessment_m', 'n_clicks'),
    prevent_initial_call=True
)
def generate_csv(n_clicks):
    if n_clicks:
        data = export_asset_summary(asset_id=asset_selected_details[0]['points'][0]['customdata'][0])


        if len(data)!=0:
            values = data[1]
            headers = data[0]



            df = pd.DataFrame([values], columns=headers)

            # Convert DataFrame to CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()



            return dict(content=csv_data, filename="latest_assessment_summary.csv", type="text/csv")

