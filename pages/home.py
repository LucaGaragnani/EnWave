import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
from dash import Dash
from dash import dcc
from dash import html
from dash.dash_table import DataTable
from dash import html, dcc, callback, Input, Output, register_page
from dash.exceptions import PreventUpdate
import webbrowser

import plotly.offline as pyo

import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import plotly.graph_objects as go
import plotly.io as pio

import base64
import os

import mysql.connector
import sqlite3

from decimal import Decimal

from PIL import Image
import io
import dash_bootstrap_components as dbc


from connectors.db_connectors_mysql import get_customer_site_from_user_id, get_site_coordinate, get_site_asset_layout, \
    get_single_asset_coordinate, get_single_asset_tag, get_transmission_line_accessories_details
from connectors.db_connectors_mysql import get_asset_list
from connectors.db_connectors_mysql import get_letest_asset_analysis
from connectors.db_connectors_mysql import get_maintenance_action

from connectors.db_connectors_mysql import get_session_user_details
from connectors.db_connectors_mysql import get_connection_status, update_connection_status


from functions import global_variables
from functions.led_logic import led_sniffer_mode, led_test_mode, led_monitoring_mode, gpio_cleanup

import threading

import csv

#read license file

# Determine the path of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))


# dash.register_page(__name__, path='/')
dash.register_page(__name__)



# # Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoiZ2FyYWduYW5pIiwiYSI6ImNsaDFpankyajEzbmczbW1waXFqc291ZHgifQ.t496-4FlGuJnbC5a40wOlQ"

# mapbox_access_token = open(".mapbox_token").read()

########################################################################################################################
############################         Import data sets from database          ############################################
site_list = get_customer_site_from_user_id()
# print('site list', site_list)

site_name_list = [item[1] for item in site_list]

# print(site_name_list)
#crete asset coordinate list for the customer
lat_initial = []
lon_initial = []
asset_tags = []
asset_tags_cable = []
asset_category = []
color_list = []
risk_list = []
cable_risk_list = []
cable_color_list = []

#differenciate the transmission lines as the accessories are like individual asset in the map
hv_transmission_line_accessories_tag_list =[]
hv_transmission_line_accessories_lat_list = []
hv_transmission_line_accessories_lon_list = []
hv_cable_accessory_risk_list = []
hv_cable_color_list = []

for site_id in site_list:
    asset_list = get_asset_list(site_id[0])

    for asset in asset_list:
        #rm, sw, tx
        if asset[24] !=4:

            lat_initial.append(asset[22])
            lon_initial.append(asset[23])
            asset_tags.append(asset[1])
            asset_category.append(asset[24])

            try:
                analysis = get_letest_asset_analysis(asset[0])
                if len(analysis)!=0:
                    risk_list.append(analysis[3])
                else:
                    risk_list.append(0)

            except TypeError:
                risk_list.append(0)
        #cable + transmission lines
        if asset[24] ==4:

            #transmission
            if asset[2]=='Transmission':
                #get accessories details
                hv_accessories_list = get_transmission_line_accessories_details(asset[0])
                for acc in hv_accessories_list:
                    hv_transmission_line_accessories_tag_list.append(acc[2])
                    hv_transmission_line_accessories_lat_list.append(acc[3])
                    hv_transmission_line_accessories_lon_list.append(acc[4])

                try:
                    analysis = get_letest_asset_analysis(asset[0])
                    if len(analysis) != 0:
                        hv_cable_accessory_risk_list.append(analysis[3])
                    else:
                        hv_cable_accessory_risk_list.append(0)
                except TypeError:
                    hv_cable_accessory_risk_list.append(0)


            #distribution
            else:

                asset_tags_cable.append(asset[1])

                try:
                    analysis = get_letest_asset_analysis(asset[0])
                    if len(analysis)!=0:
                        cable_risk_list.append(analysis[3])
                    else:
                        cable_risk_list.append(0)
                except TypeError:
                    cable_risk_list.append(0)


