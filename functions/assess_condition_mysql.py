import sqlite3
from idlelib.searchengine import search_reverse

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta, date
import csv
import matplotlib.pyplot as plt
import mysql.connector

from connectors.db_connectors_mysql import get_single_asset_characteristics, \
    get_individual_test_maintenance_action_from_list
from connectors.db_connectors_mysql import get_diagnostic_test_single_asset_list
from connectors.db_connectors_mysql import get_failure_mechanism_single_asset_list
from connectors.db_connectors_mysql import get_fmdi_weight
from connectors.db_connectors_mysql import get_component_single_asset_list
from connectors.db_connectors_mysql import get_subcomponent_single_asset_list
from connectors.db_connectors_mysql import get_scfm_weight, get_schi_weight, get_subcomponent_details
from connectors.db_connectors_mysql import get_cmsc_weight
from connectors.db_connectors_mysql import get_ascm_weight, get_latest_asset_criticality_class

""" Script to evaluate:
    - failure_mechanisms
    - subcomponent_condition
    - component_condition
    - asset_condition
"""


def assess_condition(asset_id):

    print('Risk Assessment in progress')
    # Connect to SQLite database (or create it if it doesn't exist)

    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Change to your MySQL host if needed
        user='root',  # Your MySQL username
        password='InWave!2024!',  # Your MySQL password
        database='Inwave_IHMS'  # Specify the database name
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    diagnostic_test_scores_dict = {}
    failure_mechanisms_dict = {}
    subcomponent_condition_dict = {}
    subcomponent_fmea_dict = {}


    component_condition_dict = {}

    asset_condition_dict = {}
    maintenance_actions_list = []

    def upload_result_in_db():
        # print(diagnostic_test_scores_dict)
        # print(failure_mechanisms_dict)
        # print(subcomponent_condition_dict)
        # print(component_condition_dict)
        # print(asset_condition_dict)
        # print(maintenance_actions_list)
        # print(fck)


        #insert into asset_analysis table

        # print('asset analysis')
        # print(asset_condition_dict)
        # print(asset_condition_dict.items())
        # print('component analysis')
        # print(component_condition_dict)
        # print(component_condition_dict.items())
        # print('subcompoent analysis')
        # print(subcomponent_condition_dict)
        # print(subcomponent_condition_dict.items())
        # subcomponent_condition_dict_ordered = {key: subcomponent_condition_dict[key] for key in
        #                                        sorted(subcomponent_condition_dict)}

        # print(subcomponent_condition_dict_ordered)
        # # print(fck)
        # print('failure mechanism analysis')
        # print(failure_mechanisms_dict)
        # print(failure_mechanisms_dict.items())





        if not failure_mechanisms_dict and not subcomponent_condition_dict and not component_condition_dict:
            print('No data uploaded')

        else:

            current_date = datetime.now()
            current_date_str = current_date.strftime('%d-%m-%Y %H:%M')


            # SQL statement to insert data into the table
            # select asset_analysis_id

            cursor.execute("SELECT id FROM asset_analysis WHERE asset_id = %s AND date = %s AND risk_index = %s AND health_index = %s LIMIT 1",
                           (asset_id, current_date_str, asset_condition_dict['RI'], asset_condition_dict['HI']))

            existing_record = cursor.fetchone()



            if not existing_record:


                insert_sql = '''INSERT INTO asset_analysis (date, asset_id, risk_index, health_index)
                                VALUES (%s, %s, %s, %s);'''
                cursor.execute(insert_sql, (current_date_str, asset_id, asset_condition_dict['RI'], asset_condition_dict['HI']))



                #select asset_analysis_id
                cursor.execute(
                    "SELECT id FROM asset_analysis WHERE asset_id = %s AND date = %s AND risk_index = %s AND health_index = %s LIMIT 1",
                    (asset_id, current_date_str, asset_condition_dict['RI'], asset_condition_dict['HI']))

                result = cursor.fetchone()
                asset_analysis_id = None
                if len(result)!=0:
                    asset_analysis_id = result[0]



                if asset_analysis_id !=None:



                    # insert into component analysis table

                    for item in list(component_condition_dict.items()):

                        insert_sql = '''INSERT INTO component_analysis (analysis_id, component_id, value)
                                                VALUES (%s, %s, %s);'''
                        cursor.execute(insert_sql,(asset_analysis_id, item[0],item[1]))



                    # insert into subcomponent analysis table

                    for item in list(subcomponent_condition_dict.items()):
                        insert_sql = '''INSERT INTO subcomponent_analysis (analysis_id, subcomponent_id, value)
                                                            VALUES (%s, %s, %s);'''
                        cursor.execute(insert_sql, (asset_analysis_id, item[0], item[1]))



                    # insert into failure_mechanism analysis table

                    for item in list(failure_mechanisms_dict.items()):
                        insert_sql = '''INSERT INTO failure_mechanisms_analysis (analysis_id, failure_mechanism_id, value)
                                                                       VALUES (%s, %s, %s);'''
                        cursor.execute(insert_sql, (asset_analysis_id, item[0], item[1]))



                    # insert into maintenance table
                    # check if the maintenance actions are already inserted
                    cursor.execute("""
                                    SELECT * from asset_maintenance_actions where asset_analysis_id IN
                                    (SELECT id from asset_analysis where asset_id =%s  ) and peer_reviewed_comment is null ORDER by id desc
                                                """,(asset_id,))
                    existing_open_maintenance_action_result = cursor.fetchall()
                    filtered_items = []
                    if len(existing_open_maintenance_action_result) !=0:
                        latest_id = existing_open_maintenance_action_result[0][1]
                        filtered_items = [item for item in existing_open_maintenance_action_result if item[1] == latest_id]
                    existing_open_maintenance_list = []
                    if len(filtered_items)!=0:
                        for obj in filtered_items:
                            existing_open_maintenance_list.append(obj[2])

                    for item in maintenance_actions_list:

                        if item in existing_open_maintenance_list:
                            None

                        else:

                            insert_sql = '''INSERT INTO asset_maintenance_actions (asset_analysis_id, maintenance_action)
                                                                           VALUES (%s, %s);'''
                            cursor.execute(insert_sql, (asset_analysis_id, item))



    def evaluate_failure_mechanisms():
        print('Evaluating FM')
        def get_latest_result_test(test_id):

            #check if test_id is online or offline
            cursor.execute("""
                                SELECT `asset_condition`
                                FROM diagnostic_test
                                WHERE id = %s
                            """, (test_id,))
            test_condition = cursor.fetchone()
            score = 0

            if test_condition[0] == 'Offline':
                # print(test_condition[0], test_id)
                cursor.execute("""
                        SELECT `analysis`,`date`
                        FROM offline_test_data
                        WHERE diagnostic_test_id = %s
                        AND asset_id = %s
                        ORDER BY date DESC
                        
                    """, (test_id,asset_id,))

                # Fetch the result
                result = cursor.fetchall()
                # print(result)


                if len(result)!=0:
                    # Convert dates to a comparable format
                    date_format = '%d/%m/%Y'
                    result_with_dates = [(item[0], datetime.strptime(item[1], date_format)) for item in result]
                    # Find the maximum date
                    max_date = max(item[1] for item in result_with_dates)

                    # Filter the list to keep only the items with the maximum date
                    filtered_result = [item for item in result if item[1] == max_date.strftime(date_format)]

                else:
                    filtered_result = []
                if len(filtered_result) != 0:
                    if len(filtered_result) >1:
                        result_list = []
                        for scores in filtered_result:

                            result_list.append(scores[0])
                        score= max(result_list)

                    if len(filtered_result) ==1:
                        score = filtered_result[0][0]
            if test_condition[0] == 'Online':

                cursor.execute("""
                        SELECT `analysis`,`date`
                        FROM online_test_data
                        WHERE diagnostic_test_id = %s
                        AND asset_id = %s
                        ORDER BY date DESC
                        
                    """, (test_id,asset_id,))

                # Fetch the result
                result = cursor.fetchall()
                if len(result)!=0:
                    # Convert dates to a comparable format
                    # Assuming the format is 'dd/mm/yyyy'
                    date_format = '%d/%m/%Y'
                    result_with_dates = [(item[0], datetime.strptime(item[1], date_format)) for item in result]
                    # Find the maximum date
                    max_date = max(item[1] for item in result_with_dates)

                    # Filter the list to keep only the items with the maximum date
                    filtered_result = [item for item in result if item[1] == max_date.strftime(date_format)]

                else:
                    filtered_result = []

                if len(filtered_result) != 0:
                    if len(filtered_result) >1:
                        result_list = []
                        for scores in result:
                            result_list.append(scores[0])
                        score= max(result_list)
                    if len(filtered_result) ==1:
                        score = filtered_result[0][0]


            # print('test id', test_id)
            # print('final_result', score)
            return score

        #get list of failure mechanism for the asset categoty

        fm_list = get_failure_mechanism_single_asset_list(asset_category)
        #fm id list
        fm_id_list = []
        for fms in fm_list:
            try:
                fm_id_list.append(fms[0])
            except IndexError:
                fm_id_list.append(0)
        #get list of diagnostic test for the asset category

        di_list = get_diagnostic_test_single_asset_list(asset_category)

        #create diagnostic test dictionary
        for di in di_list:
            latest_score = get_latest_result_test(di[0])
            diagnostic_test_scores_dict['{}'.format(di[0])] = latest_score

        print('Diagnosti test score dictionary')
        print(diagnostic_test_scores_dict)
        #get configuration for the specific fm to be analysed

        fmdi_weight_list_complete = get_fmdi_weight(fm_id_list)

        #filter list based on the asset characteristics
        fmdi_weight_list = []
        for rows in fmdi_weight_list_complete:
            if asset_category==1:
                if rows[1] == function and rows[2] == machine_type and rows[3] == rotor_type and rows[4] ==cooling:
                    fmdi_weight_list.append(rows)

                else:
                    None

            if asset_category == 3: #sw

                if rows[1] == voltage_class and rows[2] == insulation :
                    fmdi_weight_list.append(rows)

                else:
                    None

            if asset_category == 4:

                if rows[1] == voltage_class and rows[2] == insulation and rows[3] == term_1 and rows[4] == term_2:
                    fmdi_weight_list.append(rows)

                else:
                    None


        #evaluate the fm
        # create organise dictionary fm: test id , value
        grouped_dict = {}
        for item in fmdi_weight_list:
            # print(item)
            # Extract the first of the last three values
            key = item[-3]  # failue mechanism
            last_three_values = item[-2:]  # test id and weight
            # print(last_three_values)

            # Initialize the list for the key if it doesn't exist
            if key not in grouped_dict:
                grouped_dict[key] = []

            # Append the last three values to the appropriate key
            grouped_dict[key].append(last_three_values)

        # print(list(grouped_dict.keys()))

        for fm_id in list(grouped_dict.keys()):
            print('fm id')
            print(fm_id)
            fm_score_list = []
            fm_weight_list = []
            for di_weight in grouped_dict[fm_id]:
                print('Test id - weight')
                print(di_weight)

                if di_weight[0]==3:
                    print('WR test')

                #get lastest score for the test:
                test_id = di_weight[0]
                weight = float(di_weight[1])

                latest_score = get_latest_result_test(test_id)
                print('latest test score:')
                print(latest_score)

                fm_score_list.append(latest_score)
                fm_weight_list.append(weight)

            print('fm score ',fm_score_list)
            #evaluate result for each fm_id
            #replace empty values with 0
            fm_weight_list_cleaned = []
            fm_score_list_cleaned = []

            for wg in fm_weight_list:
                if isinstance(wg, list):
                    wg=0
                else:
                    None
                fm_weight_list_cleaned.append(wg)

            for ts in fm_score_list:

                if isinstance(ts, list):
                    ts = 0
                else:
                    None
                fm_score_list_cleaned.append(ts)

            # to highlight the bad results even when only 1 test is carried out it required to adjust the weights
            # to the number of fm analysed
            # print(fm_weight_list_cleaned)
            # print(fm_score_list_cleaned)
            reshape_fm_score_list = []
            reshape_fm_weight_list = []
            for fmscore, fmweight in zip(fm_score_list_cleaned, fm_weight_list_cleaned):
                if fmscore ==0:
                    None
                if fmscore!=0:
                    reshape_fm_score_list.append(fmscore)
                    reshape_fm_weight_list.append(fmweight)

            # increment the weights maintening the same ration
            total_weights_used = sum(reshape_fm_weight_list)
            try:
                delta_weight = (10-total_weights_used)/len(reshape_fm_weight_list)
            except ZeroDivisionError:
                delta_weight =0

            # add the delta to each member of the new weight list
            reshape_fm_weight_list_corrected = []
            for origalweights in reshape_fm_weight_list:
                reshape_fm_weight_list_corrected.append((origalweights+delta_weight))



            # Calculate the sum of products
            result_fm_id = round(sum((a if a is not None else 0) * (b if b is not None else 0) for a, b in zip(reshape_fm_score_list, reshape_fm_weight_list_corrected)),0)

            #the final result gives maximum 50% as the sum of the weights is 10 and the maximum core of the test is 5
            # result must be moltiplied by 2 to get from 0 to 100%

            failure_mechanisms_dict[fm_id] = result_fm_id *2



        print('Failure Mechanisms dict')
        print(failure_mechanisms_dict)

    def evaluate_subcomponent_condition():
        print('Evaluating Subcomponent Condition')
        def evaluate_fmea_factor(group_dict, failure_mechanisms_dict):
            print('--------------- FMEA evaluation ----------')
            # print(group_dict)
            # print('failure mec dic',failure_mechanisms_dict)
            for sub_id in list(grouped_dict.keys()):
                # print('Sub id', sub_id)
                sc_score_list = []
                sc_weight_list = []
                for fm_weight in grouped_dict[sub_id]:
                    # get lastest score for the test:
                    fm_id = fm_weight[0]
                    weight = float(fm_weight[1])
                    # print(fm_id)
                    #add condition to handle the missing fm as not all are evaluated on all the different type of asset
                    try:
                        latest_score = failure_mechanisms_dict[fm_id]
                        sc_score_list.append(latest_score)
                        sc_weight_list.append(weight)
                    except KeyError:
                        None


                # evaluate result for each fm_id
                # replace empty values with 0
                sc_weight_list_cleaned = []
                sc_score_list_cleaned = []

                for wg in sc_weight_list:
                    if isinstance(wg, list):
                        wg = 0
                    else:
                        None
                    sc_weight_list_cleaned.append(wg)

                for ts in sc_score_list:
                    if isinstance(ts, list):
                        ts = 0
                    else:
                        None
                    sc_score_list_cleaned.append(ts)

                # to highlight the bad results even when only 1 test is carried out it required to adjust the weights
                # to the number of fm analysed
                reshape_sc_score_list = []
                reshape_sc_weight_list = []
                for scscore, scweight in zip(sc_score_list_cleaned, sc_weight_list_cleaned):
                    if scscore == 0:
                        None
                    if scscore != 0:
                        reshape_sc_score_list.append(scscore)
                        reshape_sc_weight_list.append(scweight)

                    # increment the weights maintening the same ration
                    total_weights_used = sum(reshape_sc_weight_list)
                    try:
                        delta_weight = (10 - total_weights_used) / len(reshape_sc_weight_list)
                    except ZeroDivisionError:
                        delta_weight = 0

                    # add the delta to each member of the new weight list
                    reshape_sc_weight_list_corrected = []
                    for origalweights in reshape_sc_weight_list:
                        reshape_sc_weight_list_corrected.append((origalweights + delta_weight))

                # print('Sub id ------------', sub_id)
                # print(sc_score_list_cleaned)
                # print(sc_weight_list_cleaned)
                #
                # print('reshape values')
                # print(reshape_sc_score_list)
                # print(reshape_sc_weight_list_corrected)
                # Calculate the sum of products
                result_sc_id = sum((a if a is not None else 0) * (b if b is not None else 0) for a, b in
                                   zip(reshape_sc_score_list, reshape_sc_weight_list_corrected))



                subcomponent_fmea_dict[sub_id] = round(result_sc_id/200, 3)
                # print('final for sub', sub_id)
                # print(result_sc_id)
                # print(sc_weight_list)
                # print(sc_score_list)

            print('Subcomponent FMEA')
            print(subcomponent_fmea_dict)
            return subcomponent_fmea_dict

        def evaluate_subcomponet_hi(grouped_schi_dict, subcomponent_fmea_dict, sub_factors_selected):
            # print(group_dict)

            # print(grouped_schi_dict)
            # # print(sub_factors_selected)
            # print(subcomponent_fmea_dict)
            #
            # print('failure mec dic',failure_mechanisms_dict)
            # print(fcuk)
            for sub_id in list(grouped_schi_dict.keys()):
                #select age, maintenance, failure factors for the subcomponent
                age_factor_selected=0
                maintenance_factor_selected=0
                failure_factor_selected=0
                # print('subId', sub_id)

                for subconfig in sub_factors_selected:
                    # print('subconfig', subconfig)
                    if subconfig[0] == sub_id:
                        age_factor_selected=subconfig[1]
                        maintenance_factor_selected = subconfig[2]
                        failure_factor_selected= subconfig[3]
                    else:
                        None

                #add condition to eliminate sub component not existing for the selected asset
                try:
                    fmea_factor_evaluated = subcomponent_fmea_dict[sub_id]
                    # print(age_factor_selected, maintenance_factor_selected,failure_factor_selected )
                    factors_selected_list =[age_factor_selected, maintenance_factor_selected, failure_factor_selected, fmea_factor_evaluated]

                    for config in grouped_schi_dict[sub_id]:
                        # get the configuration related to the age factor of the subcomponent:

                        if config[0] == age_factor_selected:
                            age_weight = config[1]
                            maintenance_weight = config[2]
                            failure_weight = config[3]
                            fmea_weight = config[4]

                        else:
                            None

                    # print(age_weight, maintenance_weight, failure_weight, fmea_weight)
                    failure_weight_selected = [age_weight, maintenance_weight, failure_weight, fmea_weight]
                    # print(factors_selected_list)
                    # print(failure_weight_selected)

                    # Calculate the sum of products AF*WF+MF*WF+FF*WF+FMEA*WF
                    result_sc_id = sum((a if a is not None else 0) * (b if b is not None else 0) for a, b in
                                       zip(factors_selected_list, failure_weight_selected))

                    # considering that each factors is between 0 to 5 and we have 4 factors with the sum of the weight = 10
                    # we have to divde the result by 10 to get an hi from 0 to 5 where 5 is the worst condition
                    final_sc_hi = result_sc_id / 10

                    subcomponent_hi = 0
                    if 0 < final_sc_hi <= 1:
                        subcomponent_hi = 1
                    if 1 < final_sc_hi <= 2:
                        subcomponent_hi = 2
                    if 2 < final_sc_hi <= 3:
                        subcomponent_hi = 3
                    if 3 < final_sc_hi <= 4:
                        subcomponent_hi = 4
                    if 4 < final_sc_hi <= 5:
                        subcomponent_hi = 5

                    subcomponent_condition_dict[sub_id] = subcomponent_hi

                    # print('final for sub', sub_id)
                    # print(result_sc_id)
                    # print(sc_weight_list)
                    # print(sc_score_list)


                except KeyError:
                    None


            print('Subcomponent HI')
            print(subcomponent_condition_dict)
            return subcomponent_condition_dict
        #get subcomponent_list

        component_list = get_component_single_asset_list(asset_category)

        com_id_list = [i[0] for i in component_list]

        subcomponent_list = get_subcomponent_single_asset_list(com_id_list)

        sub_id_list = [j[0] for j in subcomponent_list]

        #get configuration for all the asset
        scfm_weight_list_complete = get_scfm_weight(sub_id_list)

        # print(scfm_weight_list_complete)
        #filter based on the asset under test
        # filter list based on the asset characteristics


        scfm_weight_list = []
        for rows in scfm_weight_list_complete:
            if asset_category ==1: #machine
                if rows[1] == function and rows[2] == machine_type and rows[3] == rotor_type and rows[4] == cooling and rows[5]==wind_coil_type and rows[6]==impregnation_type:
                    scfm_weight_list.append(rows)

                else:
                    None

            if asset_category == 3: #sw

                if rows[1] == voltage_class and rows[2] == insulation :
                    scfm_weight_list.append(rows)

                else:
                    None

            if asset_category ==4: #cable
                if rows[1] == voltage_class and rows[2] == insulation and rows[3] == term_1 and rows[4] == term_2:
                    scfm_weight_list.append(rows)

                else:
                    None

        # print(failure_mechanisms_dict)

        #evaluate FMEA for each subcomponent as sum of FMi*Wi
        # create organise dictionary sub id: fm id , weight
        grouped_dict = {}
        for item in scfm_weight_list:
            # Extract the first of the last three values
            key = item[-3]  # subcomponent
            last_three_values = item[-2:]  # fm id and weight

            # Initialize the list for the key if it doesn't exist
            if key not in grouped_dict:
                grouped_dict[key] = []

            # Append the last three values to the appropriate key
            grouped_dict[key].append(last_three_values)
        print('Sub component id: [failure mechanism id, weight]')
        print(grouped_dict)
        #evalua the fmea
        evaluate_fmea_factor(grouped_dict, failure_mechanisms_dict)

        # get sc hi _details
        schi_weight_list_complete = get_schi_weight(sub_id_list)

        # print(schi_weight_list_complete)
        # filter based on the asset under test
        # filter list based on the asset characteristics

        schi_weight_list = []
        for rows in schi_weight_list_complete:
            if asset_category ==1:
                if rows[1] == function and rows[2] == machine_type and rows[3] == rotor_type and rows[4] == cooling and \
                        rows[5] == wind_coil_type and rows[6] == impregnation_type:
                    schi_weight_list.append(rows)

                else:
                    None

            if asset_category == 3: #sw

                if rows[1] == voltage_class and rows[2] == insulation :
                    schi_weight_list.append(rows)

                else:
                    None

            if asset_category ==4: #cable
                if rows[1] == voltage_class and rows[2] == insulation and rows[3] == term_1 and rows[4] == term_2:
                    schi_weight_list.append(rows)

                else:
                    None


        # print(schi_weight_list[0])
        # evaluate FMEA for each subcomponent as sum of FMi*Wi
        # create organise dictionary sub id: [age factor selected, age weight, maintenance weight, failure weight, fmea weight]
        grouped_schi_dict = {}
        for item in schi_weight_list:
            # Extract the first of the last three values
            key = item[-6]  # subcomponent id
            last_three_values = item[-5:]  # [age factor selected, age weight, maintenance weight, failure weight, fmea weight]

            # Initialize the list for the key if it doesn't exist
            if key not in grouped_schi_dict:
                grouped_schi_dict[key] = []

            # Append the last three values to the appropriate key
            grouped_schi_dict[key].append(last_three_values)

        #evaluate subcomponet hi
        #get asset sub details with age factor, maintenance factor, ect
        sub_factors_selected = get_subcomponent_details(asset_id)

        evaluate_subcomponet_hi(grouped_schi_dict,subcomponent_fmea_dict, sub_factors_selected)

    def evaluate_component_condition():
        print('Evaluating Component Condition')
        #get component list for the asset
        component_list = get_component_single_asset_list(asset_category)

        com_id_list = [i[0] for i in component_list]

        # get configuration for all the asset
        cmsc_weight_list_complete = get_cmsc_weight(com_id_list)

        # filter based on the asset under test
        # filter list based on the asset characteristics

        cmsc_weight_list = []

        for rows in cmsc_weight_list_complete:
            if asset_category==1:
                if rows[1] == function and rows[2] == machine_type and rows[3] == rotor_type and rows[4] == cooling and \
                        rows[5] == wind_coil_type and rows[6] == impregnation_type:
                    cmsc_weight_list.append(rows)
                else:
                    None

            if asset_category ==3: #sw
                if rows[1] == voltage_class and rows[2] == insulation:
                    cmsc_weight_list.append(rows)

                else:
                    None

            if asset_category ==4: #cable
                if rows[1] == voltage_class and rows[2] == insulation and rows[3] == term_1 and rows[4] == term_2:
                    cmsc_weight_list.append(rows)

                else:
                    None


        # evaluate component hi as sum of sub hi * weigh
        # create organise dictionary com id: sub id , weight
        grouped_dict = {}
        for item in cmsc_weight_list:
            # Extract the first of the last three values
            key = item[-3]  # component id
            last_three_values = item[-2:]  # sub id and weight

            # Initialize the list for the key if it doesn't exist
            if key not in grouped_dict:
                grouped_dict[key] = []

            # Append the last three values to the appropriate key
            grouped_dict[key].append(last_three_values)

        for cm_id in list(grouped_dict.keys()):
            sub_score_list = []
            sub_weight_list = []
            for sub_weight in grouped_dict[cm_id]:

                #get lastest score for the test:
                sub_id = sub_weight[0]
                weight = float(sub_weight[1])
                #add condition to skip sub components non existing for selected asset
                try:
                    score = subcomponent_condition_dict[sub_id]

                    sub_score_list.append(score)
                    sub_weight_list.append(weight)
                except KeyError:
                    None


            #evaluate result for each fm_id
            #replace empty values with 0
            sub_weight_list_cleaned = []
            sub_score_list_cleaned = []

            for wg in sub_weight_list:
                if isinstance(wg, list):
                    wg=0
                else:
                    None
                sub_weight_list_cleaned.append(wg)

            for ts in sub_score_list:
                if isinstance(ts, list):
                    ts = 0
                else:
                    None
                sub_score_list_cleaned.append(ts)

            # # Calculate the sum of products
            # print('Component ----------', cm_id)
            # print(grouped_dict)
            # print(sub_score_list_cleaned)
            # print(sub_weight_list_cleaned)

            result_cm_id = sum((a if a is not None else 0) * (b if b is not None else 0) for a, b in zip(sub_score_list_cleaned, sub_weight_list_cleaned))
            #even here the result must be divided by 10 to get a value from 0 to 5, where 5 is the worst case
            result_cm_id_final = result_cm_id/10
            component_condition_dict[cm_id] = result_cm_id_final
            # print('final for cm', cm_id)
            # print(result_cm_id_final)
            # print(sub_weight_list)
            # print(sub_score_list)

        print('Component id: [Subcomponent id, Weight]')
        print(grouped_dict)

    def evaluate_asset_condition():
        print('Evaluating Asset Condition')
        # print('fm analysis')
        # print(failure_mechanisms_dict)
        # print('sub component analysis')
        # print(subcomponent_condition_dict)
        # print('fmea analsys')
        # print(subcomponent_fmea_dict)
        # print('compoennt analysis')
        # print(component_condition_dict)
        # print(fc)

        #get component list for the asset
        component_list = get_component_single_asset_list(asset_category)

        com_id_list = [i[0] for i in component_list]

        # get configuration for all the asset
        ascm_weight_list_complete = get_ascm_weight(com_id_list)

        # filter based on the asset under test
        # filter list based on the asset characteristics

        ascm_weight_list = []
        for rows in ascm_weight_list_complete:
            if asset_category==1: #machine
                if rows[1] == function and rows[2] == machine_type and rows[3] == rotor_type and rows[4] == cooling and \
                        rows[5] == wind_coil_type and rows[6] == impregnation_type:
                    ascm_weight_list.append(rows)

                else:
                    None

            if asset_category ==3: #sw
                if rows[1] == voltage_class and rows[2] == insulation:
                    ascm_weight_list.append(rows)

                else:
                    None

            if asset_category ==4: #cable
                if rows[1] == voltage_class and rows[2] == insulation and rows[3] == term_1 and rows[4] == term_2:
                    ascm_weight_list.append(rows)
                else:
                    None

        #if no data skip
        if not failure_mechanisms_dict and not subcomponent_condition_dict and not component_condition_dict:
            print('No data to analyse')

        else:

            # evaluate asset hi as sum of com hi * weigh
            # create organise dictionary com id:  weight
            grouped_dict = {}
            for item in ascm_weight_list:
                # Extract the first of the last three values
                key = item[-2]  # component id
                last_three_values = item[-1:]  #  weight

                # Initialize the list for the key if it doesn't exist
                if key not in grouped_dict:
                    grouped_dict[key] = []

                # Append the last three values to the appropriate key
                grouped_dict[key].append(last_three_values)
            cm_score_list = []
            cm_weight_list = []

            for cm_id in list(grouped_dict.keys()):

                for cm_weight in grouped_dict[cm_id]:

                    #get lastest score for the test:

                    weight = float(cm_weight[0])

                    try:
                        score = component_condition_dict[cm_id]

                        cm_score_list.append(score)
                        cm_weight_list.append(weight)
                    except KeyError:
                        None

                #evaluate result for each fm_id
                #replace empty values with 0
                cm_weight_list_cleaned = []
                cm_score_list_cleaned = []

                for wg in cm_weight_list:
                    if isinstance(wg, list):
                        wg=0
                    else:
                        None
                    cm_weight_list_cleaned.append(wg)

                for ts in cm_score_list:
                    if isinstance(ts, list):
                        ts = 0
                    else:
                        None
                    cm_score_list_cleaned.append(ts)

            # Calculate the sum of products
            # print(cm_score_list_cleaned, cm_weight_list_cleaned)


            result_as_hi = sum((a if a is not None else 0) * (b if b is not None else 0) for a, b in zip(cm_score_list_cleaned, cm_weight_list_cleaned))
            #even here the result must be divided by 10 to get a value from 0 to 5, where 5 is the worst case


            result_as_hi_final = result_as_hi/10

            rounded_as_hi = 0
            if 0 <= result_as_hi_final <=1:
                rounded_as_hi=1
            if 1 < result_as_hi_final <=2:
                rounded_as_hi=2
            if 2 < result_as_hi_final <=3:
                rounded_as_hi=3
            if 3 < result_as_hi_final <=4:
                rounded_as_hi=4
            if 4 < result_as_hi_final<=5:
                rounded_as_hi=5

            asset_condition_dict['HI'] = rounded_as_hi


            #get lated criticality class selected
            criticality_class_selected = get_latest_asset_criticality_class(asset_id)
            criticality_class_selected_number = 0
            if len(criticality_class_selected)!=0:
                criticality_class_selected_number = criticality_class_selected[0]

            risk_index = result_as_hi_final*criticality_class_selected_number

            rounded_as_ri = 0
            if 0 <= risk_index <= 1:
                rounded_as_ri = 1
            elif 1 < risk_index <= 2:
                rounded_as_ri = 2
            elif 2 < risk_index <= 3:
                rounded_as_ri = 3
            elif 3 < risk_index <= 4:
                rounded_as_ri = 4
            elif 4 < risk_index <= 5:
                rounded_as_ri = 5
            elif 5 < risk_index <= 6:
                rounded_as_ri = 6
            elif 6 < risk_index <= 7:
                rounded_as_ri = 7
            elif 7 < risk_index <= 8:
                rounded_as_ri = 8
            elif 8 < risk_index <= 9:
                rounded_as_ri = 9
            elif 9 < risk_index <= 10:
                rounded_as_ri = 10
            elif 10 < risk_index <= 11:
                rounded_as_ri = 11
            elif 11 < risk_index <= 12:
                rounded_as_ri = 12
            elif 12 < risk_index <= 13:
                rounded_as_ri = 13
            elif 13 < risk_index <= 14:
                rounded_as_ri = 14
            elif 14 < risk_index <= 15:
                rounded_as_ri = 15
            elif 15 < risk_index <= 16:
                rounded_as_ri = 16
            elif 16 < risk_index <= 17:
                rounded_as_ri = 17
            elif 17 < risk_index <= 18:
                rounded_as_ri = 18
            elif 18 < risk_index <= 19:
                rounded_as_ri = 19
            elif 19 < risk_index <= 20:
                rounded_as_ri = 20
            elif 20 < risk_index <= 21:
                rounded_as_ri = 21
            elif 21 < risk_index <= 22:
                rounded_as_ri = 22
            elif 22 < risk_index <= 23:
                rounded_as_ri = 23
            elif 23 < risk_index <= 24:
                rounded_as_ri = 24
            elif 24 < risk_index <= 25:
                rounded_as_ri = 25

            asset_condition_dict['RI'] = rounded_as_ri

            print(asset_condition_dict)

    def determine_the_maintenance_action():
        asset_maintenance_action_temp =[]
        #get the recommendation from the table for all the latest test score
        diagnostic_test_id_list = list(diagnostic_test_scores_dict.keys())

        for diagno_test_id in diagnostic_test_id_list:
            value = diagnostic_test_scores_dict.get(diagno_test_id)
            action = get_individual_test_maintenance_action_from_list(diagno_test_id, value)
            if len(action)!=0:
                asset_maintenance_action_temp.append(action[0])

        #filter the information to avoid double recommendation and provide unique string
        actions_test_id = [test_id[1] for test_id in asset_maintenance_action_temp]
        #if ir and pi is done just consider pi
        #cable
        if asset_category==4:
            #remove ir if pi is done
            has_pi = any(item[1] == 16 for item in asset_maintenance_action_temp)

            # If there is, remove the item with the second element equal to 15
            if has_pi:
                asset_maintenance_action_temp = [item for item in asset_maintenance_action_temp if item[1] != 15]

            for item in asset_maintenance_action_temp:
                maintenance_actions_list.append(item[3])

        # rm
        if asset_category == 1:
            # remove ir if pi is done
            has_pi = any(item[1] == 2 for item in asset_maintenance_action_temp)

            # If there is, remove the item with the second element equal to 15
            if has_pi:
                asset_maintenance_action_temp = [item for item in asset_maintenance_action_temp if item[1] != 1]

            for item in asset_maintenance_action_temp:
                maintenance_actions_list.append(item[3])

        # sw
        if asset_category == 3:
            # remove ir if pi is done
            has_pi = any(item[1] == 24 for item in asset_maintenance_action_temp)

            # If there is, remove the item with the second element equal to 15
            if has_pi:
                asset_maintenance_action_temp = [item for item in asset_maintenance_action_temp if item[1] != 23]

            for item in asset_maintenance_action_temp:
                maintenance_actions_list.append(item[3])

        # print(maintenance_actions_list)








    asset_details = get_single_asset_characteristics(asset_id)

    asset_category = None

    if len(asset_details) != 0:
        asset_details = asset_details[0]
        asset_category = asset_details[24]

    if len(asset_details) == 0:
        asset_details = []

    # select asset details

    yom = None
    yoi = None
    rated_voltage = None
    rated_power = None
    rated_speed = None
    machine_type = None
    function = None
    rotor_type = None
    cooling = None
    impregnation_type = None
    wind_coil_type = None
    number_of_slot = None
    number_of_poles = None

    if asset_category is not None:
        if asset_details[24] == 1:  # rotating machine

            yom = int(asset_details[4])
            yoi = int(asset_details[5])
            rated_voltage = float(asset_details[6])
            rated_power = float(asset_details[7])
            rated_speed = int(asset_details[9])
            machine_type = asset_details[11]
            function = asset_details[2]
            rotor_type = asset_details[12]
            wind_coil_type = asset_details[14]
            cooling = asset_details[10]
            impregnation_type = asset_details[15]
            number_of_slot = asset_details[16]
            number_of_poles = asset_details[18]
            number_of_turn_pole = asset_details[19]

        if asset_details[24] == 3:  # sw

            yom = int(asset_details[4])
            yoi = int(asset_details[5])
            rated_voltage = float(asset_details[6])

            insulation = asset_details[7]
            number_of_bus = asset_details[8]
            number_of_phase_per_bus = asset_details[9]
            number_of_panel_b1 = asset_details[10]
            number_of_panel_b2 = asset_details[11]

            # voltage class
            voltage_class = None
            if rated_voltage <= 35:
                voltage_class = 'Medium Voltage'
            if 35 < rated_voltage <= 150:
                voltage_class = 'High Voltage'

        if asset_details[24] == 4:  # cable
            yom = int(asset_details[4])
            yoi = int(asset_details[5])
            rated_voltage = float(asset_details[6])
            section = float(asset_details[7])
            cable_type = asset_details[8]
            insulation = asset_details[9]
            number_of_core_per_phase = asset_details[10]
            number_of_joints = asset_details[11]
            lenght_m = asset_details[12]
            term_1 = asset_details[13]
            term_2 = asset_details[14]

            #voltage class
            voltage_class = None
            if rated_voltage <=35:
                voltage_class = 'Medium Voltage'
            if 35 < rated_voltage <=150:
                voltage_class = 'High Voltage'



        # print(yom, yoi, rated_voltage, rated_power, rated_speed, function, rotor_type, wind_coil_type, impregnation_type, number_of_slot, number_of_poles)

        evaluate_failure_mechanisms()
        evaluate_subcomponent_condition()
        evaluate_component_condition()
        evaluate_asset_condition()
        determine_the_maintenance_action()

        #upload in db


        # print(failure_mechanisms_dict)
        # print(subcomponent_condition_dict)
        # print(component_condition_dict)
        # print(asset_condition_dict)
        # print(fuc)

        upload_result_in_db()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print('Risk assessment completed!')



# asset_id = 1
# assess_condition(86)
# # print('Data uploaded')