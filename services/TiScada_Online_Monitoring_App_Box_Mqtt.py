import sqlite3
from io import BytesIO

import pandas as pd
from boxsdk import OAuth2, Client
import requests
import os
import json
import jwt
import time
from cryptography.hazmat.primitives import serialization
from datetime import datetime


import mysql.connector

from functions.analyse_data_mysql import analyse_data
from functions.assess_condition_mysql import assess_condition

# Monitoring details
Monitoring = 'Yes'
monitoring_type = 'Techimp-PDScope'
connection_type = 'MQTT'

#asset details
asset_id_list = [83,84,85,86,87]
subcomponet_id =2
diagnostic_test_id  =11

temp_list_gen1 = []
temp_list_gen2 = []
temp_list_gen3 = []
temp_list_gen4 = []
temp_list_gen5 = []

data_already_inserted = None

# Function to load private key from the JSON file and decrypt it
def load_private_key_from_json(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # print(data)

    # Extract passphrase and private key from JSON
    private_key_pem = data['boxAppSettings']['appAuth']['privateKey']
    passphrase = data['boxAppSettings']['appAuth']['passphrase']
    client_id = data['boxAppSettings']['clientID']
    client_secret = data['boxAppSettings']['clientSecret']
    public_key_id = data['boxAppSettings']['appAuth']['publicKeyID']

    # Decrypt the private key using the passphrase
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),  # Make sure private key is in bytes
        password=passphrase.encode()  # Provide the passphrase for decryption
    )
    return private_key, client_id, client_secret, public_key_id, passphrase


# Function to generate JWT using the private key
def generate_jwt(private_key, client_id, public_key_id):
    payload = {
        'iss': client_id,  # Client ID from the Box app
        'sub': '40148540632',  # Use your Box user ID here
        'aud': 'https://api.box.com/oauth2/token',  # Audience
        'box_sub_type': 'user',  # Box sub-type (use 'enterprise' if it's an enterprise app)
        'jti': str(time.time()),  # JWT ID (unique identifier)
        'exp': int(time.time()) + 60  # Expiry time of the JWT (1 hour)
    }

    # Sign the JWT with the private key
    encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256', headers={'kid': public_key_id})
    return encoded_jwt


# Function to get an access token using the JWT
def get_access_token(jwt_token, client_id, client_secret):
    url = "https://api.box.com/oauth2/token"
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'client_id': client_id,
        'client_secret': client_secret,
        'assertion': jwt_token
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Error getting access token:", response.text)
        return None


# Function to list all tables in the SQLite database
def list_tables(db_file):
    conn = sqlite3.connect(db_file)
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor = conn.cursor()
    cursor.execute(query)
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]


# Function to read data from SQLite database and filter as needed
def read_sqlite_data(db_file, subject_list):
    conn = sqlite3.connect(db_file)
    query = "SELECT * FROM diagnostic_data;"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    filtered_data = []
    for item in rows:
        if item[1] in subject_list:
            filtered_data.append(
                [item[1].split('/')[5], item[1].split('/')[8], item[1].split('/')[12], item[3], item[4]])
    conn.close()
    return filtered_data


# Function to save data to Excel file
def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)


# Function to upload the file to Box
def upload_to_box(file_path, file_name, access_token,client_id, client_secret,):
    # client = Client.from_access_token(access_token)
    # folder = client.folder('0')  # Root folder
    # new_file = folder.upload(file_path, file_name=file_name)
    # print(f"File uploaded to Box: {new_file.name}")
    # OAuth2 initialization
    oauth2 = OAuth2(client_id, client_secret, access_token=access_token)
    client = Client(oauth2)

    # Upload the file to the root folder (or specify another folder)
    folder = client.folder('0')  # '0' refers to the root folder
    new_file = folder.upload(file_path, file_name=file_name)
    print(f"File uploaded to Box: {new_file.name}")

# Function to search for the file by name in the Box root folder
def search_file_by_name(file_name, access_token, client_id, client_secret):
    # OAuth2 initialization
    oauth2 = OAuth2(client_id, client_secret, access_token=access_token)
    client = Client(oauth2)

    # Search for the file by name (can be modified to search specific folders)
    # search_results = client.search().query(file_name, file_extensions=['.xlsx'], limit=1)
    search_results = client.search().query(file_name, file_type='file', limit=1)

    # print(search_results)

    # Check if the file is found and return the file ID
    for item in search_results:

        return item.id




