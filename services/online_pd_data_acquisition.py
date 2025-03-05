import csv
import os
from datetime import datetime, timezone

import matplotlib
import numpy as np
import pytz
from tenacity import retry_unless_exception_type
from tzlocal import get_localzone

matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
from opcua import Client
import requests
import time
import json
import threading
# from PDPattern_identification_LG import add_to_library_from_txt_argumented
from scipy.fft import fft
from scipy.signal import resample
# from keras import models
from numpy import loadtxt
from services.waveform_analysis_tool_rev3_v2 import peak_detection
from services.waveform_analysis_tool_rev3_v2 import time_domain_refloctometric
from services.PDPattern_identification_LG import separate_pos_neg_pulses
import asyncio
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


"""
    Service to connect to the portable acquisition unit and perform the acquisition and pre-analysis
    1. connect
    2. confirm setting
    3. check synch
    4. send command to run acquisition
    5. verify acquisition status via opcua
    6. read the data - pattern, tf map, waveform
    7. create pd pattern
    8. run ai module
    9. evaluate polarity - phase (trial)
    10. return data to be saved in db
    
"""



async def perform_pd_measurement():
    instrument_ip_addrsss = '192.168.10.115'
    server_endpoint = "opc.tcp://{}:48010".format(instrument_ip_addrsss)
    model_path = 'assets/Techimp_AI_model_rev0.h5'
    directory_path = 'temp/'

    acq_information_dict = {}
    Label_dictionary = {}
    Label_dictionary["PDPattern_classification"] = 0
    Acquisition_time_dictionary = {}
    Waveform_details_for_tdr = {}
    acq_information_dict['counter'] = 1

    # waveforms lists
    accumulated_signals_total = []
    accumulated_signals_positive_pulses = []
    accumulated_signals_negative_pulses = []
    accumulated_signals_noise = []

    formatted_date = ''
    acq_number = 1
    Qpos = 0
    Qneg = 0
    Qmax95 = 0
    Number_of_pulses = 0
    Nw= 0
    polarity_identification = 'NA'
    phase_factor ='NA'
    automatic_identification = 'NA'

    json_phase = 0
    json_amplitude = 0
    json_equ_timelenght = 0
    json_equ_frequency = 0
    json_average_waveform = 0

    async def acquire_waveform(iteration):
        # print('Acquire waveform')
        nonlocal  json_average_waveform

        node_id_to_read = "ns=2;s=pdChannel.ch1.data.samples"  # read streaming

        # Create a client and connect to the server
        client = Client(server_endpoint)
        client.connect()

        try:
            # Get the node with the specified NodeId
            node_to_read = client.get_node(node_id_to_read)

            # Read the value of the node
            value = node_to_read.get_value()

            # reshape the sample with different sample rate

            original_signal_125MSa = np.array(value)

            new_sample_rate = 100e6  # 100 MSa

            resampling_ratio = 100 / 125

            resampled_signal_100MSa = resample(original_signal_125MSa,
                                               int(len(original_signal_125MSa) * resampling_ratio))

            Waveform_details_for_tdr['Raw_Waveform'] = resampled_signal_100MSa

            # import model for waveform analysis
            # model = load_model('/home/inwave/.config/iwvcd/inwave/wavform_analysis_1us_model_5.h5')
            # # summarize model.
            # model.summary()

            # adjust the sample based on the time lenght used to increase the accurancy of the NN model
            if len(resampled_signal_100MSa) == 100:  # 1us

                # get the first 50 values - reshaped considering the different sample rating
                value_zoomed = resampled_signal_100MSa[:50]
                # print(len(value_zoomed))

            if len(resampled_signal_100MSa) == 1000:  # 10us

                # get the first 50 values - reshaped considering the different sample rating
                value_zoomed = resampled_signal_100MSa[70:120]
                # print(len(value_zoomed))

            if len(resampled_signal_100MSa) == 2000:  # 20us

                # get the first 50 values - reshaped considering the different sample rating
                value_zoomed = resampled_signal_100MSa[170:220]
                # print(len(value_zoomed))
            #                                     print(len(value_zoomed))

            # X = np.array(value_zoomed)
            # #                                     print('here')
            # #                                     print(X)
            # X_reshaped = X.reshape(1, 50)
            #
            # # print(dataset)
            # # print(type(dataset))
            # predictions = np.argmax(model.predict(X_reshaped), axis=1)
            # #                                     print(predictions)

            # Accumulate the resampled signal
            accumulated_signals_total.append(resampled_signal_100MSa)
            # temporary solution to bypass tensorflow
            predictions =0
            if predictions == 0 or predictions == 1:
                # print("Noise")
                accumulated_signals_noise.append(resampled_signal_100MSa)
                Waveform_details_for_tdr['AI_analysis'] = 'Noise'

            if predictions == 2:
                print("Pulse")
                # analyse waveform for separating positive and negative signals
                first_peak_details = peak_detection(resampled_signal_100MSa)[0]
                first_peak_polarity = first_peak_details[0]

                # Waveform_details_for_tdr['AI_analysis'] = 'Pulse'
                # print(first_peak_polarity)

                if first_peak_polarity == 'positive pulse':
                    print("Positive")
                    accumulated_signals_positive_pulses.append(resampled_signal_100MSa)
                if first_peak_polarity == 'negative pulse':
                    print("Negative")
                    accumulated_signals_negative_pulses.append(resampled_signal_100MSa)
                if first_peak_polarity == None:
                    None

            # to save each individual waveform acquired - only 10
            # # Create the CSV file on the desktop --- disable
            # if iteration < 10:
            #     csv_file_path = '{}/Substation_{}/{}/{}/{}/waveform_{}.csv'.format(root_path,acq_information_dict['Substation_name'], acq_information_dict['Asset_category'], acq_information_dict['Asset_name'], acq_information_dict['PD_sensor_used'],iteration)  #, Acquisition_time_dictionary['Datetime']
            #
            #     with open(csv_file_path, mode='w', newline='') as csv_file:
            #         writer = csv.writer(csv_file)
            #         writer.writerow(["Amplitude"])
            #         for item in resampled_signal_100MSa:
            #             writer.writerow([item])




        except KeyboardInterrupt:
            # Handle KeyboardInterrupt (Ctrl+C) to gracefully exit the loop
            pass

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Disconnect from the server
            client.disconnect()

        if iteration <= 10:
            # print(iteration)
            # print("Iteration:",iteration)
            # Schedule the next iteration after 1 second (1000 milliseconds)
            # self.after(1000, acquire_waveform, iteration + 1)
            await asyncio.sleep(1)
            await acquire_waveform(iteration+1)

            # timer = threading.Timer(1, acquire_waveform, args=((iteration+1),))
            # timer.start()

            # wait 10 seconds after all iterations are completed
        else:
            # Calculate the average signal
            Waveform_details_for_tdr['Average_Waveform_Pos'] = None
            Waveform_details_for_tdr['Average_Waveform_Neg'] = None

            sample_rating_MSa = 100000000
            time_resolution = 1 / sample_rating_MSa
            amplitude_negative = 0
            amplitude_positive = 0
            average_frequency_positive_pulse = 0
            average_frequency_negative_pulse = 0
            peak_frequency_positive = 0
            peak_frequency_negative = 0

            if accumulated_signals_total:
                average_signal = np.mean(accumulated_signals_total, axis=0)

                Waveform_details_for_tdr['Average_Waveform'] = average_signal

                average_signal_list = average_signal.tolist()

                json_average_waveform = json.dumps(average_signal_list)

                # convert sample to time in us
                time_lenght_list = []
                sample_number = 0
                for sample in average_signal:
                    time_lenght_list.append(sample_number * time_resolution * 1000000)
                    sample_number += 1

                # convert average signal amplitude in mV
                average_signal_mv = []
                for V in average_signal:
                    average_signal_mv.append(V * 1000)

                # Find the amplitude (maximum value) of the average signal
                amplitude_positive_total_signal = np.max(average_signal)
                amplitude_negative_total_signal = np.min(average_signal)

                # Calculate the FFT (Fast Fourier Transform) of the average signal
                fft_result = fft(average_signal)

                # Find the peak frequency (frequency corresponding to the highest peak in the spectrum)
                freqs = np.fft.fftfreq(len(average_signal))
                peak_freq_index = np.argmax(np.abs(fft_result))
                peak_frequency = abs(freqs[peak_freq_index])

                # # Create the CSV file for the average signal
                csv_file_path = '{}/average_waveform_{}.csv'.format(directory_path,acq_information_dict['counter'])
                #
                with open(csv_file_path, mode='w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Amplitude"])
                    for item in average_signal:
                        writer.writerow([item])


                # create png
                plt.plot(time_lenght_list, average_signal_mv, color="grey", linewidth=1, zorder=0)

                plt.xlabel('Time lenght [us]')
                plt.ylabel('Qmax [mV]')
                plt.title('Average Waveform')

                plt.savefig('{}/average_waveform_{}.png'.format(directory_path,acq_information_dict['counter']))

                # clean the plot
                plt.clf()

            if accumulated_signals_positive_pulses:
                average_signal = np.mean(accumulated_signals_positive_pulses, axis=0)

                Waveform_details_for_tdr['Average_Waveform_Pos'] = average_signal

                # Find the amplitude (maximum value) of the average signal
                amplitude_positive = np.max(average_signal)

                # evaluate the frequency with custom tool
                pulse_width = peak_detection(average_signal)[0][3]
                pulse_width_in_samples = pulse_width / time_resolution
                pulse_area = peak_detection(average_signal)[0][4]
                period = len(average_signal) * time_resolution
                period_ns = period * 1e9
                average_frequency_positive_pulse = pulse_area / (
                        (len(average_signal) / pulse_width_in_samples) * period)

                # Calculate the FFT (Fast Fourier Transform) of the average signal
                fft_result = fft(average_signal)

                # Find the peak frequency (frequency corresponding to the highest peak in the spectrum)
                freqs = np.fft.fftfreq(len(average_signal))
                peak_freq_index = np.argmax(np.abs(fft_result))
                peak_frequency_positive = abs(freqs[peak_freq_index])

                # Create the CSV file for the average signal
                csv_file_path = '{}/wavefrom_{}.csv'.format(directory_path,acq_information_dict['counter'])
                #
                #
                with open(csv_file_path, mode='w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Amplitude"])
                    for item in average_signal:
                        writer.writerow([item])
                #

            if accumulated_signals_negative_pulses:
                average_signal = np.mean(accumulated_signals_negative_pulses, axis=0)

                Waveform_details_for_tdr['Average_Waveform_Neg'] = average_signal

                # Find the amplitude (maximum value) of the average signal
                amplitude_negative = np.min(average_signal)

                # evaluate the frequency with custom tool
                pulse_width = peak_detection(average_signal)[0][3]
                pulse_width_in_samples = pulse_width / time_resolution
                pulse_area = peak_detection(average_signal)[0][4]
                period = len(average_signal) * time_resolution
                period_ns = period * 1e9

                average_frequency_negative_pulse = pulse_area / (
                        (len(average_signal) / pulse_width_in_samples) * period)

                # Calculate the FFT (Fast Fourier Transform) of the average signal
                fft_result = fft(average_signal)

                # Find the peak frequency (frequency corresponding to the highest peak in the spectrum)
                freqs = np.fft.fftfreq(len(average_signal))
                peak_freq_index = np.argmax(np.abs(fft_result))
                peak_frequency_negative = abs(freqs[peak_freq_index])

                # # Create the CSV file for the average signal
                csv_file_path = '{}/wavefrom_{}.csv'.format(directory_path,acq_information_dict['counter'])
                #
                #
                with open(csv_file_path, mode='w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Amplitude"])
                    for item in average_signal:
                        writer.writerow([item])
                #






        # set no filters

    def create_pd_pattern(amplitude_list, phase_list, formatted_date):

            ##################################################################################################################

            # export PD Pattern to PNG

            # create graph
            # add sinewaveform in the background

            # convert V to mV
            amplitude_list_mv = []
            for V in amplitude_list:
                amplitude_list_mv.append(V * 1000)

            ######################################################################################################################
            #########################       create colour   ######################################################################
            PdPattern_dict = {}

            PdPattern_dict = {'x': phase_list, 'y': amplitude_list_mv}

            # Create a dictionary to store the counts of unique (x, y) pairs
            intensity_dict = {}

            # Count the occurrences of each unique pair of (x, y) values
            for x, y in zip(PdPattern_dict['x'], PdPattern_dict['y']):
                pair = (x, y)
                intensity_dict[pair] = intensity_dict.get(pair, 0) + 1

            # Create a list of intensities based on the counts
            intensity = [intensity_dict[(x, y)] for x, y in zip(PdPattern_dict['x'], PdPattern_dict['y'])]

            PdPattern_dict['intensity'] = intensity

            # color
            color_codes = []
            for intensity_value in intensity:
                # Adjust the color range according to your preference
                if intensity_value == 1:
                    color_code = '#000000'  # Black color code
                else:
                    # Scale intensity to range [0, 1]
                    normalized_intensity = (intensity_value - 1) / (max(intensity) - 1)
                    # Calculate color gradient from black to dark red
                    red_value = int(255 * normalized_intensity)
                    color_code = f'#{red_value:02X}0000'  # Generate color code with varying red component
                color_codes.append(color_code)

            # print(color_codes)
            PdPattern_dict['color'] = color_codes

            colour_list = PdPattern_dict['color']

            # Create figure and axis objects
            fig, ax = plt.subplots()

            Fs = 360
            f = 1
            sample = 360
            x = np.arange(sample)
            # unit amplitude
            y = np.sin(2 * np.pi * f * x / Fs)

            # final amplitude based on the trigger level

            # final_amplitude = max(amplitude_list)

            positive_pulses = [i for i in amplitude_list_mv if i > 0]
            trigger_level = min(positive_pulses, default=0)

            # trigger level * 10 times
            y_autoscale = trigger_level * y * 10

            # needed to eliminate the error due to the loop of the loop #### do not remove
            # plt.switch_backend('agg')
            ax.plot(x, y_autoscale, color="grey", linewidth=1, zorder=0)
            ax.scatter(phase_list, amplitude_list_mv, color=colour_list, marker='o', s=1)

            # plt.plot(x, y_autoscale, color="grey", linewidth=1, zorder=0)

            # plt.scatter(phase_list, amplitude_list_mv, color="black", marker='o', s=1)

            # plt.xlim(0, 360)
            # plt.xlabel('Phase')
            # plt.ylabel('Qmax [mV]')
            # plt.title('Phase Resolved PD Pattern')

            naive_datetime = datetime.strptime(formatted_date, "%d/%m/%Y %H:%M")
            local_tz = get_localzone()

            datetime_obj_local = naive_datetime.replace(tzinfo=pytz.utc).astimezone(local_tz)

            # Step 4: Convert the localized datetime to a string
            local_time_str = datetime_obj_local.strftime("%d/%m/%Y %H:%M:%S")

            ax.set_xlim(0, 360)
            ax.set_xlabel('Phase')
            ax.set_ylabel('Amplitude [mV]')
            ax.set_title('Phase Resolved PD Pattern - {}'.format(local_time_str))

            ax.tick_params(axis='x', labelsize=8)  # Set x-axis tick labels with smaller font size
            ax.tick_params(axis='y', labelsize=8)  # Set y-axis tick labels with smaller font size
            # fig.text(0.5, 0.01, '© 2024 InWave', ha='center', fontsize=6, color='gray')



            # Create the directories if they don't exist
            os.makedirs(directory_path, exist_ok=True)

            # Save the file
            plt.savefig(os.path.join(directory_path, 'PDPattern_{}.png'.format(0)))

            # plt.savefig('{}/{}/{}/{}/{}/PDPattern.png'.format(root_path,acq_information_dict['Substation_name'], acq_information_dict['Asset_category'], acq_information_dict['Asset_name'], acq_information_dict['PD_sensor_used']))

            # clean the plot
            plt.clf()
    def Techimp_AI_Identification_from_txt(self, file_path):
        # load model
        model = models.load_model(model_path)
        # summarize model.
        model.summary()
        # load dataset
        dataset = loadtxt('{}.csv'.format(file_path), delimiter=',')

        X = dataset[:, :]



        # make class predictions with the model
        y_predict = np.argmax(model.predict(X), axis=-1)



        if y_predict[-1] == 0:
                PD_Pattern_classification = 'Noise'

        if y_predict[-1] == 1:
                PD_Pattern_classification = 'External Disturbance'

        if y_predict[-1] == 2:
                PD_Pattern_classification = 'Likely PD signal'


        return  PD_Pattern_classification

    async def download_pdttern_1(headers):
        # print("Dowanloading data from opc")

        nonlocal formatted_date
        nonlocal Qpos
        nonlocal Qneg
        nonlocal Qmax95
        nonlocal Number_of_pulses
        nonlocal Nw
        nonlocal polarity_identification
        nonlocal phase_factor
        nonlocal automatic_identification

        nonlocal json_phase
        nonlocal json_amplitude
        nonlocal json_equ_frequency
        nonlocal json_equ_timelenght

        # get system date
        # get_system_unix_time = "https://{}/api/systemdate".format(instrument_ip_addrsss)
        # system_unix_time_dict = requests.get(get_system_unix_time, headers=headers, verify=False).json()
        # Acquisition_time_dictionary['Systemtime'] = system_unix_time_dict['data']
        # print(Acquisition_time_dictionary)

        node_id_for_phase = "ns=2;s=pdChannel.ch1.data.P"  # read streaming
        node_id_for_amplitude = "ns=2;s=pdChannel.ch1.data.A"
        node_id_for_equ_frequency = "ns=2;s=pdChannel.ch1.data.W"  # read streaming
        node_id_for_equ_timelenght = "ns=2;s=pdChannel.ch1.data.T"
        node_id_for_timestamp = "ns=2;s=pdChannel.ch1.data.acq_timestamp"

        # Create a client and connect to the server
        client = Client(server_endpoint)
        client.connect()

        try:
            # Get the node with the specified NodeId
            phase_list_to_read = client.get_node(node_id_for_phase)
            amplitude_list_to_read = client.get_node(node_id_for_amplitude)
            equ_timelenght_list_to_read = client.get_node(node_id_for_equ_timelenght)
            equ_frequency_list_to_read = client.get_node(node_id_for_equ_frequency)
            time_stamp_value = client.get_node(node_id_for_timestamp)

            # Read the value of the node
            phase_list = phase_list_to_read.get_value()
            amplitude_list = amplitude_list_to_read.get_value()
            equ_timelenght_list = equ_timelenght_list_to_read.get_value()
            equ_frequency_list = equ_frequency_list_to_read.get_value()
            time_stamp = time_stamp_value.get_value()

            json_phase = json.dumps(phase_list)
            json_amplitude = json.dumps(amplitude_list)
            json_equ_timelenght = json.dumps(equ_timelenght_list)
            json_equ_frequency = json.dumps(equ_frequency_list)


            # evaluate the Qpos and Qneg, total number of pulses and Nw
            positive_pulses = separate_pos_neg_pulses(amplitude_list, phase_list)[0]
            negative_pulses = separate_pos_neg_pulses(amplitude_list, phase_list)[1]


            if len(positive_pulses)!=0:
                pos_amplitudes = [item['y'] for item in positive_pulses]

            if len(positive_pulses)==0:
                pos_amplitudes = 0

            if len(negative_pulses)!=0:
                neg_amplitudes = [item['y'] for item in negative_pulses]

            if len(negative_pulses)==0:
                neg_amplitudes = 0

            Qpos = abs(np.percentile(pos_amplitudes, 95))
            Qneg = abs(np.percentile(neg_amplitudes, 95))

            Number_of_pulses = len(amplitude_list)
            NW = Number_of_pulses/(0.020)

            # create pdpattern

            # Define the format of the input string
            format_string = "%Y-%m-%dT%H:%M:%S.%fZ"

            # Convert the string to a datetime object
            datetime_object = datetime.strptime(time_stamp, format_string)

            # Convert the datetime object to the desired format
            formatted_date = datetime_object.strftime("%d/%m/%Y %H:%M")
            # print(formatted_date)
            create_pd_pattern(amplitude_list, phase_list, formatted_date)

            pdpattern_zip = zip(amplitude_list, phase_list)



            # print("PD Pattern created")

            # add_to_library_from_txt_argumented(amplitude_list, phase_list)
            #
            # # classify pd pattern
            # PDPattern_classification = Techimp_AI_Identification_from_txt(library_path)

            # Label_dictionary["PDPattern_classification"] = PDPattern_classification

            polarity_identification = 'NA'
            phase_factor = 'NA'
            automatic_identification = 'NA'
            # print("--------------------", PDPattern_classification, "-------------------")
            # evaluate Qmax95%
            try:
                # Qmax_95 = abs(np.percentile(get_data_from_txt(file_path)[0], 95))

                Qmax_95 = abs(np.percentile(amplitude_list, 95))

            except IndexError:
                Qmax_95 = 0

            Label_dictionary["PDPattern_Amplitude"] = Qmax_95

        except KeyboardInterrupt:
            # Handle KeyboardInterrupt (Ctrl+C) to gracefully exit the loop
            pass

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Disconnect from the server
            client.disconnect()

        # self.progressbar_1["value"] = 80
        # self.update_idletasks()

        # # dealy 2 time acquisition duration
        # delay_2a = 5
        # iteraction = 0
        #
        # await asyncio.sleep(delay_2a)
        # await acquire_waveform(iteraction)
        #
        # # set filter one
        # timer = threading.Timer(delay_2a, acquire_waveform, args=(iteraction,))
        #
        # timer.start()
        # print('PD Pattern saved')


    async def get_system_time(headers):
        # get system date
        get_system_unix_time = "https://{}/api/systemdate".format(instrument_ip_addrsss)
        system_unix_time_dict = requests.get(get_system_unix_time, headers=headers, verify=False).json()
        Acquisition_time_dictionary['Systemtime'] = system_unix_time_dict['data']


    async def check_acq_status(headers):
        def read_node_value(status_to_read):
            """Read the value of the node."""
            try:
                return status_to_read.get_value()
            except Exception as e:
                print(f"Error reading node value: {e}")
                return None

        # print("check acquisition status")
        node_id_for_status = "ns=2;s=device.settings.acqMonitoring.status"  # read streaming

        # Create a client and connect to the server
        client = Client(server_endpoint)
        client.connect()

        try:
            # Get the node with the specified NodeId
            status_to_read = client.get_node(node_id_for_status)
            # Read the value of the node
            status = read_node_value(status_to_read)

            if status is None:
                print("Unable to read status. Retrying...")

                await asyncio.sleep(10)
                await check_acq_status(headers)
                # timer = threading.Timer(10, check_acq_status, args=(headers,))
                # timer.start()
                # return

            # print(f"Initial status: {status}")

            if status == 1:
                # Schedule the next check in 10 seconds
                await asyncio.sleep(10)
                await check_acq_status(headers)
                # timer = threading.Timer(10, check_acq_status, args=(headers,))
                # timer.start()


            if status == 0:
                None

                # # dealy 2 time acquisition duration
                # delay_2 = 30
                #
                # # download pd pattern
                # await asyncio.sleep(delay_2)
                # await download_pdttern_1(headers)
                # # timer = threading.Timer(delay_2, download_pdttern_1, args=(headers,))
                # # timer.start()



        except KeyboardInterrupt:
            # Handle KeyboardInterrupt (Ctrl+C) to gracefully exit the loop
            pass

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Disconnect from the server
            client.disconnect()

        return status


    async def force_acquisition_1(headers):
        # print("Acquisition 1 forced")


        force_acquisition_command = "https://{}/api/system/forceAcq/1".format(instrument_ip_addrsss)
        force_acquisition = requests.post(force_acquisition_command, headers=headers, verify=False)

        # get datetime
        # Get current time in UTC as a timezone-aware datetime object
        utc_now = datetime.now(timezone.utc)

        # Define the timezone for Brisbane (Australia/Brisbane) using pytz
        bris_timezone = pytz.timezone('Australia/Brisbane')

        # Get the current time in the Brisbane time zone as a timezone-aware datetime object
        current_time = datetime.now(bris_timezone)



        # Format the datetime object to display date and time
        # sgt_now_formatted = sgt_now.strftime("%Y-%m-%d %H:%M:%S")

        bris_now_formatted = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # acquisition_time.append(sgt_now_formatted)
        # Acquisition_time_dictionary['Datetime'] = sgt_now_formatted

        Acquisition_time_dictionary['Datetime'] = bris_now_formatted
        # # print(Acquisition_time_dictionary)
        #
        # delay_opc = 1
        #
        # timer = threading.Timer(delay_opc, check_acq_status, args=(headers,))
        #
        #
        # timer.start()


    def get_settings(headers):


        get_settings_url = "https://{}/api/settings/5/acquisition".format(instrument_ip_addrsss)
        settings = requests.get(get_settings_url, headers=headers, verify=False).json()

        return settings


    async def set_timelenght(headers):
        # print("set timelenght")


        # get setting
        settings = get_settings(headers)

        data = settings['data'][0]


        # print(data['timelength'])

        timelenght = str(data['timelength'])
        #                                 print(timelenght)
        #                                 print(type(timelenght))
        timelenghts = ['1e-06', '1e-05', '2e-05']

        #                                 print(timelenght not in timelenghts)

        if timelenght not in timelenghts:
            # set to 10
            # print("here")
            data['timelength'] = 1e-05
            data['pretrigger'] = 5
            # print(data)

            # update main dictionary

            settings['data'] = data
            # print(settings['data'])

            # new_filter_dict_for_upload = filter_set['data'].items()
            # print(new_filter_dict_for_upload)

            # conver to json
            new_filter = json.dumps(settings['data'])

            #
            get_settings_url = "https://{}/api/settings/1/acquisition".format(instrument_ip_addrsss)
            settings_new = requests.put(get_settings_url, data=new_filter, headers=headers, verify=False)

            # print('new settings:', get_settings(headers))

        # # wait 10 seconds
        # delay_1 = 5
        #
        # print("now delay 5s")
        # # acq waveform and start iteration at 0
        # timer = threading.Timer(delay_1, force_acquisition_1, args=(headers,))
        # timer.start()


    def get_filter_set(headers):


        get_filter_set_url = "https://{}/api/pd/1/TWMapSettings".format(instrument_ip_addrsss)
        filter_set = requests.get(get_filter_set_url, headers=headers, verify=False).json()

        return filter_set


    def set_filter_0(headers):  # no filter
        # print("set filter 0")
        # login to the page

        # get filter setting
        filter_set = get_filter_set(headers)

        data = filter_set['data']

        # update filter json
        data['twMapFilterType'] = 1  # capture
        data['twMapServerFilters'] = '[]'
        data['twMapFilterNumber'] = 0
        # print(type(data))

        # print(data)

        # update main dictionary

        filter_set['data'] = data

        # new_filter_dict_for_upload = filter_set['data'].items()
        # print(new_filter_dict_for_upload)

        # conver to json
        new_filter = json.dumps(filter_set['data'])

        # print(type(new_filter))

        #
        get_filter_set_url = "https://{}/api/pd/1/TWMapSettings".format(instrument_ip_addrsss)
        filter_zero = requests.put(get_filter_set_url, data=new_filter, headers=headers, verify=False)


        # # wait 2 seconds
        # delay_1 = 2
        #
        # print("now delay 2s")
        # # acq waveform and start iteration at 0
        # timer = threading.Timer(delay_1, set_timelenght,args=(headers,))
        # timer.start()



    # login to the pages

    username = "admin"
    password = "Admin!23"

    loginURL = "https://{}/api/login".format(instrument_ip_addrsss)
    params = {'username': username, 'password': password}
    try:
        res = requests.post(loginURL, data=params, verify=False, timeout=3).json()

        token = res['token']

        headers = {
                "Authorization": "Bearer" + token
        }


        # set filter zero
        set_filter_0(headers)

        # set timelenght
        delay_1 = 2
        await asyncio.sleep(delay_1)
        await set_timelenght(headers)


        # print("now delay 2s")
        # timer = threading.Timer(delay_1, set_timelenght, args=(headers,))
        # timer.start()

        # force acquisition
        delay_1 = 5
        await asyncio.sleep(delay_1)
        await force_acquisition_1(headers)

        # print("now delay 5s")
        # timer = threading.Timer(delay_1, force_acquisition_1, args=(headers,))
        # timer.start()

        # check status acquisition

        delay_opc = 1
        await asyncio.sleep(delay_opc)
        await check_acq_status(headers)
        # timer = threading.Timer(delay_opc, check_acq_status, args=(headers,))
        #
        # timer.start()

        # # download pd pattern
        delay_2 = 30
        await asyncio.sleep(delay_2)
        await download_pdttern_1(headers)
        # timer = threading.Timer(delay_2, download_pdttern_1, args=(headers,))
        # timer.start()

        # dealy 2 time acquisition duration
        delay_2a = 5
        iteraction = 0

        await asyncio.sleep(delay_2a)
        await acquire_waveform(iteraction)







    except requests.exceptions.ConnectionError:

            time.sleep(5)
            measurement_time = None

    except requests.exceptions.ConnectTimeout:

            time.sleep(5)
            measurement_time = None

    except requests.exceptions.JSONDecodeError:


            time.sleep(5)

            measurement_time = None



    return formatted_date, acq_number, Qpos, Qneg, Qmax95, Number_of_pulses, Nw, polarity_identification, phase_factor,automatic_identification, json_phase, json_amplitude, json_equ_timelenght, json_equ_frequency, json_average_waveform


def run_acquisition():
    print('run acqusition in progress')
    result = asyncio.run(perform_pd_measurement())
    print('measurement completed')

    return result


# print(run_acquisition())