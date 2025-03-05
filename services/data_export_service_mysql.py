import os
import sqlite3
import mysql.connector

# from pymodbus.server.sync import ModbusTcpServer
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSparseDataBlock, ModbusServerContext,ModbusSlaveContext
# from pymodbus.transaction import ModbusRtuFramer
import struct

import threading
import logging
import re


# Configure logging
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("modbus_server.log"),  # Log to a file
        logging.StreamHandler()                     # Log to console
    ]
)
# Function to get asset data from SQLite database

def connect_to_db():
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave!2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    return cursor, conn

def fetch_asset_data(cursor):

    # Fetch data from the asset table
    cursor.execute("SELECT id,tag,asset_function, manufacturer, yom, yoi, rated_voltage,feature_1,feature_2,feature_3,feature_4,feature_5,feature_6,feature_7,feature_8,feature_9,feature_10,feature_11,feature_12,feature_13, lat, lon FROM asset")  # Modify as per your table and columns
    asset_data = cursor.fetchall()



    return asset_data

def fetch_asset_analysis(cursor):
    # Fetch data from the asset table
    cursor.execute(
        "SELECT date, asset_id, risk_index, health_index FROM asset_analysis order by id desc limit 1")  # Modify as per your table and columns
    asset_analysis = cursor.fetchall()


    return asset_analysis


def fetch_asset_component_analysis(cursor):
    # Fetch data

    query = """
    SELECT ac.name, ca.value
    FROM asset_component ac
    JOIN component_analysis ca ON ac.id = ca.component_id
    ORDER BY ca.id DESC
    LIMIT 3
    """

    cursor.execute(query)
    component_analysis = cursor.fetchall()


    return component_analysis

def fetch_asset_subcomponent_analysis(cursor):
    # Fetch data

    query = """
    SELECT ac.name, ca.value
    FROM asset_subcomponent ac
    JOIN subcomponent_analysis ca ON ac.id = ca.subcomponent_id
    ORDER BY ca.id DESC
    LIMIT 12
    """

    cursor.execute(query)
    subcomponent_analysis = cursor.fetchall()

    return subcomponent_analysis

def fetch_failure_mechanisms_analysis(cursor):
    # Fetch data

    query = """
    SELECT ac.name, ca.value
    FROM failure_mechanisms ac
    JOIN failure_mechanisms_analysis ca ON ac.id = ca.failure_mechanism_id
    ORDER BY ca.id DESC
    LIMIT 16
    """

    cursor.execute(query)
    fm_analysis = cursor.fetchall()



    return fm_analysis

def fetch_offline_test_data(cursor):
    # Fetch data

    # insulation resistance
    query = """
    SELECT 
        otd.*, 
        assc.name AS subcomponent_name, 
        dt.name AS diagnostic_test_name
    FROM 
        offline_test_data otd
    JOIN 
        asset_subcomponent assc ON otd.subcomponent_id = assc.id
    JOIN 
        diagnostic_test dt ON otd.diagnostic_test_id = dt.id 
    WHERE 
        dt.asset_category_id = 1
        AND dt.id = 1
        AND otd.date = (
            SELECT MAX(date) 
            FROM offline_test_data
        )
    ORDER BY 
        otd.date DESC
    """

    cursor.execute(query)
    insulation_resistance_data = cursor.fetchall()
    insulation_resistance_data_cleaned = []
    for item in insulation_resistance_data:
        row = []
        for value in item:
            if value is None:
                row.append('N/A')
            else:
                row.append(value)
        insulation_resistance_data_cleaned.append(row)



    # polarization index
    query = """
            WITH LatestTest AS (
            SELECT MAX(date) AS max_date
            FROM offline_test_data
            WHERE diagnostic_test_id = 2
        )
        SELECT 
            otd.*, 
            assc.name AS subcomponent_name, 
            dt.name AS diagnostic_test_name
        FROM 
            offline_test_data otd
        JOIN 
            asset_subcomponent assc ON otd.subcomponent_id = assc.id
        JOIN 
            diagnostic_test dt ON otd.diagnostic_test_id = dt.id
        WHERE 
            dt.asset_category_id = 1
            AND dt.id = 2
            AND otd.date = (SELECT max_date FROM LatestTest)

        ORDER BY 
            otd.date DESC
        """

    cursor.execute(query)
    polarization_index_data = cursor.fetchall()

    polarization_index_cleaned = []
    for item in polarization_index_data:
        row=[]
        for value in item:
            if value is None:
                row.append('N/A')
            else:
                row.append(value)
        polarization_index_cleaned.append(row)
    # print(polarization_index_data)

    # winding resistance
    query = """
                WITH LatestTest AS (
                SELECT MAX(date) AS max_date
                FROM offline_test_data
                WHERE diagnostic_test_id = 3
            )
            SELECT 
                otd.*, 
                assc.name AS subcomponent_name, 
                dt.name AS diagnostic_test_name
            FROM 
                offline_test_data otd
            JOIN 
                asset_subcomponent assc ON otd.subcomponent_id = assc.id
            JOIN 
                diagnostic_test dt ON otd.diagnostic_test_id = dt.id
            WHERE 
                dt.asset_category_id = 1
                AND dt.id = 3
                AND otd.date = (SELECT max_date FROM LatestTest)

            ORDER BY 
                otd.date DESC
            """

    cursor.execute(query)
    wr_data = cursor.fetchall()

    # ddf
    query = """
                    WITH LatestTest AS (
                    SELECT MAX(date) AS max_date
                    FROM offline_test_data
                    WHERE diagnostic_test_id = 4
                )
                SELECT 
                    otd.*, 
                    assc.name AS subcomponent_name, 
                    dt.name AS diagnostic_test_name
                FROM 
                    offline_test_data otd
                JOIN 
                    asset_subcomponent assc ON otd.subcomponent_id = assc.id
                JOIN 
                    diagnostic_test dt ON otd.diagnostic_test_id = dt.id
                WHERE 
                    dt.asset_category_id = 1
                    AND dt.id = 4
                    AND otd.date = (SELECT max_date FROM LatestTest)

                ORDER BY 
                    otd.date DESC
                """

    cursor.execute(query)
    ddf_data = cursor.fetchall()

    # offlinepd
    query = """
                        WITH LatestTest AS (
                        SELECT MAX(date) AS max_date
                        FROM offline_test_data
                        WHERE diagnostic_test_id = 5
                    )
                    SELECT 
                        otd.*, 
                        assc.name AS subcomponent_name, 
                        dt.name AS diagnostic_test_name
                    FROM 
                        offline_test_data otd
                    JOIN 
                        asset_subcomponent assc ON otd.subcomponent_id = assc.id
                    JOIN 
                        diagnostic_test dt ON otd.diagnostic_test_id = dt.id
                    WHERE 
                        dt.asset_category_id = 1
                        AND dt.id = 5
                        AND otd.date = (SELECT max_date FROM LatestTest)

                    ORDER BY 
                        otd.date DESC
                    """

    cursor.execute(query)
    offpd_data = cursor.fetchall()

    # inspection
    query = """
                            WITH LatestTest AS (
                            SELECT MAX(date) AS max_date
                            FROM offline_test_data
                            WHERE diagnostic_test_id = 6
                        )
                        SELECT 
                            otd.*, 
                            assc.name AS subcomponent_name, 
                            dt.name AS diagnostic_test_name
                        FROM 
                            offline_test_data otd
                        JOIN 
                            asset_subcomponent assc ON otd.subcomponent_id = assc.id
                        JOIN 
                            diagnostic_test dt ON otd.diagnostic_test_id = dt.id
                        WHERE 
                            dt.asset_category_id = 1
                            AND dt.id = 6
                            AND otd.date = (SELECT max_date FROM LatestTest)

                        ORDER BY 
                            otd.date DESC
                        """

    cursor.execute(query)
    inspection_data = cursor.fetchall()

    # core_flux
    query = """
                    WITH LatestTest AS (
                    SELECT MAX(date) AS max_date
                    FROM offline_test_data
                    WHERE diagnostic_test_id = 7
                )
                SELECT 
                    otd.*, 
                    assc.name AS subcomponent_name, 
                    dt.name AS diagnostic_test_name
                FROM 
                    offline_test_data otd
                JOIN 
                    asset_subcomponent assc ON otd.subcomponent_id = assc.id
                JOIN 
                    diagnostic_test dt ON otd.diagnostic_test_id = dt.id
                WHERE 
                    dt.asset_category_id = 1
                    AND dt.id = 7
                    AND otd.date = (SELECT max_date FROM LatestTest)

                ORDER BY 
                    otd.date DESC
                """
    cursor.execute(query)
    core_flux_data = cursor.fetchall()

    # elcid
    query = """
                        WITH LatestTest AS (
                        SELECT MAX(date) AS max_date
                        FROM offline_test_data
                        WHERE diagnostic_test_id = 8
                    )
                    SELECT 
                        otd.*, 
                        assc.name AS subcomponent_name, 
                        dt.name AS diagnostic_test_name
                    FROM 
                        offline_test_data otd
                    JOIN 
                        asset_subcomponent assc ON otd.subcomponent_id = assc.id
                    JOIN 
                        diagnostic_test dt ON otd.diagnostic_test_id = dt.id
                    WHERE 
                        dt.asset_category_id = 1
                        AND dt.id = 8
                        AND otd.date = (SELECT max_date FROM LatestTest)

                    ORDER BY 
                        otd.date DESC
                    """
    cursor.execute(query)
    elcid_data = cursor.fetchall()

    # bump
    query = """
                            WITH LatestTest AS (
                            SELECT MAX(date) AS max_date
                            FROM offline_test_data
                            WHERE diagnostic_test_id = 9
                        )
                        SELECT 
                            otd.*, 
                            assc.name AS subcomponent_name, 
                            dt.name AS diagnostic_test_name
                        FROM 
                            offline_test_data otd
                        JOIN 
                            asset_subcomponent assc ON otd.subcomponent_id = assc.id
                        JOIN 
                            diagnostic_test dt ON otd.diagnostic_test_id = dt.id
                        WHERE 
                            dt.asset_category_id = 1
                            AND dt.id = 9
                            AND otd.date = (SELECT max_date FROM LatestTest)

                        ORDER BY 
                            otd.date DESC
                        """
    cursor.execute(query)
    bump_test_data = cursor.fetchall()




    return insulation_resistance_data_cleaned, polarization_index_cleaned, wr_data, ddf_data, offpd_data, inspection_data, core_flux_data, elcid_data, bump_test_data

