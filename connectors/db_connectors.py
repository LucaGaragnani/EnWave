import sqlite3
import pandas as pd
import os

""" db connector to handle all the queries and return data 
"""

def get_user(email):

    # Connect to SQLite database (or create it if it doesn't exist)
    print(email)
    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)


    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()


    #site
    cursor.execute("""SELECT * FROM user WHERE email = ? """, (email,))
    user_result = cursor.fetchone()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return user_result

def reset_password(hashed_password, email, user_id):

    # Connect to SQLite database (or create it if it doesn't exist)
    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)


    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()


    #site
    cursor.execute("""UPDATE user SET password = ? WHERE email = ? AND id = ? """, (hashed_password, email, user_id))
    # cursor.execute("""SELECT * FROM user WHERE email = ? """, (email,))

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return 'Password Update Successfully!'
def get_customer_site(customer_id):

    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)

    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()


    #site
    cursor.execute("""SELECT * FROM site WHERE customer_id = ?""", (customer_id,))
    site_result = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return site_result

def get_asset_list(site_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)

    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    #asset
    cursor.execute("""SELECT * FROM asset WHERE site_id = ?""", (site_id,))
    asset_result = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return asset_result

def get_asset_details(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # asset
    cursor.execute("""SELECT * FROM asset_details WHERE asset_id = ?""", (asset_id,))
    asset_details_list = cursor.fetchall()


    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return asset_details_list

def get_asset_analysis(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # asset
    cursor.execute("""SELECT * FROM asset_analysis WHERE asset_id = ?""", (asset_id,))
    asset_analysis_list = cursor.fetchall()


    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return asset_analysis_list

def get_maintenance_action(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ama.*, cc.tag
        FROM asset AS cc
        JOIN asset_analysis AS aa ON cc.id = aa.asset_id
        JOIN asset_maintenance_actions AS ama ON aa.id = ama.asset_analysis_id
        WHERE aa.asset_id = ?
    """, (asset_id,))


    asset_maintenance_actions_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()


    return asset_maintenance_actions_list



def get_letest_asset_analysis(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)

    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # asset
    cursor.execute("""SELECT * FROM asset_analysis WHERE asset_id = ? ORDER BY ID desc LIMIT 1""", (asset_id,))
    latest_asset_analysis_list = cursor.fetchone()



    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return latest_asset_analysis_list


def get_component_analysis(analysis_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)

    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # asset
    cursor.execute("""SELECT * FROM component_analysis WHERE analysis_id = ?""", (analysis_id,))
    component_analysis_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return component_analysis_list

def get_subcomponent_analysis(analysis_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # asset
    cursor.execute("""SELECT * FROM subcomponent_analysis WHERE analysis_id = ?""", (analysis_id,))
    subcomponent_analysis_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return subcomponent_analysis_list

def get_subcomponent_details(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # asset
    cursor.execute("""SELECT * FROM asset_subcomponent_details WHERE asset_id = ?""", (asset_id,))
    asset_subcomponent_list = cursor.fetchall()


    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return asset_subcomponent_list

def get_failure_mechanisms_analysis(analysis_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # asset
    cursor.execute("""SELECT * FROM failure_mechanisms_analysis WHERE analysis_id = ?""", (analysis_id,))
    failure_mechanism_analysis_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return failure_mechanism_analysis_list




def get_criticality_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM criticality_list""")
    criticality_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return criticality_list

def get_asset_category_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM asset_category""")
    asset_category_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return asset_category_list

def get_subcomponent_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')


    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM asset_subcomponent""")
    asset_subcomponent_list = cursor.fetchall()


    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return asset_subcomponent_list

def get_component_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM asset_component""")
    asset_component_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return asset_component_list

def get_failure_mechanism_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # asset
    cursor.execute("""SELECT * FROM failure_mechanisms """)
    failure_mechanism_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return failure_mechanism_list

def get_diagnostic_test_list():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM diagnostic_test""")
    diagnostic_test_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return diagnostic_test_list

##########################################     DATA - ONLine

