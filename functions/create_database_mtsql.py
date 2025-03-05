import mysql.connector
import pandas as pd
import os
from cryptography.fernet import Fernet
import base64




def create_centralized_db():

    try:

        #Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Change to your MySQL host
            user='root',  # Your MySQL username
            password='InWave@2024!',  # Your MySQL password
            # database='Inwave_RM',  # Database name you want to create/use
        )

        # Create a cursor object using which we can interact with the database
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS Inwave_IHMS")

        # Use the database
        cursor.execute("USE Inwave_IHMS")

        # Here you can add your table creation scripts and other queries

        # # Don't forget to commit any changes
        # conn.commit()


        def create_db(cursor):
            def create_company_table():
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS company (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Company table created")
            def create_site_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS site (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    site_name VARCHAR(255) NOT NULL,
                    lat DECIMAL(9, 6),
                    lon DECIMAL(9, 6),
                    customer_id INT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES company(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Site table created")
            def create_asset_category_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS asset_category (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    category VARCHAR(255) UNIQUE
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset Category table created")
            def create_asset_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS asset (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tag VARCHAR(255) NOT NULL,
                    asset_function VARCHAR(255),
                    manufacturer VARCHAR(255),
                    yom INT,
                    yoi INT,
                    rated_voltage DECIMAL(10, 2),
                    feature_1 VARCHAR(255),
                    feature_2 VARCHAR(255),
                    feature_3 VARCHAR(255),
                    feature_4 VARCHAR(255),
                    feature_5 VARCHAR(255),
                    feature_6 VARCHAR(255),
                    feature_7 VARCHAR(255),
                    feature_8 VARCHAR(255),
                    feature_9 VARCHAR(255),
                    feature_10 VARCHAR(255),
                    feature_11 VARCHAR(255),
                    feature_12 VARCHAR(255),
                    feature_13 VARCHAR(255),
                    feature_14 VARCHAR(255),
                    feature_15 VARCHAR(255),
                    lat DECIMAL(9, 6),
                    lon DECIMAL(9, 6),
                    asset_category_id INT NOT NULL,
                    site_id INT NOT NULL,
                    FOREIGN KEY (asset_category_id) REFERENCES asset_category(id),
                    FOREIGN KEY (site_id) REFERENCES site(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset table created")
            def create_asset_site_layout_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS asset_site_layout (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    from_asset_id INT,
                    to_asset_id INT,
                    site_id INT NOT NULL,
                    FOREIGN KEY (site_id) REFERENCES site(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset site layout table created")
            def create_asset_sw_layout_table():
                # SQL statement to create a table
                create_table_sql = '''
                                CREATE TABLE IF NOT EXISTS asset_sw_layout (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    bus_number VARCHAR(255),
                                    panel_number VARCHAR(255),
                                    panel_tag VARCHAR(255),
                                    connected_feeder_id INT,
                                    asset_id INT NOT NULL,
                                    FOREIGN KEY (asset_id) REFERENCES asset(id)
                                );
                                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset asset sw layout table created")
            def create_asset_details_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS asset_details (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    criticality_class INT,
                    date TEXT,
                    asset_id INT NOT NULL,
                    FOREIGN KEY (asset_id) REFERENCES asset(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset details table created")
            def create_asset_component_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS asset_component (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description VARCHAR(255),
                    asset_category_id INT NOT NULL,
                    FOREIGN KEY (asset_category_id) REFERENCES asset_category(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset component table created")
            def create_asset_subcomponent_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS asset_subcomponent (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description VARCHAR(255),
                    asset_component_id INT NOT NULL,
                    FOREIGN KEY (asset_component_id) REFERENCES asset_component(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset subcomponent table created")
            def create_asset_subcomponent_details_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS asset_subcomponent_details (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    age_factor INT,
                    maintenance_factor INT,
                    failure_factor INT,
                    description VARCHAR(255),
                    asset_subcomponent_id INT NOT NULL,
                    asset_id INT NOT NULL,
                    FOREIGN KEY (asset_subcomponent_id) REFERENCES asset_subcomponent(id),
                    FOREIGN KEY (asset_id) REFERENCES asset(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset subcomponent details table created")
            def create_failure_mechanisms_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS failure_mechanisms (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    failure_cause VARCHAR(255),
                    local_effect VARCHAR(255),
                    asset_category_id INT NOT NULL,
                    FOREIGN KEY (asset_category_id) REFERENCES asset_category(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Failure mechanisms table created")
            def create_failure_mechanisms_subcomponent_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS failure_mechanisms_subcomponent_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    failure_mechanism_id INT NOT NULL,
                    asset_subcomponent_id INT NOT NULL,
                    FOREIGN KEY (failure_mechanism_id) REFERENCES failure_mechanisms(id),
                    FOREIGN KEY (asset_subcomponent_id) REFERENCES asset_subcomponent(id)

                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Failure mechanisms subcomponent table created")
            def create_diagnostic_test_table():
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS diagnostic_test (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    asset_condition VARCHAR(255),
                    asset_category_id INT NOT NULL,
                    FOREIGN KEY (asset_category_id) REFERENCES asset_category(id),
                    UNIQUE (name, asset_category_id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Diagnostic test table created")
            def create_online_test_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS online_test_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date TEXT NOT NULL,
                    asset_id INT NOT NULL,
                    subcomponent_id INT NOT NULL,
                    diagnostic_test_id INT NOT NULL,
                    feature_1 VARCHAR(255),
                    feature_2 VARCHAR(255),
                    feature_3 VARCHAR(255),
                    feature_4 VARCHAR(255),
                    feature_5 VARCHAR(255),
                    feature_6 VARCHAR(255),
                    feature_7 VARCHAR(255),
                    feature_8 VARCHAR(255),
                    feature_9 VARCHAR(255),
                    feature_10 VARCHAR(255),
                    feature_11 VARCHAR(255),
                    feature_12 VARCHAR(255),
                    feature_13 VARCHAR(255),
                    feature_14 VARCHAR(255),
                    feature_15 VARCHAR(255),
                    feature_16 VARCHAR(255),
                    feature_17 VARCHAR(255),
                    feature_18 VARCHAR(255),
                    feature_19 VARCHAR(255),
                    feature_20 VARCHAR(255),
                    feature_21 VARCHAR(255),
                    feature_22 VARCHAR(255),
                    feature_23 VARCHAR(255),
                    feature_24 VARCHAR(255),
                    feature_25 BLOB,
                    analysis INT,
                    FOREIGN KEY (asset_id) REFERENCES asset(id),
                    FOREIGN KEY (subcomponent_id) REFERENCES asset_subcomponent(id),
                    FOREIGN KEY (diagnostic_test_id) REFERENCES diagnostic_test(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Online test data table created")
            def create_offline_test_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS offline_test_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date TEXT NOT NULL,
                    asset_id INT NOT NULL,
                    subcomponent_id INT NOT NULL,
                    diagnostic_test_id INT NOT NULL,
                    feature_1 VARCHAR(255),
                    feature_2 VARCHAR(255),
                    feature_3 VARCHAR(255),
                    feature_4 VARCHAR(255),
                    feature_5 VARCHAR(255),
                    feature_6 VARCHAR(255),
                    feature_7 VARCHAR(255),
                    feature_8 VARCHAR(255),
                    feature_9 VARCHAR(255),
                    feature_10 VARCHAR(255),
                    feature_11 VARCHAR(255),
                    feature_12 VARCHAR(255),
                    feature_13 VARCHAR(255),
                    feature_14 VARCHAR(255),
                    feature_15 VARCHAR(255),
                    feature_16 VARCHAR(255),
                    feature_17 VARCHAR(255),
                    feature_18 VARCHAR(255),
                    feature_19 VARCHAR(255),
                    feature_20 VARCHAR(255),
                    feature_21 VARCHAR(255),
                    feature_22 VARCHAR(255),
                    feature_23 VARCHAR(255),
                    feature_24 VARCHAR(255),
                    feature_25 BLOB,
                    analysis INT,
                    FOREIGN KEY (asset_id) REFERENCES asset(id),
                    FOREIGN KEY (subcomponent_id) REFERENCES asset_subcomponent(id),
                    FOREIGN KEY (diagnostic_test_id) REFERENCES diagnostic_test(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Offline test data table created")
            def create_operational_test_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS operational_test_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date TEXT NOT NULL,
                    asset_id INT NOT NULL,
                    feature_1 VARCHAR(255),
                    feature_2 VARCHAR(255),
                    feature_3 VARCHAR(255),
                    feature_4 VARCHAR(255),
                    feature_5 VARCHAR(255),
                    feature_6 VARCHAR(255),
                    feature_7 VARCHAR(255),
                    feature_8 VARCHAR(255),
                    feature_9 VARCHAR(255),
                    feature_10 VARCHAR(255),
                    feature_11 VARCHAR(255),
                    feature_12 VARCHAR(255),
                    feature_13 VARCHAR(255),
                    feature_14 VARCHAR(255),
                    feature_15 VARCHAR(255),
                    feature_16 VARCHAR(255),
                    feature_17 VARCHAR(255),
                    feature_18 VARCHAR(255),
                    feature_19 VARCHAR(255),
                    feature_20 VARCHAR(255),
                    feature_21 VARCHAR(255),
                    feature_22 VARCHAR(255),
                    feature_23 VARCHAR(255),
                    feature_24 VARCHAR(255),
                    feature_25 VARCHAR(255),
                    analysis INT,
                    FOREIGN KEY (asset_id) REFERENCES asset(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Operational test data table created")
            def create_criticality_list_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS criticality_list (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    class VARCHAR(255) UNIQUE,
                    safety VARCHAR(255),
                    financial VARCHAR(255),
                    reliability VARCHAR(255),
                    environmental VARCHAR(255)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Criticality list table created")
            def create_asset_analysis_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS asset_analysis (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date TEXT NOT NULL,
                    asset_id INT NOT NULL,
                    risk_index INT,
                    health_index INT,
                    FOREIGN KEY (asset_id) REFERENCES asset(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset analysis table created")
            def create_asset_maintenance_action_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS asset_maintenance_actions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    asset_analysis_id INT NOT NULL,
                    maintenance_action VARCHAR(255),
                    peer_reviewed_date DATE,
                    peer_reviewed_comment TEXT,
                    peer_review_eng_name VARCHAR(255),
                    FOREIGN KEY (asset_analysis_id) REFERENCES asset_analysis(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset maintenance actions table created")
            def create_asset_maintenance_action_list_stable():
                # SQL statement to create a table
                create_table_sql = '''
                                CREATE TABLE IF NOT EXISTS maintenance_action_list (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    diagnostic_test_id INT NOT NULL,
                                    score INT,
                                    action VARCHAR(255),
                                    FOREIGN KEY (diagnostic_test_id) REFERENCES diagnostic_test(id)
                                );
                                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset maintenance actions list table created")
            def create_failure_mechanisms_analysis_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS failure_mechanisms_analysis (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    analysis_id INT NOT NULL,
                    failure_mechanism_id INT NOT NULL,
                    value INT,
                    FOREIGN KEY (analysis_id) REFERENCES asset_analysis(id),
                    FOREIGN KEY (failure_mechanism_id) REFERENCES failure_mechanisms(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("FMCEA analysis table created")
            def create_subcomponent_analysis_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS subcomponent_analysis (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    analysis_id INT NOT NULL,
                    subcomponent_id INT NOT NULL,
                    value INT,
                    FOREIGN KEY (analysis_id) REFERENCES asset_analysis(id),
                    FOREIGN KEY (subcomponent_id) REFERENCES asset_subcomponent(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Subcomponent analysis table created")
            def create_component_analysis_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS component_analysis (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    analysis_id INT NOT NULL,
                    component_id INT NOT NULL,
                    value INT,
                    FOREIGN KEY (analysis_id) REFERENCES asset_analysis(id),
                    FOREIGN KEY (component_id) REFERENCES asset_component(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Component analysis table created")
            def create_fmdi_factors_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS fmdi_factors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    feature_1 TEXT,
                    feature_2 TEXT,
                    feature_3 TEXT,
                    feature_4 TEXT,
                    feature_5 TEXT,
                    feature_6 TEXT,
                    feature_7 TEXT,
                    feature_8 TEXT,
                    feature_9 TEXT,
                    feature_10 TEXT,
                    feature_11 TEXT,
                    feature_12 TEXT,
                    feature_13 TEXT,
                    feature_14 TEXT,
                    feature_15 TEXT,
                    failure_mechanism_id INT NOT NULL,
                    diagnostic_test_id INT NOT NULL,
                    value TEXT,
                    FOREIGN KEY (failure_mechanism_id) REFERENCES failure_mechanisms(id),
                    FOREIGN KEY (diagnostic_test_id) REFERENCES diagnostic_test(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Fmdi factor table created")
            def create_scfm_factors_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS scfm_factors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    feature_1 TEXT,
                    feature_2 TEXT,
                    feature_3 TEXT,
                    feature_4 TEXT,
                    feature_5 TEXT,
                    feature_6 TEXT,
                    feature_7 TEXT,
                    feature_8 TEXT,
                    feature_9 TEXT,
                    feature_10 TEXT,
                    feature_11 TEXT,
                    feature_12 TEXT,
                    feature_13 TEXT,
                    feature_14 TEXT,
                    feature_15 TEXT,
                    subcomponent_id INT NOT NULL,
                    failure_mechanism_id INT NOT NULL,
                    value TEXT,
                    FOREIGN KEY (subcomponent_id) REFERENCES asset_subcomponent(id),
                    FOREIGN KEY (failure_mechanism_id) REFERENCES failure_mechanisms(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Scfm factor table created")
            def create_schi_factors_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS schi_factors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    feature_1 TEXT,
                    feature_2 TEXT,
                    feature_3 TEXT,
                    feature_4 TEXT,
                    feature_5 TEXT,
                    feature_6 TEXT,
                    feature_7 TEXT,
                    feature_8 TEXT,
                    feature_9 TEXT,
                    feature_10 TEXT,
                    feature_11 TEXT,
                    feature_12 TEXT,
                    feature_13 TEXT,
                    feature_14 TEXT,
                    feature_15 TEXT,
                    subcomponent_id INT NOT NULL,
                    age_factor TEXT NOT NULL,
                    age_weight TEXT NOT NULL,
                    maintenance_weight TEXT NOT NULL,
                    failure_weight TEXT NOT NULL,
                    diagnostic_weight TEXT NOT NULL,
                    FOREIGN KEY (subcomponent_id) REFERENCES asset_subcomponent(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Scfm factor table created")
            def create_cmsc_factors_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS cmsc_factors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    feature_1 TEXT,
                    feature_2 TEXT,
                    feature_3 TEXT,
                    feature_4 TEXT,
                    feature_5 TEXT,
                    feature_6 TEXT,
                    feature_7 TEXT,
                    feature_8 TEXT,
                    feature_9 TEXT,
                    feature_10 TEXT,
                    feature_11 TEXT,
                    feature_12 TEXT,
                    feature_13 TEXT,
                    feature_14 TEXT,
                    feature_15 TEXT,
                    component_id INT NOT NULL,
                    subcomponent_id INT NOT NULL,
                    value TEXT,
                    FOREIGN KEY (component_id) REFERENCES asset_component(id),
                    FOREIGN KEY (subcomponent_id) REFERENCES asset_subcomponent(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Cmsc factor table created")
            def create_ascm_factors_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS ascm_factors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    feature_1 TEXT,
                    feature_2 TEXT,
                    feature_3 TEXT,
                    feature_4 TEXT,
                    feature_5 TEXT,
                    feature_6 TEXT,
                    feature_7 TEXT,
                    feature_8 TEXT,
                    feature_9 TEXT,
                    feature_10 TEXT,
                    feature_11 TEXT,
                    feature_12 TEXT,
                    feature_13 TEXT,
                    feature_14 TEXT,
                    feature_15 TEXT,
                    component_id INT NOT NULL,
                    value TEXT,
                    FOREIGN KEY (component_id) REFERENCES asset_component(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Ascm factor table created")
            def create_user_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    company_id INT NOT NULL,
                    FOREIGN KEY (company_id) REFERENCES company(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("User table created")
            def create_session_data_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS session_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    datetime DATETIME NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user(id)
                );
                '''

                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("User session table created")

            create_company_table()
            create_site_table()
            create_asset_category_table()
            create_asset_table()
            create_asset_site_layout_table()
            create_asset_sw_layout_table()
            create_asset_details_table()
            create_asset_component_table()
            create_asset_subcomponent_table()
            create_asset_subcomponent_details_table()
            create_failure_mechanisms_table()
            create_failure_mechanisms_subcomponent_table()
            create_diagnostic_test_table()
            create_online_test_table()
            create_offline_test_table()
            create_operational_test_table()
            create_criticality_list_table()
            create_asset_analysis_table()
            create_asset_maintenance_action_table()
            create_asset_maintenance_action_list_stable()
            create_failure_mechanisms_analysis_table()
            create_subcomponent_analysis_table()
            create_component_analysis_table()
            create_fmdi_factors_table()
            create_schi_factors_table()
            create_scfm_factors_table()
            create_cmsc_factors_table()
            create_ascm_factors_table()
            create_user_table()
            create_session_data_table()

        def upload_settings(cursor):
            def insert_asset_categoty():
                categories = ['Rotating Machine', 'Transformer', 'Switchgear', 'Cable']

                # SQL statement to insert a row into the table
                insert_sql = '''
                INSERT INTO asset_category (category)
                SELECT %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM asset_category WHERE category = %s
                );
                '''

                try:
                    with conn.cursor() as cursor:
                        for category in categories:
                            cursor.execute(insert_sql, (category,category))
                    # Commit the transaction
                    conn.commit()
                except mysql.connector.Error as err:
                    print(f"Error: {err}")

                print('Asset Category inserted or already exist')
            def insert_component():
                # Insert data
                components_rotating_machine = [
                    ('Stator', 'Stationary part/s of the machine.', 1),
                    ('Rotor', 'Rotating part/s of the machine.', 1),
                    ('Auxiliaries', 'Enclosure and its components of the machine.', 1),
                ]

                components_cable = [
                    ('Termination', 'The termination is the end connection of a power cable that provides a secure interface to other electrical equipment.', 4),
                    ('Section', 'Cable section of the system.', 4),
                    ('Joint', 'A joint is a connection point between two sections of power cable.', 4),
                ]

                components_switchgear = [
                    ('Bay/Panel', 'Bay/Panel usually contains essential equipment such as circuit breakers, disconnect switches, busbars, current transformers (CTs), voltage transformers (VTs), and protective relays.', 3),
                    ('Bus', 'Conducts electricity between different components of the switchgear', 3),
                    ('Main Insulation', 'Main electrical insulation of the system.', 3),

                ]

                components_transformer = [
                    ('Core', 'Made of laminated steel or iron, the core provides a pathway for the magnetic flux generated during the transformation of electrical energy.', 2),
                    ('Winding','The coil connected to the voltage source, where electrical energy is transformed into magnetic energy and viceversa.',2),
                    ('Tank/Enclosure','The outer shell that houses the core and windings.',2),
                    ('Main Insulation tx', 'Main electrical insulation of the system.', 2),
                ]

                # SQL statement to insert data into the table
                insert_sql = '''
                INSERT INTO asset_component (name, description, asset_category_id)
                SELECT %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM asset_component WHERE name = %s
                );
                '''

                try:
                    with conn.cursor() as cursor:
                        # Insert each component into the table
                        for component in components_rotating_machine:
                            cursor.execute(insert_sql, ( (component[0], component[1], component[2], component[0])))
                        for component in components_cable:
                            cursor.execute(insert_sql, ( (component[0], component[1], component[2], component[0])))
                        for component in components_switchgear:
                            cursor.execute(insert_sql, ( (component[0], component[1], component[2], component[0])))
                        for component in components_transformer:
                            cursor.execute(insert_sql, ( (component[0], component[1], component[2], component[0])))

                    # Commit the transaction
                    conn.commit()
                    print("Components inserted or already exist")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                # print("Components inserted or already exist")
            def insert_subcomponent():
                # Insert data
                subcomponents_rotating_machine = [
                    ('Core', 'Laminated iron core', 'Stator'),
                    ('Stator Winding', 'Stator winding', 'Stator'),
                    ('Stator Winding auxiliaries', 'Components to support/connect stator winding', 'Stator'),
                    ('Shaft', 'Mechanical rotating part','Rotor'),
                    ('Rotor Winding', 'Rotor winding','Rotor'),
                    ('Rotor Winding auxiliaries', 'Component to support/connect rotor winding','Rotor'),
                    ('Rotor Poles', 'Rotor Poles','Rotor'),
                    ('Bearing DE', 'Bearing on Driven End','Rotor'),
                    ('Bearing NDE', 'Bearing on Non Drive End','Rotor'),
                    ('Enclosure', 'Enclosure of the machine','Auxiliaries'),
                    ('Terminal box', 'Terminal box for connection to system','Auxiliaries'),
                    ('Cooling system', 'Machine cooling system','Auxiliaries'),
                    ('Exciter', 'Rotor Winding exciter', 'Rotor')
                ]

                subcomponents_cable = [
                    ('HV Connector', 'Conductor connector.','Termination'),
                    ('Main termination', 'Main part of the termination.','Termination'),
                    ('Ground lead Termination', 'Connection between cable screen and ground.','Termination'),
                    ('Link box Termination', 'Ground connection box.','Termination'),
                    ('Surge Voltage Limiter Termination', 'Limiting the voltage on the oversheat.','Termination'),
                    ('Main Insulation', 'High voltage insulation system.','Section'),
                    ('Oversheath insulation', 'External insulation system.','Section'),
                    ('Main joint', 'Main part of the joint.','Joint'),
                    ('Ground lead Joint', 'Connection between cable screen and ground.','Joint'),
                    ('Link box Joint', 'Ground connection box.','Joint'),
                    ('Surge Voltage Limiter Joint', 'Limiting the voltage on the oversheat.','Joint'),
                ]

                subcomponents_switchgear = [
                    ('Circuit breaker', 'Circuit breaker of the panel/bay','Bay/Panel'),
                    ('Protection Relay', 'Protection system.','Bay/Panel'),
                    ('Voltage transformer', 'Voltage measurement device.','Bay/Panel'),
                    ('Current transformer', 'Current measurement device.','Bay/Panel'),
                    ('Earthing switch', 'Earth connection system.','Bay/Panel'),
                    ('Spout', 'Spouts serve as interface points for connecting cables or busbars to the switchgear.','Bay/Panel'),
                    ('Auxiliaries Panel', 'Insulators and other auxiliaries components.','Bay/Panel'),
                    ('Bus bar', 'Main conductor system','Bus'),
                    ('Auxiliaries Bus', 'Insulators and other auxiliaries components.','Bus'),
                ]

                subcomponents_transformer = [
                    ('Laminated sheets', 'Main part of the core.','Core' ),
                    ('Clamping plates', 'Metal plates or clamps are used to hold the laminated sheets together.', 'Core'),
                    ('Tap changer', 'Voltage output regulator.','Winding'),
                    ('Bushing Primary', 'Insulation from winding to connection.','Winding'),
                    ('Bushing Secondary', 'Insulation from winding to connection.','Winding'),
                    ('Bushing Tertiary', 'Insulation from winding to connection.','Winding'),
                    ('Primary winding', 'Highest voltage winding','Winding'),
                    ('Secondary winding', 'Main low voltage winding.','Winding'),
                    ('Tertiary winding', 'Auxiliary voltage winding.','Winding'),
                    ('Enclosure/Tank', 'Main container for the transformer.','Tank/Enclosure'),
                    ('Terminal boxes Primary', 'Conteiner for the connecitons of the primary windings.','Tank/Enclosure'),
                    ('Terminal boxes Secondary', 'Conteiner for the connecitons of the secondary windings.','Tank/Enclosure'),
                    ('Terminal boxes Tertiary', 'Conteiner for the connecitons of the tertiary windings.','Tank/Enclosure'),
                    ('Oil Breather', 'Reserve tank for oil','Tank/Enclosure'),
                    ('Gauges', 'Meters','Tank/Enclosure'),
                    ('Cooling system tx', 'Fan and radiators.','Tank/Enclosure'),
                    ('Oil', 'Oil','Main Insulation tx'),
                ]

                insert_sql = '''
                    INSERT INTO asset_subcomponent (name, description, asset_component_id)
                    SELECT %s, %s, %s
                    ;
                '''

                try:
                    with conn.cursor() as cursor:
                        # Insert each subcomponent into the table
                        for subcomponent in subcomponents_rotating_machine:
                            # search component id
                            search_sql = '''SELECT id FROM asset_component WHERE name = %s AND asset_category_id = %s;'''

                            comp_name= subcomponent[2]
                            asset_category_id = 1

                            cursor.execute(search_sql, (comp_name, asset_category_id))
                            comp_id_result = cursor.fetchone()


                            # Check if a result was returned
                            if comp_id_result:
                                comp_id = comp_id_result[0]  # Get the first element of the result tuple
                            else:
                                comp_id = None  # or handle the case when no result is found


                            sub_name = subcomponent[0]
                            description = subcomponent[1]


                            cursor.execute(insert_sql, (sub_name, description, comp_id))

                        # , sub_name, comp_id
                        # "WHERE NOT EXISTS (
                        #                         SELECT 1 FROM asset_subcomponent WHERE name = %s AND asset_component_id = %s
                        #                     )"

                        for subcomponent in subcomponents_cable:
                            # search component id
                            search_sql = '''SELECT id FROM asset_component WHERE name = %s AND asset_category_id = %s;'''

                            comp_name = subcomponent[2]
                            asset_category_id = 4

                            cursor.execute(search_sql, (comp_name, asset_category_id))
                            comp_id_result = cursor.fetchone()

                            # Check if a result was returned
                            if comp_id_result:
                                comp_id = comp_id_result[0]  # Get the first element of the result tuple
                            else:
                                comp_id = None  # or handle the case when no result is found

                            sub_name = subcomponent[0]
                            description = subcomponent[1]


                            cursor.execute(insert_sql, (sub_name, description, comp_id))


                        for subcomponent in subcomponents_switchgear:
                            # search component id
                            search_sql = '''SELECT id FROM asset_component WHERE name = %s AND asset_category_id = %s;'''

                            comp_name = subcomponent[2]
                            asset_category_id = 3

                            cursor.execute(search_sql, (comp_name, asset_category_id))
                            comp_id_result = cursor.fetchone()

                            # Check if a result was returned
                            if comp_id_result:
                                comp_id = comp_id_result[0]  # Get the first element of the result tuple
                            else:
                                comp_id = None  # or handle the case when no result is found

                            sub_name = subcomponent[0]
                            description = subcomponent[1]



                            cursor.execute(insert_sql, (sub_name, description, comp_id))


                        for subcomponent in subcomponents_transformer:
                            # search component id
                            search_sql = '''SELECT id FROM asset_component WHERE name = %s AND asset_category_id = %s;'''

                            comp_name = subcomponent[2]
                            asset_category_id = 2

                            cursor.execute(search_sql, (comp_name, asset_category_id))
                            comp_id_result = cursor.fetchone()

                            # Check if a result was returned
                            if comp_id_result:
                                comp_id = comp_id_result[0]  # Get the first element of the result tuple
                            else:
                                comp_id = None  # or handle the case when no result is found

                            sub_name = subcomponent[0]
                            description = subcomponent[1]



                            cursor.execute(insert_sql, (sub_name, description, comp_id))


                    # Commit the transaction
                    conn.commit()
                    print("Subcomponents inserted or already exist")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")

                # print("Subcomponents inserted or already exist")
            def insert_diagnostic_test():
                # Insert data
                diagnostic_test_rotating_machine = [
                    ('Insulation Resistance', 'Offline', 1),
                    ('Polarization Index', 'Offline', 1),
                    ('Winding Resistance', 'Offline', 1),
                    ('Dissipation Factor', 'Offline', 1),
                    ('Partial Discharge - Offline', 'Offline', 1),
                    ('Inspection', 'Offline', 1),
                    ('Core Flux', 'Offline', 1),
                    ('Elcid', 'Offline', 1),
                    ('Bump Test', 'Offline', 1),
                    ('Rotor Flux', 'Offline', 1),
                    ('Partial Discharge - Online', 'Online', 1),
                    ('Endwinding Vibration', 'Online', 1),
                    ('Vibration analysis', 'Online', 1),
                ]

                diagnostic_test_cables = [
                    ('Oversheath test', 'Offline', 4),
                    ('Insulation Resistance', 'Offline', 4),
                    ('Polarization Index', 'Offline', 4),
                    ('Offline VLF Tan Delta', 'Offline', 4),
                    ('Offline VLF Partial Discharge', 'Offline', 4),
                    ('Inspection', 'Offline', 4),
                    ('Partial Discharge - Online', 'Online', 4),
                    ('Distributed Temperature', 'Online', 4),
                    ('Thermal Imaging', 'Online', 4),
                ]

                diagnostic_test_switchgears = [
                    ('Insulation Resistance', 'Offline', 3),
                    ('Polarization Index', 'Offline', 3),
                    ('Offline Partial Discharge', 'Offline', 3),
                    ('Inspection sw', 'Offline', 3),
                    ('Relay testing', 'Offline', 3),
                    ('Circuit Breaker testing', 'Offline', 3),
                    ('Instrument transformers testing', 'Offline', 3),
                    ('Partial Discharge - Online', 'Online', 3),
                    ('Thermal Imaging', 'Online', 3),
                ]

                diagnostic_test_transformers = [
                    ('Insulation Resistance', 'Offline', 2),
                    ('Polarization Index', 'Offline', 2),
                    ('Winding Resistance', 'Offline', 2),
                    ('Sweep Frequency Response Analysis', 'Offline', 2),
                    ('Transformer Turns Ratio', 'Offline', 2),
                    ('Dissipation Factor', 'Offline', 2),
                    ('Offline Partial Discharge', 'Offline', 2),
                    ('Inspection tx', 'Offline', 2),
                    ('Oil Dissolved Gas Analysis', 'Online', 2),
                    ('Partial Discharge - Online', 'Online', 2),
                    ('Dissipation Factor', 'Online', 2),
                ]

                insert_sql = '''
                INSERT INTO diagnostic_test (name, `asset_condition`, asset_category_id)
                SELECT %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM diagnostic_test WHERE name = %s AND asset_category_id = %s
                );
                '''

                try:
                    with conn.cursor() as cursor:
                        # Insert each diagnostic test into the table if it doesn't already exist
                        for test in diagnostic_test_rotating_machine:
                            cursor.execute(insert_sql, (test[0], test[1], test[2], test[0], test[2]))
                        for test in diagnostic_test_cables:
                            cursor.execute(insert_sql, (test[0], test[1], test[2], test[0], test[2]))
                        for test in diagnostic_test_switchgears:
                            cursor.execute(insert_sql, (test[0], test[1], test[2], test[0], test[2]))
                        for test in diagnostic_test_transformers:
                            cursor.execute(insert_sql, (test[0], test[1], test[2], test[0], test[2]))

                    # Commit the transaction
                    conn.commit()
                    print("Diagnostic tests inserted or already exist")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                # print("Diagnostic tests inserted or already exist")
            def insert_criticality():
                # Path to the Excel file
                excel_file = 'C:/Users/inwave/Desktop/InWave_EHV_RMHI/assets/criticality_list_TB422.xlsx'
                excel_file_path = os.path.abspath(excel_file)

                # Read the Excel file
                df = pd.read_excel(excel_file_path, sheet_name='Criticality')
                with conn.cursor() as cursor:

                    cursor.execute("SELECT * FROM criticality_list")
                    criticality_list_result = cursor.fetchall()

                    if not criticality_list_result:
                        # SQL statement to insert data into the table if it doesn't already exist
                        insert_sql = '''
                        INSERT INTO criticality_list (class, safety, financial, reliability, environmental)
                        SELECT %s, %s, %s, %s, %s
                        WHERE NOT EXISTS (
                            SELECT 1 FROM criticality_list WHERE class = %s
                        );
                        '''

                        try:
                            with conn.cursor() as cursor:
                                # Iterate through rows of the DataFrame and insert into MySQL table
                                for index, row in df.iterrows():
                                    values = (
                                        row['Class'],  # Ensure these match your actual column names
                                        row['Safety'],
                                        row['Financial'],
                                        row['Reliability'],
                                        row['Environmental'],
                                        row['Class']  # Used in the WHERE NOT EXISTS clause for the check
                                    )
                                    cursor.execute(insert_sql, values)

                            # Commit the transaction
                            conn.commit()
                            print("Criticality list data inserted into the table.")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
            def insert_failure_mechanisms():
                # Insert data
                failure_mechanisms_rotating_machine = [
                    ('Rotor Pole Damage', 'Imbalance, increased vibration'),
                    ('Stator Winding Insulation deterioration', 'Electrical breakdown, overheating'),
                    ('Bearing Failure', 'Increased vibration, noise'),
                    ('Brush Wear', 'Sparking, poor commutation'),
                    ('Rotor Shaft Misalignment', 'Increased vibration, bearing wear'),
                    ('Cooling System Failure', 'Overheating, reduced cooling efficiency'),
                    ('Oil Contamination', 'Deterioration of lubricating properties'),
                    ('Overload winding', 'Overheating, insulation breakdown'),
                    ('Grounding Issues', 'Potential for electrical shocks'),
                    ('Commutator Issues', 'Poor contact, sparking'),
                    ('Thermal Cycling Fatigue', 'Thermal stresses, material fatigue'),
                    ('Erosion and Corrosion', 'Surface degradation, reduced lifespan'),
                    ('Resonance and Vibration', 'Structural damage, increased wear'),
                    ('Environmental Deterioration', 'Thermal stress, material degradation'),
                    ('Phase Imbalance', 'Overheating, electrical stress'),
                    ('Winding Contamination', 'Decrease insulation resistance, reduce cooling')
                ]


                failure_mechanisms_cables = [
                    ('Contamination - Termination', 'Increase of leakage current'),
                    ('Moisture ingress', 'Increase of dielectric losses, decrease of dielectric proprieties'),
                    ('Dielectric localized aging - Partial Discharge', 'Localised aging of the insulation system'),
                    ('Dielectric localized contamination - Water Tree', 'Localised increase of dielectric losses'),
                    ('Dielectric localized aging - Thermal stress', 'Localised aging of the insulation system'),
                    ('Dielectric distributed aging', 'Increase of dielectric losses, reduce of dielectric proprieties'),
                    ('Mechanical stress', 'Increase of mechanical stress'),
                    ('Mechanical damage', 'Increase of mechanical stress'),
                    ('Chemical degradation', 'Increase of leakage current, decrease of dielectric proprieties'),
                    ('Sparking', 'Floating potential'),

                ]

                failure_mechanisms_switchgears = [
                    ('Contamination', 'Increase of leakage current, reduce cooling'),
                    ('Gas leakage', 'Decrease of dielectric proprieties'),
                    ('Moisture ingress', 'Increase of dielectric losses, decrease of dielectric proprieties'),
                    ('Sparking', 'Localised wear of electrical contacts, increase of thermal stress'),
                    ('Arcing', 'Localised damage of electrical contact, increase of thermal stress'),
                    ('Dielectric localized aging - Partial Discharge', 'Localised aging of the insulation system'),
                    ('Dielectric localized aging - Thermal stress', 'Localised aging of the insulation system'),
                    ('Chemical degradation', 'Increase of leakage current, decrease of dielectric proprieties'),
                    ('Mechanical damage', 'Increase of mechanical stress'),

                ]


                failure_mechanisms_transformers = [
                    ('Insulation Deterioration', 'Increase of dielectric losses, decrease of dielectric proprieties'),
                    ('Dielectric localized aging - Partial Discharge', 'Localised aging of the insulation system'),
                    ('Winding deformation', 'Mechanical movement or deformation of windings, core displacement, or shorted turns.'),
                    ('Core damage', 'Core insulation breakdown, core movement, or shorted laminations.'),
                    ('Dielectric localized aging - Thermal stress', 'Localised aging of the insulation system'),
                    ('Dielectric distributed aging - Thermal againg', 'Increase of dielectric losses, decrease of dielectric proprieties'),
                    ('Sparking', 'Localised wear of electrical contacts, increase of thermal stress'),
                    ('Arcing', 'Localised damage of electrical contact, increase of thermal stress'),
                    ('Chemical degradation', 'Increase of leakage current, decrease of dielectric proprieties'),
                    ('Contamination', 'Increase of dielectric losses, decrease of dielectric proprieties'),
                    ('Mechanical stress', 'Increase of mechanical stress'),
                    ('Mechanical damage', 'Increase of mechanical stress'),

                ]


                #                 ]

                insert_sql = '''
                    INSERT INTO failure_mechanisms (name, local_effect, asset_category_id)
                    SELECT %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM failure_mechanisms WHERE name = %s AND asset_category_id = %s
                    );
                '''

                try:
                    with conn.cursor() as cursor:

                        # Insert each diagnostic test into the table if it doesn't already exist
                        for mechanism in failure_mechanisms_rotating_machine:
                            name = mechanism[0]
                            loca_effect = mechanism[1]
                            asset_category_id = 1
                            cursor.execute(insert_sql, (name, loca_effect,asset_category_id, name,asset_category_id))

                        for mechanism in failure_mechanisms_cables:
                            name = mechanism[0]
                            loca_effect = mechanism[1]
                            asset_category_id = 4
                            cursor.execute(insert_sql, (name, loca_effect, asset_category_id, name, asset_category_id))

                        for mechanism in failure_mechanisms_switchgears:
                            name = mechanism[0]
                            loca_effect = mechanism[1]
                            asset_category_id = 3
                            cursor.execute(insert_sql, (name, loca_effect, asset_category_id, name, asset_category_id))

                        for mechanism in failure_mechanisms_transformers:
                            name = mechanism[0]
                            loca_effect = mechanism[1]
                            asset_category_id = 2
                            cursor.execute(insert_sql, (name, loca_effect, asset_category_id, name, asset_category_id))

                    # Commit the transaction
                    conn.commit()
                    print("Failure mechanisms inserted or already exist")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
            def insert_failure_mechanisms_subcomponent_table():
                # Insert data
                failure_mechanisms_rotating_machine = [
                    ('Rotor Pole Damage', 'Imbalance, increased vibration', [7]),
                    ('Stator Winding Insulation deterioration', 'Electrical breakdown, overheating', [2]),
                    ('Bearing Failure', 'Increased vibration, noise', [8, 9]),
                    ('Brush Wear', 'Sparking, poor commutation', [8, 9]),
                    ('Rotor Shaft Misalignment', 'Increased vibration, bearing wear', [4]),
                    ('Cooling System Failure', 'Overheating, reduced cooling efficiency', [12]),
                    ('Oil Contamination', 'Deterioration of lubricating properties', [2, 5]),
                    ('Overload winding', 'Overheating, insulation breakdown', [2, 5]),
                    ('Grounding Issues', 'Potential for electrical shocks', [10]),
                    ('Commutator Issues', 'Poor contact, sparking', [13]),
                    ('Thermal Cycling Fatigue', 'Thermal stresses, material fatigue', [2, 5]),
                    ('Erosion and Corrosion', 'Surface degradation, reduced lifespan', [2, 3, 7, 10, 11, 5, 6]),
                    ('Resonance and Vibration', 'Structural damage, increased wear', [2]),
                    ('Environmental Deterioration', 'Thermal stress, material degradation', [12]),
                    ('Phase Imbalance', 'Overheating, electrical stress', [2]),
                    ('Winding Contamination', 'Decrease insulation resistance, reduce cooling', [2, 5])
                ]

                failure_mechanisms_cables = [
                    ('Contamination - Termination', 'Increase of leakage current', [13]),
                    ('Moisture ingress', 'Increase of dielectric losses, decrease of dielectric proprieties',
                     [13, 17, 18, 19]),
                    ('Dielectric localized aging - Partial Discharge', 'Localised aging of the insulation system',
                     [13, 17, 19]),
                    (
                    'Dielectric localized contamination - Water Tree', 'Localised increase of dielectric losses', [17]),
                    ('Dielectric localized aging - Thermal stress', 'Localised aging of the insulation system',
                     [13, 17, 19]),
                    ('Dielectric distributed aging', 'Increase of dielectric losses, reduce of dielectric proprieties',
                     [17]),
                    ('Mechanical stress', 'Increase of mechanical stress', [13, 19]),
                    ('Mechanical damage', 'Increase of mechanical stress', [13, 14, 17, 18, 19, 20]),
                    ('Chemical degradation', 'Increase of leakage current, decrease of dielectric proprieties',
                     [13, 16, 19, 22]),
                    ('Sparking', 'Floating potential', [12, 14, 15, 20, 21]),

                ]

                failure_mechanisms_switchgears = [
                    ('Contamination', 'Increase of leakage current, reduce cooling', [23, 25, 26, 27, 28, 29, 30, 31]),
                    ('Gas leakage', 'Decrease of dielectric proprieties', [23, 27, 30]),
                    ('Moisture ingress', 'Increase of dielectric losses, decrease of dielectric proprieties',
                     [23, 25, 26, 27, 28, 29, 30, 31]),
                    ('Sparking', 'Localised wear of electrical contacts, increase of thermal stress', [23, 25, 30]),
                    ('Arcing', 'Localised damage of electrical contact, increase of thermal stress', [23, 27, 30]),
                    ('Dielectric localized aging - Partial Discharge', 'Localised aging of the insulation system',
                     [23, 24, 26, 29, 30, 31]),
                    ('Dielectric localized aging - Thermal stress', 'Localised aging of the insulation system',
                     [23, 25, 26, 29, 30, 31]),
                    ('Chemical degradation', 'Increase of leakage current, decrease of dielectric proprieties',
                     [23, 25, 26, 29, 30, 31]),
                    ('Mechanical damage', 'Increase of mechanical stress', [23, 27, 30]),

                ]

                failure_mechanisms_transformers = [
                    ('Insulation Deterioration', 'Increase of dielectric losses, decrease of dielectric proprieties',
                     [32, 35, 36, 37, 38, 39, 40, 48]),
                    ('Dielectric localized aging - Partial Discharge', 'Localised aging of the insulation system',
                     [35, 36, 37, 38, 39, 40, 42, 42, 44, 48]),
                    ('Winding deformation',
                     'Mechanical movement or deformation of windings, core displacement, or shorted turns.',
                     [38, 39, 40]),
                    ('Core damage', 'Core insulation breakdown, core movement, or shorted laminations.', [32]),
                    ('Dielectric localized aging - Thermal stress', 'Localised aging of the insulation system',
                     [32, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 47, 48]),
                    ('Dielectric distributed aging - Thermal againg',
                     'Increase of dielectric losses, decrease of dielectric proprieties',
                     [32, 34, 35, 36, 37, 38, 39, 40, 48]),
                    ('Sparking', 'Localised wear of electrical contacts, increase of thermal stress',
                     [34, 42, 43, 44, 48]),
                    ('Arcing', 'Localised damage of electrical contact, increase of thermal stress',
                     [34, 42, 43, 44, 48]),
                    ('Chemical degradation', 'Increase of leakage current, decrease of dielectric proprieties',
                     [35, 36, 37, 38, 39, 40, 48]),
                    ('Contamination', 'Increase of dielectric losses, decrease of dielectric proprieties',
                     [35, 36, 37, 38, 39, 40, 48]),
                    ('Mechanical stress', 'Increase of mechanical stress',
                     [32, 33, 34, 35, 36, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47]),
                    ('Mechanical damage', 'Increase of mechanical stress', [35, 36, 37, 41, 42, 43, 44, 45, 47]),

                ]

                insert_sql = '''
                                    INSERT INTO failure_mechanisms_subcomponent_table (failure_mechanism_id, asset_subcomponent_id)
                                    SELECT %s, %s
                                    ;
                                '''

                try:
                    with conn.cursor() as cursor:

                        # Insert each diagnostic test into the table if it doesn't already exist
                        for mechanism in failure_mechanisms_rotating_machine:
                            # query to select the id of the failure mechanism
                            search_query = '''
                                SELECT id FROM failure_mechanisms WHERE name = %s AND asset_category_id = %s;
                            '''

                            name = mechanism[0]
                            asset_category_id = 1

                            cursor.execute(search_query, (name, asset_category_id))
                            fm_id_result = cursor.fetchone()

                            # Check if a result was returned
                            if fm_id_result:
                                fm_id = fm_id_result[0]  # Get the first element of the result tuple
                            else:
                                fm_id = None  # or handle the case when no result is found

                            subcomponent_ids = mechanism[2]


                            # Loop through each asset_category_id in the list and insert
                            for subcomponent in subcomponent_ids:
                                cursor.execute(insert_sql, (fm_id,subcomponent))


                        for mechanism in failure_mechanisms_cables:
                            # query to select the id of the failure mechanism
                            search_query = '''
                                SELECT id FROM failure_mechanisms WHERE name = %s AND asset_category_id = %s;
                            '''

                            name = mechanism[0]
                            asset_category_id = 4

                            cursor.execute(search_query, (name, asset_category_id))
                            fm_id_result = cursor.fetchone()

                            # Check if a result was returned
                            if fm_id_result:
                                fm_id = fm_id_result[0]  # Get the first element of the result tuple
                            else:
                                fm_id = None  # or handle the case when no result is found

                            subcomponent_ids = mechanism[2]


                            # Loop through each asset_category_id in the list and insert
                            for subcomponent in subcomponent_ids:
                                cursor.execute(insert_sql, (fm_id,subcomponent))


                        for mechanism in failure_mechanisms_switchgears:
                            # query to select the id of the failure mechanism
                            search_query = '''
                                SELECT id FROM failure_mechanisms WHERE name = %s AND asset_category_id = %s;
                            '''

                            name = mechanism[0]
                            asset_category_id = 3

                            cursor.execute(search_query, (name, asset_category_id))
                            fm_id_result = cursor.fetchone()

                            # Check if a result was returned
                            if fm_id_result:
                                fm_id = fm_id_result[0]  # Get the first element of the result tuple
                            else:
                                fm_id = None  # or handle the case when no result is found

                            subcomponent_ids = mechanism[2]


                            # Loop through each asset_category_id in the list and insert
                            for subcomponent in subcomponent_ids:
                                cursor.execute(insert_sql, (fm_id,subcomponent))


                        for mechanism in failure_mechanisms_transformers:
                            # query to select the id of the failure mechanism
                            search_query = '''
                                SELECT id FROM failure_mechanisms WHERE name = %s AND asset_category_id = %s;
                            '''

                            name = mechanism[0]
                            asset_category_id = 2

                            cursor.execute(search_query, (name, asset_category_id))
                            fm_id_result = cursor.fetchone()

                            # Check if a result was returned
                            if fm_id_result:
                                fm_id = fm_id_result[0]  # Get the first element of the result tuple
                            else:
                                fm_id = None  # or handle the case when no result is found

                            subcomponent_ids = mechanism[2]


                            # Loop through each asset_category_id in the list and insert
                            for subcomponent in subcomponent_ids:
                                cursor.execute(insert_sql, (fm_id,subcomponent))


                    # Commit the transaction
                    conn.commit()
                    print("Failure mechanisms inserted or already exist")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
            def insert_fmdi_table():

                # Path to the Excel file
                excel_file = '/home/pi/Desktop/InWave_HI-main/database/fmdi_table.xlsx'
                excel_file_path = os.path.abspath(excel_file)

                # Read the Excel file - rm
                df = pd.read_excel(excel_file_path, sheet_name='fmdi_rm')
                # Replace NaN values with 'N/A'
                df = df.astype(object)
                df.fillna('N/A', inplace=True)

                df_cable = pd.read_excel(excel_file_path, sheet_name='fmdi_cable')
                # Replace NaN values with 'N/A'
                df_cable = df_cable.astype(object)
                df_cable.fillna('N/A', inplace=True)

                df_sw = pd.read_excel(excel_file_path, sheet_name='fmdi_sw')
                # Replace NaN values with 'N/A'
                df_sw = df_sw.astype(object)
                df_sw.fillna('N/A', inplace=True)

                df_tx = pd.read_excel(excel_file_path, sheet_name='fmdi_tx')
                # Replace NaN values with 'N/A'
                df_tx = df_tx.astype(object)
                df_tx.fillna('N/A', inplace=True)

                # print(df_tx['feature_1'])


                with conn.cursor() as cursor:

                    cursor.execute("SELECT * FROM fmdi_factors")
                    fmdi_factor_result = cursor.fetchall()

                    if len(fmdi_factor_result)==0:
                        # SQL statement to insert data into the table if it doesn't already exist
                        insert_sql = '''
                            INSERT INTO fmdi_factors (
                                feature_1, feature_2, feature_3, feature_4, feature_5, 
                                feature_6, feature_7, feature_8, feature_9, feature_10, 
                                feature_11, feature_12, feature_13, feature_14, feature_15, 
                                failure_mechanism_id, diagnostic_test_id, value
                            )
                            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                   %s, %s, %s, %s, %s, %s, %s, %s
                            WHERE NOT EXISTS (
                                SELECT 1 FROM fmdi_factors 
                                WHERE feature_1 = %s 
                                AND feature_2 = %s 
                                AND feature_3 = %s 
                                AND feature_4 = %s 
                                AND feature_5 = %s 
                                AND feature_6 = %s 
                                AND feature_7 = %s 
                                AND feature_8 = %s 
                                AND feature_9 = %s 
                                AND feature_10 = %s 
                                AND feature_11 = %s 
                                AND feature_12 = %s 
                                AND feature_13 = %s 
                                AND feature_14 = %s 
                                AND feature_15 = %s 
                                AND failure_mechanism_id = %s 
                                AND diagnostic_test_id = %s
                            );
                        '''

                        #encrypt the data
                        # Use the same key every time for encryption and decryption
                          # Replace with your securely stored key

                        # key = Fernet.generate_key()
                        #
                        # finalkey = key.decode()

                        key = b'P__s6c4fKKKmBfxRz0TVzpyVUuKnDKwYvcFb908jD1Y='


                        cipher = Fernet(key)

                        # Function to encrypt a single value
                        def encrypt_value(plaintext: str) -> str:
                            if isinstance(plaintext, float) or isinstance(plaintext, int):
                                plaintext = str(plaintext)  # Ensure it's a string
                            encrypted = cipher.encrypt(plaintext.encode())
                            return encrypted.decode()  # Decode to make it suitable for database storage

                        try:
                            with conn.cursor() as cursor:
                                # Iterate through rows of the DataFrame and insert into MySQL table
                                #rotating machines
                                for index, row in df.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    fm_id = row['failure_mechanism_id']  # Encrypting IDs too
                                    diagnostic_test_id = row['diagnostic_test_id']
                                    encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        fm_id,  # Encrypted failure mechanism ID
                                        diagnostic_test_id,  # Encrypted diagnostic test ID
                                        encrypted_value,  # Encrypted value field
                                        *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        fm_id,  # Encrypted failure mechanism ID for WHERE clause
                                        diagnostic_test_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)
                                    # print('Rotating Machines parameters inserted')

                                #cable

                                for index, row in df_cable.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    fm_id = row['failure_mechanism_id']  # Encrypting IDs too
                                    diagnostic_test_id = row['diagnostic_test_id']
                                    encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        fm_id,  # Encrypted failure mechanism ID
                                        diagnostic_test_id,  # Encrypted diagnostic test ID
                                        encrypted_value,  # Encrypted value field
                                        *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        fm_id,  # Encrypted failure mechanism ID for WHERE clause
                                        diagnostic_test_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)


                                #switchgear
                                for index, row in df_sw.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    fm_id = row['failure_mechanism_id']  # Encrypting IDs too
                                    diagnostic_test_id = row['diagnostic_test_id']
                                    encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        fm_id,  # Encrypted failure mechanism ID
                                        diagnostic_test_id,  # Encrypted diagnostic test ID
                                        encrypted_value,  # Encrypted value field
                                        *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        fm_id,  # Encrypted failure mechanism ID for WHERE clause
                                        diagnostic_test_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)

                                #transformer

                                for index, row in df_tx.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    fm_id = row['failure_mechanism_id']  # Encrypting IDs too
                                    diagnostic_test_id = row['diagnostic_test_id']
                                    encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        fm_id,  # Encrypted failure mechanism ID
                                        diagnostic_test_id,  # Encrypted diagnostic test ID
                                        encrypted_value,  # Encrypted value field
                                        *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        fm_id,  # Encrypted failure mechanism ID for WHERE clause
                                        diagnostic_test_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)




                            # print(i)
                            # print('lengh tx',i)


                            # Commit the transaction
                            conn.commit()
                            print("fmdi list data inserted into the table.")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
            def insert_scfm_table():

                # Path to the Excel file
                excel_file = '/home/pi/Desktop/InWave_HI-main/database/scfm_table.xlsx'
                excel_file_path = os.path.abspath(excel_file)

                # Read the Excel file - rm
                df = pd.read_excel(excel_file_path, sheet_name='scfm_rm')
                # Replace NaN values with 'N/A'
                df = df.astype(object)
                df.fillna('N/A', inplace=True)

                df_cable = pd.read_excel(excel_file_path, sheet_name='scfm_cable')
                # Replace NaN values with 'N/A'
                df_cable = df_cable.astype(object)
                df_cable.fillna('N/A', inplace=True)

                df_sw = pd.read_excel(excel_file_path, sheet_name='scfm_sw')
                # Replace NaN values with 'N/A'
                df_sw = df_sw.astype(object)
                df_sw.fillna('N/A', inplace=True)

                df_tx = pd.read_excel(excel_file_path, sheet_name='scfm_tx')
                # Replace NaN values with 'N/A'
                df_tx = df_tx.astype(object)
                df_tx.fillna('N/A', inplace=True)

                # print(df_cable)



                with conn.cursor() as cursor:


                    cursor.execute("SELECT * FROM scfm_factors")
                    scfm_factor_result = cursor.fetchall()



                    if len(scfm_factor_result)==0:

                        # SQL statement to insert data into the table if it doesn't already exist
                        insert_sql = '''
                            INSERT INTO scfm_factors (
                                feature_1, feature_2, feature_3, feature_4, feature_5, 
                                feature_6, feature_7, feature_8, feature_9, feature_10, 
                                feature_11, feature_12, feature_13, feature_14, feature_15, 
                                subcomponent_id, failure_mechanism_id, value
                            )
                            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                   %s, %s, %s, %s, %s, %s, %s, %s
                            ;
                        '''

                        #encrypt the data
                        # Use the same key every time for encryption and decryption
                          # Replace with your securely stored key

                        # key = Fernet.generate_key()
                        #
                        # finalkey = key.decode()

                        key = b'P__s6c4fKKKmBfxRz0TVzpyVUuKnDKwYvcFb908jD1Y='


                        cipher = Fernet(key)

                        # Function to encrypt a single value
                        def encrypt_value(plaintext: str) -> str:
                            if isinstance(plaintext, float) or isinstance(plaintext, int):
                                plaintext = str(plaintext)  # Ensure it's a string
                            encrypted = cipher.encrypt(plaintext.encode())
                            return encrypted.decode()  # Decode to make it suitable for database storage

                        try:
                            with conn.cursor() as cursor:
                                # Iterate through rows of the DataFrame and insert into MySQL table
                                #rotating machines
                                i=0
                                for index, row in df.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too
                                    fm_id = row['failure_mechanism_id']
                                    encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        sc_id,  # Encrypted failure mechanism ID
                                        fm_id,  # Encrypted diagnostic test ID
                                        encrypted_value,  # Encrypted value field
                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)
                                    i+=1
                                # print('Rotating Machines parameters inserted')

                                #cable
                                j=0
                                for index, row in df_cable.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    #Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too
                                    fm_id = row['failure_mechanism_id']
                                    encrypted_value = encrypt_value(str(row['value']))  # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        sc_id,  # Encrypted failure mechanism ID
                                        fm_id,  # Encrypted diagnostic test ID
                                        encrypted_value,  # Encrypted value field
                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)
                                    j+=1


                                #switchgear
                                y=0
                                for index, row in df_sw.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too
                                    fm_id = row['failure_mechanism_id']
                                    encrypted_value = encrypt_value(str(row['value']))  # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        sc_id,  # Encrypted failure mechanism ID
                                        fm_id,  # Encrypted diagnostic test ID
                                        encrypted_value,  # Encrypted value field
                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )
                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)
                                    y+=1

                                #transformer
                                k=0
                                for index, row in df_tx.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too
                                    fm_id = row['failure_mechanism_id']
                                    encrypted_value = encrypt_value(str(row['value']))  # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        sc_id,  # Encrypted failure mechanism ID
                                        fm_id,  # Encrypted diagnostic test ID
                                        encrypted_value,  # Encrypted value field
                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)
                                    k+=1



                            # print(i)
                            print('lengh rm',i)
                            print('lenght cable', y)
                            print('lenght sw', y)
                            print('lenght tx',k)


                            # Commit the transaction
                            conn.commit()
                            print("scfm list data inserted into the table.")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
            def insert_schi_table():

                # Path to the Excel file
                excel_file = '/home/pi/Desktop/InWave_HI-main/database/schi_table.xlsx'
                excel_file_path = os.path.abspath(excel_file)

                # Read the Excel file - rm
                df = pd.read_excel(excel_file_path, sheet_name='schi_rm')
                # Replace NaN values with 'N/A'
                df = df.astype(object)
                df.fillna('N/A', inplace=True)

                df_cable = pd.read_excel(excel_file_path, sheet_name='schi_cable')
                # Replace NaN values with 'N/A'
                df_cable = df_cable.astype(object)
                df_cable.fillna('N/A', inplace=True)

                df_sw = pd.read_excel(excel_file_path, sheet_name='schi_sw')
                # Replace NaN values with 'N/A'
                df_sw = df_sw.astype(object)
                df_sw.fillna('N/A', inplace=True)

                df_tx = pd.read_excel(excel_file_path, sheet_name='schi_tx')
                # Replace NaN values with 'N/A'
                df_tx = df_tx.astype(object)
                df_tx.fillna('N/A', inplace=True)

                # print(df_cable)
                #
                # # print(fuck)



                with conn.cursor() as cursor:


                    cursor.execute("SELECT * FROM schi_factors")
                    schi_factor_result = cursor.fetchall()



                    if len(schi_factor_result)==0:

                        # SQL statement to insert data into the table if it doesn't already exist
                        insert_sql = '''
                            INSERT INTO schi_factors (
                                feature_1, feature_2, feature_3, feature_4, feature_5, 
                                feature_6, feature_7, feature_8, feature_9, feature_10, 
                                feature_11, feature_12, feature_13, feature_14, feature_15, 
                                subcomponent_id, age_factor, age_weight, maintenance_weight, failure_weight,diagnostic_weight
                            )
                            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                   %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                   %s
                            ;
                        '''

                        #encrypt the data
                        # Use the same key every time for encryption and decryption
                          # Replace with your securely stored key

                        # key = Fernet.generate_key()
                        #
                        # finalkey = key.decode()

                        key = b'P__s6c4fKKKmBfxRz0TVzpyVUuKnDKwYvcFb908jD1Y='


                        cipher = Fernet(key)

                        # Function to encrypt a single value
                        def encrypt_value(plaintext: str) -> str:
                            if isinstance(plaintext, float) or isinstance(plaintext, int):
                                plaintext = str(plaintext)  # Ensure it's a string
                            encrypted = cipher.encrypt(plaintext.encode())
                            return encrypted.decode()  # Decode to make it suitable for database storage

                        try:
                            with conn.cursor() as cursor:
                                # Iterate through rows of the DataFrame and insert into MySQL table
                                #rotating machines
                                i=0
                                for index, row in df.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too
                                    age_factor = row['age_factor']
                                    age_weight = row['age_weight']
                                    maintenance_weight = row['maintenance_weight']
                                    failure_weight = row['failure_weight']
                                    diagnostic_weight = row['diagnostic_weight']
                                    # encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        sc_id,  # Encrypted failure mechanism ID
                                        age_factor,  # Encrypted diagnostic test ID
                                        age_weight,  # Encrypted value field
                                        maintenance_weight,
                                        failure_weight,
                                        diagnostic_weight

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)
                                    i+=1
                                # print('Rotating Machines parameters inserted')

                                #cable
                                l=0
                                for index, row in df_cable.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too
                                    age_factor = row['age_factor']
                                    age_weight = row['age_weight']
                                    maintenance_weight = row['maintenance_weight']
                                    failure_weight = row['failure_weight']
                                    diagnostic_weight = row['diagnostic_weight']
                                    # encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        sc_id,  # Encrypted failure mechanism ID
                                        age_factor,  # Encrypted diagnostic test ID
                                        age_weight,  # Encrypted value field
                                        maintenance_weight,
                                        failure_weight,
                                        diagnostic_weight

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)
                                    l+=1


                                #switchgear
                                y=0
                                for index, row in df_sw.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too
                                    age_factor = row['age_factor']
                                    age_weight = row['age_weight']
                                    maintenance_weight = row['maintenance_weight']
                                    failure_weight = row['failure_weight']
                                    diagnostic_weight = row['diagnostic_weight']
                                    # encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        sc_id,  # Encrypted failure mechanism ID
                                        age_factor,  # Encrypted diagnostic test ID
                                        age_weight,  # Encrypted value field
                                        maintenance_weight,
                                        failure_weight,
                                        diagnostic_weight

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )
                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)
                                    y+=1

                                #transformer
                                k=0
                                for index, row in df_tx.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too
                                    age_factor = row['age_factor']
                                    age_weight = row['age_weight']
                                    maintenance_weight = row['maintenance_weight']
                                    failure_weight = row['failure_weight']
                                    diagnostic_weight = row['diagnostic_weight']
                                    # encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        sc_id,  # Encrypted failure mechanism ID
                                        age_factor,  # Encrypted diagnostic test ID
                                        age_weight,  # Encrypted value field
                                        maintenance_weight,
                                        failure_weight,
                                        diagnostic_weight

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )
                                    # Execute the insert query with the encrypted values


                                    cursor.execute(insert_sql, values)
                                    k+=1



                            # print(i)
                            print('lengh rm',i)
                            print('lenght cable', l)
                            print('lenght sw', y)
                            print('lenght tx',k)


                            # Commit the transaction
                            conn.commit()
                            print("scfm list data inserted into the table.")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
            def insert_cmsc_table():
                # Path to the Excel file
                excel_file = '/home/pi/Desktop/InWave_HI-main/database/cmsc_table.xlsx'
                excel_file_path = os.path.abspath(excel_file)

                # Read the Excel file - rm
                df = pd.read_excel(excel_file_path, sheet_name='cmsc_rm')
                # Replace NaN values with 'N/A'
                df = df.astype(object)
                df.fillna('N/A', inplace=True)

                df_cable = pd.read_excel(excel_file_path, sheet_name='cmsc_cable')
                # Replace NaN values with 'N/A'
                df_cable = df_cable.astype(object)
                df_cable.fillna('N/A', inplace=True)

                df_sw = pd.read_excel(excel_file_path, sheet_name='cmsc_sw')
                # Replace NaN values with 'N/A'
                df_sw = df_sw.astype(object)
                df_sw.fillna('N/A', inplace=True)

                df_tx = pd.read_excel(excel_file_path, sheet_name='cmsc_tx')
                # Replace NaN values with 'N/A'
                df_tx = df_tx.astype(object)
                df_tx.fillna('N/A', inplace=True)

                # print(df_cable)
                #
                # print(fuck)

                with conn.cursor() as cursor:

                    cursor.execute("SELECT * FROM cmsc_factors")
                    schi_factor_result = cursor.fetchall()

                    if len(schi_factor_result) == 0:

                        # SQL statement to insert data into the table if it doesn't already exist
                        insert_sql = '''
                                            INSERT INTO cmsc_factors (
                                                feature_1, feature_2, feature_3, feature_4, feature_5, 
                                                feature_6, feature_7, feature_8, feature_9, feature_10, 
                                                feature_11, feature_12, feature_13, feature_14, feature_15, 
                                                component_id, subcomponent_id, value
                                            )
                                            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                                   %s, %s, %s, %s, %s, %s, %s, %s
                                            ;
                                        '''

                        # encrypt the data
                        # Use the same key every time for encryption and decryption
                        # Replace with your securely stored key

                        # key = Fernet.generate_key()
                        #
                        # finalkey = key.decode()

                        key = b'P__s6c4fKKKmBfxRz0TVzpyVUuKnDKwYvcFb908jD1Y='

                        cipher = Fernet(key)

                        # Function to encrypt a single value
                        def encrypt_value(plaintext: str) -> str:
                            if isinstance(plaintext, float) or isinstance(plaintext, int):
                                plaintext = str(plaintext)  # Ensure it's a string
                            encrypted = cipher.encrypt(plaintext.encode())
                            return encrypted.decode()  # Decode to make it suitable for database storage

                        try:
                            with conn.cursor() as cursor:
                                # Iterate through rows of the DataFrame and insert into MySQL table
                                # rotating machines
                                i = 0
                                for index, row in df.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    cm_id = row['component_id']
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too

                                    encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        cm_id,
                                        sc_id,  # Encrypted failure mechanism ID
                                        encrypted_value

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values

                                    cursor.execute(insert_sql, values)
                                    i += 1
                                # print('Rotating Machines parameters inserted')

                                # cable
                                l = 0
                                for index, row in df_cable.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    cm_id = row['component_id']
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too

                                    encrypted_value = encrypt_value(str(row['value']))  # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        cm_id,
                                        sc_id,  # Encrypted failure mechanism ID
                                        encrypted_value

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values

                                    cursor.execute(insert_sql, values)
                                    l += 1

                                # switchgear
                                y = 0
                                for index, row in df_sw.iterrows():
                                    # Encrypt the values before inserting
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    cm_id = row['component_id']
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too

                                    encrypted_value = encrypt_value(str(row['value']))  # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        cm_id,
                                        sc_id,  # Encrypted failure mechanism ID
                                        encrypted_value

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )
                                    # Execute the insert query with the encrypted values

                                    cursor.execute(insert_sql, values)
                                    y += 1

                                # transformer
                                k = 0
                                for index, row in df_tx.iterrows():
                                    # Encrypt the values before inserting
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    cm_id = row['component_id']
                                    sc_id = row['subcomponent_id']  # Encrypting IDs too

                                    encrypted_value = encrypt_value(str(row['value']))  # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        cm_id,
                                        sc_id,  # Encrypted failure mechanism ID
                                        encrypted_value

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )
                                    # Execute the insert query with the encrypted values

                                    cursor.execute(insert_sql, values)
                                    k += 1

                            # print(i)
                            print('lengh rm', i)
                            print('lenght cable', l)
                            print('lenght sw', y)
                            print('lenght tx', k)

                            # Commit the transaction
                            conn.commit()
                            print("scfm list data inserted into the table.")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")
            def insert_ascm_table():
                # Path to the Excel file
                excel_file = '/home/pi/Desktop/InWave_HI-main/database/ascm_table.xlsx'
                excel_file_path = os.path.abspath(excel_file)

                # Read the Excel file - rm
                df = pd.read_excel(excel_file_path, sheet_name='ascm_rm')
                # Replace NaN values with 'N/A'
                df = df.astype(object)
                df.fillna('N/A', inplace=True)

                df_cable = pd.read_excel(excel_file_path, sheet_name='ascm_cable')
                # Replace NaN values with 'N/A'
                df_cable = df_cable.astype(object)
                df_cable.fillna('N/A', inplace=True)

                df_sw = pd.read_excel(excel_file_path, sheet_name='ascm_sw')
                # Replace NaN values with 'N/A'
                df_sw = df_sw.astype(object)
                df_sw.fillna('N/A', inplace=True)

                df_tx = pd.read_excel(excel_file_path, sheet_name='ascm_tx')
                # Replace NaN values with 'N/A'
                df_tx = df_tx.astype(object)
                df_tx.fillna('N/A', inplace=True)

                # print(df_cable)
                #
                # print(fuck)

                with conn.cursor() as cursor:

                    cursor.execute("SELECT * FROM ascm_factors")
                    ascm_factor_result = cursor.fetchall()

                    if len(ascm_factor_result) == 0:

                        # SQL statement to insert data into the table if it doesn't already exist
                        insert_sql = '''
                                            INSERT INTO ascm_factors (
                                                feature_1, feature_2, feature_3, feature_4, feature_5, 
                                                feature_6, feature_7, feature_8, feature_9, feature_10, 
                                                feature_11, feature_12, feature_13, feature_14, feature_15, 
                                                component_id, value
                                            )
                                            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                                   %s, %s, %s, %s, %s, %s, %s
                                            ;
                                        '''

                        # encrypt the data
                        # Use the same key every time for encryption and decryption
                        # Replace with your securely stored key

                        # key = Fernet.generate_key()
                        #
                        # finalkey = key.decode()

                        key = b'P__s6c4fKKKmBfxRz0TVzpyVUuKnDKwYvcFb908jD1Y='

                        cipher = Fernet(key)

                        # Function to encrypt a single value
                        def encrypt_value(plaintext: str) -> str:
                            if isinstance(plaintext, float) or isinstance(plaintext, int):
                                plaintext = str(plaintext)  # Ensure it's a string
                            encrypted = cipher.encrypt(plaintext.encode())
                            return encrypted.decode()  # Decode to make it suitable for database storage

                        try:
                            with conn.cursor() as cursor:
                                # Iterate through rows of the DataFrame and insert into MySQL table
                                # rotating machines
                                i = 0
                                for index, row in df.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    cm_id = row['component_id']


                                    encrypted_value = encrypt_value(str(row['value'])) # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        cm_id,
                                        encrypted_value

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values

                                    cursor.execute(insert_sql, values)
                                    i += 1
                                # print('Rotating Machines parameters inserted')

                                # cable
                                l = 0
                                for index, row in df_cable.iterrows():
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    cm_id = row['component_id']

                                    encrypted_value = encrypt_value(str(row['value']))  # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        cm_id,
                                        encrypted_value

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )

                                    # Execute the insert query with the encrypted values

                                    cursor.execute(insert_sql, values)
                                    l += 1

                                # switchgear
                                y = 0
                                for index, row in df_sw.iterrows():
                                    # Encrypt the values before inserting
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    cm_id = row['component_id']

                                    encrypted_value = encrypt_value(str(row['value']))  # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        cm_id,
                                        encrypted_value

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )
                                    # Execute the insert query with the encrypted values

                                    cursor.execute(insert_sql, values)
                                    y += 1

                                # transformer
                                k = 0
                                for index, row in df_tx.iterrows():
                                    # Encrypt the values before inserting
                                    # Encrypt the values before inserting
                                    encrypted_values = [
                                        encrypt_value(str(row['feature_1'])),
                                        encrypt_value(str(row['feature_2'])),
                                        encrypt_value(str(row['feature_3'])),
                                        encrypt_value(str(row['feature_4'])),
                                        encrypt_value(str(row['feature_5'])),
                                        encrypt_value(str(row['feature_6'])),
                                        encrypt_value(str(row['feature_7'])),
                                        encrypt_value(str(row['feature_8'])),
                                        encrypt_value(str(row['feature_9'])),
                                        encrypt_value(str(row['feature_10'])),
                                        encrypt_value(str(row['feature_11'])),
                                        encrypt_value(str(row['feature_12'])),
                                        encrypt_value(str(row['feature_13'])),
                                        encrypt_value(str(row['feature_14'])),
                                        encrypt_value(str(row['feature_15']))
                                    ]

                                    # Encrypt failure_mechanism_id, diagnostic_test_id, and value
                                    cm_id = row['component_id']

                                    encrypted_value = encrypt_value(str(row['value']))  # Encrypt the `value` field

                                    # Prepare values for the SQL query
                                    values = (
                                        *encrypted_values,  # Encrypted features
                                        cm_id,
                                        encrypted_value

                                        # *encrypted_values,  # Repeat encrypted values for the WHERE NOT EXISTS clause
                                        # sc_id,  # Encrypted failure mechanism ID for WHERE clause
                                        # fm_id  # Encrypted diagnostic test ID for WHERE clause
                                    )
                                    # Execute the insert query with the encrypted values

                                    cursor.execute(insert_sql, values)
                                    k += 1

                            # print(i)
                            print('lengh rm', i)
                            print('lenght cable', l)
                            print('lenght sw', y)
                            print('lenght tx', k)

                            # Commit the transaction
                            conn.commit()
                            print("scfm list data inserted into the table.")
                        except mysql.connector.Error as err:
                            print(f"Error: {err}")





            # insert_asset_categoty()
            # insert_component()
            # insert_subcomponent()
            # insert_diagnostic_test()
            # insert_criticality()
            # insert_failure_mechanisms()

            # insert_failure_mechanisms_subcomponent_table()
            # insert_fmdi_table()
            # # insert_scfm_table()
            # insert_schi_table()
            #insert_cmsc_table()
            # insert_ascm_table()

            print('Settings uploaded')


        #create db
        create_db(cursor)

        upload_settings(cursor)

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()


        print("Table 'Inwave_IHMS' created successfully in Inwave_IHMS.db")

    except mysql.connector.Error as err:

        print(f"Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

#create_centralized_db()