def get_color_list_map():
    color_list = []
    cable_color_list = []
    hv_cable_color_list = []
    for risks in risk_list:

        if 1 <= int(risks) <= 4:
            color = "green"
        elif 4 < int(risks) <= 9:
            color = "orange"
        elif 9 < int(risks) <= 20:
            color = "red"

        else:
            color = "grey"  # Default color if condition is out of expected range
        color_list.append(color)

    for risks in cable_risk_list:

        if 1 <= int(risks) <= 4:
            color = "green"
        elif 4 < int(risks) <= 9:
            color = "orange"
        elif 9 < int(risks) <= 20:
            color = "red"

        else:
            color = "grey"  # Default color if condition is out of expected range
        cable_color_list.append(color)

    for risks in hv_cable_accessory_risk_list:

        if 1 <= int(risks) <= 4:
            color = "green"
        elif 4 < int(risks) <= 9:
            color = "orange"
        elif 9 < int(risks) <= 20:
            color = "red"

        else:
            color = "grey"  # Default color if condition is out of expected range
        hv_cable_color_list.append(color)


    return color_list, cable_color_list, hv_cable_color_list

# print(risk_list)
# print(asset_list)
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template='plotly_dark')
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig

# Sample data for the table
data_maintenance_action = [
    {"Asset Tag": "", "Open Maintenance Action": "", "Due Date": ""},

]

###################################################################################################################################################################################
##################################################################################################################################################################################


##################################################3        CARDs


######## LOG out

logout_button = html.Button("Logout", id="logout-button", style={'backgroundColor': 'red', 'color': 'white', 'width': '100%', 'border': '1.5px black solid', 'height': '50px', 'text-align': 'center', 'marginTop': '20px'})


################### plot the app
# Layout of Dash App

layout = html.Div(

    children=[
        dcc.Store(id='store', storage_type='session'),
        dcc.Location(id='url_labels', refresh=False),
        html.Div(id='content'),




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
                                style={"width": "150px", "height": "auto","border-radius": "8%"}
                            ),style={"display": "flex", "justify-content": "center", "align-items": "center"},

                            href="",
                        ),

                        html.Br(),
                        html.Br(),
                        html.H3("User Information"),
                        html.P(id="Username"),
                        # html.P(id='Function'),
                        html.P(id='Datetime'),



#                         html.Br(),
#                         html.Br(),
#                         html.Br(),
                        
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in site_name_list

                                            ],
                                            value=None,
                                            placeholder="Select site",
                                        )
                                    ],
                                    style={ 'width':'250px'}
                                )


                            ],
                            style={"display": "none", "justify-content": "center", "align-items": "center"}
                        ),

                        html.Br(),
                        html.Br(),
                        html.Br(),
                        DataTable(
                                    id='maintenance_table_h',
                                    columns=[
                                        {"name": "Asset Tag", "id": "Asset Tag"},
                                        {"name": "Open Maintenance Action", "id": "Open Maintenance Action"},
                                        {"name": "Due Date", "id": "Due Date"},
                                    ],
                                    data=data_maintenance_action,
                                    style_table={'overflowX': 'auto', 'display':'none'},
                                    style_cell={
                                                    'backgroundColor': 'grey',  # Header background color
                                                    'color': 'black',            # Header text color
                                                    'textAlign': 'center',
                                                    'whiteSpace': 'normal',

                                                },
                                    style_header={
                                                    'backgroundColor': '#444',  # Header background color
                                                    'color': 'white',            # Header text color
                                                    'textAlign': 'center',       # Center header text
                                                },
                                    page_size=10,  # Adjust as needed
                                    
                                ),

                        html.Br(),
                        html.Br(),
                        html.Div(
                            id='sniffer_mode_button',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Sniffer Mode', id='sniffer_mode_page', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),
                        html.Br(),
                        html.Div(
                            id='test_mode_button',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Test Mode', id='test_mode_page', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),

                            ]
                        ),

                        html.Br(),
                        html.Div(
                            id='stand_alone_mode_button',
                            style={"margin-top": "20px", "text-align": "center", "display": "flex", "justify-content": "center"},
                            children = [
                                html.Button('Stand-Alone Mode', id='stand_alone_mode_page', style={ 'width':'300px', 'background-color':'grey', 'border-color':'grey','color': 'black', 'font-weight': 'bold'}),
                                

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
                        logout_button,
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
                    children=[
                        dcc.Graph(id="Map_h", figure=blank_fig(),
                                  config={
                                      "displaylogo": False,
                                      'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines', 'hoverClosestCartesian', 'hoverCompareCartesian']
                                  },#remove ploty botton
                                  )  ,#plot the map

                        dcc.Location(id="url_h"), ## this allow to update the page awith the call back of point selection

                    ],
                ),
            ],)
    ],



)




