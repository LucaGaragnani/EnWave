import csv
from opcua import Client

# first neural network with keras tutorial
# from sklearn.preprocessing import StandardScaler
# from keras.layers import Dense
# from keras.models import Sequential
# from numpy import loadtxt
# from keras.models import model_from_json
import numpy
import os
# from import_txt_to_dictionary import import_txt_pattern
import pandas as pd

#to get the pattern from modbus and save as csv
def get_data_from_txt(filename):
    pdpattern_dict_complete = {}
    PdPattern_dict = {}

    with open('{}'.format(filename), 'r') as file:
        lines = file.readlines()

        i = 0
        for item in lines:
            item_list = item.split()
            pdpattern_dict_complete['{}'.format(i)] = item_list

            i += 1

    amplitude_list_complete = pdpattern_dict_complete['0']
    amplitude_list = [float(str) for str in amplitude_list_complete]

    phase_list_complete = pdpattern_dict_complete['1']
    phase_list = [float(str) for str in phase_list_complete]

    PdPattern_dict = {'x':phase_list, 'y':amplitude_list}

    return amplitude_list, phase_list


def get_data_from_csv_file(filename):
    pdpattern_dict_complete = {}
    PdPattern_dict = {}

    with open('{}'.format(filename), 'r') as file:
        lines = file.readlines()

        i = 0
        for item in lines:
            item_list = item.split()
            pdpattern_dict_complete['{}'.format(i)] = item_list

            i += 1

    amplitude_list_complete = pdpattern_dict_complete['0']
    amplitude_list_complete_v1 = amplitude_list_complete[0].split(";")




    amplitude_list = [float(str) for str in amplitude_list_complete_v1]

    phase_list_complete = pdpattern_dict_complete['1']
    phase_list_complete_v1 = phase_list_complete[0].split(";")
    phase_list = [float(str) for str in phase_list_complete_v1]

    PdPattern_dict = {'x':phase_list, 'y':amplitude_list}



    return amplitude_list, phase_list


def get_data_from_csv(measurement_number):
    col_list_pdpattern_phase = ["Phase"]

    df_pdpattern_phase = pd.read_csv(
        "PDPattern_ch_{}.csv".format(measurement_number),
        usecols=col_list_pdpattern_phase)

    list_pdpattern_phase = df_pdpattern_phase.values.tolist()

    col_list_pdpattern_amplitude = ["Amplitude"]

    df_pdpattern_amplitude = pd.read_csv(
        "PDPattern_ch_{}.csv".format(measurement_number),
        usecols=col_list_pdpattern_amplitude)

    list_pdpattern_amplitude = df_pdpattern_amplitude.values.tolist()

    amplitude_list = []
    for item in list_pdpattern_amplitude:
        for value in item:
            amplitude_list.append(value)

    phase_list = []
    for item in list_pdpattern_phase:
        for value in item:
            phase_list.append(value)

    return amplitude_list, phase_list

