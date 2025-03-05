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
    get_asset_sw_layout_individual_sw, upload_test_data_sw, insert_online_pd_data_sw
from connectors.db_connectors_mysql import get_failure_mechanism_single_asset_list
from connectors.db_connectors_mysql import get_failure_mechanisms_analysis
from connectors.db_connectors_mysql import get_subcomponent_analysis

from connectors.db_connectors_mysql import update_asset_criticality
from connectors.db_connectors_mysql import get_asset_analysis
from connectors.db_connectors_mysql import export_asset_summary
from connectors.db_connectors_mysql import get_criticality_list
from connectors.db_connectors_mysql import get_maintenance_action

from connectors.db_connectors_mysql import get_session_user_details


from functions.analyse_data_mysql import analyse_data
from functions.assess_condition_mysql import assess_condition
from functions.global_variables import asset_selected_details


import math
from functions.global_variables import acquisition_started, acquisition_is_running
import asyncio
from connectors.db_connectors_mysql import get_panel_id_sw_layout_individual_panel
from services.online_pd_data_acquisition import run_acquisition

# opne the page

dash.register_page(__name__, external_stylesheets=[dbc.themes.SPACELAB,dbc.icons.BOOTSTRAP,dbc.themes.BOOTSTRAP])



##################################################################################################################################################################################
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
        html.Div(id='content-switchgear'),
        dcc.Location(id='url_labels_monitoring_page'),


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
                        html.P(id="Username_monitoring_page"),
                        # html.P(id='Function'),
                        html.P(id='Datetime_monitoring_page'),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            id='start_stop_stand_alone_button',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Start/Stop', id='start_stop_stand_alone_button_monitoring_page', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),
                        html.Br(),
                        html.Div(
                            id='download_monitoring_button',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Download', id='download_button_monitoring_page', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),

                        # Modal for error message
                        html.Div(
                            id='modal_monitoring',
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
                                        html.P(id='modal-message-monitoring', style={'font-size': '18px', 'color': 'red'}),
                                        html.Button('Close', id='close-modal-monitoring', n_clicks=0)
                                    ]
                                )
                            ]
                        ),
                        
                        # Modal for error message
                        html.Div(
                            id='modal1_monitoring',
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
                                        html.P(id='modal1-message-monitoring', style={'font-size': '18px', 'color': 'green'}),
                                        html.Button('Close', id='close-modal1-monitoring', n_clicks=0)
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
                        html.P(id="messages_received_monitoring",children="Messages received: 0",
                               style={'color': 'green', 'text-align': 'center', 'font-size': '20px', 'margin-top': '20px'}),
                        html.Br(),
                        dcc.Interval(
                        id='message_interval_monitoring', 
                        interval=5000,  # 5 seconds
                        n_intervals=0,
                        disabled=True,  # Initially disabled
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
                    ],
                ),
            ],),

])

#######################################################################################################################
#######################         call back function


