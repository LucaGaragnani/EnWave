import mysql.connector
import pandas as pd
import os
from cryptography.fernet import Fernet
import base64
from datetime import datetime
import numpy as np

from sendgrid.helpers.endpoints.ip.unassigned import format_ret

# from connectors.db_connectors import get_asset_details
# from services.Online_PD_monitoring_integration import diagnostic_test_id

""" db connector to handle all the queries and return data 
"""




def get_user(email):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch user details based on the provided email
        cursor.execute("""SELECT * FROM user WHERE email = %s""", (email,))
        user_result = cursor.fetchone()

        # Commit the transaction (not necessary for SELECT, but keeping it as a safety)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        user_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return user_result

def get_session_user_details():
    
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch user details based on the provided email
        cursor.execute("""SELECT user_id, datetime FROM session_data ORDER BY id DESC LIMIT 1""")
        user_id_result = cursor.fetchone()

        # Commit the transaction (not necessary for SELECT, but keeping it as a safety)
        
        #Get user name and log in time
        cursor.execute("""SELECT role, user_name, user_surname FROM user WHERE id = %s""",(user_id_result[0],))
        user_details = cursor.fetchone()
        
        user_details_dict= {}
        user_details_dict['name'] = user_details[1]
        user_details_dict['surname'] = user_details[2]
        user_details_dict['role'] = user_details[0]
        user_details_dict['last_connection_time'] = user_id_result[1]
        
        
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        user_details_dict = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return user_details_dict


def get_connection_status():
    
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch user details based on the provided email
        cursor.execute("""SELECT status FROM connection_status ORDER BY id DESC LIMIT 1""")
        status_result = cursor.fetchone()

        
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        status_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return status_result






def update_connection_status(status):
    # Connect to SQLite database (or create it if it doesn't exist)


    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Prepare the update SQL query
        update_sql = '''
                            UPDATE connection_status
                            SET status = %s
                            WHERE id = %s;
                        '''
        cursor.execute(update_sql, (status, 1))

        # Commit the transaction
        conn.commit()
        
#         print('status updated')

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()


def reset_password(hashed_password, email, user_id):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:

        # Execute the query to update user password based on the provided email and user ID
        cursor.execute("UPDATE user SET password = %s WHERE email = %s AND id = %s",
                       (hashed_password, email, user_id))

        # Commit the transaction to save the changes
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return 'Password Update Successfully!'

def get_customer_site(customer_id):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch sites based on the provided customer_id
        cursor.execute("""SELECT * FROM site WHERE customer_id = %s""", (customer_id,))
        site_result = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but keeping it for consistency)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        site_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return site_result

def get_customer_site_from_user_id():
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch sites based on the provided customer_id
        cursor.execute("SELECT * FROM site where customer_id = (SELECT company_id FROM user where id=(SELECT user_id FROM session_data order by id desc limit 1))")
        site_result = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but keeping it for consistency)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        site_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return site_result

def get_site_coordinate(site_name):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch assets based on the provided site_id
        cursor.execute("SELECT lat,lon FROM site WHERE site_name = %s", (site_name,))
        site_coordinates_result = cursor.fetchall()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        site_coordinates_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return site_coordinates_result

def get_site_asset_layout(site_name):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch assets based on the provided site_id
        cursor.execute("SELECT * FROM asset_site_layout where site_id =(SELECT id FROM site WHERE site_name = %s)", (site_name,))
        site_layout_result = cursor.fetchall()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        site_layout_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return site_layout_result