def download_pdttern_1_from_modbus():
    node_id_for_phase = "ns=2;s=pdChannel.ch1.data.P"  # read streaming
    node_id_for_amplitude = "ns=2;s=pdChannel.ch1.data.A"

    # Create a client and connect to the server
    client = Client(server_endpoint)
    client.connect()

    try:
        # Get the node with the specified NodeId
        phase_list_to_read = client.get_node(node_id_for_phase)
        amplitude_list_to_read = client.get_node(node_id_for_amplitude)

        # Read the value of the node
        phase_list = phase_list_to_read.get_value()
        amplitude_list = amplitude_list_to_read.get_value()



        ##################################################################################################################
        rows_data_pdpattern = zip(phase_list, amplitude_list )

        with open(
                'PDPattern_ch_{}.csv'.format(1), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Phase", "Amplitude"])
            for row in rows_data_pdpattern:
                writer.writerow(row)


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Disconnect from the server
        client.disconnect()

#to create the mesh with the required criteria
def create_mesh():
    #define criteria

    x_tr_list = [15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    y_pos_tr_list = [0.005,0.010,0.020,0.030,0.040,0.050,0.100,0.200,0.500,1,2,5]
    y_neg_tr_list = [-0.005,-0.010, -0.020, -0.030, -0.040, -0.050, -0.100, -200, -500, -1, -2, -5]

    #create dictionary empty for the mesh
    mesh_dict = {}

    #positive mesh
    i=0
    for item in x_tr_list:
        j=0
        for pos in y_pos_tr_list:
            mesh_dict['x{}-y{}pos'.format(i,j)] = 0
            j+=1
        i+=1

    #negative mesh
    i = 0
    for item in x_tr_list:
        j = 0
        for neg in y_neg_tr_list:
            mesh_dict['x{}-y{}neg'.format(i, j)] = 0
            j += 1
        i += 1

    return mesh_dict, x_tr_list, y_pos_tr_list, y_neg_tr_list

def separate_pos_neg_pulses(amplitude_list, phase_list):



    # create list of dictionary
    PdPattern_list_ch = []
    for volts, angle in zip(amplitude_list, phase_list):
        item_dict = {"x": angle, "y": volts}
        PdPattern_list_ch.append(item_dict)


    # separate pulses into positive and negative
    #
    PdPattern_amplitude_list_positive_pulses = []
    PdPattern_amplitude_list_negative_pulses = []

    for item in amplitude_list:
        if item >= 0:
            PdPattern_amplitude_list_positive_pulses.append(item)
        if item < 0:
            PdPattern_amplitude_list_negative_pulses.append(item)

    PDPattern_positive_pulses_listofdict = []
    PDPattern_negative_pulses_listofdict = []

    index = 0
    #
    #
    while index< len(PdPattern_list_ch):

        if PdPattern_list_ch[index]["y"] >= 0:
            PDPattern_positive_pulses_listofdict.append(PdPattern_list_ch[index])

        if PdPattern_list_ch[index]["y"] < 0:
            PDPattern_negative_pulses_listofdict.append(PdPattern_list_ch[index])

        index += 1

        if index>len(PdPattern_list_ch):
            break
    #
    PDPattern_positive_pulses_listofdict.reverse()
    PDPattern_negative_pulses_listofdict.reverse()



    return PDPattern_positive_pulses_listofdict, PDPattern_negative_pulses_listofdict

#insert the count of pulses into the mesh and export to a library in csv
def separate_pulses_into_mesh(pos_pulses_dict_list, neg_pulses_dict_list):
    #get mesh details

    x_tr_list = create_mesh()[1]
    y_pos_tr_list = create_mesh()[2]
    y_neg_tr_list = create_mesh()[3]
    mesh_dict = create_mesh()[0]



    #separate pos pulses


    for pos_pulses in pos_pulses_dict_list:
        #identify the horizontal square
        x=0
        index=0
        while index < len(x_tr_list):
            if index==0:
                if pos_pulses['x'] <= x_tr_list[index]:

                    None
            if index>0:
                if x_tr_list[index-1] < pos_pulses['x'] <= x_tr_list[index]:

                    x=index

                if pos_pulses['x'] > x_tr_list[index]:
                    None
            index +=1

            if index>len(x_tr_list):
                break

        #identify the vertical square
        y=0
        index=0
        while index < len(y_pos_tr_list):
            if index==0:
                if pos_pulses['y'] <= y_pos_tr_list[index]:

                    None
            if index>0:
                if y_pos_tr_list[index-1] < pos_pulses['y'] <= y_pos_tr_list[index]:

                    y=index

                if pos_pulses['y'] > y_pos_tr_list[index]:
                    None
            index +=1

            if index>len(x_tr_list):
                break


        mesh_dict['x{}-y{}pos'.format(x,y)] = mesh_dict['x{}-y{}pos'.format(x,y)]+1


    #separate neg pulses


    for neg_pulses in neg_pulses_dict_list:
        #identify the horizontal square
        x=0
        index=0

        while index < len(x_tr_list):
            if index==0:
                if neg_pulses['x'] <= x_tr_list[index]:

                    None
            if index>0:
                if x_tr_list[index-1] < neg_pulses['x'] <= x_tr_list[index]:

                    x=index

                if neg_pulses['x'] > x_tr_list[index]:
                    None
            index +=1

            if index>len(x_tr_list):
                break

        #identify the vertical square
        y=0
        index=0
        while index < len(y_neg_tr_list):
            if index==0:
                if abs(neg_pulses['y']) <= abs(y_neg_tr_list[index]):

                    None
            if index>0:
                if abs(y_neg_tr_list[index-1]) < abs(neg_pulses['y']) <= abs(y_neg_tr_list[index]):

                    y=index

                if abs(neg_pulses['y']) > abs(y_neg_tr_list[index]):
                    None
            index +=1

            if index>len(x_tr_list):
                break




        mesh_dict['x{}-y{}neg'.format(x,y)] = mesh_dict['x{}-y{}neg'.format(x,y)]+1





    #add pattern to library

    values_only = list(mesh_dict.values())


    #normalised to 1000

    values_only_normalised = []
    for number in values_only:
        values_only_normalised.append(number/1000)



    with open('/home/inwave/.config/iwvcd/inwave/pd_pattern_library.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the values (keys) without the keys' names
        csv_writer.writerow(values_only_normalised)
        csv_writer.writerow(values_only_normalised)







def add_to_library_from_txt():
    #get data from txt and add it to the library
    amplitude_list = get_data_from_txt('test')[0]
    phase_list = get_data_from_txt('test')[1]

    pos_pulses_dict_list = separate_pos_neg_pulses(amplitude_list,phase_list)[0]
    neg_pulses_dict_list = separate_pos_neg_pulses(amplitude_list,phase_list)[1]

    separate_pulses_into_mesh(pos_pulses_dict_list, neg_pulses_dict_list)


def add_to_library_from_txt_argumented(amplitude_list,phase_list):

    pos_pulses_dict_list = separate_pos_neg_pulses(amplitude_list,phase_list)[0]
    neg_pulses_dict_list = separate_pos_neg_pulses(amplitude_list,phase_list)[1]

    separate_pulses_into_mesh(pos_pulses_dict_list, neg_pulses_dict_list)

    return None


