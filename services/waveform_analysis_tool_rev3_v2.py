import csv
import numpy as np
import pandas as pd
import os.path
from numpy import loadtxt
from scipy.fftpack import fft, ifft
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt

#parameter to be adjusted
shape_factor_criteria = 10
#note:
#sometimes the algorithm pick up the second part of the pulse so to higher amplitude and the shape factor becames ineffective

down_time_delay = 0
#note
#using 0 as dealay helps to get the right peak, but sometimes if the pulse its slow mix the peaks

noise_criteria = 1.90 #select the 90% of the pulses only
#note
# to eliminate the noise pulses

first_pulse_number_of_sample_criteria = 30 # maximum size of the first pulse - if larger the peak detection is repeated
#note
# to try to solve the problem where the second pulse has a higher peak of the first pulse




def average_waveform(file_name):
    # open the different waveform and make an average


    df_waveform = pd.read_excel("{}.xlsx".format(file_name))

    waveform_list=[]

    index = 0
    while index < 12:

        amplitude_list = list(df_waveform.get("elaborated".format(index)))
        waveform_list.append(amplitude_list)
        index +=1

        if index >12:
            break
    print(waveform_list)
    # create the average list
    average_amplitude_list = []

    index = 0
    value = 0
    while value < len(waveform_list[0]):
        value_list = []
        while index < len(waveform_list):
            value_list.append(waveform_list[index][value])
            index +=1
            if index > len(waveform_list):
                break

        average_amplitude_value = sum(value_list)/len(value_list)
        average_amplitude_list.append(average_amplitude_value)
        print(average_amplitude_list)

        value +=1
        index = 0

        if value >len(waveform_list[0]):
            break
    # print(average_amplitude_list)

    return average_amplitude_list
    
