import time

import pandas as pd
import mysql.connector

from functions.analyse_data_mysql import analyse_data
from functions.assess_condition_mysql import assess_condition

# Monitoring details
Monitoring = 'Yes'
monitoring_type = 'Techimp-PDScope'
connection_type = 'MQTT'

#asset details
asset_id = 87
subcomponet_id =2
diagnostic_test_id  =11


# Load the Excel file
file_path = 'C:/Users/inwave/Downloads/RE_ Health Index for the Rotation Machine/STG_3305/data.xlsx'


# Load the data from each sheet (ch1, ch2, ch3)
ch1_data = pd.read_excel(file_path, sheet_name='ch1')
ch2_data = pd.read_excel(file_path, sheet_name='ch2')
ch3_data = pd.read_excel(file_path, sheet_name='ch3')

# Extract the lists of each column

date_list_ch1_or = ch1_data['Date'].tolist()  # Assuming 'Date' is one of the columns
date_list_ch1 = [ item.strftime('%d/%m/%Y %H:%M') for item in date_list_ch1_or]

date_list_notime_ch1_or = [item.date() for item in date_list_ch1_or]
date_list_notime_ch1 = [ item.strftime('%d/%m/%Y') for item in date_list_notime_ch1_or]


phase_tag_list_ch1 = ['u' for item in date_list_ch1]
qmax95_list_ch1 = ch1_data['QMax95'].tolist()  # Assuming 'QMax95' is one of the columns
nw_list_ch1 = ch1_data['Nw'].tolist()  # Assuming 'Nw' is one of the columns
synch_freq_list_ch1 = ch1_data['Sync Frequency'].tolist()  #

date_list_ch2_or = ch2_data['Date'].tolist()  # Assuming 'Date' is one of the columns
date_list_ch2 = [ item.strftime('%d/%m/%Y %H:%M') for item in date_list_ch2_or]

date_list_notime_ch2_or = [item.date() for item in date_list_ch2_or]
date_list_notime_ch2 = [ item.strftime('%d/%m/%Y') for item in date_list_notime_ch2_or]

phase_tag_list_ch2 = ['v' for item in date_list_ch2]
qmax95_list_ch2 = ch2_data['QMax95'].tolist()  # Assuming 'QMax95' is one of the columns
nw_list_ch2 = ch2_data['Nw'].tolist()  # Assuming 'Nw' is one of the columns
synch_freq_list_ch2 = ch2_data['Sync Frequency'].tolist()  #

date_list_ch3_or = ch3_data['Date'].tolist()  # Assuming 'Date' is one of the columns
date_list_ch3 = [ item.strftime('%d/%m/%Y %H:%M') for item in date_list_ch3_or]

date_list_notime_ch3_or = [item.date() for item in date_list_ch3_or]
date_list_notime_ch3 = [ item.strftime('%d/%m/%Y') for item in date_list_notime_ch3_or]

phase_tag_list_ch3 = ['w' for item in date_list_ch3]
qmax95_list_ch3 = ch3_data['QMax95'].tolist()  # Assuming 'QMax95' is one of the columns
nw_list_ch3 = ch3_data['Nw'].tolist()  # Assuming 'Nw' is one of the columns
synch_freq_list_ch3 = ch3_data['Sync Frequency'].tolist()







# insert data into the db and perform analysis and assessment
for index, row in enumerate(date_list_ch1):
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
    data = [
        (date_list_notime_ch1[index], asset_id,subcomponet_id,diagnostic_test_id, phase_tag_list_ch1[index], round(qmax95_list_ch1[index]*1000,2), round(nw_list_ch1[index],2),round(synch_freq_list_ch1[index]), Monitoring, monitoring_type, connection_type, date_list_ch1[index]),
        (date_list_notime_ch2[index], asset_id,subcomponet_id,diagnostic_test_id, phase_tag_list_ch2[index], round(qmax95_list_ch2[index]*100,2), round(nw_list_ch2[index],2),round(synch_freq_list_ch2[index]), Monitoring, monitoring_type, connection_type, date_list_ch2[index]),
        (date_list_notime_ch3[index], asset_id,subcomponet_id,diagnostic_test_id, phase_tag_list_ch3[index], round(qmax95_list_ch3[index]*1000,2), round(nw_list_ch3[index],2),round(synch_freq_list_ch3[index]), Monitoring, monitoring_type, connection_type, date_list_ch3[index])
    ]

    print(data)
    # print(fukc)

    cursor.executemany(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()


    time.sleep(1)

    analyse_data(asset_id)

    time.sleep(1)

    assess_condition(asset_id)

    time.sleep(1)

    # Query to get the latest id
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave!2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()


    select_query = "SELECT MAX(id) AS latest_id FROM asset_analysis"

    # Execute the query
    cursor.execute(select_query)

    # Fetch the result
    result = cursor.fetchone()
    latest_id = result[0]  # The latest_id will be in the first column

    update_query = """
        UPDATE asset_analysis
        SET date = %s
        WHERE id = %s
    """

    # Execute the query with parameters
    cursor.execute(update_query, (date_list_ch3[index], latest_id))

    conn.commit()
    cursor.close()
    conn.close()

    print('----------------------------------------------------------------------------------------------------------------')
    print('Index:{}/{}'.format(index, (len(date_list_ch1)-1)))
    print('----------------------------------------------------------------------------------------------------------------')