#########################################################################################################################3
##################################     ADD METHOD TO CALL THE DATA FROM THE DATABASE BASED ON SELECTION  ################



# Update Map Graph based on site selected, selected data on histogram and location dropdown
# ,Input("Map", "clickData")
@callback(
    Output("Map_h", "figure"),
    Output('maintenance_table_h', 'data'),
        Output('maintenance_table_h', 'style_cell'),

    [

        Input("location-dropdown", "value")

    ],

)

def update_graph(selectedLocation):
    #set mode to none to stop yellow led
    global_variables.current_mode = None
    global_variables.sniffer_mode_condition = False
    global_variables.test_mode_condition = False
    global_variables.monitoring_mode_condtition = False
#     global_variables.current_mode = None
#     print(global_variables.current_mode)
    
    # Default map parameters
    zoom = 5
    bearing = 0
    marker_size_list = [15]
    simbol_list = ['circle']
    hv_transmission_marker_size_list = [15]# need to hablde the initial condition
    site_coordinates = get_site_coordinate(selectedLocation)

    if len(site_coordinates)!=0:
        latInitial = site_coordinates[0][0]
        lonInitial = site_coordinates[0][1]

    else:
        latInitial = 42.50920 #-32.566337
        lonInitial = 13.01978#137.835736
    # Handle initial map position
    center_lat = latInitial
    center_lon = lonInitial
    asset_tags_list = []
    asset_tags_cable_list = []
    asset_category_list=[]
    asset_details = []
    asset_details_cables = []
    hv_transmission_asset_details= []#for navigation direct all the accessories to the main page
    color_list = get_color_list_map()[0]
    cable_color_list = get_color_list_map()[1]
    hv_cable_color_list = get_color_list_map()[2]




    #maintenance table
    data_table = data_maintenance_action
    style_cell={
                'backgroundColor':'grey' ,  # Header background color
                 'color': 'black',  # Header text color
                 'textAlign': 'center',
                 'whiteSpace': 'normal',  # Allow text to wrap
                 # 'overflow': 'hidden',
                 # 'textOverflow': 'ellipsis'
    }


    # Update map position based on dropdown selection
    if selectedLocation in site_name_list:

        site_name = selectedLocation  # Example: use selectedLocation as site_id

        for item in site_list:
            if site_name == item[1]:
                simbol_list = []
                site_id=item[0]
                selected_site_asset_list = get_asset_list(site_id)
                # eliminate the cable from the list as they will be visualised as lines
                selected_site_asset_list_nocable = []
                selected_site_asset_cable_list = []
                selected_site_hv_transmission_line_accessories_list = []
                for asset in selected_site_asset_list:

                    if asset[24] ==4: #cable
                        if asset[2] !='Transmission':
                            selected_site_asset_cable_list.append(asset)
                        if asset[2] =='Transmission':
                            hv_accessories_list = get_transmission_line_accessories_details(asset[0])
                            for acc in hv_accessories_list:
                                selected_site_hv_transmission_line_accessories_list.append(acc)
                                hv_transmission_marker_size_list.append(15)
                    else:
                        selected_site_asset_list_nocable.append(asset)
                        marker_size_list.append(15)
                        if asset[24] == 3:
                            simbol_list.append('square')
                        if asset[24] == 1:
                            simbol_list.append('circle')
                        if asset[24] == 2:
                            simbol_list.append('diamond')


                lat_list = [float(lat[22]) for lat in selected_site_asset_list_nocable]
                lon_list = [float(lon[23]) for lon in selected_site_asset_list_nocable]

                asset_tags_list = [tag[1] for tag in selected_site_asset_list_nocable]
                asset_tags_cable_list = [tag[1] for tag in selected_site_asset_cable_list]
                asset_category_list = [cat[24] for cat in selected_site_asset_list_nocable]

                asset_id_list = [id[0] for id in selected_site_asset_list_nocable]
                asset_id_cable_list = [id[0] for id in selected_site_asset_cable_list]
                #note use the same color for the whole line as the risk index is based on the asset
                hv_transmission_line_accessories_ids_list = [id[1] for id in selected_site_hv_transmission_line_accessories_list]
                # hv_transmission_line_accessories_lat_list = [lat[3] for lat in selected_site_hv_transmission_line_accessories_list]
                # hv_transmission_line_accessories_lon_list = [lon[4] for lon in selected_site_hv_transmission_line_accessories_list]
                # hv_transmission_line_accessories_tag_list = [tag[2] for tag in selected_site_hv_transmission_line_accessories_list]


                asset_function_list = [fun[2] for fun in selected_site_asset_list_nocable]

                site_id_list = [site_id for rows in asset_category_list]

                #get color list based on the risk:


                risk_list = []
                cable_risk_list = []
                hv_cable_accessory_risk_list = []
                for ids in asset_id_list:
                    asset_latest_condition = get_letest_asset_analysis(ids)
                    if asset_latest_condition is not None:
                        if len(asset_latest_condition)!=0:
                            risk_list.append(asset_latest_condition[3])
                        if len(asset_latest_condition)==0:
                            risk_list.append(str(0))
                    if asset_latest_condition is None:
                        risk_list.append(0)

                for ids in asset_id_cable_list:
                    asset_latest_condition = get_letest_asset_analysis(ids)
                    if asset_latest_condition is not None:
                        if len(asset_latest_condition)!=0:
                            cable_risk_list.append(asset_latest_condition[3])
                        if len(asset_latest_condition)==0:
                            cable_risk_list.append(str(0))
                    if asset_latest_condition is None:
                        cable_risk_list.append(0)


                for ids in hv_transmission_line_accessories_ids_list:
                    accesory_latest_condition = get_letest_asset_analysis(ids)
                    if asset_latest_condition is not None:
                        if len(asset_latest_condition)!=0:
                            hv_cable_accessory_risk_list.append(asset_latest_condition[3])
                        if len(asset_latest_condition)==0:
                            hv_cable_accessory_risk_list.append(str(0))
                    if asset_latest_condition is None:
                        hv_cable_accessory_risk_list.append(0)

                color_list = []
                cable_color_list = []
                hv_cable_color_list = []
                for risks in risk_list:
                    if 1 <= int(risks) <= 4:
                        color = "green"
                    elif 4 < int(risks) <= 9:
                        color = "orange"
                    elif 9 < int(risks) <= 20:
                        color = "red"
                    else:
                        color = "grey"  # Default color if condition is out of expected range

                    color_list.append(color)

                for risks in cable_risk_list:
                    if 1 <= int(risks) <= 4:
                        color = "green"
                    elif 4 < int(risks) <= 9:
                        color = "orange"
                    elif 9 < int(risks) <= 20:
                        color = "red"
                    else:
                        color = "grey"  # Default color if condition is out of expected range

                    cable_color_list.append(color)

                for risks in hv_cable_accessory_risk_list:
                    if 1 <= int(risks) <= 4:
                        color = "green"
                    elif 4 < int(risks) <= 9:
                        color = "orange"
                    elif 9 < int(risks) <= 20:
                        color = "red"
                    else:
                        color = "grey"  # Default color if condition is out of expected range

                    hv_cable_color_list.append(color)

                # get open maintenance acitons
                maintenance_action_list = []
                for ids in asset_id_list:
                    action = get_maintenance_action(ids)
                    maintenance_action_list.append(action)

                for ids in asset_id_cable_list:
                    action = get_maintenance_action(ids)
                    maintenance_action_list.append(action)

                #remove empty items from the list
                maintenance_action_list_cleaned = []
                for actions in maintenance_action_list:
                    if len(actions)!=0:
                        maintenance_action_list_cleaned.append(actions)



                data_table = []
                for sublist in maintenance_action_list_cleaned:
                    for item in sublist:
                        data_table.append({
                            "Asset Tag": item[6],
                            "Open Maintenance Action": item[2],
                            "Due Date": item[3],
                        })


                

                style_cell = {'backgroundColor': '#FF6666',
                              'color': 'white',
                              'textAlign': 'center',
                              'whiteSpace': 'normal'}


                asset_details = []
                asset_details_cables = []
                hv_transmission_asset_details_partial = []
                for asset in selected_site_asset_list:
                    if asset[24] == 4:
                        if asset[2] !='Transmission':
                            asset_details_cables.append(asset)
                        if asset[2] =='Transmission':
                            hv_transmission_asset_details_partial.append(asset)
                    else:
                        asset_details.append(asset)

                # asset_details = [ids for ids in selected_site_asset_list if ids[2]!='Transmission']
                for acc in range(len(hv_transmission_line_accessories_ids_list)):
                    hv_transmission_asset_details.append(hv_transmission_asset_details_partial[0])

                # print(asset_details)
                # print(asset_details_cables)
                # print(hv_transmission_asset_details)

        # Calculate new center coordinates based on asset_list (mean or other logic)
        if lat_list and lon_list:
            center_lat = sum(lat_list) / len(lat_list)
            center_lon = sum(lon_list) / len(lon_list)
            zoom = 16  # Example zoom level for detailed view


    # print(asset_tags_list)
    # print('cable',asset_tags_cable_list)


    # Create Scattermapbox trace
    # print('scatter plot')
    # print(asset_tags_list)
    # # print(lat_initial)
    # # print(lon_initial)
    # print(asset_details)
    # print(marker_size_list)
    # print(color_list)

    #update coordinae list based on the asset selected
    lat_initial = []
    lon_initial = []
    if len(asset_details)!=0:
        for asset in asset_details:
            coordinate = get_single_asset_coordinate(asset[0])
            lat_initial.append(coordinate[0][0])
            lon_initial.append(coordinate[0][1])
    # else:
    #     site_list = get_customer_site_from_user_id()
    #     # print('site list', site_list)
    #
    #     # site_name_list = [item[1] for item in site_list]
    #
    #     # print(site_name_list)
    #     # crete asset coordinate list for the customer
    #     lat_initial = []
    #     lon_initial = []
    #     asset_tags = []
    #     asset_tags_cable = []
    #     asset_category = []
    #     color_list = []
    #     risk_list = []
    #     cable_risk_list = []
    #     cable_color_list = []
    #
    #     # differenciate the transmission lines as the accessories are like individual asset in the map
    #     hv_transmission_line_accessories_tag_list = []
    #     hv_transmission_line_accessories_lat_list = []
    #     hv_transmission_line_accessories_lon_list = []
    #     hv_cable_accessory_risk_list = []
    #     hv_cable_color_list = []
    #
    #     for site_id in site_list:
    #         asset_list = get_asset_list(site_id[0])
    #
    #         for asset in asset_list:
    #             # rm, sw, tx
    #             if asset[24] != 4:
    #
    #                 lat_initial.append(asset[22])
    #                 lon_initial.append(asset[23])
    #                 asset_tags.append(asset[1])
    #                 asset_category.append(asset[24])
    #
    #                 try:
    #                     analysis = get_letest_asset_analysis(asset[0])
    #                     if len(analysis) != 0:
    #                         risk_list.append(analysis[3])
    #                     else:
    #                         risk_list.append(0)
    #
    #                 except TypeError:
    #                     risk_list.append(0)
    #             # cable + transmission lines
    #             if asset[24] == 4:
    #
    #                 # transmission
    #                 if asset[2] == 'Transmission':
    #                     # get accessories details
    #                     hv_accessories_list = get_transmission_line_accessories_details(asset[0])
    #                     for acc in hv_accessories_list:
    #                         hv_transmission_line_accessories_tag_list.append(acc[2])
    #                         hv_transmission_line_accessories_lat_list.append(acc[3])
    #                         hv_transmission_line_accessories_lon_list.append(acc[4])
    #
    #                     try:
    #                         analysis = get_letest_asset_analysis(asset[0])
    #                         if len(analysis) != 0:
    #                             hv_cable_accessory_risk_list.append(analysis[3])
    #                         else:
    #                             hv_cable_accessory_risk_list.append(0)
    #                     except TypeError:
    #                         hv_cable_accessory_risk_list.append(0)
    #
    #
    #                 # distribution
    #                 else:
    #
    #                     asset_tags_cable.append(asset[1])
    #
    #                     try:
    #                         analysis = get_letest_asset_analysis(asset[0])
    #                         if len(analysis) != 0:
    #                             cable_risk_list.append(analysis[3])
    #                         else:
    #                             cable_risk_list.append(0)
    #                     except TypeError:
    #                         cable_risk_list.append(0)

    #create a list of traces to include transmission lines
    traces = []
    #symbol=simbol_list
    # # # # # # # # # # # # # # # # # # #
    #add condition to visualise rotating machine color in the home page
