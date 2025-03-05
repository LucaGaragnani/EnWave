import time

import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
from dash import Dash, clientside_callback
from dash import dcc
from dash import html,callback_context
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

from connectors.db_connectors_mysql import get_component_analysis, get_component_single_asset_list
from connectors.db_connectors_mysql import get_failure_mechanism_single_asset_list
from connectors.db_connectors_mysql import get_failure_mechanisms_analysis
from connectors.db_connectors_mysql import get_subcomponent_analysis

from connectors.db_connectors_mysql import update_asset_criticality
from connectors.db_connectors_mysql import get_asset_analysis
from connectors.db_connectors_mysql import export_asset_summary
from connectors.db_connectors_mysql import get_criticality_list
from connectors.db_connectors_mysql import get_maintenance_action


from connectors.db_connectors_mysql import get_session_user_details

from functions.assess_condition_mysql import assess_condition

# from functions.global_variables import asset_selected_details
from functions import global_variables
from functions.led_logic import message_sent
import threading

import math


# opne the page

dash.register_page(__name__, external_stylesheets=[dbc.themes.SPACELAB,dbc.icons.BOOTSTRAP,dbc.themes.BOOTSTRAP])


############################         Import data sets from database          ############################################
# Simulating an imported function that needs to be started and stopped
def start_receiving_messages():
    global is_receiving, message_count
    while is_receiving:
        time.sleep(5)  # Simulate receiving messages every 5 seconds
        new_message = "Message {}".format(message_count+1)  # Generate new message
        messages_history.append(new_message)  # Append new message to the history
        message_count +=1

# Global variables to control receiving messages and count
is_receiving = False
message_count = 0
messages_history = []  # List to store the history of messages



def convert_to_datetime(date_str):
    # Define the date format
    date_format = "%d-%m-%Y %H:%M"
    return datetime.strptime(date_str, date_format)


################### plot the app
# Layout of Dash App

layout = html.Div(



    children=[
        dcc.Store(id='store', storage_type='session'),
        # dcc.Location(id='url', refresh=False),
        html.Div(id='content-ugtl'),
        dcc.Location(id='url_labels_test_page'),


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



                        html.H3("User Information"),
                        html.P(id="Username_test_page"),
                        # html.P(id='Function'),
                        html.P(id='Datetime_test_page'),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            id='test_smart_meter_button',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Test Smart Meter', id='test_smart_meter_button_test_page', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),
                        html.Br(),
                        html.Div(
                            id='test_concentrator_button',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Test LV Concentrator', id='test_concentrator_button_test_page', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

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
                        html.Br(),
                        html.P(id="messages_received_test",children="Messages received: 0",
                               style={'color': 'green', 'text-align': 'center', 'font-size': '20px', 'margin-top': '20px'}),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        # Modal for error message
                        html.Div(
                            id='modal_test_meter',
                            style={
                                'display': 'none',
                                'position': 'fixed',
                                'top': '0',
                                'left': '0',
                                'width': '100%',
                                'height': '100%',
                                'background-color': 'rgba(0, 0, 0, 0.5)',
                                'z-index': '9999',
                                'text-align': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'position': 'absolute',
                                        'top': '50%',
                                        'left': '50%',
                                        'transform': 'translate(-50%, -50%)',
                                        'background-color': 'white',
                                        'padding': '20px',
                                        'border-radius': '5px',
                                        'width': '80%',
                                        'max-width': '400px'
                                    },
                                    children=[
                                        html.P(id='modal-test-meter', style={'font-size': '18px', 'color': 'black'}),
                                        html.H3('Meter Test', style={'color': 'black','textAlign':'center'}),
                                        dcc.Input(id='input-field-meter', type='text', placeholder='Enter your custom message', style={'width':'100%', 'height':'30px', 'margin-bottom':'10px'}),
                                        html.Br(),
                                        html.Div(
                                            children=[
                                                html.Button('Cancel', id='cancel-button-meter', style={'margin-right':'10px', 'width':'100px', 'background-color':'red', 'color':'white'}),
                                                html.Button('Send', id='send-button-meter', style={'margin-right':'10px', 'width':'100px', 'background-color':'green', 'color':'white'}),
                                                ],
                                                style={'display':'flex', 'justify-content':'center'}
                                            )
                                    ]
                                )
                            ]
                        ),
                        
                        # Modal for concentrator test
                        html.Div(
                            id='modal_test_concentrator',
                            style={
                                'display': 'none',
                                'position': 'fixed',
                                'top': '0',
                                'left': '0',
                                'width': '100%',
                                'height': '100%',
                                'background-color': 'rgba(0, 0, 0, 0.5)',
                                'z-index': '9999',
                                'text-align': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'position': 'absolute',
                                        'top': '50%',
                                        'left': '50%',
                                        'transform': 'translate(-50%, -50%)',
                                        'background-color': 'white',
                                        'padding': '20px',
                                        'border-radius': '5px',
                                        'width': '80%',
                                        'max-width': '400px'
                                    },
                                    children=[
                                        html.P(id='modal-test-concentrator', style={'font-size': '18px', 'color': 'black'}),
                                        html.H3('LV Concentrator Test', style={'color': 'black','textAlign':'center'}),
                                        dcc.Input(id='input-field-concentrator', type='text', placeholder='Enter your custom message', style={'width':'100%', 'height':'30px', 'margin-bottom':'10px'}),
                                        html.Br(),
                                        html.Div(
                                            children=[
                                                html.Button('Cancel', id='cancel-button-concentrator', style={'margin-right':'10px', 'width':'100px', 'background-color':'red', 'color':'white'}),
                                                html.Button('Send', id='send-button-concentrator', style={'margin-right':'10px', 'width':'100px', 'background-color':'green', 'color':'white'}),
                                                ],
                                                style={'display':'flex', 'justify-content':'center'}
                                            )
                                    ]
                                )
                            ]
                        ),
                        
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            id='download_button_test_mode',
                            style={"margin-top": "20px", "text-align": "center", "display": "none", "justify-content": "center"},
                            children = [
                                html.Button('Download', id='download_button_test_page', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

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
                        dcc.Store(id='send-button-clicks', data=0),
                        dcc.Store(id='send-button2-clicks', data=0)
                ],
            ),
    ],
),

])





