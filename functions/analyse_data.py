import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta


def analyse_data(asset_id):
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('functions', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()



    def offline_test_analysis():
        def correct_insulation_resistance(ir_ambient, ambient_temperature, reference_temperature,temperature_coefficient):
            """
            Function to correct insulation resistance for temperature.

            Parameters:
            - ir_ambient: Insulation resistance measured at ambient temperature (in Ohms).
            - ambient_temperature: Ambient temperature at which ir_ambient was measured (in Celsius).
            - reference_temperature: Reference temperature to which IR should be standardized (in Celsius).
            - temperature_coefficient: Temperature coefficient of the insulation material (per degree Celsius).

            Returns:
            - ir_corrected: Corrected insulation resistance value at reference temperature (in Ohms).
            """

            # Calculate the Temperature Correction Factor (TCF)
            tcf = temperature_coefficient * (reference_temperature - ambient_temperature)

            # Apply the TCF to correct the IR value
            ir_corrected = ir_ambient * (1 + tcf)

            return ir_corrected

        def analysis_insulation_resistance_data():

            # read offline test table

            cursor.execute("SELECT * FROM offline_test_data WHERE diagnostic_test_id=1 AND analysis IS NULL ")
            insulation_test_results = cursor.fetchall()

            # print(insulation_test_results)

            #analyse result

            for rows in insulation_test_results:
                #evaluate DAR
                DAR=None
                if rows[8] != None and rows[7]!=None:
                    DAR=round(float(rows[8])/float(rows[7]),2)

                # print(rows)
                #evaluate IR at 20 degrease
                IR_20 = None
                if rows[8]!=None:
                    IR_20=round(correct_insulation_resistance(float(rows[7]), float(rows[12]), 20,0.005),2)

                # evaluate RC factor
                RC = None
                if rows[8] != None and rows[10] != None:
                    RC = round(IR_20 * (float(rows[10]) / 1000),2)

                #Analyse
                analysis=None

                if DAR!=None:
                    if IR_20 >=1:
                        if DAR >=1.6:
                            analysis = 1
                        if DAR <1.6:
                            analysis =2

                    if IR_20 <1:
                        if DAR >= 1.6:
                            analysis = 3
                        if DAR < 1.6:
                            analysis = 4

                        if IR_20 < (11+1/1000):
                            analysis=5

                if DAR == None:
                    if IR_20 >= 1:
                        analysis = 1

                    if IR_20 < 1:
                        analysis = 4

                    if IR_20 < (11 + 1 / 1000):
                        analysis = 5


                #update result
                update_query = "UPDATE offline_test_data SET feature_5 = ? , feature_10 = ? , feature_11 = ? , analysis=? WHERE id = ?"
                cursor.execute(update_query, (str(DAR),str(IR_20),str(RC),analysis,rows[0]))

        def analysis_polarization_index_data():
            # read offline test table

            cursor.execute("SELECT * FROM offline_test_data WHERE diagnostic_test_id=2 AND analysis IS NULL ")
            pi_test_results = cursor.fetchall()

            # print(pi_test_results)
            # analyse result

            for rows in pi_test_results:
                # evaluate DAR
                DAR = None
                PI = None
                if rows[8] != None and rows[7] != None and rows[10]!=None:
                    DAR = round(float(rows[8]) / float(rows[7]), 2)
                    PI = round(float(rows[10])/float(rows[8]),2)

                # evaluate IR at 20 degrease
                IR_20 = None
                if rows[8] != None:
                    IR_20 = round(correct_insulation_resistance(float(rows[8]), float(rows[15]), 20, 0.005), 2)

                # evaluate RC factor
                RC = None
                if rows[8] != None and rows[13] != None:
                    RC = round(IR_20 * (float(rows[13]) / 1000), 2)

                # Analyse
                analysis = None

                if DAR != None and PI!=None:
                    if IR_20 >= 1:
                            analysis = 1


                    if IR_20 < 1:
                        if PI >=2 and DAR>=1.6:
                            analysis = 2

                        if PI >=2 and DAR <1.6:
                            analysis = 3
                        if PI <2 and DAR >= 1.6:
                            analysis = 3

                        if PI< 2 and DAR < 1.6:
                            analysis = 4

                        if IR_20 < (11 + 1 / 1000):
                            analysis = 5

                if DAR == None or PI == None:
                    if IR_20 >= 1:
                        analysis = 1

                    if IR_20 < 1:
                        analysis = 4

                    if IR_20 < (11 + 1 / 1000):
                        analysis = 5

                # update result
                update_query = "UPDATE offline_test_data SET feature_7 = ? , feature_8 = ? , feature_13 = ? , feature_14 = ? ,  analysis=? WHERE id = ?"
                cursor.execute(update_query, (str(DAR), str(PI), str(IR_20), str(RC), analysis, rows[0]))

            None

        def analysis_winding_resistance_data():
            # read offline test table

            cursor.execute("SELECT * FROM offline_test_data WHERE diagnostic_test_id=3 AND analysis IS NULL ")
            wr_results = cursor.fetchall()

            # print(wr_results)

            # analyse result

            #evaluate average winding resistance

            wind_resistance = []
            for rows in wr_results:
                wind_resistance.append(float(rows[7]))

            average_wr = round(sum(wind_resistance)/3,2)


            for rows in wr_results:
                # evaluate DAR
                WR_75 = None
                Unbalance = None
                if rows[7] != None and rows[8]:
                    WR_75 = round(correct_insulation_resistance(float(rows[7]), float(rows[9]), 75, 0.005), 2)

                # evaluate unbalanced from mean value

                Unbalance = round(((float(rows[7])* 100)/average_wr)-100,2)


                # Analyse
                analysis = None
                if 0 <= Unbalance <2:
                    analysis=1

                if -2<Unbalance <=0:
                    analysis=1

                if Unbalance >=2:
                    analysis=5

                if Unbalance <=-2:
                    analysis=5


                # update result
                update_query = "UPDATE offline_test_data SET feature_7 = ? , feature_8 = ? , analysis=? WHERE id = ?"
                cursor.execute(update_query, (str(WR_75), str(Unbalance), analysis, rows[0]))


            None

        def analysis_dissipation_factor_data():
            # read offline test table

            cursor.execute("SELECT * FROM offline_test_data WHERE diagnostic_test_id=4 AND analysis IS NULL ")
            ddf_test_results = cursor.fetchall()


            #analyse
            analysis = None

            criteria_1 = None
            criteria_2 = None
            criteria_3 = None
            criteria_4 = None
            criteria_list = []

            delta_60_20Un = None
            td_20Un = None
            increment_20 = []
            max_increment = None
            delta_CUn_C20Un = None


            for rows in ddf_test_results:
                if rows[7]!=None and rows[11]!=None and rows[9]!= None and rows[11] !=None and rows[15]!=None:

                    td_20Un = float(rows[7])

                    delta_60_20Un = float(rows[11]) - float(rows[7])

                    ddf_40_20 = float(rows[9]) - float(rows[7])
                    ddf_60_40 = float(rows[11]) - float(rows[9])
                    ddf_80_60 = float(rows[13]) - float(rows[11])
                    ddf_100_80 = float(rows[15]) - float(rows[13])

                    increment_20.append(ddf_40_20)
                    increment_20.append(ddf_60_40)
                    increment_20.append(ddf_80_60)
                    increment_20.append(ddf_100_80)

                    max_increment = max(increment_20)

                    delta_CUn_C20Un = float(rows[25]) - float(rows[17])


                    #criteria 1 - DDF at 20Un <=4%
                    if td_20Un <= 4:
                        criteria_1 = 1

                    if td_20Un > 4:
                        criteria_1 = 5

                    #criteria 2 - DDF at 60 - DDF at 20 <=2%

                    if delta_60_20Un <=2:
                        criteria_2=1

                    if delta_60_20Un >2:
                        criteria_2=5

                    #criteria 3 - Max DDF for 20Un increament <=1

                    if max_increment <=1:
                        criteria_3 =1

                    if max_increment >1:
                        criteria_3 = 5

                    #criteria 4 - Cap at Un - Cap at 20Un <=6%

                    if delta_CUn_C20Un <=6:
                        criteria_4 = 1

                    if delta_CUn_C20Un >6:
                        criteria_4 = 5

                    criteria_list.append(criteria_1)
                    criteria_list.append(criteria_2)
                    criteria_list.append(criteria_3)
                    criteria_list.append(criteria_4)


                    #define final analysis

                    max_score = max(criteria_list)

                    if max_score == 1:
                        analysis = 1

                    if max_score ==5:
                        analysis = 5

                    # update result
                    update_query = "UPDATE offline_test_data SET analysis=? WHERE id = ?"
                    cursor.execute(update_query, (analysis, rows[0]))

            None

        def analysis_partial_discharge_data():
            # read offline test table

            cursor.execute("SELECT * FROM offline_test_data WHERE diagnostic_test_id=5 AND analysis IS NULL ")
            offlinepd_test_results = cursor.fetchall()

            # print(offlinepd_test_results)

            #analyse
            analysis = None

            for rows in offlinepd_test_results:
                if rows[7]!=None and rows[8]!=None and rows[9]!=None:
                    max_amplitude = max(float(rows[7]), float(rows[8]))

                    if max_amplitude <=10000:
                        analysis=1

                    if max_amplitude >10000:
                        if rows[9] == 'Classic':
                            #analysis predominance
                            if float(rows[7]) >= (1.5*float(rows[8])):
                                #positve predominance
                                analysis=5

                            if float(rows[7]) < (1.5*float(rows[8])):
                                #no predominance
                                analysis=4

                            if float(rows[8])>=(1.5*float(rows[7])):
                                #negative predomaninance
                                if wind_coil_type == 'Multi-turn':
                                    analysis=5
                                if wind_coil_type != 'Multi-turn':
                                    analysis=4

                            if float(rows[8]) < (1.5*float(rows[7])):
                                #no predomance
                                analysis=4

                        if rows[9] == 'Non Classic':
                            analysis=3

                    # update result
                    update_query = "UPDATE offline_test_data SET analysis=? WHERE id = ?"
                    cursor.execute(update_query, (analysis, rows[0]))

            None

        def analysis_visual_inspection_data():
            # read offline test table

            cursor.execute("SELECT * FROM offline_test_data WHERE diagnostic_test_id=6 AND analysis IS NULL ")
            visual_test_results = cursor.fetchall()

            print(visual_test_results)
            None

        def analysis_elcid_data():
            # read offline test table

            cursor.execute("SELECT * FROM offline_test_data WHERE diagnostic_test_id=8 AND analysis IS NULL ")
            elcid_test_results = cursor.fetchall()

            analysis = None
            for result in elcid_test_results:
                if result[6]!=None:
                    if int(result[6]) == 0:
                        analysis = 1
                    if 0 <= int(result[6]) < int(number_of_slot)*0.05:
                        analysis=2

                    if int(number_of_slot)*0.05 <= int(result[6]) < int(number_of_slot)*0.1:
                        analysis = 3

                    if int(number_of_slot)*0.1 <= int(result[6]) < int(number_of_slot)*0.2:
                        analysis = 4

                    if int(result[6]) > int(number_of_slot)*0.2:
                        analysis = 5

                # update result
                update_query = "UPDATE offline_test_data SET analysis=? WHERE id = ?"
                cursor.execute(update_query, (analysis, result[0]))

        def analysis_core_flux_data():
            # read offline test table

            cursor.execute("SELECT * FROM offline_test_data WHERE diagnostic_test_id=7 AND analysis IS NULL ")
            core_flux_test_results = cursor.fetchall()

            analysis = None
            for result in core_flux_test_results:
                if result[8]!=None:
                    if int(result[8]) == 0:
                        analysis = 1
                    if 0 <= int(result[8]) < int(number_of_slot)*0.05:
                        analysis=2

                    if int(number_of_slot)*0.05 <= int(result[8]) < int(number_of_slot)*0.1:
                        analysis = 3

                    if int(number_of_slot)*0.1 <= int(result[8]) < int(number_of_slot)*0.2:
                        analysis = 4

                    if int(result[8]) > int(number_of_slot)*0.2:
                        analysis = 5

                # update result
                update_query = "UPDATE offline_test_data SET analysis=? WHERE id = ?"
                cursor.execute(update_query, (analysis, result[0]))





        analysis_insulation_resistance_data()
        analysis_polarization_index_data()
        analysis_winding_resistance_data()
        analysis_dissipation_factor_data()
        analysis_partial_discharge_data()
        # analysis_visual_inspection_data()
        analysis_elcid_data()
        analysis_core_flux_data()

        None

    def online_test_analysis():

        def analysis_rfa_data():

            cursor.execute("SELECT * FROM online_test_data WHERE diagnostic_test_id=10 AND analysis IS NULL ")
            rfa_test_results = cursor.fetchall()

            analysis = None

            if rotor_type=='Salient Poles':
                #check flux density is >=70%

                for result in rfa_test_results:
                    result_list = []
                    if result[6]!=None:
                        variation = 100 - float(result[6])
                        result_list.append(variation)
                    if result[7]!=None:
                        variation = 100 - float(result[7])
                        result_list.append(variation)
                    if result[8]!=None:
                        variation = 100 - float(result[8])
                        result_list.append(variation)
                    if result[9]!=None:
                        variation = 100 - float(result[9])
                        result_list.append(variation)
                    if result[10]!=None:
                        variation = 100 - float(result[10])
                        result_list.append(variation)
                    if result[11]!=None:
                        variation = 100 - float(result[11])
                        result_list.append(variation)


                    max_variation = max(result_list)

                    if max_variation <=5:
                        analysis=1

                    if 5< max_variation <=10:
                        analysis=2

                    if 10 < max_variation <=20:
                        analysis=3

                    if 20 < max_variation <=30:
                        analysis=4

                    if max_variation > 30:
                        analysis = 5

                        # update result
                    update_query = "UPDATE online_test_data SET analysis=? WHERE id = ?"
                    cursor.execute(update_query, ( analysis, result[0]))

            if rotor_type == 'Cylindrical':
                # evaluate difference

                for result in rfa_test_results:
                    result_list = []
                    if result[6] != None and result[16]!=None:

                        variation = 100 - (float(result[16])/float(result[6])*100)
                        result_list.append(variation)
                    if result[7] != None and result[17]!=None:
                        variation = 100 - (float(result[17])/float(result[7])*100)
                        result_list.append(variation)
                    if result[8] != None and result[18]!=None:
                        variation = 100 - (float(result[18])/float(result[8])*100)
                        result_list.append(variation)
                    if result[9] != None and result[19]!=None:
                        variation = 100 - (float(result[19])/float(result[9])*100)
                        result_list.append(variation)
                    if result[10] != None and result[20]!=None:
                        variation = 100 - (float(result[20])/float(result[10])*100)
                        result_list.append(variation)
                    if result[11] != None and result[21]!=None:
                        variation = 100 - (float(result[21])/float(result[11])*100)
                        result_list.append(variation)
                    if result[12] != None and result[22]!=None:
                        variation = 100 - (float(result[22])/float(result[12])*100)
                        result_list.append(variation)
                    if result[13] != None and result[23]!=None:
                        variation = 100 - (float(result[23])/float(result[13])*100)
                        result_list.append(variation)
                    if result[14] != None and result[24]!=None:
                        variation = 100 - (float(result[24])/float(result[14])*100)
                        result_list.append(variation)
                    if result[15] != None and result[25]!=None:
                        variation = 100 - (float(result[25])/float(result[15])*100)
                        result_list.append(variation)
                    if result[16] != None and result[26]!=None:
                        variation = 100 - (float(result[26])/float(result[16])*100)
                        result_list.append(variation)

                    max_variation = max(result_list)

                    if max_variation <= 1:
                        analysis = 1

                    if 1 < max_variation <= 2:
                        analysis = 2

                    if 3 < max_variation <= 4:
                        analysis = 3

                    if 4 < max_variation <= 5:
                        analysis = 4

                    if max_variation > 5:
                        analysis = 5

                        # update result
                    update_query = "UPDATE online_test_data SET analysis=? WHERE id = ?"
                    cursor.execute(update_query, (analysis, result[0]))

        def analysis_partial_discharge_data():
            # read offline test table

            cursor.execute("SELECT * FROM online_test_data WHERE diagnostic_test_id=11 AND analysis IS NULL ")
            onlinepd_test_results = cursor.fetchall()

            # print(onlinepd_test_results)


            #analyse
            analysis = None
            polarity_predominance = None
            trend_behaviour_pos = None
            trend_behaviour_neg = None
            double_in_the_last_six_months = None


            for rows in onlinepd_test_results:
                if rows[6]!=None and rows[7]!=None:
                    #analyse polarity predominance
                    identification = rows[8]

                    if identification =='Classic':
                        #evalauate polarity predominance
                        if float(rows[6]) >= 1.5*float(rows[7]):
                            #positive predominance
                            polarity_predominance = 'Positive'
                        if float(rows[7]) >=1.5*float(rows[6]):
                            #polarity predominance
                            polarity_predominance = 'Negative'

                        if (float(rows[6]) >= 1.5*float(rows[7]))!=True and (float(rows[7]) >=1.5*float(rows[6]))!=True:
                            #no predominance
                            polarity_predominance = None
                    if identification == 'Non-Classic':
                        polarity_predominance = 'NA'

                    #analyse amplitude trend
                    cursor.execute("SELECT date,feature_2,feature_3 FROM online_test_data WHERE diagnostic_test_id=11 AND feature_1 =? ORDER by ID desc", rows[5])
                    onlinepd_phase_trend_results = cursor.fetchall()


                    date_format = '%d/%m/%Y'
                    date_trend = []
                    positive_trend = []
                    negative_trend = []

                    for Qms in onlinepd_phase_trend_results:
                        date_trend.append(datetime.strptime(Qms[0], date_format))

                        positive_trend.append(float(Qms[1]))
                        negative_trend.append(float(Qms[2]))

                    positive_trend.reverse()
                    negative_trend.reverse()
                    date_trend.reverse()

                    print(positive_trend)
                    print(negative_trend)
                    print(date_trend)

                    #determine trend behaviour
                    if len(positive_trend) < 3 or len(negative_trend) <3:
                        trend_behaviour = 'NA'

                    if len(positive_trend) >=3 and len(negative_trend) >=3:
                        if len(positive_trend) == 3 and len(negative_trend) ==3:
                            #using the last three measurement session
                            #pos

                            if positive_trend[-1] > 1.20*positive_trend[-2]:
                                pos_trend_behaviour_1 = 1

                            if 0.8*positive_trend[-2] <= positive_trend[-1] <=1.20*positive_trend[-2]:
                                pos_trend_behaviour_1 = 0

                            if positive_trend[-1] < 0.8*positive_trend[-2]:
                                pos_trend_behaviour_1 = -1

                            if positive_trend[-2] > 1.20*positive_trend[-3]:
                                pos_trend_behaviour_2 = 1

                            if 0.8*positive_trend[-3] <= positive_trend[-2] <= 1.20*positive_trend[-3]:
                                pos_trend_behaviour_2 = 0

                            if positive_trend[-2] < 0.8*positive_trend[-3]:
                                pos_trend_behaviour_2 = -1


                            if -2 < (pos_trend_behaviour_1 + pos_trend_behaviour_2) <2:
                                trend_behaviour_pos = 'Stable'

                            if (pos_trend_behaviour_1 + pos_trend_behaviour_2) >=2:
                                trend_behaviour_pos = 'Increasing'

                            if (pos_trend_behaviour_1 + pos_trend_behaviour_2) <= -2:
                                trend_behaviour_pos = 'Decreasing'

                            # check the difference between first and last sample to improve trend recognition
                            if positive_trend[-1] > 1.40 * positive_trend[-3]:
                                trend_behaviour_pos = 'Increasing'

                            if positive_trend[-1] < 1.40 * positive_trend[-3]:
                                trend_behaviour_pos = 'Decreasing'

                            #neg
                            if negative_trend[-1] > 1.20 * negative_trend[-2]:
                                neg_trend_behaviour_1 = 1

                            if 0.8 * negative_trend[-2] <= negative_trend[-1] <= 1.20 * negative_trend[-2]:
                                neg_trend_behaviour_1 = 0

                            if negative_trend[-1] < 0.8 * negative_trend[-2]:
                                neg_trend_behaviour_1 = -1

                            if negative_trend[-2] > 1.20 * negative_trend[-3]:
                                neg_trend_behaviour_2 = 1

                            if 0.8 * negative_trend[-3] <= negative_trend[-2] <= 1.20 * negative_trend[-3]:
                                neg_trend_behaviour_2 = 0

                            if negative_trend[-2] < 0.8 * negative_trend[-3]:
                                neg_trend_behaviour_2 = -1

                            if -2 < (neg_trend_behaviour_1 + neg_trend_behaviour_2) < 2:
                                trend_behaviour_neg = 'Stable'

                            if (neg_trend_behaviour_1 + neg_trend_behaviour_2) >= 2:
                                trend_behaviour_neg = 'Increasing'

                            if (neg_trend_behaviour_1 +neg_trend_behaviour_2) <= -2:
                                trend_behaviour_neg = 'Decreasing'

                            # check the difference between first and last sample to improve trend recognition
                            if negative_trend[-1] > 1.40 * negative_trend[-3]:
                                trend_behaviour_neg = 'Increasing'

                            if negative_trend[-1] < 1.40 * negative_trend[-3]:
                                trend_behaviour_neg = 'Decreasing'

                    print(trend_behaviour_pos, trend_behaviour_neg)
                    #determine the doubling of amplitude over time

                    latest_date = max(date_trend)
                    six_months_earlier = latest_date - timedelta(days=6*30)
                    closest_date_index = min(range(len(date_trend)), key=lambda i: abs(date_trend[i] - six_months_earlier))

                    delta_over_6_months_pos = positive_trend[-1] - positive_trend[closest_date_index]
                    delta_over_6_months_neg = negative_trend[-1] - negative_trend[closest_date_index]

                    if delta_over_6_months_pos >= 2*positive_trend[closest_date_index] or delta_over_6_months_neg >=2*negative_trend[closest_date_index]:
                        double_in_the_last_six_months = True

                    if delta_over_6_months_pos < 2*positive_trend[closest_date_index] and delta_over_6_months_neg < 2*negative_trend[closest_date_index]:
                        double_in_the_last_six_months = False

                    # print(double_in_the_last_six_months)



                    #convert date from string to datetime
                    #determine the 6 months change




                    #final analysis
                    if identification == 'Classic':
                        if polarity_predominance == 'Positive':
                            if trend_behaviour_pos =='Increasing':
                                if double_in_the_last_six_months == True:
                                    analysis=5
                                if double_in_the_last_six_months == False:
                                    analysis=4
                                if double_in_the_last_six_months ==None:
                                    analysis=4
                            if trend_behaviour_pos == 'Decreasing':
                                if double_in_the_last_six_months == 'True':
                                    analysis=4
                                if double_in_the_last_six_months == 'False':
                                    analysis=3
                                if double_in_the_last_six_months == None:
                                    analysis=3

                            if trend_behaviour_pos == 'Stable':
                                analysis=3
                            if trend_behaviour_pos == None:
                                if double_in_the_last_six_months == True:
                                    analysis=5
                                if double_in_the_last_six_months == False:
                                    analysis=4
                                if double_in_the_last_six_months ==None:
                                    analysis=4

                        if polarity_predominance == 'Negative':
                            if wind_coil_type == 'Multi turn':
                                if trend_behaviour_neg == 'Increasing':
                                    if double_in_the_last_six_months == True:
                                        analysis = 5
                                    if double_in_the_last_six_months == False:
                                        analysis = 4
                                    if double_in_the_last_six_months == None:
                                        analysis = 4
                                if trend_behaviour_neg == 'Decreasing':
                                    if double_in_the_last_six_months == True:
                                        analysis = 4
                                    if double_in_the_last_six_months == False:
                                        analysis = 3
                                    if double_in_the_last_six_months == None:
                                        analysis = 3
                                if trend_behaviour_neg == 'Stable':
                                    analysis = 3

                                if trend_behaviour_neg == None:
                                    if double_in_the_last_six_months == True:
                                        analysis = 5
                                    if double_in_the_last_six_months == False:
                                        analysis = 4
                                    if double_in_the_last_six_months == None:
                                        analysis = 4

                            if wind_coil_type == 'Single turn':
                                if trend_behaviour_neg == 'Increasing' or trend_behaviour_pos == 'Increasing':
                                    if double_in_the_last_six_months == True:
                                        analysis = 4
                                    if double_in_the_last_six_months == False:
                                        analysis = 3
                                    if double_in_the_last_six_months == None:
                                        analysis = 3
                                if trend_behaviour_neg == 'Decreasing' or trend_behaviour_pos == 'Decreasing':
                                    if double_in_the_last_six_months == True:
                                        analysis = 3
                                    if double_in_the_last_six_months == False:
                                        analysis = 2
                                    if double_in_the_last_six_months == None:
                                        analysis = 2
                                if trend_behaviour_neg =='Stable' and trend_behaviour_pos == 'Stable':
                                    analysis = 2

                                if trend_behaviour_neg == None:
                                    if double_in_the_last_six_months == True:
                                        analysis = 4
                                    if double_in_the_last_six_months == False:
                                        analysis = 3
                                    if double_in_the_last_six_months == None:
                                        analysis = 3

                        if polarity_predominance == None:
                            if trend_behaviour_neg == 'Increasing' and trend_behaviour_pos == 'Increasing':
                                if double_in_the_last_six_months == True:
                                    analysis = 4
                                if double_in_the_last_six_months == False:
                                    analysis = 3
                                if double_in_the_last_six_months == None:
                                    analysis = 3
                            if trend_behaviour_neg == 'Decreasing' and trend_behaviour_pos == 'Decreasing':
                                if double_in_the_last_six_months == True:
                                    analysis = 3
                                if double_in_the_last_six_months == False:
                                    analysis = 2
                                if double_in_the_last_six_months == None:
                                    analysis = 2

                            if trend_behaviour_neg == 'Stable' and trend_behaviour_pos == 'Stable':
                                if double_in_the_last_six_months == True:
                                    analysis = 3
                                if double_in_the_last_six_months == False:
                                    analysis = 2
                                if double_in_the_last_six_months == None:
                                    analysis = 2

                            if trend_behaviour_neg == 'Stable' and trend_behaviour_pos == 'Increasing':
                                if double_in_the_last_six_months == True:
                                    analysis = 3
                                if double_in_the_last_six_months == False:
                                    analysis = 2
                                if double_in_the_last_six_months == None:
                                    analysis = 2

                            if trend_behaviour_neg == 'Stable' and trend_behaviour_pos =='Decreasing':
                                if double_in_the_last_six_months == True:
                                    analysis = 3
                                if double_in_the_last_six_months == False:
                                    analysis = 2
                                if double_in_the_last_six_months == None:
                                    analysis = 2

                            if trend_behaviour_pos == 'Stable' and trend_behaviour_neg == 'Increasing':
                                if double_in_the_last_six_months == True:
                                    analysis = 3
                                if double_in_the_last_six_months == False:
                                    analysis = 2
                                if double_in_the_last_six_months == None:
                                    analysis = 2
                            if trend_behaviour_pos == 'Stable' and trend_behaviour_neg =='Decreasing':
                                if double_in_the_last_six_months == True:
                                    analysis = 3
                                if double_in_the_last_six_months == False:
                                    analysis = 2
                                if double_in_the_last_six_months == None:
                                    analysis = 2

                            if trend_behaviour_neg == None or trend_behaviour_pos == None:
                                if double_in_the_last_six_months == True:
                                    analysis = 4
                                if double_in_the_last_six_months == False:
                                    analysis = 3
                                if double_in_the_last_six_months == None:
                                    analysis = 3


                    if identification == 'Non-Classic':
                        if trend_behaviour_pos =='Increasing' and trend_behaviour_neg =='Increasing':
                            if double_in_the_last_six_months == True:
                                analysis=5
                            if double_in_the_last_six_months == False:
                                analysis=4
                            if double_in_the_last_six_months ==None:
                                    analysis=4
                        if trend_behaviour_pos == 'Decreasing' and trend_behaviour_neg =='Decreasing':
                            if double_in_the_last_six_months == True:
                                analysis=4
                            if double_in_the_last_six_months == False:
                                analysis=3
                            if double_in_the_last_six_months == None:
                                analysis=3

                        if trend_behaviour_pos == 'Stable' and trend_behaviour_neg == 'Stable':
                            if double_in_the_last_six_months == True:
                                analysis=3
                            if double_in_the_last_six_months == False:
                                analysis=2
                            if double_in_the_last_six_months == None:
                                analysis=2

                        if trend_behaviour_pos == 'Stable' and trend_behaviour_neg =='Increasing':
                            if double_in_the_last_six_months == True:
                                analysis=3
                            if double_in_the_last_six_months == False:
                                analysis=2
                            if double_in_the_last_six_months == None:
                                analysis=2

                        if trend_behaviour_pos == 'Stable' and trend_behaviour_neg =='Decreasing':
                            if double_in_the_last_six_months == True:
                                analysis=3
                            if double_in_the_last_six_months == False:
                                analysis=2
                            if double_in_the_last_six_months == None:
                                analysis=2

                        if trend_behaviour_neg == 'Stable' and trend_behaviour_pos =='Increasing':
                            if double_in_the_last_six_months == True:
                                analysis=3
                            if double_in_the_last_six_months == False:
                                analysis=2
                            if double_in_the_last_six_months == None:
                                analysis=2

                        if trend_behaviour_neg == 'Stable' and trend_behaviour_pos =='Decreasing':
                            if double_in_the_last_six_months == True:
                                analysis=3
                            if double_in_the_last_six_months == False:
                                analysis=2
                            if double_in_the_last_six_months == None:
                                analysis=2

                        if trend_behaviour_neg == None or trend_behaviour_pos==None:
                            if double_in_the_last_six_months == True:
                                analysis=5
                            if double_in_the_last_six_months == False:
                                analysis=4
                            if double_in_the_last_six_months ==None:
                                analysis=4
                    # print(double_in_the_last_six_months)
                    # update result
                    update_query = "UPDATE online_test_data SET feature_11 = ? , feature_12 = ? , feature_13=? , feature_14=? , analysis=? WHERE id = ?"
                    cursor.execute(update_query, (polarity_predominance, trend_behaviour_pos, trend_behaviour_neg, double_in_the_last_six_months, analysis, rows[0]))






            #analyse
            analysis = None

            for rows in onlinepd_test_results:
                if rows[7]!=None and rows[8]!=None and rows[9]!=None:
                    max_amplitude = max(float(rows[7]), float(rows[8]))

                    if max_amplitude <=10000:
                        analysis=1

                    if max_amplitude >10000:
                        if rows[9] == 'Classic':
                            #analysis predominance
                            if float(rows[7]) >= (1.5*float(rows[8])):
                                #positve predominance
                                analysis=5

                            if float(rows[7]) < (1.5*float(rows[8])):
                                #no predominance
                                analysis=4

                            if float(rows[8])>=(1.5*float(rows[7])):
                                #negative predomaninance
                                if wind_coil_type == 'Multi-turn':
                                    analysis=5
                                if wind_coil_type != 'Multi-turn':
                                    analysis=4

                            if float(rows[8]) < (1.5*float(rows[7])):
                                #no predomance
                                analysis=4

                        if rows[9] == 'Non Classic':
                            analysis=3

                    # update result
                    print(analysis)
                    update_query = "UPDATE online_test_data SET analysis=? WHERE id = ?"
                    cursor.execute(update_query, (analysis, rows[0]))

            None

        analysis_partial_discharge_data()
        analysis_rfa_data()


        None

    #select asset details
    yom = None
    yoi = None
    rated_voltage = None
    rated_power = None
    rated_speed = None
    function = None
    rotor_type = None
    impregnation_type = None
    wind_coil_type = None
    number_of_slot = None
    number_of_poles = None

    cursor.execute("""SELECT * FROM asset WHERE id = ?""", (asset_id,))
    asset_results = cursor.fetchone()

    yom = int(asset_results[4])
    yoi = int(asset_results[5])
    rated_voltage = float(asset_results[6])
    rated_power = float(asset_results[7])
    rated_speed = int(asset_results[9])
    function = asset_results[2]
    rotor_type = asset_results[12]
    wind_coil_type = asset_results[14]
    impregnation_type = asset_results[15]
    number_of_slot = asset_results[16]
    number_of_poles = asset_results[18]
    number_of_turn_pole = asset_results[19]

    # print(number_of_turn_pole)
    # print(fuck)
    # print(yom, yoi, rated_voltage, rated_power, rated_speed, function, rotor_type, wind_coil_type, impregnation_type, number_of_slot, number_of_poles)



    offline_test_analysis()
    online_test_analysis()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()