#     print(asset_details)
#     print(color_list)
#     print(lat_initial)
#     print(asset_tags_list)
#     print(marker_size_list)


    #rm, sw, tx
    trace = go.Scattermapbox(
        lat=lat_initial,
        lon=lon_initial,
        hovertext=asset_tags_list,
        customdata=asset_details,
        mode="markers",
        marker=dict(size=marker_size_list, color=color_list),
        # line=dict(width=2, color='green'),  # Specify line properties
    )

    trace_transmission = go.Scattermapbox(
        lat=hv_transmission_line_accessories_lat_list,
        lon=hv_transmission_line_accessories_lon_list,
        hovertext=hv_transmission_line_accessories_tag_list,
        customdata=hv_transmission_asset_details, #for navigation
        mode="markers",
        marker=dict(size=hv_transmission_marker_size_list, color=hv_cable_color_list),
        # line=dict(width=2, color='green'),  # Specify line properties
    )

    traces.append(trace)
    traces.append(trace_transmission)

    #create custom data for cable
    asset_cable_details = []
    for tag_cable in asset_tags_cable_list:
        for ass in asset_details_cables:
            if ass[1] == tag_cable:
                asset_cable_details.append(ass)
            else:
                None



    #get the details of the cable from the site layout table to define the mid points of the lines
    site_asset_layout = get_site_asset_layout(selectedLocation)

    start_lat_coordinate = []
    start_lon_coordinate = []

    end_lat_coordinate = []
    end_lon_coordinate = []

    cable_asset_tag_list_new = []

    for assetcouple in site_asset_layout:

        cable_asset_tag_list_new.append(get_single_asset_tag(assetcouple[4])[0])

        start_coordinate_asset = get_single_asset_coordinate(assetcouple[1])
        end_coordinate_asset = get_single_asset_coordinate(assetcouple[2])

        start_lat_coordinate.append(start_coordinate_asset[0][0])
        start_lon_coordinate.append(start_coordinate_asset[0][1])

        end_lat_coordinate.append(end_coordinate_asset[0][0])
        end_lon_coordinate.append(end_coordinate_asset[0][1])

    cable_lat_coordinates_list = []
    cable_lon_coordinates_list = []
    cable_lat_coordinates = zip(start_lat_coordinate, end_lat_coordinate)
    cable_lon_coordinates = zip(start_lon_coordinate, end_lon_coordinate)
    for coo in cable_lat_coordinates:
        cable_lat_coordinates_list.append(coo)
    for coo in cable_lon_coordinates:
        cable_lon_coordinates_list.append(coo)


    # print(cable_asset_tag_list_new)
    # print(cable_color_list)
    # Create lines with different colors
    line_traces = []
    midpoint_latitudes = []
    midpoint_longitudes = []
    for i in range(len(cable_lat_coordinates_list)):
        # Create a line segment between two points
        line_trace = go.Scattermapbox(
            lat=[cable_lat_coordinates_list[i][0], cable_lat_coordinates_list[i][1]],  # Line segment between two points
            lon=[cable_lon_coordinates_list[i][0], cable_lon_coordinates_list[i][1]],
            hovertext=cable_asset_tag_list_new[i],  # Hover text for the line
            mode='lines',
            line=dict(width=2, color=cable_color_list[i]),  # Different color for each line
            hoverinfo='text',
            customdata=asset_details_cables,  # Optional detail
        )
        line_traces.append(line_trace)

        # Calculate midpoints

        midpoint_lat = (cable_lat_coordinates_list[i][0] + cable_lat_coordinates_list[i][1]) / 2
        midpoint_lon = (cable_lon_coordinates_list[i][0] + cable_lon_coordinates_list[i][1]) / 2
        midpoint_latitudes.append(midpoint_lat)
        midpoint_longitudes.append(midpoint_lon)

    # Create markers at midpoints
    # add condition to separate a bit the point if there are two cable on the same route

    # print(midpoint_latitudes)
    # print(midpoint_longitudes)
    # Small offset to adjust duplicates
    adjusted_latitudes = []
    adjusted_longitudes = []
    seen = set()

    offset = Decimal('0.00001')

    for lat, lon in zip(midpoint_latitudes,midpoint_longitudes):
        coordinate = (lat, lon)

        if coordinate in seen:
            # Adjust the latitude slightly for duplicates
            new_lat = lat + offset
            new_lon = lon
            adjusted_latitudes.append(new_lat)
            adjusted_longitudes.append(lon)
            # Update for next duplicate adjustment
            # offset += Decimal('0.00001')  # Increase the offset for subsequent duplicates
        else:
            adjusted_latitudes.append(lat)
            adjusted_longitudes.append(lon)
            seen.add(coordinate)

    adjusted_mid_point_cable_color = []
    i=0
    for pt in midpoint_latitudes:
        adjusted_mid_point_cable_color.append(cable_color_list[i])
        i+=1

    midpoint_trace = go.Scattermapbox(
        lat=adjusted_latitudes,
        lon=adjusted_longitudes,
        mode='markers',
        marker=dict(size=7, color=adjusted_mid_point_cable_color),  # Customize marker size and color
        hoverinfo='text',
        hovertext=asset_tags_cable_list,
        text=asset_tags_cable_list,
        customdata=asset_details_cables
    )

    #create trace for transmission line
    transmission_line_traces = []
    try:
        hv_color = hv_cable_color_list[0]

    except IndexError:
        hv_color = 'grey'

    for i in range(len(hv_transmission_line_accessories_lat_list)-1):
        # Create a line segment between two points
        transmission_line_trace = go.Scattermapbox(
            lat=[hv_transmission_line_accessories_lat_list[i], hv_transmission_line_accessories_lat_list[i+1]],  # Line segment between two points
            lon=[hv_transmission_line_accessories_lon_list[i], hv_transmission_line_accessories_lon_list[i+1]],
            # hovertext=hv_transmission_line_accessories_tag_list[i],  # Hover text for the line
            mode='lines',
            line=dict(width=2, color=hv_color),  # Different color for each line
            hoverinfo='text',
            # customdata=asset_cable_details,  # Optional detail
        )
        transmission_line_traces.append(transmission_line_trace)



    # Return updated figure
    return {
        'data': traces+ line_traces + transmission_line_traces + [midpoint_trace],
        'layout': {
            'margin': {'l': 0, 'r': 35, 't': 0, 'b': 0},
            'height': 800,
            'showlegend': False,
            'mapbox': {
                # 'style': "open-street-map",
                'accesstoken': mapbox_access_token,
                'center': {'lat': center_lat, 'lon': center_lon},
                'zoom': zoom,
                'bearing': bearing,
                'style': "dark"
            },
            'clickmode': 'none' if selectedLocation is None else 'event+select'
        }
    }, data_table , style_cell
                    