def peak_detection_rev1(waveform_file):

    df_waveform = pd.read_csv("{}".format(waveform_file))

    #time_list = list(df_waveform.get("Time [s] - Plot 0"))
    #amplitude_list = waveform_list.tolist()
    amplitude_list = list(df_waveform.get('Amplitude'))
    #print(amplitude_list)

    time_list = []
    i=1
    for item in amplitude_list:
        time_list.append(i)
        i+=1



    #evaluate average
    average_amplitude = sum(amplitude_list)/len(amplitude_list)

    # print("Average amplitude", abs(average_amplitude))
    # print("Negative noise trheshold:", (abs(average_amplitude)-abs(average_amplitude)*noise_criteria))
    # print("Positive noise trheshold:", (abs(average_amplitude) + abs(average_amplitude) * noise_criteria))



    #parameter of the aquisition
    time_lenght = len(time_list)


    #parameters of the oscilloscope
    sample_rating_MSa = 100000000 #PDcheck
    # sample_rating_MSa = 125000000 #falcon
    time_resolution = 1/sample_rating_MSa

    # print("Time lenght [s]", time_lenght*time_resolution)

    #create dictionary for each point for easier analysis of the time
    index = 0
    combined_list = []
    while index < len(time_list):
        point_dict ={}
        point_dict['{}'.format(index+1)] = [time_list[index], amplitude_list[index]]
        combined_list.append(point_dict)
        index +=1
        if index > len(time_list):
            break


    def first_peak_detector():
        #find the highest posive and negative peaks to identify the first peak
        #peak 1
        # print("----------Pulse 1 analysis------------")

        peak_position = 0
        while peak_position <len(amplitude_list):
            # print(peak_position)

            if peak_position==0:
                #amplitude
                amplitude_list.sort(reverse=True)

                pospeak1_a=amplitude_list[peak_position]


                amplitude_list.sort(reverse=False)
                negpeak1_a = amplitude_list[peak_position]

            # print("positive peak:", pospeak1_a)
            # print("negative peak:",negpeak1_a)


            #determine delta between peak to determine the size of the pulse
            index=0
            number_of_sample_positive_pulse = 0
            number_of_sample_negative_pulse = 0


            while index <len(combined_list):

                if combined_list[index]['{}'.format(index+1)][1] != pospeak1_a and combined_list[index]['{}'.format(index+1)][1] != negpeak1_a:
                    None
                # positive peak - time
                if combined_list[index]['{}'.format(index+1)][1] == pospeak1_a:
                    number_of_sample_positive_pulse=index+1

                #negative peak - time
                if combined_list[index]['{}'.format(index+1)][1] == negpeak1_a:
                    number_of_sample_negative_pulse=index+1

                index +=1
                if index > len(combined_list):
                    break



            #determine pulse polarity and width
            pulse_polarity = None
            if number_of_sample_positive_pulse>number_of_sample_negative_pulse:
                # print("pulse start sample:", number_of_sample_negative_pulse)
                # print("pulse end sample:",number_of_sample_positive_pulse)

                pulse_width_ns = (number_of_sample_positive_pulse-number_of_sample_negative_pulse)*time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "negative pulse"

            if number_of_sample_negative_pulse > number_of_sample_positive_pulse:
                # print("pulse start sample:", number_of_sample_positive_pulse)
                # print("pulse end sample:", number_of_sample_negative_pulse)

                pulse_width_ns = (number_of_sample_negative_pulse - number_of_sample_positive_pulse) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "positive pulse"

            # print("Pulse polarity:", pulse_polarity)

            # verify the distance between the identified peaks - in case the second pulse is bigger than the first we need to get the second max point
            measured_pulse_number_of_sample = abs(number_of_sample_positive_pulse - number_of_sample_negative_pulse)
            # print(measured_pulse_number_of_sample)

            if measured_pulse_number_of_sample > first_pulse_number_of_sample_criteria:
                if pulse_polarity == "positive pulse":
                    #we have to change the negative peak since it is too ahead



                    negpeak1_a = amplitude_list[peak_position+1]

                    # print("new positive peak:", pospeak1_a)
                    # print("new negative peak:", negpeak1_a)



                if pulse_polarity == "negative pulse":
                    #we have to change the positive peak since it is too ahead
                    amplitude_list.sort(reverse=True)

                    pospeak1_a = amplitude_list[peak_position+1]

                    # print("new positive peak:", pospeak1_a)
                    # print("new negative peak:", negpeak1_a)

            if measured_pulse_number_of_sample <= first_pulse_number_of_sample_criteria:
                break

            peak_position +=1
            if peak_position > len(amplitude_list):
                break

        #evaluate pulse area
        peak_max = max(pospeak1_a, negpeak1_a)

        second_pulse_search_start_point = None
        pulse_area = peak_max*pulse_width_ns

         # print("Pulse area:", pulse_area)

        #determine ration between peak and delta between peak
        if pulse_polarity == "positive pulse":
                delta_amplitude = (pospeak1_a-negpeak1_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_negative_pulse


                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        second_pulse_search_start_point = first_zero_position
                        break



                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

                # print(second_pulse_search_start_point)

        if pulse_polarity == "negative pulse":
                delta_amplitude = (negpeak1_a-pospeak1_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_positive_pulse

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        second_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

        print(second_pulse_search_start_point)



        positive_amplitude_ratio = pospeak1_a / delta_amplitude
        negative_amplitude_ratio = negpeak1_a / delta_amplitude




        return pulse_polarity, number_of_sample_positive_pulse, number_of_sample_negative_pulse, pulse_width_ns, pulse_area,positive_amplitude_ratio, negative_amplitude_ratio, second_pulse_search_start_point

    def second_peak_detection(starting_sample):
        # second peak analysis
        # print("----------Pulse 2 analysis------------")
        # create new amplitude list by eliminating all the sample prior the end of the first peak




        ##############################################################################################################################################################


        second_amplitude_list = []
        index = starting_sample +1+down_time_delay #+4to avoid to get the same pulse on the down time

        pospeak2_a = 0
        negpeak2_a = 0

        if index <time_lenght-1:


            while index < len(combined_list):

                second_amplitude_list.append(combined_list[index]['{}'.format(index+1)][1])

                index += 1
                if index > len(combined_list):
                    break





            #find second peak
            # amplitude
            second_amplitude_list.sort(reverse=True)
            pospeak2_a = second_amplitude_list[0]


            second_amplitude_list.sort(reverse=False)
            negpeak2_a = second_amplitude_list[0]


            # print("positive peak:", pospeak2_a)
            # print("negative peak:", negpeak2_a)


        # determine delta between peak to determine the size of the pulse
        index = starting_sample
        number_of_sample_positive_pulse_peak2 = 0
        number_of_sample_negative_pulse_peak2 = 0

        while index < len(combined_list):

            if combined_list[index]['{}'.format(index + 1)][1] != pospeak2_a and \
                    combined_list[index]['{}'.format(index + 1)][1] != negpeak2_a:
                None
            # positive peak - time
            if combined_list[index]['{}'.format(index + 1)][1] == pospeak2_a:
                number_of_sample_positive_pulse_peak2 = index + 1

            # negative peak - time
            if combined_list[index]['{}'.format(index + 1)][1] == negpeak2_a:
                number_of_sample_negative_pulse_peak2 = index + 1

            index += 1
            if index > len(combined_list):
                break

        #add condition to stop the search and assign the peak to None if we are at the end of the sample

        # verify the distance between the identified peaks - in case the second pulse is bigger than the first we need to get the second max point
        measured_pulse_number_of_sample = abs(number_of_sample_positive_pulse_peak2 - number_of_sample_negative_pulse_peak2)
        # print("Distance between sample",measured_pulse_number_of_sample)


        # determine pulse polarity and width
        pulse_polarity = None
        if number_of_sample_positive_pulse_peak2 != time_lenght and number_of_sample_negative_pulse_peak2 != time_lenght:
            if number_of_sample_positive_pulse_peak2 > number_of_sample_negative_pulse_peak2:
                # print("pulse start sample:", number_of_sample_negative_pulse_peak2)
                # print("pulse end sample:", number_of_sample_positive_pulse_peak2)

                pulse_width_ns = (number_of_sample_positive_pulse_peak2 - number_of_sample_negative_pulse_peak2) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "negative pulse"

            if number_of_sample_negative_pulse_peak2 > number_of_sample_positive_pulse_peak2:
                # print("pulse start sample:", number_of_sample_positive_pulse_peak2)
                # print("pulse end sample:", number_of_sample_negative_pulse_peak2)

                pulse_width_ns = (number_of_sample_positive_pulse_peak2 - number_of_sample_negative_pulse_peak2) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "positive pulse"

        if number_of_sample_positive_pulse_peak2 == time_lenght or number_of_sample_negative_pulse_peak2 == time_lenght:
            None


        # print("Pulse polarity:",pulse_polarity)

        # evaluate pulse area
        peak_max = max(pospeak2_a, negpeak2_a)

        third_pulse_search_start_point = None

        if pulse_polarity != None:
            pulse_area = peak_max * pulse_width_ns
            # print("Pulse area:", pulse_area)


            # determine ration between peak and delta between peak
            if pulse_polarity == "positive pulse":
                delta_amplitude = (pospeak2_a - negpeak2_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_negative_pulse_peak2

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        third_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

                # print(third_pulse_search_start_point)

            if pulse_polarity == "negative pulse":
                delta_amplitude = (negpeak2_a - pospeak2_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_positive_pulse_peak2

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        third_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

                # print(third_pulse_search_start_point)

            positive_amplitude_ratio = pospeak2_a / delta_amplitude
            negative_amplitude_ratio = negpeak2_a / delta_amplitude

        if pulse_polarity == None:
            pulse_width_ns = None
            pulse_area = None
            delta_amplitude = None
            positive_amplitude_ratio = None
            negative_amplitude_ratio = None

        return pulse_polarity,  number_of_sample_positive_pulse_peak2, number_of_sample_negative_pulse_peak2, pulse_width_ns, pulse_area, positive_amplitude_ratio, negative_amplitude_ratio, third_pulse_search_start_point, pospeak2_a, negpeak2_a

    def third_peak_detection(starting_sample):
        # second peak analysis
        # print("----------Pulse 3 analysis------------")

        # create new amplitude list by eliminating all the sample prior the end of the first peak




        ##############################################################################################################################################################


        third_amplitude_list = []
        index = starting_sample+1+down_time_delay #+4 to avoid to get the same pulse on the downside
        #
        # print(combined_list)
        pospeak3_a = 0
        negpeak3_a = 0

        if index <time_lenght-1:

            while index < len(combined_list):

                third_amplitude_list.append(combined_list[index]['{}'.format(index+1)][1])

                index += 1
                if index > len(combined_list):
                    break



            #find second peak
            # amplitude
            third_amplitude_list.sort(reverse=True)
            pospeak3_a = third_amplitude_list[0]


            third_amplitude_list.sort(reverse=False)
            negpeak3_a = third_amplitude_list[0]


            # print("positive peak:", pospeak3_a)
            # print("negative peak:", negpeak3_a)



        # determine delta between peak to determine the size of the pulse
        index = starting_sample
        number_of_sample_positive_pulse_peak3 = 0
        number_of_sample_negative_pulse_peak3 = 0

        while index < len(combined_list):

            if combined_list[index]['{}'.format(index + 1)][1] != pospeak3_a and \
                    combined_list[index]['{}'.format(index + 1)][1] != negpeak3_a:
                None
            # positive peak - time
            if combined_list[index]['{}'.format(index + 1)][1] == pospeak3_a:
                number_of_sample_positive_pulse_peak3 = index + 1

            # negative peak - time
            if combined_list[index]['{}'.format(index + 1)][1] == negpeak3_a:
                number_of_sample_negative_pulse_peak3 = index + 1

            index += 1
            if index > len(combined_list):
                break

        # add condition to stop the search and assign the peak to None if we are at the end of the sample
        # determine pulse polarity and width
        pulse_polarity = None
        if number_of_sample_positive_pulse_peak3 != time_lenght and number_of_sample_negative_pulse_peak3!=time_lenght:
            if number_of_sample_positive_pulse_peak3 > number_of_sample_negative_pulse_peak3:
                # print("pulse start sample:", number_of_sample_negative_pulse_peak3)
                # print("pulse end sample:", number_of_sample_positive_pulse_peak3)

                pulse_width_ns = (number_of_sample_positive_pulse_peak3 - number_of_sample_negative_pulse_peak3) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "negative pulse"

            if number_of_sample_negative_pulse_peak3 > number_of_sample_positive_pulse_peak3:
                # print("pulse start sample:", number_of_sample_positive_pulse_peak3)
                # print("pulse end sample:", number_of_sample_negative_pulse_peak3)

                pulse_width_ns = (number_of_sample_positive_pulse_peak3 - number_of_sample_negative_pulse_peak3) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "positive pulse"

        if number_of_sample_positive_pulse_peak3 == time_lenght and number_of_sample_negative_pulse_peak3==time_lenght:
            None

        # print("Pulse polarity:",pulse_polarity)

        # evaluate pulse area
        peak_max = max(pospeak3_a, negpeak3_a)
        fourth_pulse_search_start_point= None
        if pulse_polarity!=None:
            pulse_area = peak_max * pulse_width_ns
            # print("Pulse area:", pulse_area)

            # determine ration between peak and delta between peak
            if pulse_polarity == "positive pulse":
                delta_amplitude = (pospeak3_a - negpeak3_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_negative_pulse_peak3

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        fourth_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

            if pulse_polarity == "negative pulse":
                delta_amplitude = (negpeak3_a - pospeak3_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_positive_pulse_peak3

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        fourth_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

            positive_amplitude_ratio = pospeak3_a / delta_amplitude
            negative_amplitude_ratio = negpeak3_a / delta_amplitude
        if pulse_polarity == None:
            pulse_width_ns = None
            pulse_area = None
            delta_amplitude = None
            positive_amplitude_ratio = None
            negative_amplitude_ratio = None


        return pulse_polarity,  number_of_sample_positive_pulse_peak3, number_of_sample_negative_pulse_peak3, pulse_width_ns, pulse_area, positive_amplitude_ratio, negative_amplitude_ratio, fourth_pulse_search_start_point, pospeak3_a, negpeak3_a

    #################################################  first peak  ###################################################
    #first peak detection

    first_peak_details = first_peak_detector()
    first_peak_pulse_polarity = first_peak_details[0]
    first_peak_number_of_sample_positve_pulse = first_peak_details[1]
    first_peak_number_of_sample_negative_pulse = first_peak_details[2]
    first_peak_pulse_width = first_peak_details[3]
    first_peak_area = first_peak_details[4]
    first_peak_positive_amplitude_ratio = first_peak_details[5]
    first_peak_negative_amplitude_ratio = first_peak_details[6]

    first_zero_after_pulse = first_peak_details[7]
    print("first zero after pulse:", first_zero_after_pulse)

    # determine end of the first peak
    first_peak_end = 0

    if first_peak_pulse_polarity == "positive pulse":
        first_peak_end = first_peak_number_of_sample_negative_pulse

    if first_peak_pulse_polarity == "negative pulse":
        first_peak_end = first_peak_number_of_sample_positve_pulse

    #################################################  second peak  ###################################################33
    #search the second peak with iterative process
    if first_zero_after_pulse !=None:
        starting_sample = first_zero_after_pulse
    if first_zero_after_pulse == None:
        #if there is no detectuib if zero, start at the end of the waveform - only one pulse
        #starting_sample=first_peak_end - old method
        starting_sample=time_lenght-1

    while starting_sample < time_lenght:

        # print("startpoint", starting_sample)


        second_peak_details = second_peak_detection(starting_sample)
        second_peak_pulse_polarity = second_peak_details[0]
        second_peak_number_of_sample_positive_pulse = second_peak_details[1]
        second_peak_number_of_sample_negative_pulse = second_peak_details[2]
        second_peak_pulse_width = second_peak_details[3]
        second_peak_area = second_peak_details[4]
        second_peak_positive_amplitude_ratio = second_peak_details[5]
        second_peak_negative_amplitude_ratio = second_peak_details[6]
        second_peak_positive_amplitude = second_peak_details[8]
        second_peak_negative_amplitude = second_peak_details[9]

        first_zero_after_pulse_2 = second_peak_details[7]

        # print("First zero after pulse 2", first_zero_after_pulse_2)

        # determine end of the identified peak
        identified_peak_end = 0

        if second_peak_pulse_polarity == "positive pulse":
            identified_peak_end = second_peak_number_of_sample_negative_pulse

            if (abs(average_amplitude)-(abs(average_amplitude)*noise_criteria))< second_peak_positive_amplitude < (abs(average_amplitude)+(abs(average_amplitude)*noise_criteria)):
                starting_sample=identified_peak_end

            if second_peak_positive_amplitude > (abs(average_amplitude)+(abs(average_amplitude)*noise_criteria)):
                break

        if second_peak_pulse_polarity == "negative pulse":
            identified_peak_end = second_peak_number_of_sample_positive_pulse

            if (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)) < second_peak_negative_amplitude < (abs(average_amplitude) + (abs(average_amplitude) * noise_criteria)):
                starting_sample = identified_peak_end

            if second_peak_negative_amplitude < (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)):
                break

        if second_peak_pulse_polarity == None:
            #if second peak not found the third peak should not be searched
            starting_sample = time_lenght
            break



        if starting_sample >= time_lenght:
            break


    # determine end of the second peak
    second_peak_end = 0

    if second_peak_pulse_polarity == "positive pulse":
        second_peak_end = second_peak_number_of_sample_negative_pulse

    if second_peak_pulse_polarity == "negative pulse":
        second_peak_end = second_peak_number_of_sample_positive_pulse

    if second_peak_pulse_polarity == None:
        #if second peak not detected then the process should stop
        second_peak_details=None
        second_peak_end = time_lenght

    #################################################  third peak  ###################################################
    #search the third peak with iterative process
    if first_zero_after_pulse_2 !=None:
        starting_sample = first_zero_after_pulse_2

    if first_zero_after_pulse_2 == None:
        starting_sample=second_peak_end

    while starting_sample < time_lenght:
    #
    #     # print("startpoint", starting_sample)


        third_peak_details = third_peak_detection(starting_sample)
        third_peak_pulse_polarity = third_peak_details[0]
        third_peak_number_of_sample_positive_pulse = third_peak_details[1]
        third_peak_number_of_sample_negative_pulse = third_peak_details[2]
        third_peak_pulse_width = third_peak_details[3]
        third_peak_area = third_peak_details[4]
        third_peak_positive_amplitude_ratio = third_peak_details[5]
        third_peak_negative_amplitude_ratio = third_peak_details[6]

        third_peak_positive_amplitude = third_peak_details[8]
        third_peak_negative_amplitude = third_peak_details[9]






        # determine end of the identified peak
        identified_peak_end = 0

        if third_peak_pulse_polarity == "positive pulse":
            identified_peak_end = third_peak_number_of_sample_negative_pulse

            if (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)) < third_peak_positive_amplitude < (
                    abs(average_amplitude) + (abs(average_amplitude) * noise_criteria)):
                starting_sample = identified_peak_end

            if third_peak_positive_amplitude > (abs(average_amplitude) + (abs(average_amplitude) * noise_criteria)):
                if second_peak_pulse_polarity == "positive pulse":
                    factor = abs(
                        (100 - (abs(third_peak_positive_amplitude_ratio / second_peak_positive_amplitude_ratio) * 100)))
                    # print("Factor", factor)
                    if 0 <= factor <= shape_factor_criteria:
                        break
                    if factor > shape_factor_criteria or factor < 0:
                        starting_sample = identified_peak_end

                if second_peak_pulse_polarity == "negative pulse":
                    factor = abs(
                        (100 - (abs(third_peak_positive_amplitude_ratio / second_peak_negative_amplitude_ratio) * 100)))
                    # print("Factor", factor)
                    if 0 <= factor <= shape_factor_criteria:
                        break
                    if factor > shape_factor_criteria or factor < 0:
                        starting_sample = identified_peak_end


        if third_peak_pulse_polarity == "negative pulse":
            identified_peak_end = third_peak_number_of_sample_positive_pulse
            # print(third_peak_negative_amplitude)
            # print(fuck)
            if (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)) < third_peak_negative_amplitude < (
                    abs(average_amplitude) + (abs(average_amplitude) * noise_criteria)):
                starting_sample = identified_peak_end

            if third_peak_negative_amplitude < (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)):
                #verify factor
                if second_peak_pulse_polarity == "positive pulse":

                    factor = abs(
                        (100 - (abs(third_peak_negative_amplitude_ratio / second_peak_positive_amplitude_ratio) * 100)))
                    # print("Factor", factor)
                    if 0 <= factor <= shape_factor_criteria:
                        break
                    if factor > shape_factor_criteria or factor < 0:
                        starting_sample = identified_peak_end

                if second_peak_pulse_polarity == "negative pulse":
                    factor = abs(
                        (100 - (abs(third_peak_negative_amplitude_ratio / second_peak_negative_amplitude_ratio) * 100)))
                    # print("Factor", factor)
                    if 0 <= factor <= shape_factor_criteria:
                        break
                    if factor > shape_factor_criteria or factor < 0:
                        starting_sample = identified_peak_end







        if third_peak_pulse_polarity == None:
            third_peak_details=None
            break



        if starting_sample > time_lenght:
            break

    if starting_sample == time_lenght:
        third_peak_details=None





    return first_peak_details, second_peak_details, third_peak_details, time_resolution



def peak_detection(waveform_list):

    # df_waveform = pd.read_excel("{}.xlsx".format(file_name))

    # time_list = list(df_waveform.get("Time [s] - Plot 0"))
    amplitude_list = waveform_list.tolist()


    time_list = []
    i=1
    for item in amplitude_list:
        time_list.append(i)
        i+=1



    #evaluate average
    average_amplitude = sum(amplitude_list)/len(amplitude_list)

    # print("Average amplitude", abs(average_amplitude))
    # print("Negative noise trheshold:", (abs(average_amplitude)-abs(average_amplitude)*noise_criteria))
    # print("Positive noise trheshold:", (abs(average_amplitude) + abs(average_amplitude) * noise_criteria))



    #parameter of the aquisition
    time_lenght = len(time_list)


    #parameters of the oscilloscope
    sample_rating_MSa = 100000000 #PDcheck
    # sample_rating_MSa = 125000000 #falcon
    time_resolution = 1/sample_rating_MSa

    # print("Time lenght [s]", time_lenght*time_resolution)

    #create dictionary for each point for easier analysis of the time
    index = 0
    combined_list = []
    while index < len(time_list):
        point_dict ={}
        point_dict['{}'.format(index+1)] = [time_list[index], amplitude_list[index]]
        combined_list.append(point_dict)
        index +=1
        if index > len(time_list):
            break


    def first_peak_detector():
        #find the highest posive and negative peaks to identify the first peak
        #peak 1
        # print("----------Pulse 1 analysis------------")

        peak_position = 0
        while peak_position <len(amplitude_list):
            # print(peak_position)

            if peak_position==0:
                #amplitude
                amplitude_list.sort(reverse=True)

                pospeak1_a=amplitude_list[peak_position]


                amplitude_list.sort(reverse=False)
                negpeak1_a = amplitude_list[peak_position]

            # print("positive peak:", pospeak1_a)
            # print("negative peak:",negpeak1_a)


            #determine delta between peak to determine the size of the pulse
            index=0
            number_of_sample_positive_pulse = 0
            number_of_sample_negative_pulse = 0


            while index <len(combined_list):

                if combined_list[index]['{}'.format(index+1)][1] != pospeak1_a and combined_list[index]['{}'.format(index+1)][1] != negpeak1_a:
                    None
                # positive peak - time
                if combined_list[index]['{}'.format(index+1)][1] == pospeak1_a:
                    number_of_sample_positive_pulse=index+1

                #negative peak - time
                if combined_list[index]['{}'.format(index+1)][1] == negpeak1_a:
                    number_of_sample_negative_pulse=index+1

                index +=1
                if index > len(combined_list):
                    break



            #determine pulse polarity and width
            pulse_polarity = None
            if number_of_sample_positive_pulse>number_of_sample_negative_pulse:
                # print("pulse start sample:", number_of_sample_negative_pulse)
                # print("pulse end sample:",number_of_sample_positive_pulse)

                pulse_width_ns = (number_of_sample_positive_pulse-number_of_sample_negative_pulse)*time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "negative pulse"

            if number_of_sample_negative_pulse > number_of_sample_positive_pulse:
                # print("pulse start sample:", number_of_sample_positive_pulse)
                # print("pulse end sample:", number_of_sample_negative_pulse)

                pulse_width_ns = (number_of_sample_negative_pulse - number_of_sample_positive_pulse) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "positive pulse"

            # print("Pulse polarity:", pulse_polarity)

            # verify the distance between the identified peaks - in case the second pulse is bigger than the first we need to get the second max point
            measured_pulse_number_of_sample = abs(number_of_sample_positive_pulse - number_of_sample_negative_pulse)
            # print(measured_pulse_number_of_sample)

            if measured_pulse_number_of_sample > first_pulse_number_of_sample_criteria:
                if pulse_polarity == "positive pulse":
                    #we have to change the negative peak since it is too ahead



                    negpeak1_a = amplitude_list[peak_position+1]

                    # print("new positive peak:", pospeak1_a)
                    # print("new negative peak:", negpeak1_a)



                if pulse_polarity == "negative pulse":
                    #we have to change the positive peak since it is too ahead
                    amplitude_list.sort(reverse=True)

                    pospeak1_a = amplitude_list[peak_position+1]

                    # print("new positive peak:", pospeak1_a)
                    # print("new negative peak:", negpeak1_a)

            if measured_pulse_number_of_sample <= first_pulse_number_of_sample_criteria:
                break

            peak_position +=1
            if peak_position > len(amplitude_list):
                break

        #evaluate pulse area
        peak_max = max(pospeak1_a, negpeak1_a)

        second_pulse_search_start_point = None
        pulse_area = peak_max*pulse_width_ns

         # print("Pulse area:", pulse_area)

        #determine ration between peak and delta between peak
        if pulse_polarity == "positive pulse":
                delta_amplitude = (pospeak1_a-negpeak1_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_negative_pulse


                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        second_pulse_search_start_point = first_zero_position
                        break



                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

                # print(second_pulse_search_start_point)

        if pulse_polarity == "negative pulse":
                delta_amplitude = (negpeak1_a-pospeak1_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_positive_pulse

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        second_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

        # print(second_pulse_search_start_point)



        positive_amplitude_ratio = pospeak1_a / delta_amplitude
        negative_amplitude_ratio = negpeak1_a / delta_amplitude




        return pulse_polarity, number_of_sample_positive_pulse, number_of_sample_negative_pulse, pulse_width_ns, pulse_area,positive_amplitude_ratio, negative_amplitude_ratio, second_pulse_search_start_point

    def second_peak_detection(starting_sample):
        # second peak analysis
        # print("----------Pulse 2 analysis------------")
        # create new amplitude list by eliminating all the sample prior the end of the first peak




        ##############################################################################################################################################################


        second_amplitude_list = []
        index = starting_sample +1+down_time_delay #+4to avoid to get the same pulse on the down time

        pospeak2_a = 0
        negpeak2_a = 0

        if index <time_lenght-1:


            while index < len(combined_list):

                second_amplitude_list.append(combined_list[index]['{}'.format(index+1)][1])

                index += 1
                if index > len(combined_list):
                    break





            #find second peak
            # amplitude
            second_amplitude_list.sort(reverse=True)
            pospeak2_a = second_amplitude_list[0]


            second_amplitude_list.sort(reverse=False)
            negpeak2_a = second_amplitude_list[0]


            # print("positive peak:", pospeak2_a)
            # print("negative peak:", negpeak2_a)


        # determine delta between peak to determine the size of the pulse
        index = starting_sample
        number_of_sample_positive_pulse_peak2 = 0
        number_of_sample_negative_pulse_peak2 = 0

        while index < len(combined_list):

            if combined_list[index]['{}'.format(index + 1)][1] != pospeak2_a and \
                    combined_list[index]['{}'.format(index + 1)][1] != negpeak2_a:
                None
            # positive peak - time
            if combined_list[index]['{}'.format(index + 1)][1] == pospeak2_a:
                number_of_sample_positive_pulse_peak2 = index + 1

            # negative peak - time
            if combined_list[index]['{}'.format(index + 1)][1] == negpeak2_a:
                number_of_sample_negative_pulse_peak2 = index + 1

            index += 1
            if index > len(combined_list):
                break

        #add condition to stop the search and assign the peak to None if we are at the end of the sample

        # verify the distance between the identified peaks - in case the second pulse is bigger than the first we need to get the second max point
        measured_pulse_number_of_sample = abs(number_of_sample_positive_pulse_peak2 - number_of_sample_negative_pulse_peak2)
        # print("Distance between sample",measured_pulse_number_of_sample)


        # determine pulse polarity and width
        pulse_polarity = None
        if number_of_sample_positive_pulse_peak2 != time_lenght and number_of_sample_negative_pulse_peak2 != time_lenght:
            if number_of_sample_positive_pulse_peak2 > number_of_sample_negative_pulse_peak2:
                # print("pulse start sample:", number_of_sample_negative_pulse_peak2)
                # print("pulse end sample:", number_of_sample_positive_pulse_peak2)

                pulse_width_ns = (number_of_sample_positive_pulse_peak2 - number_of_sample_negative_pulse_peak2) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "negative pulse"

            if number_of_sample_negative_pulse_peak2 > number_of_sample_positive_pulse_peak2:
                # print("pulse start sample:", number_of_sample_positive_pulse_peak2)
                # print("pulse end sample:", number_of_sample_negative_pulse_peak2)

                pulse_width_ns = (number_of_sample_positive_pulse_peak2 - number_of_sample_negative_pulse_peak2) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "positive pulse"

        if number_of_sample_positive_pulse_peak2 == time_lenght or number_of_sample_negative_pulse_peak2 == time_lenght:
            None


        # print("Pulse polarity:",pulse_polarity)

        # evaluate pulse area
        peak_max = max(pospeak2_a, negpeak2_a)

        third_pulse_search_start_point = None

        if pulse_polarity != None:
            pulse_area = peak_max * pulse_width_ns
            # print("Pulse area:", pulse_area)


            # determine ration between peak and delta between peak
            if pulse_polarity == "positive pulse":
                delta_amplitude = (pospeak2_a - negpeak2_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_negative_pulse_peak2

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        third_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

                # print(third_pulse_search_start_point)

            if pulse_polarity == "negative pulse":
                delta_amplitude = (negpeak2_a - pospeak2_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_positive_pulse_peak2

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        third_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

                # print(third_pulse_search_start_point)

            positive_amplitude_ratio = pospeak2_a / delta_amplitude
            negative_amplitude_ratio = negpeak2_a / delta_amplitude

        if pulse_polarity == None:
            pulse_width_ns = None
            pulse_area = None
            delta_amplitude = None
            positive_amplitude_ratio = None
            negative_amplitude_ratio = None

        return pulse_polarity,  number_of_sample_positive_pulse_peak2, number_of_sample_negative_pulse_peak2, pulse_width_ns, pulse_area, positive_amplitude_ratio, negative_amplitude_ratio, third_pulse_search_start_point, pospeak2_a, negpeak2_a

    def third_peak_detection(starting_sample):
        # second peak analysis
        # print("----------Pulse 3 analysis------------")

        # create new amplitude list by eliminating all the sample prior the end of the first peak




        ##############################################################################################################################################################


        third_amplitude_list = []
        index = starting_sample+1+down_time_delay #+4 to avoid to get the same pulse on the downside
        #
        # print(combined_list)
        pospeak3_a = 0
        negpeak3_a = 0

        if index <time_lenght-1:

            while index < len(combined_list):

                third_amplitude_list.append(combined_list[index]['{}'.format(index+1)][1])

                index += 1
                if index > len(combined_list):
                    break



            #find second peak
            # amplitude
            third_amplitude_list.sort(reverse=True)
            pospeak3_a = third_amplitude_list[0]


            third_amplitude_list.sort(reverse=False)
            negpeak3_a = third_amplitude_list[0]


            # print("positive peak:", pospeak3_a)
            # print("negative peak:", negpeak3_a)



        # determine delta between peak to determine the size of the pulse
        index = starting_sample
        number_of_sample_positive_pulse_peak3 = 0
        number_of_sample_negative_pulse_peak3 = 0

        while index < len(combined_list):

            if combined_list[index]['{}'.format(index + 1)][1] != pospeak3_a and \
                    combined_list[index]['{}'.format(index + 1)][1] != negpeak3_a:
                None
            # positive peak - time
            if combined_list[index]['{}'.format(index + 1)][1] == pospeak3_a:
                number_of_sample_positive_pulse_peak3 = index + 1

            # negative peak - time
            if combined_list[index]['{}'.format(index + 1)][1] == negpeak3_a:
                number_of_sample_negative_pulse_peak3 = index + 1

            index += 1
            if index > len(combined_list):
                break

        # add condition to stop the search and assign the peak to None if we are at the end of the sample
        # determine pulse polarity and width
        pulse_polarity = None
        if number_of_sample_positive_pulse_peak3 != time_lenght and number_of_sample_negative_pulse_peak3!=time_lenght:
            if number_of_sample_positive_pulse_peak3 > number_of_sample_negative_pulse_peak3:
                # print("pulse start sample:", number_of_sample_negative_pulse_peak3)
                # print("pulse end sample:", number_of_sample_positive_pulse_peak3)

                pulse_width_ns = (number_of_sample_positive_pulse_peak3 - number_of_sample_negative_pulse_peak3) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "negative pulse"

            if number_of_sample_negative_pulse_peak3 > number_of_sample_positive_pulse_peak3:
                # print("pulse start sample:", number_of_sample_positive_pulse_peak3)
                # print("pulse end sample:", number_of_sample_negative_pulse_peak3)

                pulse_width_ns = (number_of_sample_positive_pulse_peak3 - number_of_sample_negative_pulse_peak3) * time_resolution
                # print("pulse width:", pulse_width_ns)

                pulse_polarity = "positive pulse"

        if number_of_sample_positive_pulse_peak3 == time_lenght and number_of_sample_negative_pulse_peak3==time_lenght:
            None

        # print("Pulse polarity:",pulse_polarity)

        # evaluate pulse area
        peak_max = max(pospeak3_a, negpeak3_a)
        fourth_pulse_search_start_point= None
        if pulse_polarity!=None:
            pulse_area = peak_max * pulse_width_ns
            # print("Pulse area:", pulse_area)

            # determine ration between peak and delta between peak
            if pulse_polarity == "positive pulse":
                delta_amplitude = (pospeak3_a - negpeak3_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_negative_pulse_peak3

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        fourth_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

            if pulse_polarity == "negative pulse":
                delta_amplitude = (negpeak3_a - pospeak3_a)

                # find the first 0 after the pulse to start the second peak search after that point
                first_zero_position = number_of_sample_positive_pulse_peak3

                while first_zero_position < len(combined_list):

                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] != 0:
                        None
                    # value is 0 - break
                    if combined_list[first_zero_position]['{}'.format(first_zero_position + 1)][1] == 0:
                        fourth_pulse_search_start_point = first_zero_position
                        break

                    first_zero_position += 1
                    if first_zero_position > len(combined_list):
                        break

            positive_amplitude_ratio = pospeak3_a / delta_amplitude
            negative_amplitude_ratio = negpeak3_a / delta_amplitude
        if pulse_polarity == None:
            pulse_width_ns = None
            pulse_area = None
            delta_amplitude = None
            positive_amplitude_ratio = None
            negative_amplitude_ratio = None


        return pulse_polarity,  number_of_sample_positive_pulse_peak3, number_of_sample_negative_pulse_peak3, pulse_width_ns, pulse_area, positive_amplitude_ratio, negative_amplitude_ratio, fourth_pulse_search_start_point, pospeak3_a, negpeak3_a

    #################################################  first peak  ###################################################
    #first peak detection

    first_peak_details = first_peak_detector()
    first_peak_pulse_polarity = first_peak_details[0]
    first_peak_number_of_sample_positve_pulse = first_peak_details[1]
    first_peak_number_of_sample_negative_pulse = first_peak_details[2]
    first_peak_pulse_width = first_peak_details[3]
    first_peak_area = first_peak_details[4]
    first_peak_positive_amplitude_ratio = first_peak_details[5]
    first_peak_negative_amplitude_ratio = first_peak_details[6]

    first_zero_after_pulse = first_peak_details[7]
    # print("first zero after pulse:", first_zero_after_pulse)

    # determine end of the first peak
    first_peak_end = 0

    if first_peak_pulse_polarity == "positive pulse":
        first_peak_end = first_peak_number_of_sample_negative_pulse

    if first_peak_pulse_polarity == "negative pulse":
        first_peak_end = first_peak_number_of_sample_positve_pulse

    #################################################  second peak  ###################################################33
    #search the second peak with iterative process
    if first_zero_after_pulse !=None:
        starting_sample = first_zero_after_pulse
    if first_zero_after_pulse == None:
        #if no zero detected after the first peak move to the end - no other pulses
        #######starting_sample=first_peak_end
        starting_sample=time_lenght-1

    while starting_sample < time_lenght:

        # print("startpoint", starting_sample)


        second_peak_details = second_peak_detection(starting_sample)
        second_peak_pulse_polarity = second_peak_details[0]
        second_peak_number_of_sample_positive_pulse = second_peak_details[1]
        second_peak_number_of_sample_negative_pulse = second_peak_details[2]
        second_peak_pulse_width = second_peak_details[3]
        second_peak_area = second_peak_details[4]
        second_peak_positive_amplitude_ratio = second_peak_details[5]
        second_peak_negative_amplitude_ratio = second_peak_details[6]
        second_peak_positive_amplitude = second_peak_details[8]
        second_peak_negative_amplitude = second_peak_details[9]

        first_zero_after_pulse_2 = second_peak_details[7]

        # print("First zero after pulse 2", first_zero_after_pulse_2)

        # determine end of the identified peak
        identified_peak_end = 0

        if second_peak_pulse_polarity == "positive pulse":
            identified_peak_end = second_peak_number_of_sample_negative_pulse

            if (abs(average_amplitude)-(abs(average_amplitude)*noise_criteria))< second_peak_positive_amplitude < (abs(average_amplitude)+(abs(average_amplitude)*noise_criteria)):
                starting_sample=identified_peak_end

            if second_peak_positive_amplitude > (abs(average_amplitude)+(abs(average_amplitude)*noise_criteria)):
                break

        if second_peak_pulse_polarity == "negative pulse":
            identified_peak_end = second_peak_number_of_sample_positive_pulse

            if (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)) < second_peak_negative_amplitude < (abs(average_amplitude) + (abs(average_amplitude) * noise_criteria)):
                starting_sample = identified_peak_end

            if second_peak_negative_amplitude < (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)):
                break

        if second_peak_pulse_polarity == None:
            #if second peak not found the third peak should not be searched
            starting_sample = time_lenght
            break



        if starting_sample >= time_lenght:
            break


    # determine end of the second peak
    second_peak_end = 0

    if second_peak_pulse_polarity == "positive pulse":
        second_peak_end = second_peak_number_of_sample_negative_pulse

    if second_peak_pulse_polarity == "negative pulse":
        second_peak_end = second_peak_number_of_sample_positive_pulse

    if second_peak_pulse_polarity == None:
        #if second peak not detected then the process should stop
        second_peak_details=None
        second_peak_end = time_lenght

    #################################################  third peak  ###################################################
    #search the third peak with iterative process
    if first_zero_after_pulse_2 !=None:
        starting_sample = first_zero_after_pulse_2

    if first_zero_after_pulse_2 == None:
        starting_sample=second_peak_end

    while starting_sample < time_lenght:
    #
    #     # print("startpoint", starting_sample)


        third_peak_details = third_peak_detection(starting_sample)
        third_peak_pulse_polarity = third_peak_details[0]
        third_peak_number_of_sample_positive_pulse = third_peak_details[1]
        third_peak_number_of_sample_negative_pulse = third_peak_details[2]
        third_peak_pulse_width = third_peak_details[3]
        third_peak_area = third_peak_details[4]
        third_peak_positive_amplitude_ratio = third_peak_details[5]
        third_peak_negative_amplitude_ratio = third_peak_details[6]

        third_peak_positive_amplitude = third_peak_details[8]
        third_peak_negative_amplitude = third_peak_details[9]






        # determine end of the identified peak
        identified_peak_end = 0

        if third_peak_pulse_polarity == "positive pulse":
            identified_peak_end = third_peak_number_of_sample_negative_pulse

            if (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)) < third_peak_positive_amplitude < (
                    abs(average_amplitude) + (abs(average_amplitude) * noise_criteria)):
                starting_sample = identified_peak_end

            if third_peak_positive_amplitude > (abs(average_amplitude) + (abs(average_amplitude) * noise_criteria)):
                if second_peak_pulse_polarity == "positive pulse":
                    factor = abs(
                        (100 - (abs(third_peak_positive_amplitude_ratio / second_peak_positive_amplitude_ratio) * 100)))
                    # print("Factor", factor)
                    if 0 <= factor <= shape_factor_criteria:
                        break
                    if factor > shape_factor_criteria or factor < 0:
                        starting_sample = identified_peak_end

                if second_peak_pulse_polarity == "negative pulse":
                    factor = abs(
                        (100 - (abs(third_peak_positive_amplitude_ratio / second_peak_negative_amplitude_ratio) * 100)))
                    # print("Factor", factor)
                    if 0 <= factor <= shape_factor_criteria:
                        break
                    if factor > shape_factor_criteria or factor < 0:
                        starting_sample = identified_peak_end


        if third_peak_pulse_polarity == "negative pulse":
            identified_peak_end = third_peak_number_of_sample_positive_pulse
            # print(third_peak_negative_amplitude)
            # print(fuck)
            if (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)) < third_peak_negative_amplitude < (
                    abs(average_amplitude) + (abs(average_amplitude) * noise_criteria)):
                starting_sample = identified_peak_end

            if third_peak_negative_amplitude < (abs(average_amplitude) - (abs(average_amplitude) * noise_criteria)):
                #verify factor
                if second_peak_pulse_polarity == "positive pulse":

                    factor = abs(
                        (100 - (abs(third_peak_negative_amplitude_ratio / second_peak_positive_amplitude_ratio) * 100)))
                    # print("Factor", factor)
                    if 0 <= factor <= shape_factor_criteria:
                        break
                    if factor > shape_factor_criteria or factor < 0:
                        starting_sample = identified_peak_end

                if second_peak_pulse_polarity == "negative pulse":
                    factor = abs(
                        (100 - (abs(third_peak_negative_amplitude_ratio / second_peak_negative_amplitude_ratio) * 100)))
                    # print("Factor", factor)
                    if 0 <= factor <= shape_factor_criteria:
                        break
                    if factor > shape_factor_criteria or factor < 0:
                        starting_sample = identified_peak_end







        if third_peak_pulse_polarity == None:
            third_peak_details=None
            break



        if starting_sample > time_lenght:
            break

    if starting_sample == time_lenght:
        third_peak_details=None





    return first_peak_details, second_peak_details, third_peak_details, time_resolution


def time_domain_refloctometric(waveform_list, speed):

    ####################################################################################################################
    print("-------------------   Time Domain Reflectometric   ---------------------------------------------------")



    # peaks_details = peak_detection("{}".format(file_name))

    peaks_details = peak_detection(waveform_list)

    time_resolution = peaks_details[3]


    first_peak_polarity = peaks_details[0][0]
    first_peak_positive_pulse_sample = peaks_details[0][1]
    first_peak_negative_pulse_sample = peaks_details[0][2]

    if first_peak_polarity == 'positive pulse':
        first_peak_start_sample = first_peak_positive_pulse_sample
    if first_peak_polarity == 'negative pulse':
        first_peak_start_sample = first_peak_negative_pulse_sample

    if peaks_details[1] !=None:
        second_peak_polarity = peaks_details[1][0]
        second_peak_positive_pulse_sample = peaks_details[1][1]
        second_peak_negative_pulse_sample = peaks_details[1][2]

        if second_peak_polarity == 'positive pulse':
            second_peak_start_sample = second_peak_positive_pulse_sample
        if second_peak_polarity == 'negative pulse':
            second_peak_start_sample = second_peak_negative_pulse_sample

    if peaks_details[2]!=None:
        third_peak_polarity = peaks_details[2][0]
        third_peak_positive_pulse_sample = peaks_details[2][1]
        third_peak_negative_pulse_sample = peaks_details[2][2]

        if third_peak_polarity == 'positive pulse':
            third_peak_start_sample = third_peak_positive_pulse_sample
        if third_peak_polarity == 'negative pulse':
            third_peak_start_sample = third_peak_negative_pulse_sample

    ###########################################################################################

    conclusion = 0

    if peaks_details[1] !=None and peaks_details[2]!=None:


        peak_1_to_peak_2_us = ((second_peak_start_sample - first_peak_start_sample) *time_resolution)/0.000001
        peak_1_to_peak_3_us = ((third_peak_start_sample - first_peak_start_sample) * time_resolution)/0.000001
        peak_2_to_peak_3_us = ((third_peak_start_sample - second_peak_start_sample) * time_resolution)/0.000001

        print(peak_1_to_peak_2_us, peak_1_to_peak_3_us, peak_2_to_peak_3_us)

        cable_lenght = round((peak_1_to_peak_3_us)*speed,1)
        distance_from_measurement_point = round((peak_2_to_peak_3_us)*speed,1)
        distance_from_opposite_termination = round((peak_1_to_peak_2_us)*speed,1)

        print("Cable length:",cable_lenght)
        print("Distance_from_measurement point:", distance_from_measurement_point)
        print("Distance_from_opposite termination:", distance_from_opposite_termination)
        print("Discharge in a joint at {}m from the measurement location".format(distance_from_measurement_point))

        conclusion = 1

    if peaks_details[1] !=None and peaks_details[2] == None:
        peak_1_to_peak_2_us = ((second_peak_start_sample - first_peak_start_sample) * time_resolution) / 0.000001
        print(peak_1_to_peak_2_us)

        cable_lenght = round((peak_1_to_peak_2_us) * speed, 1)
        distance_from_measurement_point = round((peak_1_to_peak_2_us) * speed, 1)
        distance_from_opposite_termination = round((peak_1_to_peak_2_us) * speed, 1)

        print("Cable length:", cable_lenght)
        print("Distance_from_measurement point:", distance_from_measurement_point)
        print("Distance_from_opposite termination:", distance_from_opposite_termination)
        print("Discharge likely in one of the termination compare amplitude")

        conclusion = 2

    if peaks_details[1] == None and peaks_details[2]==None:
        print("No reflections identified in the waveforms")
        conclusion = 0
        cable_lenght = None
        distance_from_measurement_point = None
        distance_from_opposite_termination = None

    return conclusion, cable_lenght, distance_from_measurement_point, distance_from_opposite_termination


# time_domain_refloctometric("cg10_test100723", 90)

# average_waveform('allwaveforms')


# first_peak_detector()
# second_peak_detection()
#print(peak_detection_rev1('/home/inwave/Desktop/Inwave/Data/Substation_LG/Cable/LG/HFCT/average_wfm.csv'))