# Function to read the Excel file from Box without downloading
def read_file_from_box(file_id, access_token, client_id, client_secret):
    # OAuth2 initialization
    oauth2 = OAuth2(client_id, client_secret, access_token=access_token)
    client = Client(oauth2)

    # Get the file from Box using its file ID
    file = client.file(file_id).get()

    # Read the file as a binary stream
    file_content = file.content()

    # Use pandas to read the content from the binary stream (in-memory file)
    df = pd.read_excel(BytesIO(file_content))

    return df


def upload_to_db(data):
    for index, row in enumerate(data):
        print('Inserting Gen{}, phase {}'.format(row[1],row[4]))
        # insert data into the db and perform analysis and assessment

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave!2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # id, date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11, feature_12, feature_13, feature_14, feature_15, feature_16, feature_17, feature_18, feature_19, feature_20, feature_21, feature_22, feature_23, feature_24, feature_25, analysis
        insert_query = """
            INSERT INTO online_test_data (date, asset_id, subcomponent_id, diagnostic_test_id,feature_1, feature_2, feature_3,feature_15, feature_16, feature_17, feature_18, feature_19)
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)
        """

        # Data to be inserted (for example)



        # print(fukc)

        cursor.execute(insert_query, row)
        conn.commit()
        cursor.close()
        conn.close()

def analyse_the_data(asset_id):


    analyse_data(asset_id)

    time.sleep(5)

def assess_condition_data(asset_id):
    assess_condition(asset_id)

    time.sleep(5)

# def read_from_box(file_id, access_token, client_id, client_secret):
#     oauth2 = OAuth2(client_id, client_secret, access_token=access_token)
#     client = Client(oauth2)  # Create the client instance
#
#     # Retrieve the file from Box by file ID
#     try:
#         box_file = client.file(file_id).get()  # Fetch the file object
#         file_name = box_file.name  # Get the file name
#
#         # Download the file content to a local file
#         file_content = box_file.content()  # Get the file content
#
#         # Save the file content to a local file
#         with open(file_name, 'wb') as local_file:
#             local_file.write(file_content)
#
#         print(f"File '{file_name}' downloaded successfully.")
#
#     except Exception as e:
#         print(f"Error downloading file: {e}")


