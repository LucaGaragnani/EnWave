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



import requests
import json
import bcrypt
import smtplib
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer
from connectors.db_connectors_mysql import reset_password





app=dash.register_page(__name__)


########################################################################################################################
############################         Import data sets from database          ############################################

#################################3     ASSESSMENT COLOUR IS MISSING    #################################################3

#
# password = "Test123!"
#
# # Hash the password
# hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#
# print(hashed)





###################################################################################################################################################################################
#hash the password

# # Hash the password
def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed


#################################################################################################################################################################################

################### plot the app
# Layout of Dash App

### test modal



layout = dbc.Container(
    [
        dcc.Location(id='url_rst', refresh=True),  # Add this line
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
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Label("Email", style={'marginLeft': '250px'}),
                        dbc.Input(type="email", id="email", placeholder="Enter your email",
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
                        html.Label("New Password", style={'marginLeft': '250px'}),
                        dbc.Input(type="Npassword", id="Npassword", placeholder="Enter the new password",
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
                        html.Label("Confirm Password", style={'marginLeft': '250px'}),
                        dbc.Input(type="Cpassword", id="Cpassword", placeholder="Confirm your new password",
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

        dbc.Row(
            dbc.Col(
                dbc.Button("Confirm", id="confirm-button", style={'backgroundColor': 'RGB(20,54,214)', 'color':'white','width':'400px' , 'border':'1.5px black solid','height': '50px','text-align':'center', 'marginLeft': '250px', 'marginRight': '250px','marginTop': 20}, n_clicks=0),
                className="text-center",
            ),
            className="justify-content-center",
            style={"display": "flex", "justify-content": "center", "align-items": "center"},

        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

        html.Div(
        id='password_update_modal',
        style={'display': 'none', 'position': 'fixed', 'top': '50%', 'left': '50%',
               'transform': 'translate(-50%, -50%)', 'z-index': 1000},
        children=[
            html.Div(
                style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'background-color': 'white', 'padding': '20px', 'border': '1px solid #ccc',
                       'border-radius': '5px'},
                children=[
                    html.H5('Password Reset Successfully!',
                            style={'color': 'black', 'font-weight': 'bold', "text-align": "center"}),
                    html.P("You will now be redirected to the home page.",
                           style={'color': 'black', 'text-align': 'center'}),
                    html.Button('Ok', id='ok-modal-btn',
                                style={'color': 'black', 'width': '100px', 'margin-top': '10px',
                                       'background-color': 'gray', 'border-color': 'grey',
                                       'text-align': 'center', 'opacity': 0.9}),
                ]
            )
        ]
    ),


    ],
    className="mt-5 background",
    style={"overflowY": "auto"},

)



#########################################################################################################################3
##################################     ADD METHOD TO CALL THE DATA FROM THE DATABASE BASED ON SELECTION  ################

#
@callback(
    # Output("login-result", "children"),
    Output("Npassword", "style"),
    Output("Cpassword", "style"),
    Output('password_update_modal', 'style'),
    Input("confirm-button", "n_clicks"),
    State('email', 'value'),
    State("Npassword", "value"),
    State("Cpassword", "value"),

    prevent_initial_call='initial_duplicate',

)
def authenticate_user(n_clicks, email,Npassword, Cpassword):



    if n_clicks==0 or not Npassword or not Cpassword:
        Npassword_style = {'color': 'black', 'width': '400px',
                       'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                       'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

        Cpassword_style = {'color': 'black', 'width': '400px',
                          'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                          'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

        return Npassword_style, Cpassword_style,{'display': 'none'}
    # Query the database to check user credentials

    result = get_user(email)

    if result:

        #chekc if Npassword == Cpassword

        if Npassword==Cpassword:
            hashed_password = hash_password(Npassword)

            user_id = result[0]

            #update db with new password
            text = reset_password(hashed_password, email, user_id)



            current_date = datetime.today()
            current_date_str = current_date.strftime('%d-%m-%Y %H:%M:%S')

            upload_session_data(user_id, current_date_str)

            Npassword_style = {'color': 'black', 'width': '400px',
                            'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                            'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

            Cpassword_style = {'color': 'black', 'width': '400px',
                                'border': '1.5px black solid', 'height': '50px', 'text-align': 'left',
                              'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}




            return Npassword_style, Cpassword_style, {'display': 'block', 'position': 'fixed', 'top': '50%', 'left': '50%',
                'transform': 'translate(-50%, -50%)', 'z-index': 1000}

        else:
            # Invalid password
            Npassword_style = {'color': 'black', 'width': '400px',
                           'border': '1.5px red solid', 'height': '50px', 'text-align': 'left',
                           'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

            Cpassword_style = {'color': 'black', 'width': '400px',
                              'border': '1.5px red solid', 'height': '50px', 'text-align': 'left',
                              'marginLeft': '250px', 'marginRight': '250px', 'marginTop': 20}

            return Npassword_style, Cpassword_style,{'display': 'none'}

    return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@callback(    Output('url_rst', 'pathname',allow_duplicate=True),
    Output('password_update_modal', 'style',allow_duplicate=True),
    Input('ok-modal-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def close_success_modal(n_clicks):
    if n_clicks:
        # move to home page directly
        home_page = 'home'




        return home_page, {'display': 'none'}  # Hide the success modal
    return dash.no_update