def fetch_online_test_data(cursor):
    # polarization index
    query = """
                WITH LatestTest AS (
                SELECT MAX(date) AS max_date
                FROM online_test_data
                WHERE diagnostic_test_id = 10
            )
            SELECT 
                otd.*, 
                assc.name AS subcomponent_name, 
                dt.name AS diagnostic_test_name
            FROM 
                online_test_data otd
            JOIN 
                asset_subcomponent assc ON otd.subcomponent_id = assc.id
            JOIN 
                diagnostic_test dt ON otd.diagnostic_test_id = dt.id
            WHERE 
                dt.asset_category_id = 1
                AND dt.id = 10
                AND otd.date = (SELECT max_date FROM LatestTest)

            ORDER BY 
                otd.date DESC
            """

    cursor.execute(query)
    rotor_flux_analysis_data = cursor.fetchall()
    # print(rotor_flux_analysis_data)

    query = """
        WITH LatestTest AS (
            SELECT MAX(date) AS max_date
            FROM online_test_data
            WHERE diagnostic_test_id = 11
        ),
        FilteredData AS (
            SELECT 
                otd.*, 
                assc.name AS subcomponent_name, 
                dt.name AS diagnostic_test_name,
                ROW_NUMBER() OVER (PARTITION BY otd.date ORDER BY otd.id DESC) AS rn
            FROM 
                online_test_data otd
            JOIN 
                asset_subcomponent assc ON otd.subcomponent_id = assc.id
            JOIN 
                diagnostic_test dt ON otd.diagnostic_test_id = dt.id
            WHERE 
                dt.asset_category_id = 1
                AND dt.id = 11
                AND otd.date = (SELECT max_date FROM LatestTest)
        )
        SELECT *
        FROM FilteredData
        WHERE rn <= 3
        ORDER BY date DESC, id 
    """

    cursor.execute(query)
    onlinepd_data = cursor.fetchall()

    #relace None with NA:
    onlinepd_data_cleaned = []
    for value in onlinepd_data:
        phase = []
        for item in value:
            if item is None:
                phase.append('N/A')
            else:
                phase.append(item)
        onlinepd_data_cleaned.append(phase)



    query = """
                        WITH LatestTest AS (
                        SELECT MAX(date) AS max_date
                        FROM online_test_data
                        WHERE diagnostic_test_id = 12
                    )
                    SELECT 
                        otd.*, 
                        assc.name AS subcomponent_name, 
                        dt.name AS diagnostic_test_name
                    FROM 
                        online_test_data otd
                    JOIN 
                        asset_subcomponent assc ON otd.subcomponent_id = assc.id
                    JOIN 
                        diagnostic_test dt ON otd.diagnostic_test_id = dt.id
                    WHERE 
                        dt.asset_category_id = 1
                        AND dt.id = 12
                        AND otd.date = (SELECT max_date FROM LatestTest)

                    ORDER BY 
                        otd.date DESC
                    """
    cursor.execute(query)
    vibration_analasys_data = cursor.fetchall()

    return rotor_flux_analysis_data, onlinepd_data_cleaned, vibration_analasys_data


#convert float
def float_to_registers(value):
    """Convert a float to two 16-bit registers (IEEE 754)."""
    # Pack the float into bytes, then unpack into two 16-bit integers
    packed = struct.pack('>f', value)  # Use '>f' for big-endian float
    return list(struct.unpack('>HH', packed))  # Unpack to two unsigned shorts

#string to asiic
def string_to_ascii_padded(input_string, length=10):
    ascii_values = [ord(char) for char in input_string]
    # Pad with zeros if necessary
    return ascii_values + [0] * (length - len(ascii_values))


