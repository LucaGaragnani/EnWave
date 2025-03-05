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








# opne the page

dash.register_page(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



##################################################################################################################################################
#######################     form

email_input = dbc.Row([
        dbc.Label("Email"
                , html_for="example-email-row"
                , width=2),
        dbc.Col(dbc.Input(
                type="email"
                , id="example-email-row"
                , placeholder="Enter email"
            ),width=10,
        )],className="mb-3"
)
user_input = dbc.Row([
        dbc.Label("Password", html_for="example-name-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text"
                , id="example-name-row"
                , placeholder="Enter name"
                , maxLength = 80
            ),width=10
        )], className="mb-3"
)
message = dbc.Row([
        dbc.Label("Message"
         , html_for="example-message-row", width=2)
        ,dbc.Col(
            dbc.Textarea(id = "example-message-row"
                , className="mb-3"
                , placeholder="Enter message"
                , required = True)
            , width=10)
        ], className="mb-3")





################### plot the app
# Layout of Dash App
markdown = ''' # Your request has been sent to our engineering team. We will notify you soon. Thank you!'''

layout = html.Div(
    children=[
        html.Div([dbc.Container([

        html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()

        # , dbc.Card(
        #     dbc.CardBody([
        #         dbc.Form([email_input
        #                      , user_input
        #                      , message])
        #         , html.Div(id='div-button', children=[
        #             dbc.Button('Submit'
        #                        , color='primary'
        #                        , id='button-submit'
        #                        , n_clicks=0)
        #         ])  # end div
        #     ])  # end cardbody
        # )  # end card
        ,dcc.Markdown(markdown)
        , html.Br()
        , html.Br()
        ,dcc.Link(
                dbc.Button("Go Back", style={'backgroundColor': 'RGB(20,54,214)', 'color':'white','width':'400px' , 'border':'1.5px black solid','height': '50px','text-align':'center', 'margin': 'auto'}),
                href="https://demowebapplication-572cbf089b33.herokuapp.com/asset-overview",),
    ])
    ])
    ],

)




#############################################################################################################################################




######################################################################################################################################################################################
##################################            call back functions

# @callback(Output('div-button', 'children'),
#               Input("button-submit", 'n_clicks')
#     # , Input("example-email-row", 'value')
#     # , Input("example-name-row", 'value')
#     # , Input("example-message-row", 'value')
#               )
# def submit(n):
#     print(n)
# def submit_message(n, email, name, message):
#     print(message)
#     # port = 465  # For SSL
#     # sender_email = email
#     # receiver_email = '<your email address here>'
#     #
#     # # Create a secure SSL context
#     # context = ssl.create_default_context()
#     #
#     # if n > 0:
#     #     with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     #         server.login("<you email address here>", '<you email password here>')
#     #         server.sendmail(sender_email, receiver_email, message)
#     #         server.quit()
#     #     return [html.P("Message Sent")]
#     # else:
#     #     return [dbc.Button('Submit', color='primary', id='button-submit', n_clicks=0)]
#
#
#
# # contact_form()