def get_online_test_data_to_be_analysis(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM online_test_data WHERE analysis IS NULL""")
    online_PD_test_data_to_be_analysed = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return online_PD_test_data_to_be_analysed


def get_online_test_analysis_data(asset_id, subcomponent_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT `date`, `diagnostic_test_id`, `analysis` FROM online_test_data WHERE asset_id = ? AND subcomponent_id = ?""", (asset_id, subcomponent_id))
    online_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return online_test_data_list

def get_offline_test_analysis_data(asset_id, subcomponent_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT `date`, `diagnostic_test_id`, `analysis` FROM offline_test_data WHERE asset_id = ? AND subcomponent_id = ?""", (asset_id,subcomponent_id,))
    offline_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return offline_test_data_list


def get_online_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM online_test_data WHERE asset_id = ? order by ID LIMIT 50""", (asset_id,))
    online_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return online_test_data_list

#rotor flux
def get_rfa_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM online_test_data WHERE diagnostic_test_id = 10 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    rfa_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return rfa_test_data_list

#online PD test
def get_online_pd_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM online_test_data WHERE diagnostic_test_id = 11 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    online_PD_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return online_PD_test_data_list

#endwinding vibration
def get_online_ew_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM online_test_data WHERE diagnostic_test_id = 12 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    online_EW_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return online_EW_test_data_list

#vibration analysis
def get_online_va_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM online_test_data WHERE diagnostic_test_id = 13 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    online_VA_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return online_VA_test_data_list


##########################################     DATA - OFFLine

def get_offline_test_data_to_be_analysis(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE analysis IS NULL""")
    offline_PD_test_data_to_be_analysed = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return offline_PD_test_data_to_be_analysed

def get_offline_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE asset_id = ? order by ID LIMIT 50""", (asset_id,))
    offline_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return offline_test_data_list

def get_ir_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE diagnostic_test_id = 1 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    ir_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return ir_test_data_list

def get_pi_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE diagnostic_test_id = 2 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    pi_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return pi_test_data_list

def get_wr_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE diagnostic_test_id = 3 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    wr_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return wr_test_data_list

def get_ddf_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE diagnostic_test_id = 4 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    ddf_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return ddf_test_data_list

def get_offline_pd_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE diagnostic_test_id = 5 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    offline_PD_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return offline_PD_test_data_list

def get_inspection_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE diagnostic_test_id = 6 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    inspection_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return inspection_test_data_list

def get_coreflux_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE diagnostic_test_id = 7 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    coreflux_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return coreflux_test_data_list

def get_elcid_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE diagnostic_test_id = 8 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    elcid_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return elcid_test_data_list