# Main function that orchestrates the process
def main():
    json_file_path = '1269683032_r6f7p0lq_config.json'  # Path to your JSON credentials file
    file_name = 'output'
    # Load credentials and private key from JSON file
    private_key, client_id, client_secret, public_key_id, passphrase = load_private_key_from_json(json_file_path)

    # Step 1: Generate JWT
    jwt_token = generate_jwt(private_key, client_id, public_key_id)

    # Step 2: Get access token
    access_token = get_access_token(jwt_token, client_id, client_secret)
    if not access_token:
        print("Error: Failed to get access token.")
        return

    # Step 3: Search for the file by name in Box
    file_id = search_file_by_name(file_name, access_token, client_id, client_secret)
    if not file_id:
        print("Error: Could not find the file on Box.")
        return

    # Step 4: Read the file directly from Box
    df = read_file_from_box(file_id, access_token, client_id, client_secret)

    # # Step 5: Process the data (just display the first few rows as an example)
    # print(df.head())  # Display the first few rows of the Excel file

    list_of_lists = df.values.tolist()
    print(list_of_lists)
    gen1_datetime_ch1 = None
    gen1_qmax95_ch1 =None
    gen1_nw_ch1=None
    gen1_sync_ch1 = None

    gen1_datetime_ch2 = None
    gen1_qmax95_ch2 = None
    gen1_nw_ch2 = None
    gen1_sync_ch2 = None

    gen1_datetime_ch3 = None
    gen1_qmax95_ch3 = None
    gen1_nw_ch3 = None
    gen1_sync_ch3 = None

    gen2_datetime_ch1 = None
    gen2_qmax95_ch1 = None
    gen2_nw_ch1 = None
    gen2_sync_ch1 = None

    gen2_datetime_ch2 = None
    gen2_qmax95_ch2 = None
    gen2_nw_ch2 = None
    gen2_sync_ch2 = None

    gen2_datetime_ch3 = None
    gen2_qmax95_ch3 = None
    gen2_nw_ch3 = None
    gen2_sync_ch3 = None

    gen3_datetime_ch1 = None
    gen3_qmax95_ch1 = None
    gen3_nw_ch1 = None
    gen3_sync_ch1 = None

    gen3_datetime_ch2 = None
    gen3_qmax95_ch2 = None
    gen3_nw_ch2 = None
    gen3_sync_ch2 = None

    gen3_datetime_ch3 = None
    gen3_qmax95_ch3 = None
    gen3_nw_ch3 = None
    gen3_sync_ch3 = None

    gen4_datetime_ch1 = None
    gen4_qmax95_ch1 = None
    gen4_nw_ch1 = None
    gen4_sync_ch1 = None

    gen4_datetime_ch2 = None
    gen4_qmax95_ch2 = None
    gen4_nw_ch2 = None
    gen4_sync_ch2 = None

    gen4_datetime_ch3 = None
    gen4_qmax95_ch3 = None
    gen4_nw_ch3 = None
    gen4_sync_ch3 = None

    gen5_datetime_ch1 = None
    gen5_qmax95_ch1 = None
    gen5_nw_ch1 = None
    gen5_sync_ch1 = None

    gen5_datetime_ch2 = None
    gen5_qmax95_ch2 = None
    gen5_nw_ch2 = None
    gen5_sync_ch2 = None

    gen5_datetime_ch3 = None
    gen5_qmax95_ch3 = None
    gen5_nw_ch3 = None
    gen5_sync_ch3 = None

    # Your for loop to process data
    for rows in list_of_lists:
        if rows[0] == 'GEN_1':
            if rows[1] == 'Ch1':
                if rows[2] == 'QMax95':
                    gen1_qmax95_ch1 = rows[3]
                    gen1_datetime_ch1 = rows[4]
                if rows[2] == 'Nw':
                    gen1_nw_ch1 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen1_sync_ch1 = rows[3]
            if rows[1] == 'Ch2':
                if rows[2] == 'QMax95':
                    gen1_qmax95_ch2 = rows[3]
                    gen1_datetime_ch2 = rows[4]
                if rows[2] == 'Nw':
                    gen1_nw_ch2 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen1_sync_ch2 = rows[3]
            if rows[1] == 'Ch3':
                if rows[2] == 'QMax95':
                    gen1_qmax95_ch3 = rows[3]
                    gen1_datetime_ch3 = rows[4]
                if rows[2] == 'Nw':
                    gen1_nw_ch3 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen1_sync_ch3 = rows[3]

        elif rows[0] == 'GEN_2':
            if rows[1] == 'Ch1':
                if rows[2] == 'QMax95':
                    gen2_qmax95_ch1 = rows[3]
                    gen2_datetime_ch1 = rows[4]
                if rows[2] == 'Nw':
                    gen2_nw_ch1 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen2_sync_ch1 = rows[3]
            if rows[1] == 'Ch2':
                if rows[2] == 'QMax95':
                    gen2_qmax95_ch2 = rows[3]
                    gen2_datetime_ch2 = rows[4]
                if rows[2] == 'Nw':
                    gen2_nw_ch2 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen2_sync_ch2 = rows[3]
            if rows[1] == 'Ch3':
                if rows[2] == 'QMax95':
                    gen2_qmax95_ch3 = rows[3]
                    gen2_datetime_ch3 = rows[4]
                if rows[2] == 'Nw':
                    gen2_nw_ch3 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen2_sync_ch3 = rows[3]

        elif rows[0] == 'GEN_3':
            if rows[1] == 'Ch1':
                if rows[2] == 'QMax95':
                    gen3_qmax95_ch1 = rows[3]
                    gen3_datetime_ch1 = rows[4]
                if rows[2] == 'Nw':
                    gen3_nw_ch1 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen3_sync_ch1 = rows[3]
            if rows[1] == 'Ch2':
                if rows[2] == 'QMax95':
                    gen3_qmax95_ch2 = rows[3]
                    gen3_datetime_ch2 = rows[4]
                if rows[2] == 'Nw':
                    gen3_nw_ch2 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen3_sync_ch2 = rows[3]
            if rows[1] == 'Ch3':
                if rows[2] == 'QMax95':
                    gen3_qmax95_ch3 = rows[3]
                    gen3_datetime_ch3 = rows[4]
                if rows[2] == 'Nw':
                    gen3_nw_ch3 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen3_sync_ch3 = rows[3]

        elif rows[0] == 'GEN_4':
            if rows[1] == 'Ch1':
                if rows[2] == 'QMax95':
                    gen4_qmax95_ch1 = rows[3]
                    gen4_datetime_ch1 = rows[4]
                if rows[2] == 'Nw':
                    gen4_nw_ch1 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen4_sync_ch1 = rows[3]
            if rows[1] == 'Ch2':
                if rows[2] == 'QMax95':
                    gen4_qmax95_ch2 = rows[3]
                    gen4_datetime_ch2 = rows[4]
                if rows[2] == 'Nw':
                    gen4_nw_ch2 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen4_sync_ch2 = rows[3]
            if rows[1] == 'Ch3':
                if rows[2] == 'QMax95':
                    gen4_qmax95_ch3 = rows[3]
                    gen4_datetime_ch3 = rows[4]
                if rows[2] == 'Nw':
                    gen4_nw_ch3 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen4_sync_ch3 = rows[3]

        elif rows[0] == 'GEN_5':
            if rows[1] == 'Ch1':
                if rows[2] == 'QMax95':
                    gen5_qmax95_ch1 = rows[3]
                    gen5_datetime_ch1 = rows[4]
                if rows[2] == 'Nw':
                    gen5_nw_ch1 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen5_sync_ch1 = rows[3]
            if rows[1] == 'Ch2':
                if rows[2] == 'QMax95':
                    gen5_qmax95_ch2 = rows[3]
                    gen5_datetime_ch2 = rows[4]
                if rows[2] == 'Nw':
                    gen5_nw_ch2 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen5_sync_ch2 = rows[3]
            if rows[1] == 'Ch3':
                if rows[2] == 'QMax95':
                    gen5_qmax95_ch3 = rows[3]
                    gen5_datetime_ch3 = rows[4]
                if rows[2] == 'Nw':
                    gen5_nw_ch3 = rows[3]
                if rows[2] == 'Sync Frequency':
                    gen5_sync_ch3 = rows[3]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen1_datetime_ch1_dt = datetime.strptime(gen1_datetime_ch1, "%Y-%m-%dT%H:%M:%S.%fZ")

    gen1_date_ch1 = gen1_datetime_ch1_dt.strftime('%d/%m/%Y')
    gen1_datetime_ch1 = gen1_datetime_ch1_dt.strftime('%d/%m/%Y %H:%M')
    gen1_ch1 = [gen1_date_ch1, asset_id_list[0],subcomponet_id,diagnostic_test_id,'u',round(gen1_qmax95_ch1*1000,2), round(gen1_nw_ch1,2), round(gen1_sync_ch1), Monitoring, monitoring_type, connection_type, gen1_datetime_ch1]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen1_datetime_ch2_dt = datetime.strptime(gen1_datetime_ch2, "%Y-%m-%dT%H:%M:%S.%fZ")

    gen1_date_ch2 = gen1_datetime_ch2_dt.strftime('%d/%m/%Y')
    gen1_datetime_ch2 = gen1_datetime_ch2_dt.strftime('%d/%m/%Y %H:%M')
    gen1_ch2 = [gen1_date_ch2, asset_id_list[0], subcomponet_id, diagnostic_test_id, 'v',
                round(gen1_qmax95_ch2 * 1000, 2), round(gen1_nw_ch2, 2), round(gen1_sync_ch2), Monitoring,
                monitoring_type, connection_type, gen1_datetime_ch2]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen1_datetime_ch3_dt = datetime.strptime(gen1_datetime_ch3, "%Y-%m-%dT%H:%M:%S.%fZ")

    gen1_date_ch3 = gen1_datetime_ch3_dt.strftime('%d/%m/%Y')
    gen1_datetime_ch3 = gen1_datetime_ch3_dt.strftime('%d/%m/%Y %H:%M')
    gen1_ch3 = [gen1_date_ch3, asset_id_list[0], subcomponet_id, diagnostic_test_id, 'w',
                round(gen1_qmax95_ch3 * 1000, 2), round(gen1_nw_ch3, 2), round(gen1_sync_ch3), Monitoring,
                monitoring_type, connection_type, gen1_datetime_ch3]

    # Gen 2
    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen2_datetime_ch1_dt = datetime.strptime(gen2_datetime_ch1, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen2_date_ch1 = gen2_datetime_ch1_dt.strftime('%d/%m/%Y')
    gen2_datetime_ch1 = gen2_datetime_ch1_dt.strftime('%d/%m/%Y %H:%M')
    gen2_ch1 = [gen2_date_ch1, asset_id_list[1], subcomponet_id, diagnostic_test_id, 'u',
                round(gen2_qmax95_ch1 * 1000, 2), round(gen2_nw_ch1, 2), round(gen2_sync_ch1), Monitoring,
                monitoring_type, connection_type, gen2_datetime_ch1]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen2_datetime_ch2_dt = datetime.strptime(gen2_datetime_ch2, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen2_date_ch2 = gen2_datetime_ch2_dt.strftime('%d/%m/%Y')
    gen2_datetime_ch2 = gen2_datetime_ch2_dt.strftime('%d/%m/%Y %H:%M')
    gen2_ch2 = [gen2_date_ch2, asset_id_list[1], subcomponet_id, diagnostic_test_id, 'v',
                round(gen2_qmax95_ch2 * 1000, 2), round(gen2_nw_ch2, 2), round(gen2_sync_ch2), Monitoring,
                monitoring_type, connection_type, gen2_datetime_ch2]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen2_datetime_ch3_dt = datetime.strptime(gen2_datetime_ch3, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen2_date_ch3 = gen2_datetime_ch3_dt.strftime('%d/%m/%Y')
    gen2_datetime_ch3 = gen2_datetime_ch3_dt.strftime('%d/%m/%Y %H:%M')
    gen2_ch3 = [gen2_date_ch3, asset_id_list[1], subcomponet_id, diagnostic_test_id, 'w',
                round(gen2_qmax95_ch3 * 1000, 2), round(gen2_nw_ch3, 2), round(gen2_sync_ch3), Monitoring,
                monitoring_type, connection_type, gen2_datetime_ch3]

    # Gen 3
    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen3_datetime_ch1_dt = datetime.strptime(gen3_datetime_ch1, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen3_date_ch1 = gen3_datetime_ch1_dt.strftime('%d/%m/%Y')
    gen3_datetime_ch1 = gen3_datetime_ch1_dt.strftime('%d/%m/%Y %H:%M')
    gen3_ch1 = [gen3_date_ch1, asset_id_list[2], subcomponet_id, diagnostic_test_id, 'u',
                round(gen3_qmax95_ch1 * 1000, 2), round(gen3_nw_ch1, 2), round(gen3_sync_ch1), Monitoring,
                monitoring_type, connection_type, gen3_datetime_ch1]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen3_datetime_ch2_dt = datetime.strptime(gen3_datetime_ch2, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen3_date_ch2 = gen3_datetime_ch2_dt.strftime('%d/%m/%Y')
    gen3_datetime_ch2 = gen3_datetime_ch2_dt.strftime('%d/%m/%Y %H:%M')
    gen3_ch2 = [gen3_date_ch2, asset_id_list[2], subcomponet_id, diagnostic_test_id, 'v',
                round(gen3_qmax95_ch2 * 1000, 2), round(gen3_nw_ch2, 2), round(gen3_sync_ch2), Monitoring,
                monitoring_type, connection_type, gen3_datetime_ch2]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen3_datetime_ch3_dt = datetime.strptime(gen3_datetime_ch3, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen3_date_ch3 = gen3_datetime_ch3_dt.strftime('%d/%m/%Y')
    gen3_datetime_ch3 = gen3_datetime_ch3_dt.strftime('%d/%m/%Y %H:%M')
    gen3_ch3 = [gen3_date_ch3, asset_id_list[2], subcomponet_id, diagnostic_test_id, 'w',
                round(gen3_qmax95_ch3 * 1000, 2), round(gen3_nw_ch3, 2), round(gen3_sync_ch3), Monitoring,
                monitoring_type, connection_type, gen3_datetime_ch3]

    # Gen 4
    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen4_datetime_ch1_dt = datetime.strptime(gen4_datetime_ch1, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen4_date_ch1 = gen4_datetime_ch1_dt.strftime('%d/%m/%Y')
    gen4_datetime_ch1 = gen4_datetime_ch1_dt.strftime('%d/%m/%Y %H:%M')
    gen4_ch1 = [gen4_date_ch1, asset_id_list[3], subcomponet_id, diagnostic_test_id, 'u',
                round(gen4_qmax95_ch1 * 1000, 2), round(gen4_nw_ch1, 2), round(gen4_sync_ch1), Monitoring,
                monitoring_type, connection_type, gen4_datetime_ch1]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen4_datetime_ch2_dt = datetime.strptime(gen4_datetime_ch2, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen4_date_ch2 = gen4_datetime_ch2_dt.strftime('%d/%m/%Y')
    gen4_datetime_ch2 = gen4_datetime_ch2_dt.strftime('%d/%m/%Y %H:%M')
    gen4_ch2 = [gen4_date_ch2, asset_id_list[3], subcomponet_id, diagnostic_test_id, 'v',
                round(gen4_qmax95_ch2 * 1000, 2), round(gen4_nw_ch2, 2), round(gen4_sync_ch2), Monitoring,
                monitoring_type, connection_type, gen4_datetime_ch2]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen4_datetime_ch3_dt = datetime.strptime(gen4_datetime_ch3, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen4_date_ch3 = gen4_datetime_ch3_dt.strftime('%d/%m/%Y')
    gen4_datetime_ch3 = gen4_datetime_ch3_dt.strftime('%d/%m/%Y %H:%M')
    gen4_ch3 = [gen4_date_ch3, asset_id_list[3], subcomponet_id, diagnostic_test_id, 'w',
                round(gen4_qmax95_ch3 * 1000, 2), round(gen4_nw_ch3, 2), round(gen4_sync_ch3), Monitoring,
                monitoring_type, connection_type, gen4_datetime_ch3]

    # Gen 5
    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen5_datetime_ch1_dt = datetime.strptime(gen5_datetime_ch1, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen5_date_ch1 = gen5_datetime_ch1_dt.strftime('%d/%m/%Y')
    gen5_datetime_ch1 = gen5_datetime_ch1_dt.strftime('%d/%m/%Y %H:%M')
    gen5_ch1 = [gen5_date_ch1, asset_id_list[4], subcomponet_id, diagnostic_test_id, 'u',
                round(gen5_qmax95_ch1 * 1000, 2), round(gen5_nw_ch1, 2), round(gen5_sync_ch1), Monitoring,
                monitoring_type, connection_type, gen5_datetime_ch1]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen5_datetime_ch2_dt = datetime.strptime(gen5_datetime_ch2, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen5_date_ch2 = gen5_datetime_ch2_dt.strftime('%d/%m/%Y')
    gen5_datetime_ch2 = gen5_datetime_ch2_dt.strftime('%d/%m/%Y %H:%M')
    gen5_ch2 = [gen5_date_ch2, asset_id_list[4], subcomponet_id, diagnostic_test_id, 'v',
                round(gen5_qmax95_ch2 * 1000, 2), round(gen5_nw_ch2, 2), round(gen5_sync_ch2), Monitoring,
                monitoring_type, connection_type, gen5_datetime_ch2]

    # Convert string to datetime object (Note: we remove the milliseconds and 'Z' part)
    gen5_datetime_ch3_dt = datetime.strptime(gen5_datetime_ch3, "%Y-%m-%dT%H:%M:%S.%fZ")
    gen5_date_ch3 = gen5_datetime_ch3_dt.strftime('%d/%m/%Y')
    gen5_datetime_ch3 = gen5_datetime_ch3_dt.strftime('%d/%m/%Y %H:%M')
    gen5_ch3 = [gen5_date_ch3, asset_id_list[4], subcomponet_id, diagnostic_test_id, 'w',
                round(gen5_qmax95_ch3 * 1000, 2), round(gen5_nw_ch3, 2), round(gen5_sync_ch3), Monitoring,
                monitoring_type, connection_type, gen5_datetime_ch3]

    # chekc if the data is the same
    # print(len(temp_list_gen1))
    data_already_inserted = False
    if len(temp_list_gen1)!=0:
        if temp_list_gen1[0] == gen1_ch1:
            print('data already inserted')
            data_already_inserted = True
        elif temp_list_gen1[0] != gen1_ch1:
            data_already_inserted = False

    if len(temp_list_gen1)!=0:
        #chekc if the data is the same
        if temp_list_gen1[0] == gen1_ch1:
            print('data already inserted')
            # data_already_inserted = True
        if temp_list_gen1[0] != gen1_ch1:
            temp_list_gen1.clear()
            temp_list_gen1.append(gen1_ch1)
            temp_list_gen1.append(gen1_ch2)
            temp_list_gen1.append(gen1_ch3)
            # data_already_inserted = False

    if len(temp_list_gen1) ==0:
        temp_list_gen1.append(gen1_ch1)
        temp_list_gen1.append(gen1_ch2)
        temp_list_gen1.append(gen1_ch3)

    if len(temp_list_gen2) != 0:
        # chekc if the data is the same
        if temp_list_gen2[0] == gen2_ch1:
            print('data already inserted')

            # data_already_inserted = True

        if temp_list_gen2[0] != gen2_ch1:
            temp_list_gen2.clear()
            temp_list_gen2.append(gen2_ch1)
            temp_list_gen2.append(gen2_ch2)
            temp_list_gen2.append(gen2_ch3)

            # data_already_inserted = False

    if len(temp_list_gen2) ==0:
        # Append Gen 2
        temp_list_gen2.append(gen2_ch1)
        temp_list_gen2.append(gen2_ch2)
        temp_list_gen2.append(gen2_ch3)

    if len(temp_list_gen3) != 0:
        # chekc if the data is the same
        if temp_list_gen3[0] == gen3_ch1:
            print('data already inserted')
            # data_already_inserted = True


        if temp_list_gen3[0] != gen3_ch1:
            temp_list_gen3.clear()
            temp_list_gen3.append(gen3_ch1)
            temp_list_gen3.append(gen3_ch2)
            temp_list_gen3.append(gen3_ch3)

            # data_already_inserted = False

    if len(temp_list_gen3) ==0:
        # Append Gen 3
        temp_list_gen3.append(gen3_ch1)
        temp_list_gen3.append(gen3_ch2)
        temp_list_gen3.append(gen3_ch3)

    if len(temp_list_gen4) != 0:
        # chekc if the data is the same
        if temp_list_gen4[0] == gen4_ch1:
            print('data already inserted')
            # data_already_inserted = True

        if temp_list_gen4[0] != gen4_ch1:
            temp_list_gen4.clear()
            temp_list_gen4.append(gen4_ch1)
            temp_list_gen4.append(gen4_ch2)
            temp_list_gen4.append(gen4_ch3)
            # data_already_inserted = False

    if len(temp_list_gen4) ==0:
        # Append Gen 4
        temp_list_gen4.append(gen4_ch1)
        temp_list_gen4.append(gen4_ch2)
        temp_list_gen4.append(gen4_ch3)

    if len(temp_list_gen5) != 0:
        # chekc if the data is the same
        if temp_list_gen5[0] == gen5_ch1:
            print('data already inserted gen5')
            # data_already_inserted = True


        if temp_list_gen5[0] != gen5_ch1:
            temp_list_gen5.clear()
            temp_list_gen5.append(gen5_ch1)
            temp_list_gen5.append(gen5_ch2)
            temp_list_gen5.append(gen5_ch3)

            # data_already_inserted = False
    if len(temp_list_gen5)==0:
        # Append Gen 5
        temp_list_gen5.append(gen5_ch1)
        temp_list_gen5.append(gen5_ch2)
        temp_list_gen5.append(gen5_ch3)


    # print(temp_list_gen1)
    # print(temp_list_gen2)
    # print(temp_list_gen3)
    # print(temp_list_gen4)
    # print(temp_list_gen5)
    # print(fuck)
    # print(data_already_inserted)
    if data_already_inserted is False:
        # insert data into the db and perform analysis and assessment
        upload_to_db(temp_list_gen1)
        analyse_the_data(asset_id_list[0])
        assess_condition_data(asset_id_list[0])
        upload_to_db(temp_list_gen2)
        analyse_the_data(asset_id_list[1])
        assess_condition_data(asset_id_list[1])
        upload_to_db(temp_list_gen3)
        analyse_the_data(asset_id_list[2])
        assess_condition_data(asset_id_list[2])
        upload_to_db(temp_list_gen4)
        analyse_the_data(asset_id_list[3])
        assess_condition_data(asset_id_list[3])
        upload_to_db(temp_list_gen5)
        analyse_the_data(asset_id_list[4])
        assess_condition(asset_id_list[4])


    if data_already_inserted is True:
        None



# # Schedule the script to run every hour
# schedule.every(1).hours.do(main)

while True:
    main()
    time.sleep(14400)  # Sleep for 1 hour before running again

