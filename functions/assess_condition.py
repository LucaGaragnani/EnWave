import sqlite3
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta, date
import csv
import matplotlib.pyplot as plt

""" Script to evaluate:
    - failure_mechanisms
    - subcomponent_condition
    - component_condition
    - asset_condition
"""


def assess_condition(asset_id):

    print('Risk Assessment in progress')
    # Connect to SQLite database (or create it if it doesn't exist)

    # Determine the path of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    db_directory = current_directory.replace('functions', 'database')

    # Construct the path to the database file
    database_path = os.path.join(db_directory, 'Inwave_RM.db')

    conn = sqlite3.connect(database_path)
    # Create a cursor object using which we can interact with the database
    cursor = conn.cursor()


    def read_inwave_file(file_path):
        """
        Opens and reads a .InWave file as CSV.

        Args:
        - file_path (str): Path to the .InWave file

        Returns:
        - pandas DataFrame: DataFrame containing the data from the .InWave file
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file '{file_path}': {str(e)}")
            return None

    failure_mechanisms_dict = {}
    failure_mechanisms_diagnostic_test = {}
    failure_mechanisms_diagnostic_test_latest_result = {}
    failure_mechanisms_weights = {}
    failure_mechanisms_subcomponent = {}

    subcomponent_condition_dict = {}
    subcomponent_factors_dict = {}
    subcomponent_condition_weight = {}

    component_condition_dict = {}

    asset_condition_dict = {}

    def upload_result_in_db():

        #insert into asset_analysis table

        current_date = date.today()
        current_date_str = current_date.strftime('%d-%m-%Y')


        # SQL statement to insert data into the table
        # select asset_analysis_id
        cursor.execute("""SELECT `id` FROM asset_analysis
                                        WHERE asset_id = ? AND date = ? AND risk_index = ? AND health_index = ? LIMIT 1""",
                       (asset_id, current_date_str, asset_condition_dict['RiskFactor'], asset_condition_dict['HI']))

        existing_record = cursor.fetchone()

        if not existing_record:


            insert_sql = '''INSERT INTO asset_analysis (date, asset_id, risk_index, health_index)
                            SELECT ?, ?, ?, ?;'''
            cursor.execute(insert_sql, (current_date_str, asset_id, asset_condition_dict['RiskFactor'], asset_condition_dict['HI']))

            # Commit the transaction
            conn.commit()

            #select asset_analysis_id
            cursor.execute("""SELECT `id` FROM asset_analysis
                                    WHERE asset_id = ? AND date = ? AND risk_index = ? AND health_index = ? LIMIT 1""", (asset_id, current_date_str,asset_condition_dict['RiskFactor'], asset_condition_dict['HI'] ))

            result = cursor.fetchone()
            asset_analysis_id = None
            if len(result)!=0:
                asset_analysis_id = result[0]


            if asset_analysis_id !=None:

                # insert into component analysis table

                for item in list(component_condition_dict.items()):

                    insert_sql = '''INSERT INTO component_analysis (analysis_id, component_id, value)
                                            SELECT ?, ?, ?;'''
                    cursor.execute(insert_sql,(asset_analysis_id, item[0],item[1]))

                # Commit the transaction
                conn.commit()

                # insert into subcomponent analysis table

                for item in list(subcomponent_condition_dict.items()):
                    insert_sql = '''INSERT INTO subcomponent_analysis (analysis_id, subcomponent_id, value)
                                                        SELECT ?, ?, ?;'''
                    cursor.execute(insert_sql, (asset_analysis_id, item[0], item[1]))

                # Commit the transaction
                conn.commit()

                # insert into failure_mechanism analysis table

                for item in list(subcomponent_condition_dict.items()):
                    insert_sql = '''INSERT INTO failure_mechanisms_analysis (analysis_id, failure_mechanism_id, value)
                                                                    SELECT ?, ?, ?;'''
                    cursor.execute(insert_sql, (asset_analysis_id, item[0], item[1]))

                # Commit the transaction
                conn.commit()
    def evaluate_failure_mechanisms():
        def get_latest_result_test(test_id):

            #check if test_id is online or offline
            cursor.execute("""
                                SELECT `condition`
                                FROM diagnostic_test
                                WHERE id = ?
                            """, (test_id,))
            test_condition = cursor.fetchone()


            if test_condition[0] == 'Offline':

                cursor.execute("""
                        SELECT `analysis`
                        FROM offline_test_data
                        WHERE diagnostic_test_id = ?
                        ORDER BY date DESC
                        LIMIT 1
                    """, (test_id,))

                # Fetch the result
                result = cursor.fetchone()

                if result != None:
                    result = result[0]

            if test_condition[0] == 'Online':

                cursor.execute("""
                        SELECT `analysis`
                        FROM online_test_data
                        WHERE diagnostic_test_id = ?
                        ORDER BY date DESC
                        LIMIT 1
                    """, (test_id,))

                # Fetch the result
                result = cursor.fetchone()

                if result != None:
                    result = result[0]

            return result

        #read Inwave file
        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        file_dictory = current_directory.replace('functions', 'database')

        # Construct the path to the database file
        file_path = os.path.join(file_dictory, 'failure_mechanisms_list.csv')


        # file_path = '/Users/marianasouzaoliveira/Desktop/InWave_EHV_RMHI/database/failure_mechanisms_list.csv'

        try:
            inwave_df = read_inwave_file(file_path)
            if inwave_df is not None:
                print(f"Successfully read {len(inwave_df)} rows from {file_path}")
                # print(inwave_df.head())  # Print first few rows of the DataFrame

                df_values = inwave_df.values.tolist()

                # print(df_values[0])

                for item in df_values:
                    failure_mechanisms_dict['{}'.format(item[1])] = 0
                    diagnostic_test_list = item[5].split(',')

                    cleaned_items = [item.strip().replace("'", "") for item in diagnostic_test_list]

                    failure_mechanisms_diagnostic_test['{}'.format(item[1])] = cleaned_items
                    failure_mechanisms_diagnostic_test_latest_result['{}'.format(item[1])] =[]
                    weights_list = item[6].split(',')
                    cleaned_weights = [item.strip().replace("'", "") for item in weights_list]
                    failure_mechanisms_weights['{}'.format(item[1])] = cleaned_weights

                    if len(item[4]) !=1:
                        subcomponent = item[4].split(',')
                        clean_subcomponent = [item.strip().replace("'", "") for item in subcomponent]
                    if len(item[4]) ==1:
                        clean_subcomponent = item[4]
                    failure_mechanisms_subcomponent['{}'.format(item[1])] = clean_subcomponent

                # print(failure_mechanisms_dict)
                # print(failure_mechanisms_diagnostic_test)
                # print(failure_mechanisms_weights)
                # print('subcomponent list')
                # print(failure_mechanisms_subcomponent)

                #search diagnostic test result - latest
                # print(list(failure_mechanisms_diagnostic_test.values()))

                i = 1

                for test_id in list(failure_mechanisms_diagnostic_test.values()):

                    for ids in test_id:
                        result = get_latest_result_test(ids)
                        if result == None:
                            result =0
                        failure_mechanisms_diagnostic_test_latest_result['{}'.format(i)].append(result)


                    i+=1
                    None

                # print('Scores')
                # print(list(failure_mechanisms_diagnostic_test_latest_result.values()))

                # evaluate failure mechanism using the weights

                # print('Weights')
                # print(list(failure_mechanisms_weights.values()))

                i=1
                for weights in list(failure_mechanisms_weights.values()):
                    fm_values = []
                    j=0
                    for weight in weights:
                        # print(list(failure_mechanisms_diagnostic_test_latest_result.values())[i-1][j])
                        # print(weight)

                        factor = int((list(failure_mechanisms_diagnostic_test_latest_result.values())[i-1][j])) * int(weight)

                        fm_values.append(factor)
                        # print(fm_values)
                        j+=1
                    # test_max_failure_mechanisms = 100
                    failure_mechanisms_dict['{}'.format(i)] = sum(fm_values)
                    # failure_mechanisms_dict['{}'.format(i)] = test_max_failure_mechanisms

                    # print('final result, failure mechanism {}'.format(i), sum(fm_values))
                    i+=1
                    None

                # print('Final Failure mechanisms')
                # print(failure_mechanisms_dict)
        except Exception as e:
            print(f"Error: {str(e)}")

        None
    def evaluate_subcomponent_condition():
        def evaluate_fmea_factor(sub_failure_mechanisms_weights, failure_mechanisms_dict, sub):

            subcomponent_FMAE_factors_dict = {}
            subcomponent_failure_mechanism_list = []
            subcomponent_failure_mechanism_weight_list = []

            sub_failure_configuration_exist=0
            #detmine failure mechanisms related to the subcomponent and their weights
            for row in sub_failure_mechanisms_weights:
                if row[0] == function and row[1] == type and row[2] == rotor_type and row[3] == cooling and row[
                    4] == wind_coil_type and row[5] == impregnation_type:

                    if row[6]==sub:
                        if row[7] !=None:
                            failure_mechanisms_related_list = row[7].split(',')
                            failure_mechanisms_related_list_cleaned_items = [item.strip().replace("'", "") for item in failure_mechanisms_related_list]

                            subcomponent_failure_mechanism_list = failure_mechanisms_related_list_cleaned_items

                            failure_mechanism_related_weights_list = row[8].split(',')
                            failure_mechanism_related_weights_list_cleaned_items = [item.strip().replace("'", "") for item in failure_mechanism_related_weights_list ]

                            subcomponent_failure_mechanism_weight_list = failure_mechanism_related_weights_list_cleaned_items

                        if row[7]==None:
                            None
                        sub_failure_configuration_exist = 1

                if row[0] != function or row[1] != type or row[2] != rotor_type or row[3] != cooling or row[
                    4] != wind_coil_type or row[5] != impregnation_type:
                    print('Configuration sub failure does not exist!')

            #evaluate FMEA facotr for the subcomponent
            # print(failure_mechanisms_dict)
            FMAE_value=0
            if sub_failure_configuration_exist !=0:
                FMEA_value_list = []
                i=0
                # print(list(failure_mechanisms_dict.values()))
                # print(subcomponent_failure_mechanism_weight_list)
                for fms in subcomponent_failure_mechanism_list:
                    # print(fms)
                    # print(float(failure_mechanisms_dict['{}'.format(fms)]))
                    # print(float(subcomponent_failure_mechanism_weight_list[i]))

                    temp = float(failure_mechanisms_dict['{}'.format(fms)])*float(subcomponent_failure_mechanism_weight_list[i])

                    # print(float(subcomponent_failure_mechanism_weight_list[i]))
                    FMEA_value_list.append(float(temp))

                    i+=1

                # normalize to 5
                if len(subcomponent_failure_mechanism_weight_list)!=0:

                    norm = round((sum(FMEA_value_list)* 5) / 1000,2)
                    # print('fmea norm', norm)

                    FMEA_value =float(norm)
                if len(subcomponent_failure_mechanism_weight_list)==0:
                    FMEA_value=0

            return FMEA_value
        #get subcomponent_list
        subcomponent_list = []
        cursor.execute("""SELECT `id` FROM asset_subcomponent""")
        asset_subcomponent = cursor.fetchall()

        for sub in asset_subcomponent:
            subcomponent_list.append(sub[0])

        #get subcomponent_details
        cursor.execute("""SELECT `age_factor`, `maintenance_factor`, `failure_factor` FROM asset_subcomponent_details WHERE asset_id = ?""", (asset_id,))
        asset_subcomponent_details = cursor.fetchall()

        i=1
        for factors in asset_subcomponent_details:
            subcomponent_factors_dict['{}'.format(i)] = list(factors)
            i+=1

        # print(subcomponent_factors_dict)

        # read Inwave file

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        file_dictory = current_directory.replace('functions', 'database')

        # Construct the path to the database file
        file_path = os.path.join(file_dictory, 'subcomponents_weigths.csv')
        file_path_1 = os.path.join(file_dictory, 'subcomponents_failure_mechanisms_weigths.csv')


        # file_path = '/Users/marianasouzaoliveira/Desktop/InWave_EHV_RMHI/database/subcomponents_weigths.csv'
        # file_path_1='/Users/marianasouzaoliveira/Desktop/InWave_EHV_RMHI/database/subcomponents_failure_mechanisms_weigths.csv'

        try:
            inwave_df = read_inwave_file(file_path)
            inwave_df_1 = read_inwave_file(file_path_1)
            if inwave_df is not None and inwave_df_1 is not None:
                print(f"Successfully read {len(inwave_df)} rows from {file_path}")
                # print(inwave_df.head())  # Print first few rows of the DataFrame

                df_values = inwave_df.values.tolist()


                df_values = inwave_df.values.tolist()

                df_values_1 = pd.DataFrame(inwave_df_1)
                df_values_1_replaced = df_values_1.where(pd.notna(df_values_1), None)
                df_values_1_replaced_list = df_values_1_replaced.values.tolist()

                # print(df_values)
                configuration_exist = 0

                #select right weights
                for sub in subcomponent_list:
                    age_factor = subcomponent_factors_dict['{}'.format(sub)][0]
                    maintenance_factor = subcomponent_factors_dict['{}'.format(sub)][1]
                    failure_factor = subcomponent_factors_dict['{}'.format(sub)][2]


                    for conf in df_values:
                        if conf[0] == function and conf[1] == type and conf[2]==rotor_type and conf[3]==cooling and conf[4]==wind_coil_type and conf[5]==impregnation_type:
                            if conf[6]==sub and conf[7]==age_factor:
                                subcomponent_condition_weight['{}'.format(sub)] = [conf[8],conf[9],conf[10],conf[11]]
                                configuration_exist=1
                        if conf[0] != function or conf[1] != type or conf[2]!=rotor_type or conf[3]!=cooling or conf[4]!=wind_coil_type or conf[5]!=impregnation_type:
                                print('Configuration subcomponent weight does not exist!')



                if configuration_exist!=0:
                    #evaluate subcomponent health index
                    for sub in subcomponent_list:
                        age_factor = float(subcomponent_condition_weight['{}'.format(sub)][0])*float(subcomponent_factors_dict['{}'.format(sub)][0])

                        maintenance_factor = float(subcomponent_condition_weight['{}'.format(sub)][1])*float(subcomponent_factors_dict['{}'.format(sub)][1])
                        failure_factor = float(subcomponent_condition_weight['{}'.format(sub)][2])*float(subcomponent_factors_dict['{}'.format(sub)][2])

                        #print(age_factor)
                        # print(maintenance_factor)
                        # print(failure_factor)
                        # age_factor=5
                        # maintenance_factor=5
                        # failure_factor=5

                        #evaluate FMEA Factor:
                        FMAE_value = evaluate_fmea_factor(df_values_1_replaced_list,failure_mechanisms_dict, sub)
                        FMAE_factor = FMAE_value * int(subcomponent_condition_weight['{}'.format(sub)][3])

                        # print(float(age_factor+maintenance_factor+failure_factor+FMAE_factor))
                        # print('af',age_factor)
                        # print('mf',maintenance_factor)
                        # print('ff',failure_factor)
                        # print('FMEA',FMAE_factor)

                        final_subcomponent_hi = int(age_factor+maintenance_factor+failure_factor+FMAE_factor)
                        final_subcomponent_hi_norm = round(((final_subcomponent_hi)*5/55),2)

                        subcomponent_hi = 0
                        if 0< final_subcomponent_hi_norm <=1:
                            subcomponent_hi=1
                        if 1 < final_subcomponent_hi_norm <=2:
                            subcomponent_hi=2
                        if 2 < final_subcomponent_hi_norm <=3:
                            subcomponent_hi =3
                        if 3 < final_subcomponent_hi_norm <=4:
                            subcomponent_hi =4
                        if 4 < final_subcomponent_hi_norm <=5:
                            subcomponent_hi=5

                        # print('finalsubhi', final_subcomponent_hi, final_subcomponent_hi_norm, subcomponent_hi)


                        subcomponent_condition_dict['{}'.format(sub)] = final_subcomponent_hi_norm

                    # print(subcomponent_condition_dict)
        except Exception as e:
            print(f"Error: {str(e)}")

    def evaluate_component_condition():

        #test max cond
        # subcomponent_condition_dict['1'] = 5
        # subcomponent_condition_dict['12'] = 5




        # read Inwave file

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        file_dictory = current_directory.replace('functions', 'database')

        # Construct the path to the database file
        file_path = os.path.join(file_dictory, 'components_subcompo_weigths.csv')

        # file_path = '/Users/marianasouzaoliveira/Desktop/InWave_EHV_RMHI/database/components_subcompo_weigths.csv'

        component_conf_exist = 0
        try:
            inwave_df = read_inwave_file(file_path)
            if inwave_df is not None:
                print(f"Successfully read {len(inwave_df)} rows from {file_path}")
                # print(inwave_df.head())  # Print first few rows of the DataFrame

                df_values = inwave_df.values.tolist()

                for rows in df_values:
                    if rows[0] == function and rows[1] == type and rows[2] == rotor_type and rows[3] == cooling and rows[
                        4] == wind_coil_type and rows[5] == impregnation_type:

                        comp_subcomp_list = []
                        comp_subcomp_weight_list = []
                        if rows[6]!=None:
                            comp_subcomp_list_temp = rows[7].split(',')
                            comp_subcomp_list_cleaned_items = [item.strip().replace("'", "") for item in comp_subcomp_list_temp]

                            comp_subcomp_list = comp_subcomp_list_cleaned_items

                        if rows[6]!=None:
                            comp_subcomp_weight_list_temp = rows[8].split(',')
                            comp_subcomp_weight_list_cleaned_items = [item.strip().replace("'", "") for item in comp_subcomp_weight_list_temp]

                            comp_subcomp_weight_list = comp_subcomp_weight_list_cleaned_items

                        i=0
                        temp_factor_list = []
                        for item in comp_subcomp_list:
                            temp_factor = subcomponent_condition_dict['{}'.format(item)] * int(comp_subcomp_weight_list[i])
                            temp_factor_list.append(temp_factor)

                            i+=1

                        component_condition_dict['{}'.format(rows[6])] = round(int(sum(temp_factor_list))*0.1,2)

                    if rows[0] != function or rows[1] != type or rows[2] != rotor_type or rows[3] != cooling or rows[
                        4] != wind_coil_type or rows[5] != impregnation_type:
                        print('Configuration component does not exist!')

        except Exception as e:
            print(f"Error: {str(e)}")

    def evaluate_asset_condition():
        # read Inwave file

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))


        file_dictory = current_directory.replace('functions', 'database')

        # Construct the path to the database file
        file_path = os.path.join(file_dictory, 'asset_compo_weigths.csv')

        # file_path = '/Users/marianasouzaoliveira/Desktop/InWave_EHV_RMHI/database/asset_compo_weigths.csv'

        try:
            inwave_df = read_inwave_file(file_path)
            if inwave_df is not None:
                print(f"Successfully read {len(inwave_df)} rows from {file_path}")
                # print(inwave_df.head())  # Print first few rows of the DataFrame

                df_values = inwave_df.values.tolist()
                # print(df_values)

                #get the right configuration and exctract weight
                weight_comp_list = []

                for rows in df_values:
                    #select machine
                    if rows[0] == function and rows[1] == type and rows[2]==rotor_type and rows[3]==cooling and rows[4] == wind_coil_type and rows[5]==impregnation_type:
                        #exctract weight
                        weight_comp_list.append(rows[6])
                        weight_comp_list.append(rows[7])
                        weight_comp_list.append(rows[8])

                    if rows[0] != function or rows[1] != type or rows[2] !=rotor_type or rows[3]!=cooling or rows[4] != wind_coil_type or rows[5]==impregnation_type:
                        None

                #evaluate health index
                asset_hi_list = []
                i=1
                for items in weight_comp_list:
                    asset_hi_factor = component_condition_dict['{}'.format(i)] * int(items)
                    asset_hi_list.append(asset_hi_factor)


                asset_hi = sum(asset_hi_list)*0.1

                final_asset_hi = 0
                if 0 < asset_hi <= 1:
                    final_asset_hi = 1
                if 1 < asset_hi <= 2:
                    final_asset_hi = 2
                if 2 < asset_hi <= 3:
                    final_asset_hi = 3
                if 3 < asset_hi <= 4:
                    final_asset_hi = 4
                if 4 < asset_hi <= 5:
                    final_asset_hi = 5



                asset_condition_dict['HI'] = final_asset_hi

                #select latest criticality class to evaluate the risk factor
                cursor.execute("""
                                        SELECT `criticality_class`
                                        FROM asset_details
                                        WHERE asset_id = ?
                                        ORDER BY date
                                        LIMIT 1
                                    """, (asset_id,))

                # Fetch the result
                result = cursor.fetchone()

                risk_factor=0
                if len(result) !=0:

                    risk_factor = result[0]
                    # print(risk_factor, asset_hi)

                asset_risk_factor = risk_factor*final_asset_hi

                asset_condition_dict['RiskFactor'] = int(asset_risk_factor)
        except Exception as e:
            print(f"Error: {str(e)}")

        # print(failure_mechanisms_dict)
        # print(subcomponent_condition_dict)
        # print(component_condition_dict)
        # print(asset_condition_dict)
        # print(fuck)

    # select asset details
    yom = None
    yoi = None
    rated_voltage = None
    rated_power = None
    rated_speed = None
    function = None
    type = None
    rotor_type = None
    cooling = None
    impregnation_type = None
    wind_coil_type = None
    number_of_slot = None
    number_of_poles = None

    cursor.execute("SELECT * FROM asset WHERE id= ?", (asset_id,))
    asset_results = cursor.fetchone()

    yom = int(asset_results[4])
    yoi = int(asset_results[5])
    rated_voltage = float(asset_results[6])
    rated_power = float(asset_results[7])
    rated_speed = int(asset_results[9])
    function = asset_results[2]
    cooling = asset_results[10]
    type = asset_results[11]
    rotor_type = asset_results[12]
    wind_coil_type = asset_results[14]
    impregnation_type = asset_results[15]
    number_of_slot = asset_results[16]
    number_of_poles = asset_results[18]

    # print(yom, yoi, rated_voltage, rated_power, rated_speed, function, rotor_type, wind_coil_type, impregnation_type, number_of_slot, number_of_poles)

    evaluate_failure_mechanisms()
    evaluate_subcomponent_condition()
    evaluate_component_condition()
    evaluate_asset_condition()

    #upload in db
    upload_result_in_db()

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print('Risk assessment completed!')



# asset_id = 1
# assess_condition(asset_id)
# # print('Data uploaded')