# #open the analytic page when clicking the page
@callback(
    Output("store", "data"),
    Output('url_h','pathname'),
    Input("Map_h", "clickData"),

)
def get_selected_asset(custom_data):
    page_url='home'
    # store results in a dcc.Store in app.py
    selected_asset = custom_data

    # print(selected_asset)
    if selected_asset:
        try:
            asset_tag = selected_asset["points"][0]["hovertext"]

            asset_category = selected_asset["points"][0]['customdata'][24]
            asset_function = selected_asset["points"][0]['customdata'][2]
            asset_feature_1 = 'Air'


            rotor_type = selected_asset["points"][0]['customdata'][12]

            if asset_category ==1:
                if asset_function == 'Generator':
                    page_url = 'asset-overview-rotatingmachine-generator'
                if asset_function == 'Motor':
                    page_url = 'asset-overview-rotatingmachine-motor'
                if asset_function == 'Syncronous Condenser':
                    page_url = ''

            if asset_category ==2:
                # if asset_function == 'Power':
                #     page_url = 'asset-overview_transformer'
                # if asset_function == 'Distribution':
                #     page_url = 'asset-overview-transformer'
                # if asset_function == 'Special':
                page_url = 'asset-overview-transformer'

            if asset_category ==3:
                if asset_feature_1 == 'Air':
                    page_url = 'asset-overview-switchgear-air'
                if asset_feature_1 == 'SF6':
                    page_url = 'asset-overview-switchgear-sf6'

            if asset_category ==4:
                if asset_function == 'Transmission':
                     page_url = 'asset-overview-transmissionline'
                else:
                    page_url = 'asset-overview-cable'
                
        except KeyError:

            None



    else:
        
        raise PreventUpdate
    # print('home',selected_asset)
    return selected_asset, page_url


