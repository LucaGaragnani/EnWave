from pymodbus.client.sync import ModbusTcpClient
import struct
import logging
import csv


############ register map

#### asset details
register_map = {
    1000: "asset_id",                       # Asset ID
    **{1001 + i: f"tag_{i+1}" for i in range(10)},  # Tag values
    **{1011 + i: f"function_{i+1}" for i in range(10)},  # Function values
    **{1021 + i: f"manufacturer_{i+1}" for i in range(10)},  # Manufacturer values
    1031: "year_of_manufacture",            # Year of Manufacture
    1032: "year_of_installation",            # Year of Installation
    1033: "rated_voltage_part1",             # Rated Voltage (first part of the float)
    1034: "rated_voltage_part2",             # Rated Voltage (second part of the float)
    **{1035 + i: f"rated_power_MVA_{i+1}" for i in range(10)},  # Feature 1
    **{1045 + i: f"frequency_{i+1}" for i in range(10)},  # Feature 2
    **{1055 + i: f"rated_speed_{i+1}" for i in range(10)},  # Feature 3
    **{1065 + i: f"cooling_{i+1}" for i in range(10)},  # Feature 4
    **{1075 + i: f"machine_type_{i+1}" for i in range(10)},  # Feature 5
    **{1085 + i: f"rotor_type_{i+1}" for i in range(10)},  # Feature 6
    **{1095 + i: f"stator_winding_insulation_thermal_class_{i+1}" for i in range(10)},  # Feature 7
    **{1105 + i: f"stator_winding_type_{i+1}" for i in range(10)},  # Feature 8
    **{1115 + i: f"stator_winding_impregnation_{i+1}" for i in range(10)},  # Feature 9
    **{1125 + i: f"number_of_stator_slot_{i+1}" for i in range(10)},  # Feature 10
    **{1135 + i: f"rotor_winding_insulation_thermal_class_{i+1}" for i in range(10)},  # Feature 11
    **{1145 + i: f"rotor_winding_number_of_poles_{i+1}" for i in range(10)},  # Feature 12
    **{1155 + i: f"feature_13_{i+1}" for i in range(10)},  # Feature 13
    1165: "latitude_part1",                  # Latitude (first part of the float)
    1166: "latitude_part2",                  # Latitude (second part of the float)
    1167: "longitude_part1",                 # Longitude (first part of the float)
    1168: "longitude_part2",                 # Longitude (second part of the float)
}


#int to float
def registers_to_float(high, low):
    """Convert two 16-bit registers back into a float (IEEE 754)."""
    # Pack the two 16-bit registers into a byte array
    packed = struct.pack('>HH', high, low)  # Use '>HH' for big-endian unsigned shorts
    # Unpack the byte array back into a float
    return struct.unpack('>f', packed)[0]  # Return the float value

#asiic to string
def ascii_to_string(ascii_values):

    #eliminate 0 at the end
    ascii_values_cleaned = []
    for value in ascii_values:
        if value !=0:
            ascii_values_cleaned.append(value)
        if value ==0:
            None

    return ''.join(chr(value) for value in ascii_values_cleaned)

