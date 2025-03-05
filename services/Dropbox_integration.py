# import dropbox
# import csv
# import time
# from io import StringIO
# import json
# import pandas as pd
#
#
# # Dropbox access token
# DROPBOX_ACCESS_TOKEN = 'sl.u.AFj3uEaJoEAwgbSXaWIYhPsajMy8pNmw7gkc270VC_m44FPboyhtBGBzFfw6TxYfNmq5O1ncCetvl4WG6P0vQ6wiQtSlyYSLNArtV4sWPkXEn7WyQLYA6QZdRfaALX16AYFWVEP2b3gR8yBMPnMtjmVFf558fb49rD0m01Zq99YkybCf2W3eNT1_a6I4aikJGb9F-5A9YnT7LZ4nDPmnSABb5mX1_KBWp5XA9S1CBEtqNS80Jvxer6tvROJvU1crQl1PqtR9e8qj4jXwlcvH0taOqUL4UniuYjrJ7oQgwiXD2QZCIxrVf_y49-hXceX208Ufn3N-upk-JMMh-slvm8-AIo-CwtqwnGBP3skCXM9AslhvCvdmzRcU86FVb5NYZ3_xXWInbgfXtp3sJiJYL2E0LGx263rXU880i7onkjjavPuKF6lEuNmYpLFhGmvulZqnHqvoqQjZp16DHgHd4ZQLFId-kb2V5Dwiocswcpu0UF-nZS-FO8nM70uccEbHk64YjqGrb5LG_6pj9DMT8MBgRdDLIgOWBvUCxClb7QJKYi9SxvPS3-wKxVhZxxkl9ZcXgAsfa6pe1DxMvrEQBuVIhNjvXzQV_cCU0heqRjSHdLREqdBGBvdEjFLrBsz4OoSrp6LRLWdWct9C0mabn4vABqbWBUKe8DqiwQVKZc9Mp98udY2g52Qrtod6zMgws7XbP2B7lTBVt_F8E3fgs9a-0bOG8ckPt5KRtrvxF93GkusYPDVqC2jo4mr2r7RHbOKZSFSFqcrE0QUHvlNpk9uf4c4kaBILpVKQqpd7DGXCSc7ezgO28ZJSuVjPnUTaARd068KYzAmUi3v9LNAsgPpsRzRJ_zVjK1-Dzik5q9mxhwvIcWJkZalciTT7AnWlUS1Kb3rac25G9Ml9tqA4fCkSywsEdYwlwoXhGF9LVKMHOkBSlMfbjiMDlfpvoVxtl_EN-8wvlta7Aix-w29VKzYKvzvqe1RiyMUwjUCMdpKhC4pjjz_sp26DwshfSdgGX4l-Fl6-ipbNGqLXmjn0Br_ypXVhYMy_69ecgCecRpeKKhuQVnHmH2MejVepi2MEYxYrQYMc-IOzBvQODwQ8et70BUMOFT3IjOCCG3pLAtnWPpanVTs2ouVeYXIx5b3Kgp8IAJL475nPVvZY7pDay2WvyP-KXbhWGqBFXiXXOuqn6b49U3ZVLaO1P3ecpk3DgV_Qychny5G6DBZqG6fEx1Fmv_4dmwd033O0dni3bu_P0DmThHKT0mbuN6yQ5Rq59hUcClRjNcD7ZQXcaeA6yVrQZT8SlaxMWs2dbP8eGBqlVg9Jfqtk0tkvnMII105q61Ah9fFialARYBVub_dwcCvpOkiyrHNX5SrVy-QgVtdCWMYqTziqoZy2QXcTD9fCHIVctD5X3UIt34cFD9CY8sF9PAyBCe-VkwXjIzYz0J0LUxUsf2Mh5ArBiry4gvzyR8s'
#
#
# # Path of the file on Dropbox
# dropbox_path = '/Lutur_InWave/IHMS/data.csv'
#
# # Initialize Dropbox client
# dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
#
#
# # List of topics you want to filter messages for
# FILTER_TOPICS = [
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 1/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_2/PDSCOPE 2/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_3/PDSCOPE 3/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch1/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch1/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch1/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch1/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch2/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch2/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch2/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch2/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch3/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch3/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch3/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_1/PDSCOPE 4/Channel4/Ch3/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel1/Ch1/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel2/Ch2/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/QMax95',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/N',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/Nw',
#     'tiscada/data/acquisition/PTTGC6/SS_02/GEN_5/PDSCOPE 5/Channel3/Ch3/Subsession 0/Area Entire/Statistical Parameters/Sync Frequency',
#
# ]
#
# Gen_1_data = {}
# Gen_2_data = {}
# Gen_3_data = {}
# Gen_4_data = {}
# Gen_5_data = {}
#
#
# # Function to download the CSV file from Dropbox
# def download_file_from_dropbox():
#     try:
#         # Download the file from Dropbox
#         metadata, response = dbx.files_download(dropbox_path)
#         content = response.content.decode("utf-8")
#
#         # Create a StringIO object to read the CSV data
#         csv_file = StringIO(content)
#         return csv_file
#     except dropbox.exceptions.ApiError as e:
#         print(f"Error downloading file from Dropbox: {e}")
#         return None
#
#
# # Function to read the CSV data and create a local copy
# def create_local_csv(csv_file):
#     reader = csv.reader(csv_file)
#     headers = next(reader)  # Read the header row
#
#     # Open a local CSV file to write the data
#     with open('local_copy.csv', mode='w', newline='') as local_csvfile:
#         writer = csv.writer(local_csvfile)
#
#         writer.writerow(headers)  # Write the header row
#
#         # Read each row from the original CSV and write it to the local file
#         for row in reader:
#             writer.writerow(row)
#
#         print("Local CSV file 'local_copy.csv' created successfully.")
#
# def convert_row_values(row):
#     for key, value in row.items():
#         if key in ['QMax95', 'N', 'Nw', 'Sync_Frequency']:
#             try:
#                 row[key] = float(value)
#             except ValueError:
#                 pass  # If conversion fails, keep it as a string
#     return row
#
# # Function to check if the last row is identical to the new data
# def is_last_row_identical(data, file_path):
#     try:
#         # Open the CSV file in read mode
#         with open(file_path, mode='r') as file:
#             reader = csv.DictReader(file)
#
#             # Get the last row of the CSV file
#             last_row = None
#             for row in reader:
#                 last_row = row  # Keep updating to the last row
#
#             # If the file is empty, return False (no rows to compare)
#             if last_row is None:
#                 return False
#
#             # Convert the last row values to appropriate types for comparison
#             last_row = convert_row_values(last_row)
#
#
#
#             # Compare the new data with the last row
#             return all(data[key] == last_row[key] for key in data.keys())
#     except FileNotFoundError:
#         return False
#     except Exception as e:
#         print(f"Error checking last row: {e}")
#         return False
#
# # Function to append the dictionary data to the CSV file
# def append_to_csv(data, file_path):
#     try:
#         # Check if the last row is identical to the new data
#         if is_last_row_identical(data, file_path):
#             # print("The last row is identical to the new data. No data will be appended.")
#             return  # Don't append if they are identical
#
#         # Check if the file exists
#         file_exists = False
#         try:
#             with open(file_path, 'r'):
#                 file_exists = True
#         except FileNotFoundError:
#             file_exists = False
#
#         # Open the CSV file in append mode
#         with open(file_path, mode='a', newline='') as file:
#             writer = csv.DictWriter(file, fieldnames=data.keys())
#
#             # If the file does not exist, write the header
#             if not file_exists:
#                 writer.writeheader()
#
#             # Write the row (dictionary)
#             writer.writerow(data)
#
#         print("Data has been successfully appended to the CSV.")
#     except Exception as e:
#         print(f"An error occurred while writing to the CSV: {e}")
#
#
# # Function to read and print the content of a local CSV file using pandas
# def print_local_csv_with_dataframe(file_path):
#     try:
#         # Use pandas to read the CSV file into a DataFrame
#         df = pd.read_csv(file_path)
#
#         df_list = df.values.tolist()
#         # print(df_list[0])
#
#         # Filter the data based on the topic
#         for item in df_list:
#
#             for topics in FILTER_TOPICS:
#                 data = json.loads(item[2])
#
#                 if item[1] == topics:
#                     details = topics.split('/')
#                     if details[5] == 'GEN_1':
#                         if details[8] =='Ch1':
#
#                             if details[12] == 'QMax95':
#                                 Gen_1_data['Acq_time'] = data['acqDateTime']
#                                 Gen_1_data['QMax95']=float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_1_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_1_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_1_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] =='Ch2':
#
#                             if details[12] == 'QMax95':
#                                 Gen_1_data['Acq_time'] = data['acqDateTime']
#                                 Gen_1_data['QMax95']=float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_1_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_1_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_1_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] =='Ch3':
#
#                             if details[12] == 'QMax95':
#                                 Gen_1_data['Acq_time'] = data['acqDateTime']
#                                 Gen_1_data['QMax95']=float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_1_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_1_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_1_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#                     if details[5] == 'GEN_2':
#                         if details[8] == 'Ch1':
#
#                             if details[12] == 'QMax95':
#                                 Gen_2_data['Acq_time'] = data['acqDateTime']
#                                 Gen_2_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_2_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_2_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_2_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] == 'Ch2':
#
#                             if details[12] == 'QMax95':
#                                 Gen_2_data['Acq_time'] = data['acqDateTime']
#                                 Gen_2_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_2_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_2_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_2_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] == 'Ch3':
#
#                             if details[12] == 'QMax95':
#                                 Gen_2_data['Acq_time'] = data['acqDateTime']
#                                 Gen_2_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_2_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_2_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_2_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#                     if details[5] == 'GEN_3':
#                         if details[8] == 'Ch1':
#
#                             if details[12] == 'QMax95':
#                                 Gen_3_data['Acq_time'] = data['acqDateTime']
#                                 Gen_3_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_3_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_3_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_3_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] == 'Ch2':
#
#                             if details[12] == 'QMax95':
#                                 Gen_3_data['Acq_time'] = data['acqDateTime']
#                                 Gen_3_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_3_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_3_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_3_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] == 'Ch3':
#
#                             if details[12] == 'QMax95':
#                                 Gen_3_data['Acq_time'] = data['acqDateTime']
#                                 Gen_3_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_3_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_3_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_3_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                     if details[5] == 'GEN_4':
#                         if details[8] == 'Ch1':
#
#                             if details[12] == 'QMax95':
#                                 Gen_4_data['Acq_time'] = data['acqDateTime']
#                                 Gen_4_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_4_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_4_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_4_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] == 'Ch2':
#
#                             if details[12] == 'QMax95':
#                                 Gen_4_data['Acq_time'] = data['acqDateTime']
#                                 Gen_4_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_4_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_4_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_4_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] == 'Ch3':
#
#                             if details[12] == 'QMax95':
#                                 Gen_3_data['Acq_time'] = data['acqDateTime']
#                                 Gen_3_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_3_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_3_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_3_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                     if details[5] == 'GEN_5':
#                         if details[8] == 'Ch1':
#
#                             if details[12] == 'QMax95':
#                                 Gen_5_data['Acq_time'] = data['acqDateTime']
#                                 Gen_5_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_5_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_5_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_5_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] == 'Ch2':
#
#                             if details[12] == 'QMax95':
#                                 Gen_5_data['Acq_time'] = data['acqDateTime']
#                                 Gen_5_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_5_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_5_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_5_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#                         if details[8] == 'Ch3':
#
#                             if details[12] == 'QMax95':
#                                 Gen_5_data['Acq_time'] = data['acqDateTime']
#                                 Gen_5_data['QMax95'] = float(data['valueAsNumeric'])
#                             if details[12] == 'N':
#                                 Gen_5_data['N'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Nw':
#                                 Gen_5_data['Nw'] = float(data['valueAsNumeric'])
#                             if details[12] == 'Sync Frequency':
#                                 Gen_5_data['Sync_Frequency'] = float(data['valueAsNumeric'])
#
#
#                     # print(item[2])
#                #     for row in df:
#         # Appedn Gen 1 data
#         append_to_csv(Gen_1_data, 'GEN_1.csv')
#         append_to_csv(Gen_2_data, 'GEN_2.csv')
#         append_to_csv(Gen_3_data, 'GEN_3.csv')
#         append_to_csv(Gen_4_data, 'GEN_4.csv')
#         append_to_csv(Gen_5_data, 'GEN_5.csv')
#         # # print(df.iloc[0][1])  # The DataFrame will display the CSV data in a tabular format
#
#     except FileNotFoundError:
#         print(f"Error: The file '{file_path}' was not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#
# # Main loop to check the file and create local CSV regularly
# def main():
#     while True:
#         # Download the CSV file from Dropbox
#         csv_file = download_file_from_dropbox()
#
#         if csv_file:
#             print("CSV file downloaded successfully.")
#             create_local_csv(csv_file)
#             time.sleep(2)
#             # Now, print the local copy of the CSV file using pandas
#             print_local_csv_with_dataframe('local_copy.csv')
#         else:
#             print("Failed to download the file.")
#
#         # Wait for a while before checking again (e.g., every 5 seconds)
#         time.sleep(500)
#
#
# if __name__ == "__main__":
#     main()

