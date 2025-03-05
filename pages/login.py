import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
from dash import Dash, dcc
# from dash import dcc
from dash import html
from dash import html, callback, Input, Output, register_page, State
from dash.exceptions import PreventUpdate
import webbrowser
from flask import request

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date


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
import json
import requests
import dash_bootstrap_components as dbc

from connectors.db_connectors_mysql import get_user
from connectors.db_connectors_mysql import upload_session_data
from connectors.db_connectors_mysql import get_connection_status, update_connection_status

from functions import global_variables
from functions.led_logic import user_connected_led
import threading 



import requests
import json
import bcrypt
import smtplib
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import certifi






dash.register_page(__name__, path='/')

secret_key = 'inwave!2024!integratedhealthmonitoringsystem'


########################################################################################################################
############################         Import data sets from database          ############################################

#################################3     ASSESSMENT COLOUR IS MISSING    #################################################3

#
# password = "Test123!"
#
# # Hash the password
# hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# #
# print(hashed)
#
# stored_hashed_password = hashed
# input_password = 'Test123!'
#
# # Verify the password
# if bcrypt.checkpw(input_password.encode('utf-8'), stored_hashed_password):
#     print("Password is correct!")
# print(fuck)




###################################################################################################################################################################################

def verify_reset_token(token, expiration=3600):  # Token is valid for 1 hour
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(token, max_age=expiration)
    except Exception as e:
        return None  # Token is invalid or expired
    return email

def generate_reset_token(email):
    # Create a serializer object with a secret key
    serializer = URLSafeTimedSerializer(secret_key)

    # Generate the token using the email
    token = serializer.dumps(email)

    return token


# reset password
def send_reset_email(email):
    reset_token = generate_reset_token(email)
    reset_link = f"{request.scheme}://{request.host}/reset-password?token={reset_token}"
    # reset_link = f"http://127.0.0.1:8050/reset-password?token={reset_token}"

    message = Mail(
        from_email='info@inwave.au',  # Replace with your verified sender email
        to_emails=email,
        subject='Password Reset Request',
        plain_text_content=f"Click here to reset your password: {reset_link}",
        html_content=f"<strong>Click here to reset your password:</strong> <a href='{reset_link}'>{reset_link}</a>"
    )

    ssl_cert_path = r'/home/pi/Desktop/InWave_HI-main/database/cacert.pem'

    # try:
    # sg = SendGridAPIClient(api_key='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')  # Replace with your SendGrid API key
    api_key = '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'

    # sg.session = session
        # response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)

    try:
        # Send the email using the specified SSL certificate for verification
        ### rev0 "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"
        ### rev1 "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"
        response = requests.post(
            'https://api.sendgrid.com/v3/mail/send',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json=message.get(),
            verify=ssl_cert_path  # Use the specified path for SSL verification
        )
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")



#################################################################################################################################################################################

################### plot the app
# Layout of Dash App

### test modal