###################################################################################################################################################################
#thread for led parallel operation
def thread_led_sniffer_mode():
    thread = threading.Thread(target=led_sniffer_mode)
    thread.daemon = True
    thread.start()


def thread_led_test_mode():
    thread = threading.Thread(target=led_test_mode)
    thread.daemon = True
    thread.start()

def thread_led_monitoring_mode():
    thread = threading.Thread(target=led_monitoring_mode)
    thread.daemon = True
    thread.start()

# Update user information
@callback(
    Output("Username", "children"),
    Output('Datetime', 'children'),
    Input("url_labels", "pathname")
    )
def update_username(_):
    user_dict = get_session_user_details()
    
    name_string = user_dict['name'] + " "+ user_dict['surname']
    datetime_string = user_dict['last_connection_time']
    datetime_string_final = datetime_string.strftime("%Y-%m-%d %H:%M:%S")

    
    
    return name_string, datetime_string_final


#Navitage to other pages

#Sniffer mode
@callback(
    Output('url_h', 'pathname', allow_duplicate=True),
    Input('sniffer_mode_button', 'n_clicks'),
    prevent_initial_call=True,
)
def sniffer_mode(n_clicks):
    if n_clicks:
        # Perform logout operations here (e.g., clearing session data, redirecting to login page)