import plotly.graph_objects as go
from datetime import datetime

# Data
u = [{'x': '15/02/2025 01:12', 'y': 10}]
v = [{'x': '15/02/2025 01:14', 'y': 12}]
w = [{'x': '15/02/2025 01:16', 'y': 16}]

# Convert strings to datetime objects
u = [{'x': datetime.strptime(item['x'], '%d/%m/%Y %H:%M'), 'y': item['y']} for item in u]
v = [{'x': datetime.strptime(item['x'], '%d/%m/%Y %H:%M'), 'y': item['y']} for item in v]
w = [{'x': datetime.strptime(item['x'], '%d/%m/%Y %H:%M'), 'y': item['y']} for item in w]

# Create traces
trace_u = go.Scatter(x=[item['x'] for item in u], y=[item['y'] for item in u], mode='lines+markers', name='u')
trace_v = go.Scatter(x=[item['x'] for item in v], y=[item['y'] for item in v], mode='lines+markers', name='v')
trace_w = go.Scatter(x=[item['x'] for item in w], y=[item['y'] for item in w], mode='lines+markers', name='w')

# Create figure
fig = go.Figure(data=[trace_u, trace_v, trace_w])

# Add labels and title
fig.update_layout(
    title="Three Lines on Same Graph",
    xaxis_title="Time",
    yaxis_title="Value",
    xaxis=dict(type='date')  # Ensure the x-axis is treated as dates
)

# Show the plot
fig.show()