def write_to_csv(data, filename='modbus_registers.csv'):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Register Name', 'Value'])  # Write header
        for name, value in data.items():
            writer.writerow([name, value])  # Write each row

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def read_registers(client, register_map):
    results = {}

    tag_registers = []
    function_registers = []
    manufacturer_registers = []
    rated_voltage_registers = []
    rated_power_registers = []
    frequency_registers = []
    rated_speed_registers = []
    cooling_registers = []
    machine_type_registers = []
    rotor_type_registers = []
    stator_winding_insulation_thermal_class_registers = []
    stator_winding_type_registers = []
    stator_winding_impregnation_registers = []
    number_of_stator_slot_registers = []
    rotor_winding_insulation_thermal_class_registers = []
    rotor_winding_number_of_poles_registers = []
    feature_13_registers = []
    latitude_registers = []
    longitude_registers= []

    for register_address, register_name in register_map.items():
        print(register_name)
        if 'tag' in register_name:

            tag_registers.append(register_address-1)

        if "function_" in register_name:
            function_registers.append(register_address - 1)

        if "manufacturer_" in register_name:
            manufacturer_registers.append(register_address - 1)

        if "rated_power_MVA_" in register_name:
            rated_power_registers.append(register_address - 1)

        if "frequency_" in register_name:
            frequency_registers.append(register_address - 1)

        if "rated_speed_" in register_name:
            rated_speed_registers.append(register_address - 1)

        if "cooling_" in register_name:
            cooling_registers.append(register_address - 1)

        if "machine_type_" in register_name:
            machine_type_registers.append(register_address - 1)

        if "rotor_type_" in register_name:
            rotor_type_registers.append(register_address - 1)

        if "stator_winding_insulation_thermal_class_" in register_name:
            stator_winding_insulation_thermal_class_registers.append(register_address - 1)

        if "stator_winding_type_" in register_name:
            stator_winding_type_registers.append(register_address - 1)

        if "stator_winding_impregnation_" in register_name:
            stator_winding_impregnation_registers.append(register_address - 1)

        if "number_of_stator_slot_" in register_name:
            number_of_stator_slot_registers.append(register_address - 1)

        if "rotor_winding_insulation_thermal_class_" in register_name:
            rotor_winding_insulation_thermal_class_registers.append(register_address - 1)

        if "rotor_winding_number_of_poles_" in register_name:
            rotor_winding_number_of_poles_registers.append(register_address - 1)

        if "feature_13_" in register_name:
            feature_13_registers.append(register_address - 1)

        if "asset_id" in register_name or "year_of_manufacture" in register_name or "year_of_installation" in register_name:
    #     # Read single register values
            single_value = client.read_holding_registers(register_address-1, count=1, unit=1)

            results[register_name] = single_value.registers[0]

        if "rated_voltage_" in register_name:
            rated_voltage_registers.append(register_address-1)

        if "latitude_" in register_name:
            latitude_registers.append(register_address-1)

        if "longitude_" in register_name:
            longitude_registers.append(register_address-1)





        # elif "function" in register_name or "manufacturer" in register_name:
        #     # Read 10 registers for manufacturer and function values
        #     ascii_values = client.read_holding_registers(register_address-1, count=10, unit=1)
        #     if not ascii_values.isError():
        #         result_string = ''.join(chr(value) for value in ascii_values.registers if value != 0)
        #         results[register_name] = result_string  # Store as a single entry
        #     else:
        #         results[register_name] = None
        # elif "latitude" in register_name or "longitude" in register_name:
        #     # Read 2 registers for float values
        #     float_values = client.read_holding_registers(register_address-1, count=2, unit=1)
        #     if not float_values.isError():
        #         result_float = struct.unpack('>f', struct.pack('>HH', *float_values.registers))[0]
        #         results[register_name] = result_float
        #     else:
        #         results[register_name] = None
        #


    #tag
    # print(tag_registers)
    try:
        ascii_values = client.read_holding_registers(tag_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["tag"] = result_string
    except IndexError:
        results["tag"] = 'NA'

    # function
    try:
        ascii_values = client.read_holding_registers(function_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["function"] = result_string
    except IndexError:
        results['function'] = 'NA'

    # manufaturer
    try:
        ascii_values = client.read_holding_registers(manufacturer_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["manufacturer"] = result_string
    except IndexError:
        results['manufacturer'] = 'NA'


    #rated voltage
    try:
        float_values = client.read_holding_registers(rated_voltage_registers[0], count=2, unit=1)

        high, low = float_values.registers

        results['rated_voltage_kV'] = registers_to_float(high, low)
    except IndexError:
        results['rated_voltage_kV'] = 'NA'

    # rated power
    try:
        ascii_values = client.read_holding_registers(rated_power_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["rated_power_MVA"] = result_string
    except IndexError:
        results['rated_power_MVA'] = 'NA'


    # frequency
    try:
        ascii_values = client.read_holding_registers(frequency_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["frequency"] = result_string
    except IndexError:
        results['frequency'] = 'NA'


    # speed
    try:
        ascii_values = client.read_holding_registers(rated_speed_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["rated_speed"] = result_string
    except IndexError:
        results['rated_speed'] ='NA'

    # cooling
    try:
        ascii_values = client.read_holding_registers(cooling_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["cooling"] = result_string
    except IndexError:
        results['cooling'] ='NA'

    # machine type
    try:
        ascii_values = client.read_holding_registers(machine_type_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["machine_type"] = result_string
    except IndexError:
        results['machine_type'] ='NA'

    # rotor type
    try:
        ascii_values = client.read_holding_registers(rotor_type_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["rotor_type"] = result_string
    except IndexError:
        results['rotor_type'] ='NA'


    # stator winding insulation thermal class
    try:
        ascii_values = client.read_holding_registers(stator_winding_insulation_thermal_class_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["stator_winding_insulation_thermal_class"] = result_string
    except IndexError:
        results['stator_winding_insulation_thermal_class'] ='NA'


    # winding type
    try:
        ascii_values = client.read_holding_registers(stator_winding_type_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["stator_winding_type"] = result_string
    except IndexError:
        results['stator_winding_type'] ='NA'


    # impregnation
    try:
        ascii_values = client.read_holding_registers(stator_winding_impregnation_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["stator_winding_impregnation"] = result_string
    except IndexError:
        results['stator_winding_impregnation'] ='NA'


    # number of slot
    try:
        ascii_values = client.read_holding_registers(number_of_stator_slot_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["number_of_stator_slot"] = result_string
    except IndexError:
        results['number_of_stator_slot'] ='NA'

    # rotor winding themrla class
    try:
        ascii_values = client.read_holding_registers(rotor_winding_insulation_thermal_class_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["rotor_winding_insulation_thermal_class"] = result_string
    except IndexError:
        results['rotor_winding_insulation_thermal_class'] ='NA'

    # rotor winding poles
    try:
        ascii_values = client.read_holding_registers(rotor_winding_number_of_poles_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["rotor_winding_number_of_poles"] = result_string
    except IndexError:
        results['rotor_winding_number_of_poles'] ='NA'

    #feature 13
    try:
        ascii_values = client.read_holding_registers(feature_13_registers[0], count=10, unit=1)
        result_string = ascii_to_string(ascii_values.registers)
        results["feature_13"] = result_string
    except IndexError:
        results['feature_13'] ='NA'

    # latitudine
    try:
        float_values = client.read_holding_registers(latitude_registers[0], count=2, unit=1)
        high, low = float_values.registers
        results['latitude'] = registers_to_float(high, low)
    except IndexError:
        results['latitude'] ='NA'

    # longitude
    try:
        float_values = client.read_holding_registers(longitude_registers[0], count=2, unit=1)
        high, low = float_values.registers
        results['longitude'] = registers_to_float(high, low)
    except IndexError:
        results['longitude'] ='NA'

    print(results)
    return results

def main():
    # Connect to the Modbus server
    client = ModbusTcpClient('localhost', port=502)

    if client.connect():
        logging.info("Connected to Modbus server.")

        #
        # Read registers

        data = read_registers(client, register_map)

        # # Log the results
        # for name, value in data.items():
        #     logging.debug(f"{name}: {value}")

        # Log and print all the results
        for name in register_map.values():
            value = data.get(name, "Not Read")  # Default to "Not Read" if not in data
            print(f"{name}: {value}")  # Print each register's value
            logging.debug(f"{name}: {value}")  # Log the results

        # Write results to CSV
        write_to_csv(data)


        # Close the client connection
        client.close()
    else:
        logging.error("Failed to connect to Modbus server.")

if __name__ == "__main__":
    main()