layout = dbc.Container(
    [
        dcc.Location(id='url_lg', refresh=True),  # Add this line
        dcc.Store(id="store", data={}),
        # html.Br(),
        # html.Br(),
        # html.Br(),
        html.Br(),
        html.A(
                html.Img(
                        className="logo",
                        src=dash.get_asset_url("dash-logo-new-removebg-preview.png"),
                        style={"width": "300px", "height": "auto","border-radius": "8%"}
                            ),style={"display": "flex", "justify-content": "center", "align-items": "center"},

                            href="",
                        ),
        # html.H1("InWave",style={'marginLeft': '350px'}),
        html.Br(),
        # html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Label("Email", style={'marginLeft': '250px'}),
                        dbc.Input(type="email", id="email", placeholder="Enter your email address",
                                  style={ 'color': 'black', 'width': '400px',
                                         'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                                         'marginLeft': '250px', 'marginRight': '250px','marginTop': 20}),
                    ],
                    className="mb-3",
                ),
            ),
            className="justify-content-center",
            style={"display": "flex", "justify-content": "center", "align-items": "center"},

        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Label("Password", style={'marginLeft': '250px'}),
                        dbc.Input(type="password", id="password", placeholder="Enter your password",
                                  style={ 'color': 'black', 'width': '400px',
                                         'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                                         'marginLeft': '250px', 'marginRight': '250px','marginTop': 20}),

                    ],
                    className="mb-3",
                ),
            ),
            className="justify-content-center",
            style={"display": "flex", "justify-content": "center", "align-items": "center"},

        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [

                        dbc.Button(
                            id="toggle-password-btn",
                            children="Show",
                            style={'marginLeft': '350px',
                                   'border': 'none',         # No border
                                    'color': 'white',         # White text
                                    'backgroundColor': 'transparent',
                                    'text-align': 'right'},
                        ),
                    ],
                    className="mb-3",
                ),
            ),
            className="justify-content-center",
            style={"display": "flex", "justify-content": "center", "align-items": "center"},

        ),

        html.Br(),

        dbc.Row(
            dbc.Col(
                dbc.Button("Log In", id="login-button", style={'backgroundColor': 'RGB(20,54,214)', 'color':'white','width':'400px' , 'border':'1.5px black solid','height': '50px','text-align':'center', 'marginLeft': '250px', 'marginRight': '250px','marginTop': 20}, n_clicks=0),
                className="text-center",
            ),
            className="justify-content-center",
            style={"display": "flex", "justify-content": "center", "align-items": "center"},

        ),

        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Span("Can’t remember your password? ",
                                  style={'color': 'white', 'text-decoration': 'underline',
                                         'text-align': 'left', 'cursor': 'pointer'},
                                  id='open-modal-link'),
                    ],
                    className="mb-3",
                ),
            ),
            className="justify-content-center",
            style={"display": "flex", "justify-content": "center", "align-items": "center", 'marginTop': '10px'},
        ),


        html.Div(
            id='modal_reset_password',
            style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
                   'transform': 'translate(-50%, -50%)', 'z-index': 1000},
            children=[
                html.Div(
                    id='modal_content',
                    style={'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                           'border-radius': '5px'},
                    children=[
                        html.H5('Reset Password',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        dcc.Input(type='email', id='reset-email', placeholder='Enter your email',
                                  style={'marginBottom': '10px', 'width': '100%','margin-top': '10px'}),
                        html.Div(
                            children=[
                                html.Button('Reset', id='submit-reset-btn',
                                            style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                                   'background-color': 'green', 'border-color': 'grey',
                                                   'text-align': 'center', 'opacity': 0.9, 'margin-right': '40px'}),
                                html.Button('Cancel', id='close-modal-btn',
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
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

    ],
    className="mt-5 background",
    style={"overflowY": "auto"},


)



#########################################################################################################################3
##################################     ADD METHOD TO CALL THE DATA FROM THE DATABASE BASED ON SELECTION  ################
#thread for led

def thread_led():
    thread = threading.Thread(target=user_connected_led)
    thread.daemon = True
    thread.start()

@callback(
    # Output("login-result", "children"),
    Output('url_lg', 'pathname',allow_duplicate=True),
    Output("email", "style"),
    Output("password", "style"),
    Input("login-button", "n_clicks"),
    State("email", "value"),
    State('password', 'value'),

    prevent_initial_call='initial_duplicate',

)
def authenticate_user(n_clicks, email, password):



    if n_clicks==0 or not email or not password:
        email_style = {'color': 'black', 'width': '400px',
                       'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                       'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

        password_style = {'color': 'black', 'width': '400px',
                          'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                          'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

        return dash.no_update, email_style, password_style
    # Query the database to check user credentials

    result = get_user(email)

    if result:

        stored_hashed_password = result[2].encode('utf-8')  # Assuming second item is the hashed password

        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):

            home_page = 'home'
            email_style = {'color': 'black', 'width': '400px',
                         'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                         'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

            password_style = {'color': 'black', 'width': '400px',
                               'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                               'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}


            user_id = result[0]
            current_date = dt.today()
            current_date_str = current_date.strftime('%d-%m-%Y %H:%M:%S')

            upload_session_data(user_id, current_date_str)
            
            #update connection status for led functionality
            update_connection_status(1)
            global_variables.connection_status = 1
            global_variables.current_mode = None
            global_variables.sniffer_mode_condition = False
            global_variables.test_mode_condition = False
            global_variables.monitoring_mode_condtition = False
            
            #start the led
            thread_led()
            
            
            return home_page, email_style, password_style

        else:
            # Invalid password
            email_style = {'color': 'black', 'width': '400px',
                           'border': '1.5px red solid', 'height': '50px', 'text-align': 'left',
                           'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

            password_style = {'color': 'black', 'width': '400px',
                              'border': '1.5px red solid', 'height': '50px', 'text-align': 'left',
                              'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

            return dash.no_update, email_style, password_style







# Callback to open and close the modal

@callback(
    Output("modal_reset_password", "style"),
    Input("open-modal-link", "n_clicks"),
    prevent_initial_call=True,
)
def open_modal(n_clicks):
    if n_clicks:
        return {'display': 'block', 'position': 'fixed', 'top': '50%', 'left': '50%',
                'transform': 'translate(-50%, -50%)', 'z-index': 1000}
    return dash.no_update

#
# Callback to handle the reset link submission -
@callback(
    Output("reset-email", "value"),
    Output('modal_content', 'children'),
    Input("submit-reset-btn", "n_clicks"),
    State("reset-email", "value"),
)
def send_reset_link(n_clicks, email):
    if n_clicks:
        if n_clicks > 0 and email:
            send_reset_email(email)

            #change message
            updated_content = [
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'textAlign': 'center'},
                    children=[
                        html.H5('Reset Link Sent!',
                                style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                        html.P(f"A reset link has been sent to {email}. Please check your inbox.",
                               style={'color': 'black', 'text-align': 'center'}),
                        html.Button('Close', id='close-modal-btn',
                                    style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                           'background-color': 'gray', 'border-color': 'grey',
                                           'text-align': 'center', 'opacity': 0.9}),
                    ]
                )
            ]


            return "", updated_content # Clear the input after sending
    return dash.no_update

@callback(
    Output('modal_reset_password', 'style',allow_duplicate=True),
    Input('close-modal-btn', 'n_clicks'),
    prevent_initial_call=True
)
def close_modal(n_clicks):
    if n_clicks:
        return {'display': 'none'}  # Hide the modal
    return dash.no_update


#visualise inserted password
@callback(
    Output("password", "type"),
    Output("toggle-password-btn", "children"),
    Input("toggle-password-btn", "n_clicks"),
    State("password", "type"),
)
def toggle_password_visibility(n_clicks, current_type):
    if n_clicks:
        if current_type == "password":
            return "text", "Hide"
        else:
            return "password", "Show"
    return current_type, "Show"