def get_site_asset_layout_individual_cable(cable_asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch assets based on the provided site_id
        cursor.execute("SELECT * FROM asset_site_layout where cable_asset_id =%s", (cable_asset_id,))
        cable_layout_result = cursor.fetchall()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cable_layout_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return cable_layout_result

def get_asset_sw_layout_individual_sw(sw_asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch assets based on the provided site_id
        cursor.execute("SELECT * FROM asset_sw_layout where asset_id =%s", (sw_asset_id,))
        sw_layout_result = cursor.fetchall()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sw_layout_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return sw_layout_result

def get_panel_id_sw_layout_individual_panel(sw_asset_id, bus_label, panel_label):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch assets based on the provided site_id
        cursor.execute("SELECT id FROM asset_sw_layout where asset_id =%s and bus_number=%s and panel_number =%s", (sw_asset_id,bus_label, panel_label,))
        sw_panel_id_result = cursor.fetchone()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sw_panel_id_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return sw_panel_id_result


def get_single_asset_coordinate(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch assets based on the provided site_id
        cursor.execute("SELECT lat,lon FROM asset WHERE id = %s", (asset_id,))
        asset_coordinates_result = cursor.fetchall()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_coordinates_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_coordinates_result

# print(get_site_asset_layout('Port Augusta Renewable Park'))
def get_asset_list(site_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch assets based on the provided site_id
        cursor.execute("SELECT * FROM asset WHERE site_id = %s", (site_id,))
        asset_result = cursor.fetchall()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_result = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_result

def get_single_asset_characteristics(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch assets based on the provided site_id
        cursor.execute("""SELECT * FROM asset WHERE id = %s""", (asset_id,))
        asset_characteristics = cursor.fetchall()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_characteristics = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_characteristics

def get_single_asset_tag(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch assets based on the provided site_id
        cursor.execute("""SELECT tag FROM asset WHERE id = %s""", (asset_id,))
        asset_tag = cursor.fetchone()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_tag = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_tag

def get_asset_details(asset_id):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch asset details based on the provided asset_id
        cursor.execute("""SELECT * FROM asset_details WHERE asset_id = %s""", (asset_id,))
        asset_details_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_details_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_details_list


def get_transmission_line_accessories_details(asset_id):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch asset details based on the provided asset_id
        cursor.execute("""SELECT * FROM transmission_line_details WHERE asset_id = %s""", (asset_id,))
        transmission_line_details_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        transmission_line_details_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return transmission_line_details_list


def get_latest_asset_criticality_class(asset_id):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch asset details based on the provided asset_id
        cursor.execute("""SELECT criticality_class FROM asset_details WHERE asset_id = %s ORDER BY ID DESC LIMIT 1""", (asset_id,))
        asset_criticality_class = cursor.fetchone()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_criticality_class = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_criticality_class


def get_asset_analysis(asset_id):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch asset analysis based on the provided asset_id
        cursor.execute("""SELECT * FROM asset_analysis WHERE asset_id = %s""", (asset_id,))
        asset_analysis_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_analysis_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()


    return asset_analysis_list

def get_maintenance_action(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch asset maintenance actions based on the provided asset_id
        cursor.execute("""
                SELECT ama.*, cc.tag
                FROM asset AS cc
                JOIN asset_analysis AS aa ON cc.id = aa.asset_id
                JOIN asset_maintenance_actions AS ama ON aa.id = ama.asset_analysis_id
                WHERE aa.asset_id = %s
            """, (asset_id,))

        asset_maintenance_actions_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_maintenance_actions_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_maintenance_actions_list

def get_individual_test_maintenance_action_from_list(diagnostic_test_id,score):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch asset maintenance actions based on the provided asset_id
        cursor.execute("""
                SELECT *
                FROM maintenance_action_list
                WHERE diagnostic_test_id = %s
                AND score = %s
            """, (diagnostic_test_id,score,))

        diagnostic_test_maintenance_actions_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        diagnostic_test_maintenance_actions_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return diagnostic_test_maintenance_actions_list

def get_letest_asset_analysis(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch the latest asset analysis based on asset_id
        cursor.execute("""SELECT * FROM asset_analysis WHERE asset_id = %s ORDER BY ID DESC LIMIT 1""", (asset_id,))
        latest_asset_analysis_list = cursor.fetchone()

        # Commit the transaction (not required for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        latest_asset_analysis_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return latest_asset_analysis_list

def get_component_analysis(analysis_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch component analysis based on analysis_id
        cursor.execute("""SELECT * FROM component_analysis WHERE analysis_id = %s""", (analysis_id,))
        component_analysis_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        component_analysis_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return component_analysis_list

def get_subcomponent_analysis(analysis_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch subcomponent analysis based on analysis_id
        cursor.execute("""SELECT * FROM subcomponent_analysis WHERE analysis_id = %s""", (analysis_id,))
        subcomponent_analysis_list = cursor.fetchall()

        # Commit the transaction (not required for SELECT queries, but it's good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        subcomponent_analysis_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return subcomponent_analysis_list

def get_subcomponent_details(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch asset subcomponent details based on asset_id
        cursor.execute("""SELECT asset_subcomponent_id, age_factor, maintenance_factor, failure_factor FROM asset_subcomponent_details WHERE asset_id = %s""", (asset_id,))
        asset_subcomponent_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_subcomponent_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_subcomponent_list

def get_failure_mechanisms_analysis(analysis_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch failure mechanism analysis based on analysis_id
        cursor.execute("""SELECT * FROM failure_mechanisms_analysis WHERE analysis_id = %s""", (analysis_id,))
        failure_mechanism_analysis_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        failure_mechanism_analysis_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return failure_mechanism_analysis_list

key = b'P__s6c4fKKKmBfxRz0TVzpyVUuKnDKwYvcFb908jD1Y='
cipher = Fernet(key)

# Function to decrypt a single value
def decrypt_value(encrypted_text: str) -> str:
    decrypted = cipher.decrypt(encrypted_text.encode())
    return decrypted.decode()  # Decode to convert back to string

def get_fmdi_weight(fm_id_list):

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()


    try:

        fmdi_list = []
        for ids in fm_id_list:

            # Execute the query to fetch failure mechanism analysis based on analysis_id
            cursor.execute("""SELECT * FROM fmdi_factors where failure_mechanism_id=%s""", (ids,))
            fmdi_item = cursor.fetchall()

            fmdi_list.append(fmdi_item)

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()


        fmdi_list_complete = []
        for row in fmdi_list:
            for value in row:
                fmdi_list_complete.append(value)



        #decrypt the data
        fmdi_list_decrypted = []
        for row in fmdi_list_complete:
            line = []
            for item in row:

                if isinstance(item, str):
                    decrypted_value = decrypt_value(item)
                    line.append(decrypted_value)
                else:
                    line.append(item)
            fmdi_list_decrypted.append(line)




    except mysql.connector.Error as err:
        print(f"Error: {err}")
        fmdi_list_decrypted = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return fmdi_list_decrypted

def get_scfm_weight(sub_id_list):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        scfm_list = []
        for ids in sub_id_list:
            # Execute the query to fetch failure mechanism analysis based on analysis_id
            cursor.execute("""SELECT * FROM scfm_factors where subcomponent_id=%s""", (ids,))
            scfm_item = cursor.fetchall()

            scfm_list.append(scfm_item)

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

        scfm_list_complete = []
        for row in scfm_list:
            for value in row:
                scfm_list_complete.append(value)

        # decrypt the data
        scfm_list_decrypted = []
        for row in scfm_list_complete:
            line = []
            for item in row:

                if isinstance(item, str):
                    decrypted_value = decrypt_value(item)
                    line.append(decrypted_value)
                else:
                    line.append(item)
            scfm_list_decrypted.append(line)


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        scfm_list_decrypted = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return scfm_list_decrypted

def get_schi_weight(sub_id_list):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        schi_list = []
        for ids in sub_id_list:
            # Execute the query to fetch failure mechanism analysis based on analysis_id
            cursor.execute("SELECT * FROM schi_factors where subcomponent_id=%s", (ids,))
            schi_item = cursor.fetchall()

            schi_list.append(schi_item)

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

        schi_list_complete = []
        for row in schi_list:
            for value in row:
                schi_list_complete.append(value)

        # decrypt the data
        schi_list_decrypted = []
        for row in schi_list_complete:
            line = []
            for item in row:
                if isinstance(item, str):
                    #check if it is number of string
                    try:
                        decrypted_value =float(item)


                    except ValueError:
                        decrypted_value = decrypt_value(item)

                    line.append(decrypted_value)
                else:
                    line.append(item)
            schi_list_decrypted.append(line)


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        schi_list_decrypted = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return schi_list_decrypted

def get_cmsc_weight(com_id_list):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        cmsc_list = []
        for ids in com_id_list:
            # Execute the query to fetch
            cursor.execute("SELECT * FROM cmsc_factors where component_id=%s", (ids,))
            cmsc_item = cursor.fetchall()

            cmsc_list.append(cmsc_item)

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

        cmsc_list_complete = []
        for row in cmsc_list:
            for value in row:
                cmsc_list_complete.append(value)

        # decrypt the data
        cmsc_list_decrypted = []
        for row in cmsc_list_complete:
            line = []
            for item in row:
                if isinstance(item, str):
                    #check if it is number of string
                    try:
                        decrypted_value =float(item)


                    except ValueError:
                        decrypted_value = decrypt_value(item)

                    line.append(decrypted_value)
                else:
                    line.append(item)
            cmsc_list_decrypted.append(line)


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cmsc_list_decrypted = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return cmsc_list_decrypted


def get_ascm_weight(com_id_list):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        ascm_list = []
        for ids in com_id_list:
            # Execute the query to fetch
            cursor.execute("SELECT * FROM ascm_factors where component_id=%s", (ids,))
            ascm_item = cursor.fetchall()

            ascm_list.append(ascm_item)

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

        ascm_list_complete = []
        for row in ascm_list:
            for value in row:
                ascm_list_complete.append(value)

        # decrypt the data
        ascm_list_decrypted = []
        for row in ascm_list_complete:
            line = []
            for item in row:
                if isinstance(item, str):
                    #check if it is number of string
                    try:
                        decrypted_value =float(item)


                    except ValueError:
                        decrypted_value = decrypt_value(item)

                    line.append(decrypted_value)
                else:
                    line.append(item)
            ascm_list_decrypted.append(line)


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        ascm_list_decrypted = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return ascm_list_decrypted



def get_criticality_list():
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the criticality_list
        cursor.execute("""SELECT * FROM criticality_list""")
        criticality_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        criticality_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return criticality_list

def get_asset_category_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the asset_category table
        cursor.execute("""SELECT * FROM asset_category""")
        asset_category_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_category_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_category_list

def get_subcomponent_list():
    # Connect to SQLite database (or create it if it doesn't exist)
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the asset_subcomponent table
        cursor.execute("""SELECT * FROM asset_subcomponent""")
        asset_subcomponent_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_subcomponent_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_subcomponent_list

def get_subcomponent_single_asset_list(comp_id_list):
    # Connect to SQLite database (or create it if it doesn't exist)
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        asset_subcomponent_list = []
        asset_subcomponent_list_cleaned = []
        for com in comp_id_list:
            # Execute the query to fetch all entries from the asset_subcomponent table
            cursor.execute("SELECT * FROM asset_subcomponent where asset_component_id=%s", (com,))
            asset_sub_ind_list = cursor.fetchall()

            asset_subcomponent_list.append(asset_sub_ind_list)

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

        for item in asset_subcomponent_list:
            for value in item:
                asset_subcomponent_list_cleaned.append(value)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_subcomponent_list_cleaned = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_subcomponent_list_cleaned


def get_component_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the asset_component table
        cursor.execute("""SELECT * FROM asset_component""")
        asset_component_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_component_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_component_list

def get_component_single_asset_list(asset_category_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the asset_component table
        cursor.execute("SELECT * FROM asset_component where asset_category_id=%s", (asset_category_id,))
        asset_component_single_asset_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()
# pas
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        asset_component_single_asset_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return asset_component_single_asset_list


def get_failure_mechanism_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the failure_mechanisms table
        cursor.execute("""SELECT * FROM failure_mechanisms""")
        failure_mechanism_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        failure_mechanism_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return failure_mechanism_list

def get_failure_mechanism_single_asset_list(asset_category_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the failure_mechanisms table
        cursor.execute("""SELECT * FROM failure_mechanisms WHERE asset_category_id = %s""",(asset_category_id,))
        failure_mechanism_list_single_asset = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        failure_mechanism_list_single_asset = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return failure_mechanism_list_single_asset

def get_failure_mechanism_subcomponent(component_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()


    try:
        # Execute the query to fetch all entries from the failure_mechanisms table
        cursor.execute("""SELECT failure_mechanism_id FROM failure_mechanisms_subcomponent_table where asset_subcomponent_id in (SELECT id FROM asset_subcomponent where asset_component_id=%s)""", (component_id,))
        failure_mechanism_component_list = cursor.fetchall()

        failure_mechanism_component_list_cleaned = [item[0] for item in failure_mechanism_component_list]
        unique_sorted_numbers = sorted(set(failure_mechanism_component_list_cleaned))

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        unique_sorted_numbers  = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return  unique_sorted_numbers




def get_diagnostic_test_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the diagnostic_test table
        cursor.execute("""SELECT * FROM diagnostic_test""")
        diagnostic_test_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        diagnostic_test_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return diagnostic_test_list

def get_diagnostic_test_single_asset_list(asset_category_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the diagnostic_test table
        cursor.execute("""SELECT * FROM diagnostic_test WHERE asset_category_id = %s""", (asset_category_id,))
        diagnostic_test_list_single_asset = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        diagnostic_test_list_single_asset = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return diagnostic_test_list_single_asset


##########################################     DATA - ONLine

def get_online_test_data_to_be_analysis(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all entries from the online_test_data table where analysis is NULL
        cursor.execute("""SELECT * FROM online_test_data WHERE analysis IS NULL""")
        online_PD_test_data_to_be_analyzed = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        online_PD_test_data_to_be_analyzed = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return online_PD_test_data_to_be_analyzed


def get_online_test_analysis_data(asset_id, subcomponent_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from online_test_data
        cursor.execute("""
                SELECT `date`, `diagnostic_test_id`, `analysis`,feature_16, feature_19 
                FROM online_test_data 
                WHERE asset_id = %s AND subcomponent_id = %s
            """, (asset_id, subcomponent_id))

        online_test_data_list = cursor.fetchall()

        online_test_data_list_completed = []
        for item in online_test_data_list:
            date = item[0]
            diagnostic_test_id = item[1]
            analysis = item[2]
            monitoring = item[3]
            datetime = item[4]

            if monitoring == 'Yes':
                date = datetime

            list=[date, diagnostic_test_id, analysis]
            tuple_list = tuple(list)

            online_test_data_list_completed.append(tuple_list)

        # print(online_test_data_list_completed)
        online_test_data_list = tuple(online_test_data_list_completed)
        # print(online_test_data_list)
        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        online_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return online_test_data_list

def get_offline_test_analysis_data(asset_id, subcomponent_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from offline_test_data
        cursor.execute("""
                SELECT `date`, `diagnostic_test_id`, `analysis` 
                FROM offline_test_data 
                WHERE asset_id = %s AND subcomponent_id = %s
            """, (asset_id, subcomponent_id))

        offline_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        offline_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return offline_test_data_list


def get_online_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch the first 50 rows from online_test_data where asset_id matches
        cursor.execute("""
                SELECT * 
                FROM online_test_data 
                WHERE asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        online_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        online_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return online_test_data_list

def get_online_test_analysis_data_full_asset(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from online_test_data
        cursor.execute("""
                SELECT `date`, `diagnostic_test_id`, `analysis` 
                FROM online_test_data 
                WHERE asset_id = %s
            """, (asset_id,))

        online_test_data_analysis_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        online_test_data_analysis_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return online_test_data_analysis_list
def get_offline_test_analysis_data_full_asset(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from offline_test_data
        cursor.execute("""
                SELECT `date`, `diagnostic_test_id`, `analysis` 
                FROM offline_test_data 
                WHERE asset_id = %s 
            """, (asset_id,))

        offline_test_data_analysis_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        offline_test_data_analysis_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return offline_test_data_analysis_list

#cable
def get_offline_latest_JT_value_for_summary_table(asset_id, number_of_cores_phases):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from online_test_data
        cursor.execute("""
                SELECT `date`, `feature_1`, `feature_2`,  `feature_4`
                FROM offline_test_data 
                WHERE asset_id = %s and diagnostic_test_id = %s ORDER BY id DESC 
                LIMIT %s
            """, (asset_id,14, number_of_cores_phases))

        latest_ir_results = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        latest_ir_results = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return latest_ir_results
def get_offline_latest_IR_value_for_summary_table(asset_id, number_of_cores_phases):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from online_test_data
        cursor.execute("""
                SELECT `date`, `feature_1`, `feature_2`,  `feature_5`
                FROM offline_test_data 
                WHERE asset_id = %s and diagnostic_test_id = %s ORDER BY id DESC 
                LIMIT %s
            """, (asset_id,15, number_of_cores_phases))

        latest_ir_results = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        latest_ir_results = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return latest_ir_results
def get_offline_latest_PI_value_for_summary_table(asset_id, number_of_cores_phases):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from online_test_data
        cursor.execute("""
                SELECT `date`, `feature_1`, `feature_2`,  `feature_9`
                FROM offline_test_data 
                WHERE asset_id = %s and diagnostic_test_id = %s ORDER BY id DESC 
                LIMIT %s
            """, (asset_id,16, number_of_cores_phases))

        latest_ir_results = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        latest_ir_results = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return latest_ir_results
def get_offline_latest_TD_value_for_summary_table(asset_id, number_of_cores_phases):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from online_test_data
        cursor.execute("""
                SELECT `date`, `feature_1`, `feature_2`,  `feature_9`
                FROM offline_test_data 
                WHERE asset_id = %s and diagnostic_test_id = %s ORDER BY id DESC 
                LIMIT %s
            """, (asset_id,17, number_of_cores_phases))

        latest_ir_results = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        latest_ir_results = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return latest_ir_results

def get_online_pd_test_data_cable(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT * 
                FROM online_test_data 
                WHERE diagnostic_test_id = 20 AND feature_3=1 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        online_PD_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        online_PD_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return online_PD_test_data_list
def get_online_pd_patter_cable(pdpattern_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT feature_25
                FROM online_test_data
                WHERE id = %s

            """, (pdpattern_id,))

        pdpattern = cursor.fetchone()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        pdpattern = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return pdpattern
def insert_online_pd_data(data):
    # Connect to SQLite database (or create it if it doesn't exist)
    # print(data)
    # File path for the pdpattern
    image_path = 'services/temp/PDPattern_0.png'

    # Open the image file in binary mode and read its contents
    with open(image_path, 'rb') as img_file:
        image_data = img_file.read()

    # Assuming 'data' is your list containing all the features and other fields
    # Add the image data as the last element in the list
    data.append(image_data)
    # print(len(data))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Prepare the update SQL query
        update_sql = '''
                               INSERT INTO online_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11, feature_12, feature_20, feature_21, feature_22, feature_23, feature_24, feature_25)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                               '''
        cursor.execute(update_sql, (data))

        # Commit the transaction
        conn.commit()


    except mysql.connector.Error as err:

        print(f"Error: {err}")


    finally:

        # Close the cursor and database connection

        cursor.close()

        conn.close()



#sw
def get_offline_latest_IR_value_for_summary_table_sw(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from online_test_data
        cursor.execute("""
                SELECT `date`, `feature_1`, `feature_2`,  `feature_5`
                FROM offline_test_data 
                WHERE asset_id = %s and diagnostic_test_id = %s ORDER BY id DESC 
                LIMIT %s
            """, (asset_id,23,3))

        latest_ir_results = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        latest_ir_results = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return latest_ir_results
def get_offline_latest_PI_value_for_summary_table_sw(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch date, diagnostic_test_id, and analysis from online_test_data
        cursor.execute("""
                SELECT `date`, `feature_1`, `feature_2`,  `feature_9`
                FROM offline_test_data 
                WHERE asset_id = %s and diagnostic_test_id = %s ORDER BY id DESC 
                LIMIT %s
            """, (asset_id,24, 3))

        latest_pi_results = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        latest_pi_results = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return latest_pi_results

def get_online_pd_test_data_sw(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT * 
                FROM online_test_data 
                WHERE diagnostic_test_id = 20 AND feature_3=1 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        online_PD_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        online_PD_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return online_PD_test_data_list
def get_online_pd_patter_sw(pdpattern_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT feature_25
                FROM online_test_data
                WHERE id = %s

            """, (pdpattern_id,))

        pdpattern = cursor.fetchone()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        pdpattern = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return pdpattern
def insert_online_pd_data_sw(data):
    # Connect to SQLite database (or create it if it doesn't exist)
    # print(data)
    # File path for the pdpattern
    image_path = 'services/temp/PDPattern_0.png'

    # Open the image file in binary mode and read its contents
    with open(image_path, 'rb') as img_file:
        image_data = img_file.read()

    # Assuming 'data' is your list containing all the features and other fields
    # Add the image data as the last element in the list
    data.append(image_data)
    # print(len(data))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Prepare the update SQL query
        print(len(data))
        update_sql = '''
                               INSERT INTO online_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11, feature_20, feature_21, feature_22, feature_23, feature_24, feature_25)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                               '''
        cursor.execute(update_sql, (data))

        # Commit the transaction
        conn.commit()


    except mysql.connector.Error as err:

        print(f"Error: {err}")


    finally:

        # Close the cursor and database connection

        cursor.close()

        conn.close()




#machine

#rotor flux
def get_rfa_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT * 
                FROM online_test_data 
                WHERE diagnostic_test_id = 10 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        rfa_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        rfa_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return rfa_test_data_list

#online PD test
def get_online_pd_patter_rm(pdpattern_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT feature_25
                FROM online_test_data
                WHERE id = %s

            """, (pdpattern_id,))

        pdpattern = cursor.fetchone()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        pdpattern = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return pdpattern
def get_online_pd_patter_identification_polarity(pdpattern_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT feature_4, feature_11
                FROM online_test_data
                WHERE id = %s

            """, (pdpattern_id,))

        label = cursor.fetchone()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        label = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return label

def get_online_pd_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT * 
                FROM online_test_data 
                WHERE diagnostic_test_id = 11 AND asset_id = %s 
                ORDER BY ID DESC
                LIMIT 50
            """, (asset_id,))

        online_PD_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        online_PD_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return online_PD_test_data_list

#endwinding vibration
def get_online_ew_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT * 
                FROM online_test_data 
                WHERE diagnostic_test_id = 12 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        online_EW_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        online_EW_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return online_EW_test_data_list

#vibration analysis
def get_online_va_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from online_test_data
        cursor.execute("""
                SELECT * 
                FROM online_test_data 
                WHERE diagnostic_test_id = 13 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        online_VA_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        online_VA_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return online_VA_test_data_list


##########################################     DATA - OFFLine

def get_offline_test_data_to_be_analysis(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE analysis IS NULL
            """)

        offline_PD_test_data_to_be_analysed = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        offline_PD_test_data_to_be_analysed = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return offline_PD_test_data_to_be_analysed

def get_offline_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        offline_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        offline_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return offline_test_data_list

def get_ir_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()


    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE diagnostic_test_id = 1 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        ir_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        ir_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return ir_test_data_list

def get_pi_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE diagnostic_test_id = 2 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        pi_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        pi_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return pi_test_data_list

def get_wr_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE diagnostic_test_id = 3 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        wr_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        wr_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return wr_test_data_list

def get_ddf_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE diagnostic_test_id = 4 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        ddf_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        ddf_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return ddf_test_data_list

def get_offline_pd_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE diagnostic_test_id = 5 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        offline_pd_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        offline_pd_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return offline_pd_test_data_list

def get_inspection_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE diagnostic_test_id = 6 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        inspection_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        inspection_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return inspection_test_data_list

def get_coreflux_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE diagnostic_test_id = 7 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        coreflux_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        coreflux_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return coreflux_test_data_list

def get_elcid_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE diagnostic_test_id = 8 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        elcid_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        elcid_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return elcid_test_data_list

def get_bump_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch data from offline_test_data for the given asset_id
        cursor.execute("""
                SELECT * 
                FROM offline_test_data 
                WHERE diagnostic_test_id = 9 AND asset_id = %s 
                ORDER BY ID 
                LIMIT 50
            """, (asset_id,))

        bump_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        bump_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return bump_test_data_list

##########################################     DATA - Operational

def get_operational_test_data():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    ## Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query to fetch all records from operational_test_data
        cursor.execute("SELECT * FROM operational_test_data")
        operational_test_data_list = cursor.fetchall()

        # Commit the transaction (not necessary for SELECT, but good practice)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        operational_test_data_list = None

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    return operational_test_data_list


########################################   Custom function

def upload_session_data(user_id, datetime_str):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Current datetime in the appropriate format

        date_format = "%d-%m-%Y %H:%M:%S"  # Define the format
        converted_datetime = datetime.strptime(datetime_str, date_format)

        current_datetime = converted_datetime.now()


        # Prepare the insert SQL query
        insert_sql = '''INSERT INTO session_data (user_id, datetime) VALUES (%s, %s);'''
        cursor.execute(insert_sql, (user_id, current_datetime))

        # Commit the transaction
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()


def update_asset_criticality(criticality, asset_id, date):

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Prepare the insert SQL query

        insert_sql = '''INSERT INTO asset_details (criticality_class, date, asset_id) VALUES (%s, %s, %s);'''
        cursor.execute(insert_sql, (criticality, date, asset_id))

        # Commit the transaction
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()


def update_subcomponent_factors_details(age_factor, maintenance_factor, failure_factor, asset_subcomponent_id, asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Prepare the update SQL query
        update_sql = '''
                            UPDATE asset_subcomponent_details
                            SET age_factor = %s,
                                maintenance_factor = %s,
                                failure_factor = %s
                            WHERE asset_subcomponent_id = %s
                              AND asset_id = %s;
                        '''
        cursor.execute(update_sql, (age_factor, maintenance_factor, failure_factor, asset_subcomponent_id, asset_id))

        # Commit the transaction
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

def insert_subcomponent_factors_details(age_factor, maintenance_factor, failure_factor, asset_subcomponent_id, asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Prepare the update SQL query
        update_sql = '''
                        INSERT INTO asset_subcomponent_details (age_factor, maintenance_factor, failure_factor, asset_subcomponent_id, asset_id)
                        VALUES (%s, %s, %s, %s, %s);
                        '''
        cursor.execute(update_sql, (age_factor, maintenance_factor, failure_factor, asset_subcomponent_id, asset_id))

        # Commit the transaction
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()


#########################################    Upload data functions

def upload_test_data(data):

    #insulation resistance
    def upload_insulation_resistance_data(data):
        # remove rotor winding details used for RFA
        print('IR data')
        print(data)

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_6, feature_8, feature_9)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('IR data inserted')
    #pi
    def upload_polarization_index_data(data):
        print('PI data')
        print(data)
        # data.remove(data[4])
        # data.remove(data[-2])
        # data.remove(data[-1])
        # print(data)

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_9, feature_11, feature_12)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")


            data.remove(data[4])
            data.remove(data[-2])
            data.remove(data[-1])

            print('PI data filtered')
            print(data)

            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_9, feature_11, feature_12)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()



        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('PI data inserted')
    #WR
    def upload_winding_resistance_data(data):
        # remove rotor winding details used for RFA
        print('WR data')
        print(data)

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_5, feature_6)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

            data.remove(data[4])
            data.remove(data[-2])
            data.remove(data[-1])

            print('WR data filtered')
            print(data)

            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_5, feature_6)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('WR data inserted')
    #ddf
    def upload_ddf_data(data):
        # # remove rotor winding details used for RFA
        #
        # data.remove(data[4])
        # data.remove(data[-2])
        # data.remove(data[-1])

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data 
                                (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11, feature_23, feature_24)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('DDF data inserted')
    #OfflinePD
    def upload_offlinePD_data(data):
        # remove rotor winding details used for RFA

        # data.remove(data[4])
        # data.remove(data[-2])
        # data.remove(data[-1])

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data 
                                (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_7, feature_8, feature_25)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('OfflinePD data inserted')
    #online PD
    def upload_onlinePD_data(data):
        # remove rotor winding details used for RFA

        # data.remove(data[4])
        # data.remove(data[-2])
        # data.remove(data[-1])

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO online_test_data 
                                (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_6, feature_7, feature_8, feature_9, feature_10, feature_25)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()
        print('OnlinePD data inserted')
    #RFA
    def upload_RFA_data(data):


        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            rotor_type = data[4]
            numb_of_poles = data[-2]
            number_of_turn_per_pole = data[-1]

            # Remove the last two elements from data
            data.pop(-2)
            data.pop(-1)

            if rotor_type == 'Salient Poles':
                if int(numb_of_poles) == 4:
                    # Prepare the SQL query for 4 poles
                    insert_sql = '''INSERT INTO online_test_data 
                                        (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_23, feature_24, feature_25)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

                elif int(numb_of_poles) == 6:
                    # Prepare the SQL query for 6 poles
                    insert_sql = '''INSERT INTO online_test_data 
                                        (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_23, feature_24, feature_25)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            elif rotor_type == 'Cylindrical Rotor':
                if int(number_of_turn_per_pole) == 7:
                    # Prepare the SQL query for 7 turns per pole
                    insert_sql = '''INSERT INTO online_test_data 
                                        (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_12, feature_13, feature_14, feature_15, feature_16, feature_17, feature_18, feature_23, feature_24, feature_25)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()
        print('RFA data inserted')



    if int(data[3]) == 1:
        upload_insulation_resistance_data(data)
    if int(data[3]) == 2:
        upload_polarization_index_data(data)
    if int(data[3]) == 3:
        upload_winding_resistance_data(data)
    if int(data[3]) == 4:
        upload_ddf_data(data)
    if int(data[3]) == 5:
        upload_offlinePD_data(data)
    if int(data[3]) == 6:
        None
    if int(data[3]) == 7:
        None
    if int(data[3]) == 8:
        None
    if int(data[3]) == 9:
        None
    if int(data[3]) == 10:
        upload_RFA_data(data)
    if int(data[3]) == 11:
        upload_onlinePD_data(data)
    if int(data[3]) == 12:
        None

def upload_test_data_cable(data):

    #Ovrsheath
    def upload_oversheat_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('Cable Oversheath data inserted')
    #insulation resistance
    def upload_insulation_resistance_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_7, feature_8, feature_9)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('IR data inserted')
    #pi
    def upload_polarization_index_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_10, feature_11, feature_12)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('PI data inserted')
    #VLF TD
    def upload_ddf_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data 
                                (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3, feature_4, feature_5, feature_6, feature_7,feature_8, feature_9, feature_10,feature_11, feature_12, feature_13, feature_14)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('VLF TD data inserted')
    #OfflinePD
    def upload_offlinePD_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data 
                                (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_7, feature_8, feature_25)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('OfflinePD data inserted')
    #online PD
    def upload_onlinePD_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO online_test_data 
                                (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_6, feature_7, feature_8, feature_9, feature_10, feature_25)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()
        print('OnlinePD data inserted')
    #RFA
    def upload_RFA_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            rotor_type = data[5]
            numb_of_poles = data[-2]
            number_of_turn_per_pole = data[-1]

            # Remove the last two elements from data
            data.pop(-2)
            data.pop(-1)

            if rotor_type == 'Salient Poles':
                if int(numb_of_poles) == 4:
                    # Prepare the SQL query for 4 poles
                    insert_sql = '''INSERT INTO online_test_data 
                                        (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_23, feature_24, feature_25)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

                elif int(numb_of_poles) == 6:
                    # Prepare the SQL query for 6 poles
                    insert_sql = '''INSERT INTO online_test_data 
                                        (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_23, feature_24, feature_25)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            elif rotor_type == 'Cylindrical Rotor':
                if int(number_of_turn_per_pole) == 7:
                    # Prepare the SQL query for 7 turns per pole
                    insert_sql = '''INSERT INTO online_test_data 
                                        (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_12, feature_13, feature_14, feature_15, feature_16, feature_17, feature_18, feature_23, feature_24, feature_25)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()
        print('RFA data inserted')


    if int(data[3]) == 14:
        upload_oversheat_data(data)
    if int(data[3]) == 15:
        upload_insulation_resistance_data(data)
    if int(data[3]) == 16:
        upload_polarization_index_data(data)
    if int(data[3]) == 17:
        upload_ddf_data(data)
    if int(data[3]) == 18:
        None

    if int(data[3]) == 20:
        upload_onlinePD_data(data)

def upload_test_data_sw(data):


    #insulation resistance
    def upload_insulation_resistance_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_7, feature_8, feature_9,feature_10, feature_11)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('IR data inserted')
    #pi
    def upload_polarization_index_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_10, feature_11, feature_12,feature_13, feature_14)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('PI data inserted')

    #OfflinePD
    def upload_offlinePD_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO offline_test_data 
                                (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_7, feature_8, feature_25)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        print('OfflinePD data inserted')
    #online PD
    def upload_onlinePD_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host if needed
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            database='Inwave_IHMS'  # Specify the database name
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        try:
            # Prepare the insert SQL query
            insert_sql = '''INSERT INTO online_test_data 
                                (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2, feature_3, feature_4, feature_6, feature_7, feature_8, feature_9, feature_10, feature_25)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            # Execute the insert statement
            cursor.execute(insert_sql, data)

            # Commit the transaction
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()
        print('OnlinePD data inserted')




    if int(data[3]) == 23:
        upload_insulation_resistance_data(data)
    if int(data[3]) == 24:
        upload_polarization_index_data(data)

    if int(data[3]) == 25:
        None

    if int(data[3]) == 30:
        upload_onlinePD_data(data)


def create_new_site(site_data):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Prepare the insert SQL query
        columns = ', '.join(site_data.keys())
        placeholders = ', '.join(['%s'] * len(site_data))
        insert_query = f"INSERT INTO site ({columns}) VALUES ({placeholders})"

        # Execute the insert statement
        cursor.execute(insert_query, tuple(site_data.values()))

        # Commit the transaction
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    print('Site created!')



def create_new_asset(data):

    #default cricality class = 1
    criticality =1

    #default age factor =1
    #default maintenance factor =1
    #default failure factor =1
    age_factor =1
    maintenance_factor=1
    failure_factor=1


    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()




    def create_asset(cursor, conn, data):

        try:

            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))



            insert_query = f"INSERT INTO asset ({columns}) VALUES ({placeholders})"


            # Execute the insert statement
            cursor.execute(insert_query, tuple(data.values()))

            #read id
            # Get the ID of the last inserted row
            last_asset_id = cursor.lastrowid

            #get asset subcomponet list

            cursor.execute("""
                           SELECT id FROM asset_subcomponent where asset_component_id in (SELECT id FROM asset_component where asset_category_id=%s)
                        """, (data['asset_category_id'],))
            sub_id_list = cursor.fetchall()

            final_sub_id_list = sorted([item[0] for item in sub_id_list])


            # Commit the transaction
            conn.commit()

            # update criticality
            today = datetime.now()
            formatted_date_str = today.strftime('%d/%m/%Y')
            update_asset_criticality(criticality, last_asset_id, formatted_date_str)

            print('criticality updated')
            # update the factors
            for sub_id in final_sub_id_list:
                insert_subcomponent_factors_details(age_factor, maintenance_factor, failure_factor,
                                                    sub_id, last_asset_id)

            print('details sub updated')

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()


        print('Asset created!')



    create_asset(cursor,conn,data)




##########################################      Export data to csv funxtion

def export_asset_summary(asset_id):

    """Function to export a list containing all the information related to the latest assessment:
    - asset details
    - Risk index
    - Health Index
    - Components Health indexes
    - Subcomponent Health indexes
    - Failure mechanisms analysis

    The function returns two list:
    - headers
    - data
    """
    # Connect to SQLite database (or create it if it doesn't exist)



    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave@2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()


    try:
        # Get asset details
        cursor.execute("SELECT * FROM asset WHERE id = %s", (asset_id,))
        asset_details = cursor.fetchone()


        # Get latest asset analysis
        cursor.execute("SELECT * FROM asset_analysis WHERE asset_id = %s ORDER BY ID DESC limit 1", (asset_id,))
        latest_assessment = cursor.fetchone()




        if latest_assessment is None:
            print("No assessment found for the given asset ID.")
            return

        analysis_id = latest_assessment[0]




        # Get asset component analysis
        cursor.execute("SELECT * FROM component_analysis WHERE analysis_id = %s", (analysis_id,))
        latest_component_assessment = cursor.fetchall()


        component_list = get_component_list()

        # Replace id with name
        latest_component_assessment_cleaned = []
        for item in latest_component_assessment:
            sub = []
            for name in component_list:
                if name[0] == item[2]:  # Assuming item[2] is the component_id
                    sub.append(name[1])  # name[1] is the component name
                    sub.append(item[3])  # Assuming item[3] is the assessment value
            latest_component_assessment_cleaned.append(sub)

        # Get asset subcomponent analysis
        cursor.execute("SELECT * FROM subcomponent_analysis WHERE analysis_id = %s", (analysis_id,))
        latest_subcomponent_assessment = cursor.fetchall()

        subcomponent_list = get_subcomponent_list()

        # Replace id with name
        latest_subcomponent_assessment_cleaned = []
        for item in latest_subcomponent_assessment:
            sub = []
            for name in subcomponent_list:
                if name[0] == item[2]:  # Assuming item[2] is the subcomponent_id
                    sub.append(name[1])  # name[1] is the subcomponent name
                    sub.append(item[3])  # Assuming item[3] is the assessment value
            latest_subcomponent_assessment_cleaned.append(sub)

        # Failure mechanisms
        cursor.execute("SELECT * FROM failure_mechanisms_analysis WHERE analysis_id = %s", (analysis_id,))
        latest_fma_assessment = cursor.fetchall()

        failure_mechanisms_name = get_failure_mechanism_list()

        # Replace id with name
        latest_fma_assessment_cleaned = []
        for item in latest_fma_assessment:
            sub = []
            for name in failure_mechanisms_name:
                if name[0] == item[2]:  # Assuming item[2] is the mechanism_id
                    sub.append(name[1])  # name[1] is the mechanism name
                    sub.append(item[3])  # Assuming item[3] is the assessment value
            latest_fma_assessment_cleaned.append(sub)

        # return {
        #     'asset_details': asset_details,
        #     'latest_assessment': latest_assessment,
        #     'component_assessment': latest_component_assessment_cleaned,
        #     'subcomponent_assessment': latest_subcomponent_assessment_cleaned,
        #     'failure_mechanisms_assessment': latest_fma_assessment_cleaned
        # }

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    #combined all in one list to be exported to csv

    # Combine data into a single list
    latest_assessment_cleaned = list(latest_assessment)
    latest_assessment_cleaned.pop(2)
    latest_assessment_modified = tuple(latest_assessment_cleaned)

    combined_data = list(asset_details[1:20]) + list(latest_assessment_modified[1:]) + [item[1] for item in latest_component_assessment_cleaned] + [
            item[1] for item in latest_subcomponent_assessment_cleaned] + [item[1] for item in latest_fma_assessment_cleaned]


    headers_1 = [
        'Asset Tag', 'Function', 'Manufactorer', 'Year of Manufactured', 'Year of Installation', 'Rated Voltage [kV]', 'Rated Power [MVA]',
        'Frequency [Hz]', 'Rated Speed [rmp]', 'Cooling Type', 'Type', 'Rotor Type', 'Stator Winding Insulation Thermal Class', 'Stator Winding Type',
        'Stator Winding Impregnation Type', 'Number of stator slot', 'Rotor Winding Insulation Thermal Class', 'Number of Poles', 'Number of turn per pole',
        'Latest assessment', 'Risk Index', 'Health Index'
    ]


    headers_2 = [f'{item[0]} Health Index' for item in latest_component_assessment_cleaned] + [
            f'{item[0]} Health Index' for item in latest_subcomponent_assessment_cleaned] + [f'{item[0]}' for item in latest_fma_assessment_cleaned]

    headers = headers_1+headers_2



    return headers, combined_data


# export_asset_summary(74)


data_asset = {
    'tag':'testrm',
    'asset_function':'na',
    'manufacturer':'na',
    'yom':'2021',
    'yoi':'2022',
    'rated_voltage':'11',
    'feature_1':'40',
    'feature_2':'50',
    'feature_3': '3000',
    'feature_4':'Air',
    'feature_5':'Synchronuous',
    'feature_6':'Cylindrical',
    'feature_7':'Class F',
    'feature_8':'Single turn',
    'feature_9':'Vacuum impregnated',
    'feature_10':'38',
    'feature_11':'Class F',
    'feature_12':'1',
    'feature_13':'7',
    'feature_14':'',
    'feature_15':'',
    'lat':'1.2543641520890003',
    'lon':'103.6617774728823',
    'asset_category_id':'1',
    'site_id': '2'
}

# id, site_name, lat, lon, customer_id
site_data = {
    'site_name': '',
    'lat': '',
    'lon':'',
    'customer_id':''
}


#id, email, password, role
new_user_data = {
    'email': '',
    'password': '',
    'role':''
}
# file_path = 'D:/xx.Final IHMS/0.Demo customer/1.PAREP/site_asset_iberdrola_sa.xlsx'
# try:
#     excel_file = pd.ExcelFile(file_path)
#
#     # Print the names of the sheets
#     sheet_names = excel_file.sheet_names
#     # print("Sheet names:", sheet_names)
#     #
#     # print(fuck)
#
#     # Optionally, load a specific sheet
#     sheet_name = sheet_names[0]  # Replace with the desired sheet name or index
#     df = pd.read_excel(file_path, sheet_name=sheet_name)
#
#     # Change the values in a specific column - if emoty add float
#     column_name = 'lat'  # Replace with the actual column name
#     column_name_1 = 'lon'
#     new_value = 0.0  # Replace with the value you want to set
#     #
#     # # Modify the column (e.g., setting all values to new_value)
#     # df[column_name] = new_value
#     df[column_name] = df[column_name].where(df[column_name].notna(), new_value)
#     df[column_name_1] = df[column_name_1].where(df[column_name_1].notna(), new_value)
#
#     # # Alternatively, modify specific rows, e.g., where another column matches a condition
#     # df.loc[df['AnotherColumn'] == 'SomeCondition', column_name] = new_value
#
#     # Display the first few rows after modification
#     # print("After modification:")
#     # print(df['lat'])
#     # print(df.head())
#
#     # Optionally, save the changes back to the Excel file
#     df.to_excel(file_path, sheet_name=sheet_name, index=False)
#
#     # Create a list to hold dictionaries for each row
#     data_assets = []
#
#     # Iterate through each row in the DataFrame
#     for _, row in df.iterrows():
#         data_asset = {
#             'tag': '' if pd.isna(row.get('tag')) else row['tag'],
#             'asset_function': '' if pd.isna(row.get('asset_function')) else row['asset_function'],
#             'manufacturer': '' if pd.isna(row.get('manufacturer')) else row['manufacturer'],
#             'yom': '' if pd.isna(row.get('yom')) else row['yom'],
#             'yoi': '' if pd.isna(row.get('yoi')) else row['yoi'],
#             'rated_voltage': '' if pd.isna(row.get('rated_voltage')) else row['rated_voltage'],
#             'feature_1': '' if pd.isna(row.get('feature_1')) else row['feature_1'],
#             'feature_2': '' if pd.isna(row.get('feature_2')) else row['feature_2'],
#             'feature_3': '' if pd.isna(row.get('feature_3')) else row['feature_3'],
#             'feature_4': '' if pd.isna(row.get('feature_4')) else row['feature_4'],
#             'feature_5': '' if pd.isna(row.get('feature_5')) else row['feature_5'],
#             'feature_6': '' if pd.isna(row.get('feature_6')) else row['feature_6'],
#             'feature_7': '' if pd.isna(row.get('feature_7')) else row['feature_7'],
#             'feature_8': '' if pd.isna(row.get('feature_8')) else row['feature_8'],
#             'feature_9': '' if pd.isna(row.get('feature_9')) else row['feature_9'],
#             'feature_10': '' if pd.isna(row.get('feature_10')) else row['feature_10'],
#             'feature_11': '' if pd.isna(row.get('feature_11')) else row['feature_11'],
#             'feature_12': '' if pd.isna(row.get('feature_12')) else row['feature_12'],
#             'feature_13': '' if pd.isna(row.get('feature_13')) else row['feature_13'],
#             'feature_14': '' if pd.isna(row.get('feature_14')) else row['feature_14'],
#             'feature_15': '' if pd.isna(row.get('feature_15')) else row['feature_15'],
#             'lat': '' if pd.isna(row.get('lat')) else row.get('lat'),
#             'lon': '' if pd.isna(row.get('lon')) else row.get('lon'),
#             'asset_category_id': '' if pd.isna(row.get('asset_category_id')) else row['asset_category_id'],
#             'site_id': '' if pd.isna(row.get('site_id')) else row['site_id']
#         }
#         data_assets.append(data_asset)
#
#     # Display the list of dictionaries
#     i=0
#     for asset in data_assets:
#         print(asset)
#
#         print(i)
#         create_new_asset(asset)
#         i+=1
#
#
#
# except Exception as e:
#     print(f"An error occurred: {e}")
# create_new_asset(data_asset)
get_online_test_analysis_data(83, 2)