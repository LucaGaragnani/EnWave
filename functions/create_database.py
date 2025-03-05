import sqlite3
import pandas as pd
import os

def create_centralized_db():

    try:

        # Connect to SQLite database (or create it if it doesn't exist)

        # Determine the path of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))


        db_directory = current_directory.replace('functions', 'database')


        # Construct the path to the database file
        database_path = os.path.join(db_directory, 'Inwave_RM.db')


        conn = sqlite3.connect(database_path)

        # conn = sqlite3.connect('/Users/marianasouzaoliveira/Desktop/InWave_EHV_RMHI/database/Inwave_RM.db')

        # Create a cursor object using which we can interact with the database
        cursor = conn.cursor()


        def create_db(cursor):
            def create_company_table():
                # SQL statement to create a table
                create_table_sql = '''
                CREATE TABLE IF NOT EXISTS company (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                );
                '''
                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Company table created")
            def create_site_table():
                # SQL statement to create a table
                create_table_sql = '''
                       CREATE TABLE IF NOT EXISTS site (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           site_name TEXT NOT NULL,
                           lat REAL,
                           lon REAL,
                           customer_id INTEGER NOT NULL,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           category TEXT
                       );
                       '''
                # Execute the SQL statement
                cursor.execute(create_table_sql)


                print("Asset Category table created")
            def create_asset_table():
                # SQL statement to create a table
                create_table_sql = '''
                       CREATE TABLE IF NOT EXISTS asset (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           tag TEXT NOT NULL,
                           function TEXT,
                           manufactorer TEXT,
                           yom INTEGER,
                           yoi INTEGER,
                           rated_voltage REAL,
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
                           lat REAL,
                           lon REAL,
                           asset_category_id INTEGER NOT NULL,
                           site_id INTEGER NOT NULL,
                           FOREIGN KEY (asset_category_id) REFERENCES asset_category(id),
                           FOREIGN KEY (site_id) REFERENCES site(id)
                       );
                       '''
                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset table created")
            def create_asset_details_table():
                # SQL statement to create a table
                create_table_sql = '''
                       CREATE TABLE IF NOT EXISTS asset_details (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           criticality_class INTEGER,
                           date TEXT,
                           asset_id INTEGER NOT NULL,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           description TEXT,
                           asset_category_id INTEGER NOT NULL,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           description TEXT,
                           asset_component_id INTEGER NOT NULL,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           age_factor INTEGER,
                           maintenance_factor INTEGER,
                           failure_factor INTEGER,
                           description TEXT,
                           asset_subcomponent_id INTEGER NOT NULL,
                           asset_id INTEGER NOT NULL,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           failure_cause TEXT,
                           local_effect TEXT,
                           asset_subcomponent_id INTEGER NOT NULL,
                           FOREIGN KEY (asset_subcomponent_id) REFERENCES asset_subcomponent(id)
                       );
                       '''
                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Failure mechanisms table created")
            def create_diagnostic_test_table():
                # SQL statement to create a table
                create_table_sql = '''
                       CREATE TABLE IF NOT EXISTS diagnostic_test (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           condition TEXT,
                           asset_category_id INTEGER NOT NULL,
                           FOREIGN KEY (asset_category_id) REFERENCES asset_category(id)
                       );
                       '''
                # Execute the SQL statement
                cursor.execute(create_table_sql)





                print("Diagnostic test table created")
            def create_online_test_table():
                # SQL statement to create a table
                create_table_sql = '''
                       CREATE TABLE IF NOT EXISTS online_test_data (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           date TEXT NOT NULL,
                           asset_id INTEGER NOT NULL,
                           subcomponent_id INTEGER NOT NULL,
                           diagnostic_test_id INTEGER NOT NULL,
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
                           feature_16 TEXT,
                           feature_17 TEXT,
                           feature_18 TEXT,
                           feature_19 TEXT,
                           feature_20 TEXT,
                           feature_21 TEXT,
                           feature_22 TEXT,
                           feature_23 TEXT,
                           feature_24 TEXT,
                           feature_25 BLOB,
                           analysis INTEGER,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           date TEXT NOT NULL,
                           asset_id INTEGER NOT NULL,
                           subcomponent_id INTEGER NOT NULL,
                           diagnostic_test_id INTEGER NOT NULL,
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
                           feature_16 TEXT,
                           feature_17 TEXT,
                           feature_18 TEXT,
                           feature_19 TEXT,
                           feature_20 TEXT,
                           feature_21 TEXT,
                           feature_22 TEXT,
                           feature_23 TEXT,
                           feature_24 TEXT,
                           feature_25 BLOB,
                           analysis INTEGER,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           date TEXT NOT NULL,
                           asset_id INTEGER NOT NULL,
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
                           feature_16 TEXT,
                           feature_17 TEXT,
                           feature_18 TEXT,
                           feature_19 TEXT,
                           feature_20 TEXT,
                           feature_21 TEXT,
                           feature_22 TEXT,
                           feature_23 TEXT,
                           feature_24 TEXT,
                           feature_25 TEXT,
                           analysis INTEGER,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           class TEXT,
                           safety TEXT,
                           financial TEXT,
                           reliability TEXT,
                           enviromental TEXT
                       );
                       '''
                # Execute the SQL statement
                cursor.execute(create_table_sql)
            def create_asset_analysis_table():

                # SQL statement to create a table
                create_table_sql = '''
                       CREATE TABLE IF NOT EXISTS asset_analysis (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           date TEXT NOT NULL,
                           asset_id INTEGER NOT NULL,
                           risk_index INTEGER,
                           health_index INTEGER,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           asset_analysis_id INTEGER NOT NULL,
                           maintenance_action TEXT,
                           peer_reviewed_date TEXT,
                           peer_reviewed_comment TEXT,
                           peer_review_eng_name TEXT,
                           FOREIGN KEY (asset_analysis_id) REFERENCES asset_analysis(id)
                       );
                       '''
                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Asset maintenance actions table created")
            def create_failure_mechanisms_analysis_table():

                # SQL statement to create a table
                create_table_sql = '''
                       CREATE TABLE IF NOT EXISTS failure_mechanisms_analysis (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           analysis_id INTEGER NOT NULL,
                           failure_mechanism_id INTEGER NOT NULL,
                           value INTEGER,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           analysis_id INTEGER NOT NULL,
                           subcomponent_id INTEGER NOT NULL,
                           value INTEGER,
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           analysis_id INTEGER NOT NULL,
                           component_id INTEGER NOT NULL,
                           value INTEGER,
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
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   function TEXT,
                                   type TEXT,
                                   rotor_type TEXT,
                                   rated_voltage REAL,
                                   failure_mechanism_id INTEGER NOT NULL,
                                   diagnostic_test_id INTEGER NOT NULL,
                                   value INTEGER,
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
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   function TEXT,
                                   type TEXT,
                                   rotor_type TEXT,
                                   rated_voltage REAL,
                                   subcomponent_id INTEGER NOT NULL,
                                   failure_mechanism_id INTEGER NOT NULL,
                                   value INTEGER,
                                   FOREIGN KEY (subcomponent_id) REFERENCES asset_subcomponent(id),
                                   FOREIGN KEY (failure_mechanism_id) REFERENCES failure_mechanisms(id)
                               );
                               '''
                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("Scfm factor table created")
            def create_cmsc_factors_table():
                # SQL statement to create a table
                create_table_sql = '''
                               CREATE TABLE IF NOT EXISTS cmsc_factors (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   function TEXT,
                                   type TEXT,
                                   rotor_type TEXT,
                                   rated_voltage REAL,
                                   component_id INTEGER NOT NULL,
                                   subcomponent_id INTEGER NOT NULL,
                                   value INTEGER,
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
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   function TEXT,
                                   type TEXT,
                                   rotor_type TEXT,
                                   rated_voltage REAL,
                                   asset_category_id INTEGER NOT NULL,
                                   component_id INTEGER NOT NULL,
                                   value INTEGER,
                                   FOREIGN KEY (asset_category_id) REFERENCES asset_category(id),
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
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           email TEXT NOT NULL,
                           password TEXT NOT NULL,
                           role TEXT NOT NULL
                       );
                       '''
                # Execute the SQL statement
                cursor.execute(create_table_sql)

                print("User table created")
            def create_session_data_table():
                # SQL statement to create a table
                create_table_sql = '''
                       CREATE TABLE IF NOT EXISTS session_data (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id INTEGER NOT NULL,
                           datetime TEXT NOT NULL,
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
            create_asset_details_table()
            create_asset_component_table()
            create_asset_subcomponent_table()
            create_asset_subcomponent_details_table()
            create_failure_mechanisms_table()
            create_diagnostic_test_table()
            create_online_test_table()
            create_offline_test_table()
            create_operational_test_table()
            create_criticality_list_table()
            create_asset_analysis_table()
            create_asset_maintenance_action_table()
            create_failure_mechanisms_analysis_table()
            create_subcomponent_analysis_table()
            create_component_analysis_table()
            # create_fmdi_factors_table()
            # create_scfm_factors_table()
            # create_cmsc_factors_table()
            # create_ascm_factors_table()
            create_user_table()
            create_session_data_table()

        def upload_settings(cursor):
            def insert_asset_categoty():
                #insert data
                # Insert values into the table
                categories = ['Rotating Machine', 'Transformer', 'Switchgear', 'Cable']

                # SQL statement to insert a row into the table
                insert_sql = '''
                                INSERT INTO asset_category (category)
                                SELECT ? WHERE NOT EXISTS (SELECT 1 FROM asset_category WHERE category = ?);
                                '''

                for category in categories:
                    # Execute the insert statement with the category value
                    cursor.execute(insert_sql, (category, category))
            def insert_component():
                # Insert data
                components_rotating_machine = [
                    ('Stator', 'Stationary part/s of the machine', 1),
                    ('Rotor', 'Rotating part/s of the machine', 1),
                    ('Auxiliaries', 'Enclosure and its components of the machine', 1),
                ]

                components_cable = [
                    ('Termination',
                     'The termination is the end connection of a power cable that provides a secure interface to other electrical equipment.',
                     4),
                    ('Section', 'Cable section of the system.', 4),
                    ('Joint', 'A joint is a connection point between two sections of power cable.', 4),
                ]

                components_switchgear = [
                    ('Bay/Panel',
                     'Bay/Panel usually contains essential equipment such as circuit breakers, disconnect switches, busbars, current transformers (CTs), voltage transformers (VTs), and protective relays.',
                     3),
                    ('Bus', 'Conducts electricity between different components of the switchgear', 3),
                ]

                components_transformer = [
                    ('Core',
                     'Made of laminated steel or iron, the core provides a pathway for the magnetic flux generated during the transformation of electrical energy.',
                     3),
                    ('Winding',
                     'The coil connected to the voltage source, where electrical energy is transformed into magnetic energy and viceversa.',
                     2),
                    ('Tank/Enclosure', 'The outer shell that houses the core and windings.', 2),
                ]

                # SQL statement to insert data into the table
                insert_sql = '''
                             INSERT INTO asset_component (name, description, asset_category_id)
                             SELECT ?, ?, ?
                             WHERE NOT EXISTS (SELECT 1 FROM asset_component WHERE name = ? LIMIT 1);
                             '''

                # Insert each subcomponent into the table
                for component in components_rotating_machine:
                    # Check if the component already exists
                    cursor.execute("SELECT 1 FROM asset_component WHERE name = ? LIMIT 1", (component[0],))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the component if it does not exist
                        cursor.execute(insert_sql, (*component, component[0]))

                for component in components_cable:
                    # Check if the component already exists
                    cursor.execute("SELECT 1 FROM asset_component WHERE name = ? LIMIT 1", (component[0],))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the component if it does not exist
                        cursor.execute(insert_sql, (*component, component[0]))

                for component in components_switchgear:
                    # Check if the component already exists
                    cursor.execute("SELECT 1 FROM asset_component WHERE name = ? LIMIT 1", (component[0],))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the component if it does not exist
                        cursor.execute(insert_sql, (*component, component[0]))

                for component in components_transformer:
                    # Check if the component already exists
                    cursor.execute("SELECT 1 FROM asset_component WHERE name = ? LIMIT 1", (component[0],))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the component if it does not exist
                        cursor.execute(insert_sql, (*component, component[0]))

            def insert_subcomponent():
                # insert data
                subcomponents_rotating_machine = [
                    ('Core', 'Laminated iron core', 1),
                    ('Winding', 'Stator winding', 1),
                    ('Winding auxiliaries', 'Components to support/connect stator winding', 1),
                    ('Shaft', 'Mechanical rotating part', 2),
                    ('Winding', 'Rotor winding', 2),
                    ('Winding auxiliaries', 'Component to support/connect rotor winding', 2),
                    ('Bearing DE', 'Bearing on Driven End', 2),
                    ('Bearing NDE', 'Bearing on Non Drive End', 2),
                    ('Enclosure', 'Enclosure of the machine', 3),
                    ('Terminal box', 'Terminal box for connection to system', 3),
                    ('Cooling system', 'Machine cooling system', 3),
                ]

                subcomponents_cable = [
                    ('HV Connector', 'Conductor connector.', 4),
                    ('Main termination', 'Main part of the termination.', 4),
                    ('Ground lead Termination', 'Connection between cable screen and ground.', 4),
                    ('Link box Termination', 'Ground connection box.', 4),
                    ('Surge Voltage Limiter Termination', 'Limiting the voltage on the oversheat.', 4),
                    ('Main Insulation', 'High voltage insulation system.', 5),
                    ('Oversheath insulation', 'External insulation system.', 5),
                    ('Main joint', 'Main part of the joint.', 6),
                    ('Ground lead Joint', 'Connection between cable screen and ground.', 6),
                    ('Link box Joint', 'Ground connection box.', 6),
                    ('Surge Voltage Limiter Joint', 'Limiting the voltage on the oversheat.', 6),
                ]

                subcomponents_switchgear = [
                    ('Circuit breaker', 'Circuit breaker of the panel/bay', 7),
                    ('Protection Relay', 'Protection system.', 7),
                    ('Voltage transformer', 'Voltage measurement device.', 7),
                    ('Current transformer', 'Current measurement device.', 7),
                    ('Earthing switch', 'Earth connection system.', 7),
                    (
                    'Spout', 'Spouts serve as interface points for connecting cables or busbars to the switchgear.', 7),
                    ('Auxiliaries Panel', 'Insulators and other auxiliaries components.', 7),
                    ('Bus bar', 'Main conductor system', 8),
                    ('Auxiliaries Bus', 'Insulators and other auxiliaries components.', 8),
                ]

                subcomponents_transformer = [
                    ('Laminated sheets', 'Main part of the core.', 9),
                    ('Clamping plates', 'Metal plates or clamps are used to hold the laminated sheets together.', 9),
                    ('Tap changer', 'Voltage output regulator.', 10),
                    ('Bushing Primary', 'Insulation from winding to connection.', 10),
                    ('Bushing Secondary', 'Insulation from winding to connection.', 10),
                    ('Bushing Tertiary', 'Insulation from winding to connection.', 10),
                    ('Primary winding', 'Highest voltage winding', 10),
                    ('Secondary winding', 'Main low voltage winding.', 10),
                    ('Tertiary winding', 'Auxiliary voltage winding.', 10),
                    ('Enclosure/Tank', 'Main container for the transformer.', 11),
                    ('Terminal boxes Primary', 'Conteiner for the connecitons of the primary windings.', 11),
                    ('Terminal boxes Secondary', 'Conteiner for the connecitons of the secondary windings.', 11),
                    ('Terminal boxes Tertiary', 'Conteiner for the connecitons of the tertiary windings.', 11),
                    ('Oil Breather', 'Reserve tank for oil', 8),
                    ('Gauges', 'Meters', 8),
                    ('Cooling system tx', 'Fan and radiators.', 8),
                ]

                # SQL statement to insert data into the table
                insert_sql = '''
                             INSERT INTO asset_subcomponent (name, description, asset_component_id)
                             SELECT ?, ?, ?
                             WHERE NOT EXISTS (SELECT 1 FROM asset_subcomponent WHERE name = ? LIMIT 1);
                             '''

                # Insert each subcomponent into the table
                for subcomponent in subcomponents_rotating_machine:
                    # Check if the subcomponent already exists
                    cursor.execute("SELECT 1 FROM asset_subcomponent WHERE name = ? LIMIT 1", (subcomponent[0],))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the subcomponent if it does not exist
                        cursor.execute(insert_sql, (*subcomponent, subcomponent[0]))

                for subcomponent in subcomponents_cable:
                    # Check if the subcomponent already exists
                    cursor.execute("SELECT 1 FROM asset_subcomponent WHERE name = ? LIMIT 1", (subcomponent[0],))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the subcomponent if it does not exist
                        cursor.execute(insert_sql, (*subcomponent, subcomponent[0]))

                for subcomponent in subcomponents_switchgear:
                    # Check if the subcomponent already exists
                    cursor.execute("SELECT 1 FROM asset_subcomponent WHERE name = ? LIMIT 1", (subcomponent[0],))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the subcomponent if it does not exist
                        cursor.execute(insert_sql, (*subcomponent, subcomponent[0]))

                for subcomponent in subcomponents_transformer:
                    # Check if the subcomponent already exists
                    cursor.execute("SELECT 1 FROM asset_subcomponent WHERE name = ? LIMIT 1", (subcomponent[0],))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the subcomponent if it does not exist
                        cursor.execute(insert_sql, (*subcomponent, subcomponent[0]))
            def insert_diagnostic_test():
                # insert data
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
                    ('Dissipation Factor Monitoring', 'Online', 2),
                ]

                # SQL statement to insert data into the table
                insert_sql = '''
                             INSERT INTO diagnostic_test (name, condition, asset_category_id)
                             SELECT ?, ?, ?
                             WHERE NOT EXISTS (SELECT 1 FROM diagnostic_test WHERE name = ? AND asset_category_id = ? LIMIT 1);
                             '''

                # Insert each diagnostic test into the table
                for test in diagnostic_test_rotating_machine:
                    # Check if the test already exists
                    cursor.execute("SELECT 1 FROM diagnostic_test WHERE name = ? AND asset_category_id = ? LIMIT 1", (test[0],test[2]))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the test if it does not exist
                        cursor.execute(insert_sql, (*test, test[0],test[2]))



                for test in diagnostic_test_cables:
                    # Check if the test already exists
                    cursor.execute("SELECT 1 FROM diagnostic_test WHERE name = ? AND asset_category_id = ? LIMIT 1", (test[0],test[2]))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the test if it does not exist
                        cursor.execute(insert_sql, (*test, test[0],test[2]))

                for test in diagnostic_test_switchgears:
                    # Check if the test already exists
                    cursor.execute("SELECT 1 FROM diagnostic_test WHERE name = ? AND asset_category_id = ? LIMIT 1", (test[0],test[2]))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the test if it does not exist
                        cursor.execute(insert_sql, (*test, test[0],test[2]))

                for test in diagnostic_test_transformers:
                    # Check if the test already exists
                    cursor.execute("SELECT 1 FROM diagnostic_test WHERE name = ? AND asset_category_id = ? LIMIT 1", (test[0],test[2]))
                    existing_row = cursor.fetchone()

                    if not existing_row:
                        # Insert the test if it does not exist
                        cursor.execute(insert_sql, (*test, test[0],test[2]))
            def insert_criticality():
                # get data from file
                excel_file = '/Users/marianasouzaoliveira/Desktop/InWave_EHV_RMHI/assets/criticality_list_TB422.xlsx'

                # Get the absolute path based on the current working directory
                excel_file_path = os.path.abspath(excel_file)

                df = pd.read_excel(excel_file_path, sheet_name='Criticality')

                cursor.execute("""SELECT * FROM criticality_list""")
                criticality_list_result = cursor.fetchall()

                if criticality_list_result:
                    None

                else:

                    insert_sql = '''
                                 INSERT INTO criticality_list (class, safety, financial, reliability, enviromental)
                                 VALUES (?, ?, ?, ?, ?);
                                 '''

                    # Iterate through rows of the DataFrame and insert into SQLite table
                    for index, row in df.iterrows():

                        values = (
                            row['Class'],  # Replace with actual column names from your Excel file
                            row['Safety'],
                            row['Financial'],
                            row['Reliability'],
                            row['Environmental']
                        )
                        cursor.execute(insert_sql, values)

                    print("Criticality list table created")

            insert_asset_categoty()
            insert_component()
            insert_subcomponent()
            insert_diagnostic_test()
            insert_criticality()

            print('Settings uploaded')


        #create db
        create_db(cursor)

        upload_settings(cursor)

        # Commit the transaction
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()


        print("Table 'Inwave_RM' created successfully in Inwave_RM.db")

    except ConnectionError:
        print('Connection Error')


# create_centralized_db()