def get_bump_test_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM offline_test_data WHERE diagnostic_test_id = 9 AND asset_id = ? order by ID LIMIT 50""", (asset_id,))
    bump_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return bump_test_data_list

##########################################     DATA - Operational

def get_operational_test_data():
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    cursor.execute("""SELECT * FROM operational_test_data""")
    operational_test_data_list = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return operational_test_data_list


########################################   Custom function

def upload_session_data(user_id, datetime):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    insert_sql = '''INSERT INTO session_data (user_id, datetime)
                                    SELECT ?, ?;'''
    cursor.execute(insert_sql, (user_id, datetime))

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()


def update_asset_criticality(criticality, asset_id, date):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site
    insert_sql = '''INSERT INTO asset_details (criticality_class, date, asset_id)
                                SELECT ?, ?, ?;'''
    cursor.execute(insert_sql,(criticality, asset_id, date))

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

def update_subcomponent_factors_details(age_factor, maintenance_factor, failure_factor, asset_subcomponent_id, asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    # site

    cursor.execute('''
                        UPDATE asset_subcomponent_details
                        SET age_factor = ?,
                            maintenance_factor = ?,
                            failure_factor = ?
                        WHERE asset_subcomponent_id = ?
                          AND asset_id = ?;
                    ''', (age_factor, maintenance_factor, failure_factor, asset_subcomponent_id, asset_id))

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()


#########################################    Upload data functions

def upload_test_data(data):

    #insulation resistance
    def upload_insulation_resistance_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        db_directory = current_directory.replace('connectors', 'database')

        # Construct the path to the database file
        database_path = os.path.join(db_directory, 'Inwave_RM.db')

        conn = sqlite3.connect(database_path)
        # Create a cursor object using which we can interact with the database
        cursor = conn.cursor()

        # site
        insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3,feature_4,feature_6,feature_8, feature_9)
                                        SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?;'''
        cursor.execute(insert_sql, (data))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        print('IR data inserted')
    #pi
    def upload_polarization_index_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        db_directory = current_directory.replace('connectors', 'database')

        # Construct the path to the database file
        database_path = os.path.join(db_directory, 'Inwave_RM.db')

        conn = sqlite3.connect(database_path)
        # Create a cursor object using which we can interact with the database
        cursor = conn.cursor()

        # site
        insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3,feature_4,feature_5,feature_6, feature_9,feature_11, feature_12)
                                        SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?;'''
        cursor.execute(insert_sql, (data))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        print('PI data inserted')
    #WR
    def upload_winding_resistance_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        db_directory = current_directory.replace('connectors', 'database')

        # Construct the path to the database file
        database_path = os.path.join(db_directory, 'Inwave_RM.db')

        conn = sqlite3.connect(database_path)
        # Create a cursor object using which we can interact with the database
        cursor = conn.cursor()

        # site
        insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3,feature_5,feature_6)
                                        SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?;'''
        cursor.execute(insert_sql, (data))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        print('WR data inserted')
    #ddf
    def upload_ddf_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        db_directory = current_directory.replace('connectors', 'database')

        # Construct the path to the database file
        database_path = os.path.join(db_directory, 'Inwave_RM.db')

        conn = sqlite3.connect(database_path)
        # Create a cursor object using which we can interact with the database
        cursor = conn.cursor()

        # site
        insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3,feature_4,feature_5,feature_6,feature_7,feature_8, feature_9,feature_10,feature_11, feature_23, feature_24)
                                        SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?;'''
        cursor.execute(insert_sql, (data))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        print('DDF data inserted')
    #OfflinePD
    def upload_offlinePD_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        db_directory = current_directory.replace('connectors', 'database')

        # Construct the path to the database file
        database_path = os.path.join(db_directory, 'Inwave_RM.db')

        conn = sqlite3.connect(database_path)
        # Create a cursor object using which we can interact with the database
        cursor = conn.cursor()

        # site
        insert_sql = '''INSERT INTO offline_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3,feature_4,feature_5,feature_7,feature_8,feature_25)
                                        SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?;'''
        cursor.execute(insert_sql, (data))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        print('OfflinePD data inserted')
    #online PD
    def upload_onlinePD_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        db_directory = current_directory.replace('connectors', 'database')

        # Construct the path to the database file
        database_path = os.path.join(db_directory, 'Inwave_RM.db')

        conn = sqlite3.connect(database_path)
        # Create a cursor object using which we can interact with the database
        cursor = conn.cursor()

        # site
        insert_sql = '''INSERT INTO online_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3,feature_4,feature_6,feature_7,feature_8,feature_9,feature_10, feature_25 )
                                        SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?;'''
        cursor.execute(insert_sql, (data))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        print('OnlinePD data inserted')
    #RFA
    def upload_RFA_data(data):
        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        db_directory = current_directory.replace('connectors', 'database')

        # Construct the path to the database file
        database_path = os.path.join(db_directory, 'Inwave_RM.db')

        conn = sqlite3.connect(database_path)
        # Create a cursor object using which we can interact with the database
        cursor = conn.cursor()

        rotor_type = data[5]
        numb_of_poles = data[-2]
        number_of_turn_per_pole = data[-1]

        data.pop(-2)
        data.pop(-1)

        if rotor_type=='Salient Poles':
            if int(numb_of_poles)==4:

                # site
                insert_sql = '''INSERT INTO online_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3,feature_4,feature_5,feature_23,feature_24, feature_25 )
                                                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?;'''

            if int(numb_of_poles) == 6:
                # site
                insert_sql = '''INSERT INTO online_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3,feature_4,feature_5,feature_6,feature_7,feature_23,feature_24, feature_25 )
                                                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?;'''


        if rotor_type=='Cylindrical Rotor':
            if int(number_of_turn_per_pole)==7:

                # site
                insert_sql = '''INSERT INTO online_test_data (date, asset_id, subcomponent_id, diagnostic_test_id, feature_1, feature_2,feature_3,feature_4,feature_5,feature_6,feature_7,feature_8,feature_12,feature_13,feature_14,feature_15,feature_16,feature_17,feature_18,feature_23,feature_24, feature_25 )
                                                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?;'''


        cursor.execute(insert_sql, (data))

        # Commit the transaction
        conn.commit()

        # Close the database connection
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

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('connectors', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()

    #get asset details
    cursor.execute("""SELECT * FROM asset WHERE id = ? """,
                   (asset_id,))
    asset_details = cursor.fetchone()



    cursor.execute("""SELECT * FROM asset_analysis WHERE asset_id = ? ORDER BY ID desc """,
                   (asset_id,))
    latest_assessment = cursor.fetchone()



    analysis_id = latest_assessment[0]

    # get asset component analysis
    cursor.execute("""SELECT * FROM component_analysis WHERE analysis_id = ?  """,
                   (analysis_id,))
    latest_component_assessment = cursor.fetchall()

    component_list = get_component_list()

    # replace id with name

    latest_component_assessment_clened = []
    for item in latest_component_assessment:
        sub = []
        for name in component_list:
            if name[0] == item[2]:
                sub.append(name[1])
                sub.append(item[3])
        latest_component_assessment_clened.append(sub)


    # get asset subcomponent analysis
    cursor.execute("""SELECT * FROM subcomponent_analysis WHERE analysis_id = ?  """,
                   (analysis_id,))
    latest_subcomponent_assessment = cursor.fetchall()

    subcomponent_list = get_subcomponent_list()

    #replace id with name

    latest_subcomponent_assessment_clened = []
    for item in latest_subcomponent_assessment:
        sub = []
        for name in subcomponent_list:
            if name[0] == item[2]:
                sub.append(name[1])
                sub.append(item[3])
        latest_subcomponent_assessment_clened.append(sub)

    #failure mechanisms
    cursor.execute("""SELECT * FROM failure_mechanisms_analysis WHERE analysis_id = ?  """,
                   (analysis_id,))
    latest_fma_assessment = cursor.fetchall()

    failure_mechanisms_name = get_failure_mechanism_list()


    # replace id with name

    latest_fma_assessment_clened = []
    for item in latest_fma_assessment:
        sub = []
        for name in failure_mechanisms_name:
            if name[0] == item[2]:
                sub.append(name[1])
                sub.append(item[3])
        latest_fma_assessment_clened.append(sub)

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()

    conn.close()

    #combined all in one list to be exported to csv

    # Combine data into a single list
    latest_assessment_cleaned = list(latest_assessment)
    latest_assessment_cleaned.pop(2)
    latest_assessment_modified = tuple(latest_assessment_cleaned)

    combined_data = list(asset_details[1:20]) + list(latest_assessment_modified[1:]) + [item[1] for item in latest_component_assessment_clened] + [
            item[1] for item in latest_subcomponent_assessment_clened] + [item[1] for item in latest_fma_assessment_clened]


    headers_1 = [
        'Asset Tag', 'Function', 'Manufactorer', 'Year of Manufactured', 'Year of Installation', 'Rated Voltage [kV]', 'Rated Power [MVA]',
        'Frequency [Hz]', 'Rated Speed [rmp]', 'Cooling Type', 'Type', 'Rotor Type', 'Stator Winding Insulation Thermal Class', 'Stator Winding Type',
        'Stator Winding Impregnation Type', 'Number of stator slot', 'Rotor Winding Insulation Thermal Class', 'Number of Poles', 'Number of turn per pole',
        'Latest assessment', 'Risk Index', 'Health Index'
    ]


    headers_2 = [f'{item[0]} Health Index' for item in latest_component_assessment_clened] + [
            f'{item[0]} Health Index' for item in latest_subcomponent_assessment_clened] + [f'{item[0]}' for item in latest_fma_assessment_clened]

    headers = headers_1+headers_2


    return headers, combined_data