#         gpio_cleanup()
        global_variables.current_mode = 'Sniffer'
        global_variables.sniffer_mode_condition = True
        global_variables.test_mode_condition = False
        global_variables.monitoring_mode_condtition = False
        thread_led_sniffer_mode()
        # Redirect to the login page or perform any logout operation
        return 'sniffer-mode-page'  # Redirect to the login page URL
    else:
        raise PreventUpdate
    
#Test Mode
@callback(
    Output('url_h', 'pathname', allow_duplicate=True),
    Input('test_mode_button', 'n_clicks'),
    prevent_initial_call=True,
)
def test_mode(n_clicks):
    if n_clicks:
        # Perform logout operations here (e.g., clearing session data, redirecting to login page)
#         gpio_cleanup()
        global_variables.current_mode = 'Test'
        global_variables.sniffer_mode_condition = False
        global_variables.test_mode_condition = True
        global_variables.monitoring_mode_condtition = False
        thread_led_test_mode()
        # Redirect to the login page or perform any logout operation
        return 'test-mode-page'  # Redirect to the login page URL
    else:
        raise PreventUpdate
    
#Stand alone Mode
@callback(
    Output('url_h', 'pathname', allow_duplicate=True),
    Input('stand_alone_mode_button', 'n_clicks'),
    prevent_initial_call=True,
)
def monitoring_mode(n_clicks):
    if n_clicks:
        # Perform logout operations here (e.g., clearing session data, redirecting to login page)
#         gpio_cleanup()
        global_variables.current_mode = 'Monitoring'
        global_variables.sniffer_mode_condition = False
        global_variables.test_mode_condition = False
        global_variables.monitoring_mode_condtition = True
        
        thread_led_monitoring_mode()
        # Redirect to the login page or perform any logout operation
        return 'stand-alone-mode-page'  # Redirect to the login page URL
    else:
        raise PreventUpdate

# Log out

@callback(
    Output('url_h', 'pathname', allow_duplicate=True),
    Input('logout-button', 'n_clicks'),
    prevent_initial_call=True,
)
def logout_user(n_clicks):
    if n_clicks:
        # Perform logout operations here (e.g., clearing session data, redirecting to login page)
        # Redirect to the login page or perform any logout operation
        update_connection_status(0)
        global_variables.connection_status = 0
        global_variables.current_mode = None
        global_variables.sniffer_mode_condition = False
        global_variables.test_mode_condition = False
        global_variables.monitoring_mode_condtition = False
        
        global_variables.stop_event.set()
        
        
#         gpio_cleanup()
        
        return ''  # Redirect to the login page URL
    else:
        raise PreventUpdate