#######################################################################################################################
#######################         call back function

# asset_selected_details = []

# @callback(
#     Output('content-ugtl', 'children'),
#     Input('store', 'data'),
#     prevent_initial_call='initial_duplicate'
# )
# def display_selected_asset(selected_asset):
#     if selected_asset:
#         # asset_selected_details.append(selected_asset)
#         global asset_selected_details
# 
#         asset_selected_details.insert(0,selected_asset)
#         custom_data = selected_asset.get('points', [{}])[-1].get('customdata', [])
#         content = ''
# 
#     content=''
# 
#     return content

#thread for led parallel operation
def thread_led_sent_message():
    thread = threading.Thread(target=message_sent)
    thread.daemon = True
    thread.start()


#Update user information
@callback(
    Output("Username_test_page", "children"),
    Output('Datetime_test_page', 'children'),
    Input("url_labels_test_page", "pathname")
    )
def update_username(_):
    user_dict = get_session_user_details()
    
    name_string = user_dict['name'] + " "+ user_dict['surname']
    datetime_string = user_dict['last_connection_time']
    datetime_string_final = datetime_string.strftime("%Y-%m-%d %H:%M:%S")

    
    
    return name_string, datetime_string_final

# Open model to send message- METER
@callback(
    Output('modal_test_meter', 'style',allow_duplicate=True),
    [Input('test_smart_meter_button_test_page', 'n_clicks')],
    prevent_initial_call=True,
    )
def open_modal_meter(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return {'display':'block'}


#Close the modal when cancel is press
@callback(
    Output('modal_test_meter', 'style',allow_duplicate=True),
    [Input('cancel-button-meter', 'n_clicks')],
    prevent_initial_call=True,
    )
def close_modal_meter(n_clicks):
    if n_clicks:
        return {'display':'none'}
    return {'display':'none'}


#send the message and close the modal meter
@callback(
    [Output('modal_test_meter', 'style',allow_duplicate=True),
    Output('send-button-clicks', 'data')],

    [Input('send-button-meter', 'n_clicks')],
    [Input('input-field-meter' ,'value')],
    [Input('send-button-clicks','data')],
    prevent_initial_call=True,
    )
def send_message_and_close(n_clicks, input_value, store_data):
    if not n_clicks:
        raise PreventUpdate
    
    print(n_clicks, input_value, store_data)
    
    if n_clicks:
        if store_data==0:
            
            #do something with the message -- custom function
            thread_led_sent_message()
            print('message inputed: {}'.format(input_value))
            store_data +=1
            #close the modal        
            return {'display':'none'}, store_data
        
        elif store_data>0:
            if n_clicks == store_data:
            
            
                return {'display':'block'}, store_data
            if n_clicks >= store_data:
                #do something with the message -- custom function
                print('message inputed: {}'.format(input_value))
                thread_led_sent_message()
                store_data +=1
                #close the modal        
                return {'display':'none'}, store_data
           
        
        
    else:
        return {'display':'none'}, 0
        
        
    return {'display':'none'}
    


# Open model to send message -CONCENTRATOR
@callback(
    Output('modal_test_concentrator', 'style',allow_duplicate=True),
    [Input('test_concentrator_button_test_page', 'n_clicks')],
    prevent_initial_call=True,
    )
def open_modal_meter(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return {'display':'block'}


#Close the modal when cancel is press
@callback(
    Output('modal_test_concentrator', 'style',allow_duplicate=True),
    [Input('cancel-button-concentrator', 'n_clicks')],
    prevent_initial_call=True,
    )
def close_modal_meter(n_clicks):
    if n_clicks:
        return {'display':'none'}
    return {'display':'none'}


#send the message and close the modal meter
@callback(
    [Output('modal_test_concentrator', 'style',allow_duplicate=True),
    Output('send-button2-clicks', 'data')],

    [Input('send-button-concentrator', 'n_clicks')],
    [Input('input-field-concentrator' ,'value')],
    [Input('send-button2-clicks','data')],
    prevent_initial_call=True,
    )
def send_message_and_close(n_clicks, input_value, store_data):
    if not n_clicks:
        raise PreventUpdate
    
    print(n_clicks, input_value, store_data)
    
    if n_clicks:
        if store_data==0:
            
            #do something with the message -- custom function
            print('message inputed concentrator {}'.format(input_value))
            thread_led_sent_message()
            store_data +=1
            #close the modal        
            return {'display':'none'}, store_data
        
        elif store_data>0:
            if n_clicks == store_data:
            
            
                return {'display':'block'}, store_data
            if n_clicks >= store_data:
                #do something with the message -- custom function
                print('message inputed concentrator: {}'.format(input_value))
                thread_led_sent_message()
                store_data +=1
                #close the modal        
                return {'display':'none'}, store_data
           
        
        
    else:
        return {'display':'none'}, 0
        
        
    return {'display':'none'}


#add the message receivment to be printed on display and enable the download button