@callback(
    Output('content-switchgear', 'children', allow_duplicate=True),
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

#Update labels

@callback(
    Output("Username_monitoring_page", "children"),
    Output('Datetime_monitoring_page', 'children'),
    Input("url_labels_monitoring_page", "pathname")
    )
def update_username(_):
    user_dict = get_session_user_details()
    
    name_string = user_dict['name'] + " "+ user_dict['surname']
    datetime_string = user_dict['last_connection_time']
    datetime_string_final = datetime_string.strftime("%Y-%m-%d %H:%M:%S")

    
    
    return name_string, datetime_string_final



#Sniffer mode
@callback(
    [Output('start_stop_stand_alone_button_monitoring_page', 'style'),
     Output('messages_received_monitoring', 'children',allow_duplicate=True),
     Output('message_interval_monitoring', 'disabled'),
     Output('download_button_monitoring_page', 'disabled', allow_duplicate=True)],
    [Input('start_stop_stand_alone_button_monitoring_page', 'n_clicks')],
    [State('start_stop_stand_alone_button_monitoring_page', 'style')],
    prevent_initial_call=True,
)
def start_stop_button_click(n_clicks, button_style):
    global is_receiving, message_count

    if n_clicks is None:
        return button_style, "Messages received: 0", True, True  # Initial state

    # First press: start receiving messages
    if n_clicks % 2 == 1:
        # Change button style to "pressed"
        button_style['background-color'] = 'green'
        is_receiving = True
        message_count = 0  # Reset message count
        messages_history.clear()  # Clear history when starting
        threading.Thread(target=start_receiving_messages, daemon=True).start()
        return button_style, "Messages received: 0", False, True  # Disable Interval (start it) and disable button 

    # Second press: stop receiving messages
    else:
        # Revert button style to original
        button_style['background-color'] = 'grey'
        is_receiving = False
        return button_style, f"Messages received: {message_count}", True, False  # Enable Interval (stop it) and enable download button

# Callback to update the label every 5 seconds
@callback(
    Output('messages_received_monitoring', 'children', allow_duplicate=True),
    [Input('message_interval_monitoring', 'n_intervals')],
    prevent_initial_call=True,
)
def update_message_label(n):
    return "\n".join(messages_history) if messages_history else "Message received:0"



# Function to check if USB drive is connected

# Function to check if USB drive is connected and has write permissions
def check_usb_drive():
    usb_mount_point = '/media/pi'
    if os.path.exists(usb_mount_point):
        for device in os.listdir(usb_mount_point):
            if device !='D09E-E905':
                device_path = os.path.join(usb_mount_point, device)
                if os.path.isdir(device_path):
                    try:
                        # Check write permissions by creating and deleting a temp file
                        test_file = os.path.join(device_path, "test_write_permission.txt")
                        with open(test_file, 'w') as f:
                            f.write("test")
                        os.remove(test_file)  # Clean up test file
                        return device_path
                    except PermissionError:
                        return None
            else:
                None
    return None


# Callback for downloading the message history to USB

# Callback for downloading the message history and showing modal
@callback(
    [Output('modal1_monitoring', 'style',allow_duplicate=True),
     Output('modal1-message-monitoring', 'children'),
     Output('modal_monitoring', 'style',allow_duplicate=True),
     Output('modal-message-monitoring', 'children'),
     Output('download_button_monitoring_page', 'disabled', allow_duplicate=True)],
    [Input('download_button_monitoring_page', 'n_clicks')],
    prevent_initial_call=True,
)
def download_messages(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    # Check if USB is connected and writable
    usb_device_path = check_usb_drive()

    if usb_device_path is None:
        # Show modal with error message
        return {'display': 'none'},'Please connect your USB drive and ensure it is writable.',{'display': 'block'}, 'Please connect your USB drive and ensure it is writable.', False

    # Create the file path on the USB drive
    file_path = os.path.join(usb_device_path, 'messages_history.txt')

    # Write messages to a text file on the USB
    try:
        with open(file_path, 'w') as file:
            for message in messages_history:
                file.write(f"{message}\n")
        # Hide the modal and enable download button again
        return {'display': 'block'},'File saved successfully to the USB drive!', {'display': 'none'}, 'File saved successfully to the USB drive!', True
    except PermissionError:
        return {'display': 'none'},'Permission denied. Please ensure your USB drive is writable.',{'display': 'block'}, 'Permission denied. Please ensure your USB drive is writable.', False



# Callback for closing the modal
@callback(
    Output('modal_monitoring', 'style', allow_duplicate=True),
    [Input('close-modal-monitoring', 'n_clicks')],
    prevent_initial_call=True,
)
def close_modal(n_clicks):
    if n_clicks:
        return {'display': 'none'}  # Hide modal when button is clicked
    return {'display': 'none'}



# Callback for closing the modal1
@callback(
    Output('modal1_monitoring', 'style', allow_duplicate=True),
    [Input('close-modal1-monitoring', 'n_clicks')],
    prevent_initial_call=True,
)
def close_modal(n_clicks):
    if n_clicks:
        return {'display': 'none'}  # Hide modal when button is clicked
    return {'display': 'none'}