# Function to create a Modbus data store
def create_data_store():
    cursor, conn = connect_to_db()
    asset_data = fetch_asset_data(cursor)

    asset_analysis = fetch_asset_analysis(cursor)
    component_analysis = fetch_asset_component_analysis(cursor)
    subcomponent_analysis = fetch_asset_subcomponent_analysis(cursor)
    fm_analysis = fetch_failure_mechanisms_analysis(cursor)
    offline_test_data = fetch_offline_test_data(cursor)
    online_test_data = fetch_online_test_data(cursor)
    # id,tag,function, manufactorer, yom, yoi, rated_voltage,feature_1,feature_2,feature_3,feature_4,feature_5,feature_6,feature_7,feature_8,feature_9,feature_10,feature_11,feature_12, lat, lon FROM asset")  # Modify as per your table and columns

    #prepare data to be exported - asset details
    asset_id = asset_data[0][0]
    tag = string_to_ascii_padded(asset_data[0][1], 10)
    function = string_to_ascii_padded(asset_data[0][2], 10)
    manufactorer = string_to_ascii_padded(asset_data[0][3], 10)
    yom = asset_data[0][4]
    yoi = asset_data[0][5]

    rated_voltage_list = float_to_registers(asset_data[0][6]) #2 registers

    # Prepare features as a list of padded ASCII values
    features = [string_to_ascii_padded(asset_data[0][i], 10) for i in range(7, 20)]

    lat = float_to_registers(asset_data[0][20])
    lon = float_to_registers(asset_data[0][21])


    #### asset analysis
    asset_id_analysis = asset_analysis[0][1]
    assessment_date = [string_to_ascii_padded(asset_analysis[0][0], 10)]
    risk_index = asset_analysis[0][2]
    health_index = asset_analysis[0][3]


    #component analysis
    component_1_name = [string_to_ascii_padded(component_analysis[0][0], 10)]
    component_1_hi = float_to_registers(component_analysis[0][1])
    component_2_name = [string_to_ascii_padded(component_analysis[1][0], 10)]
    component_2_hi = float_to_registers(component_analysis[1][1])
    component_3_name = [string_to_ascii_padded(component_analysis[2][0], 10)]
    component_3_hi = float_to_registers(component_analysis[2][1])

    #subcomponent analysis
    subcomponent_1_name = [string_to_ascii_padded(subcomponent_analysis[0][0], 10)]
    subcomponent_1_hi = float_to_registers(subcomponent_analysis[0][1])
    subcomponent_2_name = [string_to_ascii_padded(subcomponent_analysis[1][0], 10)]
    subcomponent_2_hi = float_to_registers(subcomponent_analysis[1][1])
    subcomponent_3_name = [string_to_ascii_padded(subcomponent_analysis[2][0], 10)]
    subcomponent_3_hi = float_to_registers(subcomponent_analysis[2][1])
    subcomponent_4_name = [string_to_ascii_padded(subcomponent_analysis[3][0], 10)]
    subcomponent_4_hi = float_to_registers(subcomponent_analysis[3][1])
    subcomponent_5_name = [string_to_ascii_padded(subcomponent_analysis[4][0], 10)]
    subcomponent_5_hi = float_to_registers(subcomponent_analysis[4][1])
    subcomponent_6_name = [string_to_ascii_padded(subcomponent_analysis[5][0], 10)]
    subcomponent_6_hi = float_to_registers(subcomponent_analysis[5][1])
    subcomponent_7_name = [string_to_ascii_padded(subcomponent_analysis[6][0], 10)]
    subcomponent_7_hi = float_to_registers(subcomponent_analysis[6][1])
    subcomponent_8_name = [string_to_ascii_padded(subcomponent_analysis[7][0], 10)]
    subcomponent_8_hi = float_to_registers(subcomponent_analysis[7][1])
    subcomponent_9_name = [string_to_ascii_padded(subcomponent_analysis[8][0], 10)]
    subcomponent_9_hi = float_to_registers(subcomponent_analysis[8][1])
    subcomponent_10_name = [string_to_ascii_padded(subcomponent_analysis[9][0], 10)]
    subcomponent_10_hi = float_to_registers(subcomponent_analysis[9][1])
    subcomponent_11_name = [string_to_ascii_padded(subcomponent_analysis[10][0], 10)]
    subcomponent_11_hi = float_to_registers(subcomponent_analysis[10][1])
    subcomponent_12_name = [string_to_ascii_padded(subcomponent_analysis[11][0], 10)]
    subcomponent_12_hi = float_to_registers(subcomponent_analysis[11][1])

    #failure mechanisms analysis
    failuremechanism_1_name = [string_to_ascii_padded(fm_analysis[1][0], 10)]
    failuremechanism_1_hi = float_to_registers(fm_analysis[1][1])
    failuremechanism_2_name = [string_to_ascii_padded(fm_analysis[2][0], 10)]
    failuremechanism_2_hi = float_to_registers(fm_analysis[2][1])
    failuremechanism_3_name = [string_to_ascii_padded(fm_analysis[3][0], 10)]
    failuremechanism_3_hi = float_to_registers(fm_analysis[3][1])
    failuremechanism_4_name = [string_to_ascii_padded(fm_analysis[4][0], 10)]
    failuremechanism_4_hi = float_to_registers(fm_analysis[4][1])
    failuremechanism_5_name = [string_to_ascii_padded(fm_analysis[5][0], 10)]
    failuremechanism_5_hi = float_to_registers(fm_analysis[5][1])
    failuremechanism_6_name = [string_to_ascii_padded(fm_analysis[6][0], 10)]
    failuremechanism_6_hi = float_to_registers(fm_analysis[6][1])
    failuremechanism_7_name = [string_to_ascii_padded(fm_analysis[7][0], 10)]
    failuremechanism_7_hi = float_to_registers(fm_analysis[7][1])
    failuremechanism_8_name = [string_to_ascii_padded(fm_analysis[8][0], 10)]
    failuremechanism_8_hi = float_to_registers(fm_analysis[8][1])
    failuremechanism_9_name = [string_to_ascii_padded(fm_analysis[9][0], 10)]
    failuremechanism_9_hi = float_to_registers(fm_analysis[9][1])
    failuremechanism_10_name = [string_to_ascii_padded(fm_analysis[10][0], 10)]
    failuremechanism_10_hi = float_to_registers(fm_analysis[10][1])
    failuremechanism_11_name = [string_to_ascii_padded(fm_analysis[11][0], 10)]
    failuremechanism_11_hi = float_to_registers(fm_analysis[11][1])
    failuremechanism_12_name = [string_to_ascii_padded(fm_analysis[11][0], 10)]
    failuremechanism_12_hi = float_to_registers(fm_analysis[11][1])
    failuremechanism_13_name = [string_to_ascii_padded(fm_analysis[12][0], 10)]
    failuremechanism_13_hi = float_to_registers(fm_analysis[12][1])
    failuremechanism_14_name = [string_to_ascii_padded(fm_analysis[13][0], 10)]
    failuremechanism_14_hi = float_to_registers(fm_analysis[13][1])
    failuremechanism_15_name = [string_to_ascii_padded(fm_analysis[14][0], 10)]
    failuremechanism_15_hi = float_to_registers(fm_analysis[14][1])
    failuremechanism_16_name = [string_to_ascii_padded(fm_analysis[15][0], 10)]
    failuremechanism_16_hi = float_to_registers(fm_analysis[15][1])

    #### online PD testing data

    #phase1
    onp_test_date_1 = [string_to_ascii_padded(online_test_data[1][0][1], 10)]
    phase_1 = [string_to_ascii_padded(online_test_data[1][0][5], 10)]
    qm_pos_1 = [string_to_ascii_padded(online_test_data[1][0][6], 10)]
    qm_neg_1 = [string_to_ascii_padded(online_test_data[1][0][7], 10)]
    identification_1 = [string_to_ascii_padded(online_test_data[1][0][8], 10)]
    ai_identification_1 = [string_to_ascii_padded(online_test_data[1][0][9], 10)]
    wind_temperature_1 = [string_to_ascii_padded(online_test_data[1][0][10], 10)]
    amb_temperature_1 = [string_to_ascii_padded(online_test_data[1][0][11], 10)]
    humidity_1 = [string_to_ascii_padded(online_test_data[1][0][12], 10)]
    active_load_1 = [string_to_ascii_padded(online_test_data[1][0][13], 10)]
    reactive_load_1 = [string_to_ascii_padded(online_test_data[1][0][14], 10)]


    # phase2
    onp_test_date_2 = [string_to_ascii_padded(online_test_data[1][1][1], 10)]
    phase_2 = [string_to_ascii_padded(online_test_data[1][1][5], 10)]
    qm_pos_2 = [string_to_ascii_padded(online_test_data[1][1][6], 10)]
    qm_neg_2 = [string_to_ascii_padded(online_test_data[1][1][7], 10)]
    identification_2 = [string_to_ascii_padded(online_test_data[1][1][8], 10)]
    ai_identification_2 = [string_to_ascii_padded(online_test_data[1][1][9], 10)]
    wind_temperature_2 = [string_to_ascii_padded(online_test_data[1][1][10], 10)]
    amb_temperature_2 = [string_to_ascii_padded(online_test_data[1][1][11], 10)]
    humidity_2 = [string_to_ascii_padded(online_test_data[1][1][12], 10)]
    active_load_2 = [string_to_ascii_padded(online_test_data[1][1][13], 10)]
    reactive_load_2 = [string_to_ascii_padded(online_test_data[1][1][14], 10)]

    # phase3
    onp_test_date_3 = [string_to_ascii_padded(online_test_data[1][2][1], 10)]
    phase_3 = [string_to_ascii_padded(online_test_data[1][2][5], 10)]
    qm_pos_3 = [string_to_ascii_padded(online_test_data[1][2][6], 10)]
    qm_neg_3 = [string_to_ascii_padded(online_test_data[1][2][7], 10)]
    identification_3 = [string_to_ascii_padded(online_test_data[1][2][8], 10)]
    ai_identification_3 = [string_to_ascii_padded(online_test_data[1][2][9], 10)]
    wind_temperature_3 = [string_to_ascii_padded(online_test_data[1][2][10], 10)]
    amb_temperature_3 = [string_to_ascii_padded(online_test_data[1][2][11], 10)]
    humidity_3 = [string_to_ascii_padded(online_test_data[1][2][12], 10)]
    active_load_3 = [string_to_ascii_padded(online_test_data[1][2][13], 10)]
    reactive_load_3 = [string_to_ascii_padded(online_test_data[1][2][14], 10)]

    #offline test data
    #insulation resistance

    #set default value to NA
    # set other value to NA
    # set three phase to NA
    ir_test_date = [string_to_ascii_padded('N/A', 10)]
    phase = [string_to_ascii_padded('N/A', 10)]
    applied_voltage = [string_to_ascii_padded('N/A', 10)]
    ir_30 = [string_to_ascii_padded('N/A', 10)]
    ir_60 = [string_to_ascii_padded('N/A', 10)]
    dar = [string_to_ascii_padded('N/A', 10)]
    cap = [string_to_ascii_padded('N/A', 10)]
    win_tem = [string_to_ascii_padded('N/A', 10)]
    amb_tem = [string_to_ascii_padded('N/A', 10)]
    humidity = [string_to_ascii_padded('N/A', 10)]
    ir_60s_40degrees = [string_to_ascii_padded('N/A', 10)]

    ir_test_date_1 = [string_to_ascii_padded('N/A', 10)]
    phase_1 = [string_to_ascii_padded('N/A', 10)]
    applied_voltage_1 = [string_to_ascii_padded('N/A', 10)]
    ir_30_1 = [string_to_ascii_padded('N/A', 10)]
    ir_60_1 = [string_to_ascii_padded('N/A', 10)]
    dar_1 = [string_to_ascii_padded('N/A', 10)]
    cap_1 = [string_to_ascii_padded('N/A', 10)]
    win_tem_1 = [string_to_ascii_padded('N/A', 10)]
    amb_tem_1 = [string_to_ascii_padded('N/A', 10)]
    humidity_1 = [string_to_ascii_padded('N/A', 10)]
    ir_60s_40degrees_1 = [string_to_ascii_padded('N/A', 10)]

    ir_test_date_2 = [string_to_ascii_padded('N/A', 10)]
    phase_2 = [string_to_ascii_padded('N/A', 10)]
    applied_voltage_2 = [string_to_ascii_padded('N/A', 10)]
    ir_30_2 = [string_to_ascii_padded('N/A', 10)]
    ir_60_2 = [string_to_ascii_padded('N/A', 10)]
    dar_2 = [string_to_ascii_padded('N/A', 10)]
    cap_2 = [string_to_ascii_padded('N/A', 10)]
    win_tem_2 = [string_to_ascii_padded('N/A', 10)]
    amb_tem_2 = [string_to_ascii_padded('N/A', 10)]
    humidity_2 = [string_to_ascii_padded('N/A', 10)]
    ir_60s_40degrees_2 = [string_to_ascii_padded('N/A', 10)]

    ir_test_date_3 = [string_to_ascii_padded('N/A', 10)]
    phase_3 = [string_to_ascii_padded('N/A', 10)]
    applied_voltage_3 = [string_to_ascii_padded('N/A', 10)]
    ir_30_3 = [string_to_ascii_padded('N/A', 10)]
    ir_60_3 = [string_to_ascii_padded('N/A', 10)]
    dar_3 = [string_to_ascii_padded('N/A', 10)]
    cap_3 = [string_to_ascii_padded('N/A', 10)]
    win_tem_3 = [string_to_ascii_padded('N/A', 10)]
    amb_tem_3 = [string_to_ascii_padded('N/A', 10)]
    humidity_3 = [string_to_ascii_padded('N/A', 10)]
    ir_60s_40degrees_3 = [string_to_ascii_padded('N/A', 10)]

    #check how many phases inserted:
    if len(offline_test_data[0]) ==1:
        ir_test_date = [string_to_ascii_padded(offline_test_data[0][0][1], 10)]
        phase = [string_to_ascii_padded(offline_test_data[0][0][5], 10)]
        applied_voltage = [string_to_ascii_padded(offline_test_data[0][0][6], 10)]
        ir_30 = [string_to_ascii_padded(offline_test_data[0][0][7], 10)]
        ir_60 = [string_to_ascii_padded(offline_test_data[0][0][8], 10)]
        dar = [string_to_ascii_padded(offline_test_data[0][0][9], 10)]
        cap = [string_to_ascii_padded(offline_test_data[0][0][10], 10)]
        win_tem = [string_to_ascii_padded(offline_test_data[0][0][11], 10)]
        amb_tem = [string_to_ascii_padded(offline_test_data[0][0][12], 10)]
        humidity = [string_to_ascii_padded(offline_test_data[0][0][13], 10)]
        ir_60s_40degrees = [string_to_ascii_padded(offline_test_data[0][0][14], 10)]
    if len(offline_test_data[0]) ==3:


        ir_test_date_1 = [string_to_ascii_padded(offline_test_data[0][0][1], 10)]
        phase_1 = [string_to_ascii_padded(offline_test_data[0][0][5], 10)]
        applied_voltage_1 = [string_to_ascii_padded(offline_test_data[0][0][6], 10)]
        ir_30_1 = [string_to_ascii_padded(offline_test_data[0][0][7], 10)]
        ir_60_1 = [string_to_ascii_padded(offline_test_data[0][0][8], 10)]
        dar_1 = [string_to_ascii_padded(offline_test_data[0][0][9], 10)]
        cap_1 = [string_to_ascii_padded(offline_test_data[0][0][10], 10)]
        win_tem_1 = [string_to_ascii_padded(offline_test_data[0][0][11], 10)]
        amb_tem_1 = [string_to_ascii_padded(offline_test_data[0][0][12], 10)]
        humidity_1 = [string_to_ascii_padded(offline_test_data[0][0][13], 10)]
        ir_60s_40degrees_1 = [string_to_ascii_padded(offline_test_data[0][0][14], 10)]

        ir_test_date_2 = [string_to_ascii_padded(offline_test_data[0][1][1], 10)]
        phase_2 = [string_to_ascii_padded(offline_test_data[0][1][5], 10)]
        applied_voltage_2 = [string_to_ascii_padded(offline_test_data[0][1][6], 10)]
        ir_30_2 = [string_to_ascii_padded(offline_test_data[0][1][7], 10)]
        ir_60_2 = [string_to_ascii_padded(offline_test_data[0][1][8], 10)]
        dar_2 = [string_to_ascii_padded(offline_test_data[0][1][9], 10)]
        cap_2 = [string_to_ascii_padded(offline_test_data[0][1][10], 10)]
        win_tem_2 = [string_to_ascii_padded(offline_test_data[0][1][11], 10)]
        amb_tem_2 = [string_to_ascii_padded(offline_test_data[0][1][12], 10)]
        humidity_2 = [string_to_ascii_padded(offline_test_data[0][1][13], 10)]
        ir_60s_40degrees_2 = [string_to_ascii_padded(offline_test_data[0][1][14], 10)]

        ir_test_date_3 = [string_to_ascii_padded(offline_test_data[0][2][1], 10)]
        phase_3 = [string_to_ascii_padded(offline_test_data[0][2][5], 10)]
        applied_voltage_3 = [string_to_ascii_padded(offline_test_data[0][2][6], 10)]
        ir_30_3 = [string_to_ascii_padded(offline_test_data[0][2][7], 10)]
        ir_60_3 = [string_to_ascii_padded(offline_test_data[0][2][8], 10)]
        dar_3 = [string_to_ascii_padded(offline_test_data[0][2][9], 10)]
        cap_3 = [string_to_ascii_padded(offline_test_data[0][2][10], 10)]
        win_tem_3 = [string_to_ascii_padded(offline_test_data[0][2][11], 10)]
        amb_tem_3 = [string_to_ascii_padded(offline_test_data[0][2][12], 10)]
        humidity_3 = [string_to_ascii_padded(offline_test_data[0][2][13], 10)]
        ir_60s_40degrees_3 = [string_to_ascii_padded(offline_test_data[0][2][14], 10)]

    #polarization_index
    # print(offline_test_data[1])

    # set default value to NA
    # set other value to NA
    # set three phase to NA
    pi_ir_test_date = [string_to_ascii_padded('N/A', 10)]
    pi_phase = [string_to_ascii_padded('N/A', 10)]
    pi_applied_voltage = [string_to_ascii_padded('N/A', 10)]
    pi_ir_30 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_60 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_300 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_600 = [string_to_ascii_padded('N/A', 10)]
    pi_dar = [string_to_ascii_padded('N/A', 10)]
    pi_pi = [string_to_ascii_padded('N/A', 10)]
    pi_cap = [string_to_ascii_padded('N/A', 10)]
    pi_win_tem = [string_to_ascii_padded('N/A', 10)]
    pi_amb_tem = [string_to_ascii_padded('N/A', 10)]
    pi_humidity = [string_to_ascii_padded('N/A', 10)]
    pi_ir_60s_40degrees = [string_to_ascii_padded('N/A', 10)]

    pi_ir_test_date_1 = [string_to_ascii_padded('N/A', 10)]
    pi_phase_1 = [string_to_ascii_padded('N/A', 10)]
    pi_applied_voltage_1 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_30_1 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_60_1 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_300_1 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_600_1 = [string_to_ascii_padded('N/A', 10)]
    pi_dar_1 = [string_to_ascii_padded('N/A', 10)]
    pi_pi_1 = [string_to_ascii_padded('N/A', 10)]
    pi_cap_1 = [string_to_ascii_padded('N/A', 10)]
    pi_win_tem_1 = [string_to_ascii_padded('N/A', 10)]
    pi_amb_tem_1 = [string_to_ascii_padded('N/A', 10)]
    pi_humidity_1 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_60s_40degrees_1 = [string_to_ascii_padded('N/A', 10)]

    pi_ir_test_date_2 = [string_to_ascii_padded('N/A', 10)]
    pi_phase_2 = [string_to_ascii_padded('N/A', 10)]
    pi_applied_voltage_2 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_30_2 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_60_2 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_300_2 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_600_2 = [string_to_ascii_padded('N/A', 10)]
    pi_dar_2 = [string_to_ascii_padded('N/A', 10)]
    pi_pi_2 = [string_to_ascii_padded('N/A', 10)]
    pi_cap_2 = [string_to_ascii_padded('N/A', 10)]
    pi_win_tem_2 = [string_to_ascii_padded('N/A', 10)]
    pi_amb_tem_2 = [string_to_ascii_padded('N/A', 10)]
    pi_humidity_2 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_60s_40degrees_2 = [string_to_ascii_padded('N/A', 10)]

    pi_ir_test_date_3 = [string_to_ascii_padded('N/A', 10)]
    pi_phase_3 = [string_to_ascii_padded('N/A', 10)]
    pi_applied_voltage_3 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_30_3 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_60_3 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_300_3 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_600_3 = [string_to_ascii_padded('N/A', 10)]
    pi_dar_3 = [string_to_ascii_padded('N/A', 10)]
    pi_pi_3 = [string_to_ascii_padded('N/A', 10)]
    pi_cap_3 = [string_to_ascii_padded('N/A', 10)]
    pi_win_tem_3 = [string_to_ascii_padded('N/A', 10)]
    pi_amb_tem_3 = [string_to_ascii_padded('N/A', 10)]
    pi_humidity_3 = [string_to_ascii_padded('N/A', 10)]
    pi_ir_60s_40degrees_3 = [string_to_ascii_padded('N/A', 10)]

    # check how many phases inserted:
    if len(offline_test_data[1]) == 1:
        pi_ir_test_date = [string_to_ascii_padded(offline_test_data[1][0][1], 10)]
        pi_phase = [string_to_ascii_padded(offline_test_data[1][0][5], 10)]
        pi_applied_voltage = [string_to_ascii_padded(offline_test_data[1][0][6], 10)]
        pi_ir_30 = [string_to_ascii_padded(offline_test_data[1][0][7], 10)]
        pi_ir_60 = [string_to_ascii_padded(offline_test_data[1][0][8], 10)]
        pi_ir_300 = [string_to_ascii_padded(offline_test_data[1][0][9], 10)]
        pi_ir_600 = [string_to_ascii_padded(offline_test_data[1][0][10], 10)]
        pi_dar = [string_to_ascii_padded(offline_test_data[1][0][11], 10)]
        pi_pi = [string_to_ascii_padded(offline_test_data[1][0][12], 10)]
        pi_cap = [string_to_ascii_padded(offline_test_data[1][0][13], 10)]
        pi_win_tem = [string_to_ascii_padded(offline_test_data[1][0][14], 10)]
        pi_amb_tem = [string_to_ascii_padded(offline_test_data[1][0][15], 10)]
        pi_humidity = [string_to_ascii_padded(offline_test_data[1][0][16], 10)]
        pi_ir_60s_40degrees = [string_to_ascii_padded(offline_test_data[1][0][17], 10)]
    if len(offline_test_data[1]) == 3:
        pi_ir_test_date_1 = [string_to_ascii_padded(offline_test_data[1][0][1], 10)]
        pi_phase_1 = [string_to_ascii_padded(offline_test_data[1][0][5], 10)]
        pi_applied_voltage_1 = [string_to_ascii_padded(offline_test_data[1][0][6], 10)]
        pi_ir_30_1 = [string_to_ascii_padded(offline_test_data[1][0][7], 10)]
        pi_ir_60_1 = [string_to_ascii_padded(offline_test_data[1][0][8], 10)]
        pi_ir_300_1 = [string_to_ascii_padded(offline_test_data[1][0][9], 10)]
        pi_ir_600_1 = [string_to_ascii_padded(offline_test_data[1][0][10], 10)]
        pi_dar_1 = [string_to_ascii_padded(offline_test_data[1][0][11], 10)]
        pi_pi_1 = [string_to_ascii_padded(offline_test_data[1][0][12], 10)]
        pi_cap_1 = [string_to_ascii_padded(offline_test_data[1][0][13], 10)]
        pi_win_tem_1 = [string_to_ascii_padded(offline_test_data[1][0][14], 10)]
        pi_amb_tem_1 = [string_to_ascii_padded(offline_test_data[1][0][15], 10)]
        pi_humidity_1 = [string_to_ascii_padded(offline_test_data[1][0][16], 10)]
        pi_ir_60s_40degrees_1 = [string_to_ascii_padded(offline_test_data[1][0][17], 10)]

        pi_ir_test_date_2 = [string_to_ascii_padded(offline_test_data[1][1][1], 10)]
        pi_phase_2 = [string_to_ascii_padded(offline_test_data[1][1][5], 10)]
        pi_applied_voltage_2 = [string_to_ascii_padded(offline_test_data[1][1][6], 10)]
        pi_ir_30_2 = [string_to_ascii_padded(offline_test_data[1][1][7], 10)]
        pi_ir_60_2 = [string_to_ascii_padded(offline_test_data[1][1][8], 10)]
        pi_ir_300_2 = [string_to_ascii_padded(offline_test_data[1][1][9], 10)]
        pi_ir_600_2 = [string_to_ascii_padded(offline_test_data[1][1][10], 10)]
        pi_dar_2 = [string_to_ascii_padded(offline_test_data[1][1][11], 10)]
        pi_pi_2 = [string_to_ascii_padded(offline_test_data[1][1][12], 10)]
        pi_cap_2 = [string_to_ascii_padded(offline_test_data[1][1][13], 10)]
        pi_win_tem_2 = [string_to_ascii_padded(offline_test_data[1][1][14], 10)]
        pi_amb_tem_2 = [string_to_ascii_padded(offline_test_data[1][1][15], 10)]
        pi_humidity_2 = [string_to_ascii_padded(offline_test_data[1][1][16], 10)]
        pi_ir_60s_40degrees_2 = [string_to_ascii_padded(offline_test_data[1][1][17], 10)]

        pi_ir_test_date_3 = [string_to_ascii_padded(offline_test_data[1][2][1], 10)]
        pi_phase_3 = [string_to_ascii_padded(offline_test_data[1][2][5], 10)]
        pi_applied_voltage_3 = [string_to_ascii_padded(offline_test_data[1][2][6], 10)]
        pi_ir_30_3 = [string_to_ascii_padded(offline_test_data[1][2][7], 10)]
        pi_ir_60_3 = [string_to_ascii_padded(offline_test_data[1][2][8], 10)]
        pi_ir_300_3 = [string_to_ascii_padded(offline_test_data[1][2][9], 10)]
        pi_ir_600_3 = [string_to_ascii_padded(offline_test_data[1][2][10], 10)]
        pi_dar_3 = [string_to_ascii_padded(offline_test_data[1][2][11], 10)]
        pi_pi_3 = [string_to_ascii_padded(offline_test_data[1][2][12], 10)]
        pi_cap_3 = [string_to_ascii_padded(offline_test_data[1][2][13], 10)]
        pi_win_tem_3 = [string_to_ascii_padded(offline_test_data[1][2][14], 10)]
        pi_amb_tem_3 = [string_to_ascii_padded(offline_test_data[1][2][15], 10)]
        pi_humidity_3 = [string_to_ascii_padded(offline_test_data[1][2][16], 10)]
        pi_ir_60s_40degrees_3 = [string_to_ascii_padded(offline_test_data[1][2][17], 10)]






    store = ModbusSlaveContext(
        hr=ModbusSparseDataBlock({
            1000: [asset_id],  # asset_id
            **{1001 + i: [tag[i]] for i in range(10)},  # Tag values
            **{1011 + i: [function[i]] for i in range(10)},  # Function values
            **{1021 + i: [manufactorer[i]] for i in range(10)},  # Manufacturer values
            1031: [yom],  # Year of Manufacture
            1032: [yoi],  # Year of Installation
            1033: [rated_voltage_list[0]],  # rated_voltage (first part of the float)
            1034: [rated_voltage_list[1]],  # rated_voltage (second part of the float)
            **{1035 + i: [features[0][i]] for i in range(10)},  # feature 1
            **{1045 + i: [features[1][i]] for i in range(10)},  # feature 2
            **{1055 + i: [features[2][i]] for i in range(10)},  # feature 3
            **{1065 + i: [features[3][i]] for i in range(10)},  # feature 4
            **{1075 + i: [features[4][i]] for i in range(10)},  # feature 5
            **{1085 + i: [features[5][i]] for i in range(10)},  # feature 6
            **{1095 + i: [features[6][i]] for i in range(10)},  # feature 7
            **{1105 + i: [features[7][i]] for i in range(10)},  # feature 8
            **{1115 + i: [features[8][i]] for i in range(10)},  # feature 9
            **{1125 + i: [features[9][i]] for i in range(10)},  # feature 10
            **{1135 + i: [features[10][i]] for i in range(10)},  # feature 11
            **{1145 + i: [features[11][i]] for i in range(10)},  # feature 12
            **{1155 + i: [features[12][i]] for i in range(10)},  # feature 13
            1165: [lat[0]],  # lat (first part of the float)
            1166: [lat[1]],  # lat (second part of the float)
            1167: [lon[0]],  # lon (first part of the float)
            1168: [lon[1]],  # lon (second part of the float)
            #asset_analysis
            1169: [asset_id_analysis],
            ** {1170 + i: [assessment_date[0][i]] for i in range(10)},  # Tag values
            1180: [risk_index],
            1181: [health_index],
            #component analyssi
            ** {1182 + i: [component_1_name[0][i]] for i in range(10)},  # feature 13
            1192: [component_1_hi[0]],  # lat (first part of the float)
            1193: [component_1_hi[1]],  # lat (second part of the float)
            **{1194 + i: [component_2_name[0][i]] for i in range(10)},  # feature 13
            1204: [component_2_hi[0]],  # lat (first part of the float)
            1205: [component_2_hi[1]],  # lat (second part of the float)
            **{1206 + i: [component_3_name[0][i]] for i in range(10)},  # feature 13
            1216: [component_3_hi[0]],  # lat (first part of the float)
            1217: [component_3_hi[1]],  # lat (second part of the float)
            #subcomponent analsysis
            ** {1218 + i: [subcomponent_1_name[0][i]] for i in range(10)},  # feature 13
            1228: [subcomponent_1_hi[0]],  # lat (first part of the float)
            1229: [subcomponent_1_hi[1]],  # lat (second part of the float)
            ** {1230 + i: [subcomponent_2_name[0][i]] for i in range(10)},  # feature 13
            1240: [subcomponent_2_hi[0]],  # lat (first part of the float)
            1241: [subcomponent_2_hi[1]],  # lat (second part of the float)
            ** {1242 + i: [subcomponent_3_name[0][i]] for i in range(10)},  # feature 13
            1252: [subcomponent_3_hi[0]],  # lat (first part of the float)
            1253: [subcomponent_3_hi[1]],  # lat (second part of the float)
            ** {1254 + i: [subcomponent_4_name[0][i]] for i in range(10)},  # feature 13
            1264: [subcomponent_4_hi[0]],  # lat (first part of the float)
            1265: [subcomponent_4_hi[1]],  # lat (second part of the float)
            ** {1266 + i: [subcomponent_5_name[0][i]] for i in range(10)},  # feature 13
            1276: [subcomponent_5_hi[0]],  # lat (first part of the float)
            1277: [subcomponent_5_hi[1]],  # lat (second part of the float)
            ** {1278 + i: [subcomponent_6_name[0][i]] for i in range(10)},  # feature 13
            1288: [subcomponent_6_hi[0]],  # lat (first part of the float)
            1289: [subcomponent_6_hi[1]],  # lat (second part of the float)
            ** {1290 + i: [subcomponent_7_name[0][i]] for i in range(10)},  # feature 13
            1300: [subcomponent_7_hi[0]],  # lat (first part of the float)
            1301: [subcomponent_7_hi[1]],  # lat (second part of the float)
            ** {1302 + i: [subcomponent_8_name[0][i]] for i in range(10)},  # feature 13
            1312: [subcomponent_8_hi[0]],  # lat (first part of the float)
            1313: [subcomponent_8_hi[1]],  # lat (second part of the float)
            ** {1314 + i: [subcomponent_9_name[0][i]] for i in range(10)},  # feature 13
            1324: [subcomponent_9_hi[0]],  # lat (first part of the float)
            1325: [subcomponent_9_hi[1]],  # lat (second part of the float)
            ** {1326 + i: [subcomponent_10_name[0][i]] for i in range(10)},  # feature 13
            1336: [subcomponent_10_hi[0]],  # lat (first part of the float)
            1337: [subcomponent_10_hi[1]],  # lat (second part of the float)
            ** {1338 + i: [subcomponent_11_name[0][i]] for i in range(10)},  # feature 13
            1348: [subcomponent_11_hi[0]],  # lat (first part of the float)
            1349: [subcomponent_11_hi[1]],  # lat (second part of the float)
            ** {1350 + i: [subcomponent_12_name[0][i]] for i in range(10)},  # feature 13
            1360: [subcomponent_12_hi[0]],  # lat (first part of the float)
            1361: [subcomponent_12_hi[1]],  # lat (second part of the float)
            #failure mechanisms
            ** {1362 + i: [failuremechanism_1_name[0][i]] for i in range(10)},  # feature 13
            1372: [failuremechanism_1_hi[0]],  # lat (first part of the float)
            1373: [failuremechanism_1_hi[1]],  # lat (second part of the float)
            ** {1374 + i: [failuremechanism_2_name[0][i]] for i in range(10)},  # feature 13
            1384: [failuremechanism_2_hi[0]],  # lat (first part of the float)
            1385: [failuremechanism_2_hi[1]],  # lat (second part of the float)
            ** {1386 + i: [failuremechanism_3_name[0][i]] for i in range(10)},  # feature 13
            1396: [failuremechanism_3_hi[0]],  # lat (first part of the float)
            1397: [failuremechanism_3_hi[1]],  # lat (second part of the float)
            ** {1398 + i: [failuremechanism_4_name[0][i]] for i in range(10)},  # feature 13
            1408: [failuremechanism_4_hi[0]],  # lat (first part of the float)
            1409: [failuremechanism_4_hi[1]],  # lat (second part of the float)
            ** {1410 + i: [failuremechanism_5_name[0][i]] for i in range(10)},  # feature 13
            1420: [failuremechanism_5_hi[0]],  # lat (first part of the float)
            1421: [failuremechanism_5_hi[1]],  # lat (second part of the float)
            ** {1422 + i: [failuremechanism_6_name[0][i]] for i in range(10)},  # feature 13
            1432: [failuremechanism_6_hi[0]],  # lat (first part of the float)
            1433: [failuremechanism_6_hi[1]],  # lat (second part of the float)
            ** {1434 + i: [failuremechanism_7_name[0][i]] for i in range(10)},  # feature 13
            1444: [failuremechanism_7_hi[0]],  # lat (first part of the float)
            1445: [failuremechanism_7_hi[1]],  # lat (second part of the float)
            ** {1446 + i: [failuremechanism_8_name[0][i]] for i in range(10)},  # feature 13
            1456: [failuremechanism_8_hi[0]],  # lat (first part of the float)
            1457: [failuremechanism_8_hi[1]],  # lat (second part of the float)
            ** {1458 + i: [failuremechanism_9_name[0][i]] for i in range(10)},  # feature 13
            1468: [failuremechanism_9_hi[0]],  # lat (first part of the float)
            1469: [failuremechanism_9_hi[1]],  # lat (second part of the float)
            ** {1470 + i: [failuremechanism_10_name[0][i]] for i in range(10)},  # feature 13
            1480: [failuremechanism_10_hi[0]],  # lat (first part of the float)
            1481: [failuremechanism_10_hi[1]],  # lat (second part of the float)
            ** {1482 + i: [failuremechanism_11_name[0][i]] for i in range(10)},  # feature 13
            1492: [failuremechanism_11_hi[0]],  # lat (first part of the float)
            1493: [failuremechanism_11_hi[1]],  # lat (second part of the float)
            ** {1494 + i: [failuremechanism_12_name[0][i]] for i in range(10)},  # feature 13
            1504: [failuremechanism_12_hi[0]],  # lat (first part of the float)
            1505: [failuremechanism_12_hi[1]],  # lat (second part of the float)
            ** {1506 + i: [failuremechanism_13_name[0][i]] for i in range(10)},  # feature 13
            1516: [failuremechanism_13_hi[0]],  # lat (first part of the float)
            1517: [failuremechanism_13_hi[1]],  # lat (second part of the float)
            ** {1518 + i: [failuremechanism_14_name[0][i]] for i in range(10)},  # feature 13
            1528: [failuremechanism_14_hi[0]],  # lat (first part of the float)
            1529: [failuremechanism_14_hi[1]],  # lat (second part of the float)
            ** {1530 + i: [failuremechanism_15_name[0][i]] for i in range(10)},  # feature 13
            1540: [failuremechanism_15_hi[0]],  # lat (first part of the float)
            1541: [failuremechanism_15_hi[1]],  # lat (second part of the float)
            ** {1542 + i: [failuremechanism_16_name[0][i]] for i in range(10)},  # feature 13
            1552: [failuremechanism_16_hi[0]],  # lat (first part of the float)
            1553: [failuremechanism_16_hi[1]],  # lat (second part of the float)

            #onlinePD
            ** {1554 + i: [onp_test_date_1[0][i]] for i in range(10)},  # feature 13
            **{1564 + i: [phase_1[0][i]] for i in range(10)},
            **{1574 + i: [qm_pos_1[0][i]] for i in range(10)},
            **{1584 + i: [qm_neg_1[0][i]] for i in range(10)},
            **{1594 + i: [identification_1[0][i]] for i in range(10)},
            **{1604 + i: [ai_identification_1[0][i]] for i in range(10)},
            **{1614 + i: [wind_temperature_1[0][i]] for i in range(10)},
            **{1624 + i: [amb_temperature_1[0][i]] for i in range(10)},
            **{1634 + i: [humidity_1[0][i]] for i in range(10)},
            **{1644 + i: [active_load_1[0][i]] for i in range(10)},
            **{1654 + i: [reactive_load_1[0][i]] for i in range(10)},

            **{1664 + i: [onp_test_date_2[0][i]] for i in range(10)},  # feature 13
            **{1674 + i: [phase_2[0][i]] for i in range(10)},
            **{1684 + i: [qm_pos_2[0][i]] for i in range(10)},
            **{1694 + i: [qm_neg_2[0][i]] for i in range(10)},
            **{1704 + i: [identification_2[0][i]] for i in range(10)},
            **{1714 + i: [ai_identification_2[0][i]] for i in range(10)},
            **{1724 + i: [wind_temperature_2[0][i]] for i in range(10)},
            **{1734 + i: [amb_temperature_2[0][i]] for i in range(10)},
            **{1744 + i: [humidity_2[0][i]] for i in range(10)},
            **{1754 + i: [active_load_2[0][i]] for i in range(10)},
            **{1764 + i: [reactive_load_2[0][i]] for i in range(10)},

            **{1774 + i: [onp_test_date_3[0][i]] for i in range(10)},  # feature 13
            **{1784 + i: [phase_3[0][i]] for i in range(10)},
            **{1794 + i: [qm_pos_3[0][i]] for i in range(10)},
            **{1804 + i: [qm_neg_3[0][i]] for i in range(10)},
            **{1814 + i: [identification_3[0][i]] for i in range(10)},
            **{1824 + i: [ai_identification_3[0][i]] for i in range(10)},
            **{1834 + i: [wind_temperature_3[0][i]] for i in range(10)},
            **{1844 + i: [amb_temperature_3[0][i]] for i in range(10)},
            **{1854 + i: [humidity_3[0][i]] for i in range(10)},
            **{1864 + i: [active_load_3[0][i]] for i in range(10)},
            **{1874 + i: [reactive_load_3[0][i]] for i in range(10)},

            #offline test data - Insulation resistance
            #three phase
            **{1884 + i: [ir_test_date[0][i]] for i in range(10)},  # feature 13
            **{1894 + i: [phase[0][i]] for i in range(10)},
            **{1904 + i: [applied_voltage[0][i]] for i in range(10)},
            **{1914 + i: [ir_30[0][i]] for i in range(10)},
            **{1924 + i: [ir_60[0][i]] for i in range(10)},
            **{1934 + i: [dar[0][i]] for i in range(10)},
            **{1944 + i: [cap[0][i]] for i in range(10)},
            **{1954 + i: [win_tem[0][i]] for i in range(10)},
            **{1964 + i: [amb_tem[0][i]] for i in range(10)},
            **{1974 + i: [humidity[0][i]] for i in range(10)},
            **{1984 + i: [ir_60s_40degrees[0][i]] for i in range(10)},

            #phase 1
            **{1994 + i: [ir_test_date_1[0][i]] for i in range(10)},  # feature 13
            **{2004 + i: [phase_1[0][i]] for i in range(10)},
            **{2014 + i: [applied_voltage_1[0][i]] for i in range(10)},
            **{2024 + i: [ir_30_1[0][i]] for i in range(10)},
            **{2034 + i: [ir_60_1[0][i]] for i in range(10)},
            **{2044 + i: [dar_1[0][i]] for i in range(10)},
            **{2054 + i: [cap_1[0][i]] for i in range(10)},
            **{2064 + i: [win_tem_1[0][i]] for i in range(10)},
            **{2074 + i: [amb_tem_1[0][i]] for i in range(10)},
            **{2084 + i: [humidity_1[0][i]] for i in range(10)},
            **{2094 + i: [ir_60s_40degrees_1[0][i]] for i in range(10)},

            #phase 2
            **{2104 + i: [ir_test_date_2[0][i]] for i in range(10)},  # feature 13
            **{2114 + i: [phase_2[0][i]] for i in range(10)},
            **{2124 + i: [applied_voltage_2[0][i]] for i in range(10)},
            **{2134 + i: [ir_30_2[0][i]] for i in range(10)},
            **{2144 + i: [ir_60_2[0][i]] for i in range(10)},
            **{2154 + i: [dar_2[0][i]] for i in range(10)},
            **{2164 + i: [cap_2[0][i]] for i in range(10)},
            **{2174 + i: [win_tem_2[0][i]] for i in range(10)},
            **{2184 + i: [amb_tem_2[0][i]] for i in range(10)},
            **{2194 + i: [humidity_2[0][i]] for i in range(10)},
            **{2204 + i: [ir_60s_40degrees_2[0][i]] for i in range(10)},

            # phase 3
            **{2214 + i: [ir_test_date_3[0][i]] for i in range(10)},  # feature 13
            **{2224 + i: [phase_3[0][i]] for i in range(10)},
            **{2234 + i: [applied_voltage_3[0][i]] for i in range(10)},
            **{2244 + i: [ir_30_3[0][i]] for i in range(10)},
            **{2254 + i: [ir_60_3[0][i]] for i in range(10)},
            **{2264 + i: [dar_3[0][i]] for i in range(10)},
            **{2274 + i: [cap_3[0][i]] for i in range(10)},
            **{2284 + i: [win_tem_3[0][i]] for i in range(10)},
            **{2294 + i: [amb_tem_3[0][i]] for i in range(10)},
            **{2304 + i: [humidity_3[0][i]] for i in range(10)},
            **{2314 + i: [ir_60s_40degrees_3[0][i]] for i in range(10)},

            # offline test data - PI
            #three phase
            **{2324 + i: [pi_ir_test_date[0][i]] for i in range(10)},
            **{2334 + i: [pi_phase[0][i]] for i in range(10)},
            **{2344 + i: [pi_applied_voltage[0][i]] for i in range(10)},
            **{2354 + i: [pi_ir_30[0][i]] for i in range(10)},
            **{2364 + i: [pi_ir_60[0][i]] for i in range(10)},
            **{2374 + i: [pi_ir_300[0][i]] for i in range(10)},
            **{2384 + i: [pi_ir_600[0][i]] for i in range(10)},
            **{2394 + i: [pi_dar[0][i]] for i in range(10)},
            **{2404 + i: [pi_pi[0][i]] for i in range(10)},
            **{2414 + i: [pi_cap[0][i]] for i in range(10)},
            **{2424 + i: [pi_win_tem[0][i]] for i in range(10)},
            **{2434 + i: [pi_amb_tem[0][i]] for i in range(10)},
            **{2444 + i: [pi_humidity[0][i]] for i in range(10)},
            **{2454 + i: [pi_ir_60s_40degrees[0][i]] for i in range(10)},
            #phase 1
            **{2464 + i: [pi_ir_test_date_1[0][i]] for i in range(10)},
            **{2474 + i: [pi_phase_1[0][i]] for i in range(10)},
            **{2484 + i: [pi_applied_voltage_1[0][i]] for i in range(10)},
            **{2494 + i: [pi_ir_30_1[0][i]] for i in range(10)},
            **{2504 + i: [pi_ir_60_1[0][i]] for i in range(10)},
            **{2514 + i: [pi_ir_300_1[0][i]] for i in range(10)},
            **{2524 + i: [pi_ir_600_1[0][i]] for i in range(10)},
            **{2534 + i: [pi_dar_1[0][i]] for i in range(10)},
            **{2544 + i: [pi_pi_1[0][i]] for i in range(10)},
            **{2554 + i: [pi_cap_1[0][i]] for i in range(10)},
            **{2564 + i: [pi_win_tem_1[0][i]] for i in range(10)},
            **{2574 + i: [pi_amb_tem_1[0][i]] for i in range(10)},
            **{2584 + i: [pi_humidity_1[0][i]] for i in range(10)},
            **{2594 + i: [pi_ir_60s_40degrees_1[0][i]] for i in range(10)},

            # phase 2
            **{2604 + i: [pi_ir_test_date_2[0][i]] for i in range(10)},
            **{2614 + i: [pi_phase_2[0][i]] for i in range(10)},
            **{2624 + i: [pi_applied_voltage_2[0][i]] for i in range(10)},
            **{2634 + i: [pi_ir_30_2[0][i]] for i in range(10)},
            **{2644 + i: [pi_ir_60_2[0][i]] for i in range(10)},
            **{2654 + i: [pi_ir_300_2[0][i]] for i in range(10)},
            **{2664 + i: [pi_ir_600_2[0][i]] for i in range(10)},
            **{2674 + i: [pi_dar_2[0][i]] for i in range(10)},
            **{2684 + i: [pi_pi_2[0][i]] for i in range(10)},
            **{2694 + i: [pi_cap_2[0][i]] for i in range(10)},
            **{2704 + i: [pi_win_tem_2[0][i]] for i in range(10)},
            **{2714 + i: [pi_amb_tem_2[0][i]] for i in range(10)},
            **{2724 + i: [pi_humidity_2[0][i]] for i in range(10)},
            **{2734 + i: [pi_ir_60s_40degrees_2[0][i]] for i in range(10)},

            # phase 3
            **{2744 + i: [pi_ir_test_date_3[0][i]] for i in range(10)},
            **{2754 + i: [pi_phase_3[0][i]] for i in range(10)},
            **{2764 + i: [pi_applied_voltage_3[0][i]] for i in range(10)},
            **{2774 + i: [pi_ir_30_3[0][i]] for i in range(10)},
            **{2784 + i: [pi_ir_60_3[0][i]] for i in range(10)},
            **{2794 + i: [pi_ir_300_3[0][i]] for i in range(10)},
            **{2804 + i: [pi_ir_600_3[0][i]] for i in range(10)},
            **{2814 + i: [pi_dar_3[0][i]] for i in range(10)},
            **{2824 + i: [pi_pi_3[0][i]] for i in range(10)},
            **{2834 + i: [pi_cap_3[0][i]] for i in range(10)},
            **{2844 + i: [pi_win_tem_3[0][i]] for i in range(10)},
            **{2854 + i: [pi_amb_tem_3[0][i]] for i in range(10)},
            **{2864 + i: [pi_humidity_3[0][i]] for i in range(10)},
            **{2874 + i: [pi_ir_60s_40degrees_3[0][i]] for i in range(10)},

        })
    )



    conn.close()
    logging.debug("Data store values after population: %s", store.getValues(3, 999, 1873))  # Read back the values

    print('store',store)
    return store

# Start Modbus server
# Start Modbus server
def run_server():
    store = create_data_store()
    context = ModbusServerContext(slaves={1: store}, single=False)
    # server = ModbusTcpServer(context)
    # server = ModbusTcpServer(store, framer=ModbusRtuFramer)

    try:
        logging.info("Starting Modbus server...")
        StartTcpServer(context, address=("0.0.0.0", 502))  # Start the server

        # server.serve_forever()
    except Exception as e:
        logging.error("Server encountered an error: %s", e)

if __name__ == "__main__":
    # Run the server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    logging.info("Modbus server is running...")
