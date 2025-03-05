
import serial
import time

def sniffer():
    # Configure serial port (adjust port and baud rate as per WIRL-WMB1 specs)
    port = "/dev/ttyUSB0"  # Check your device port
    baud_rate = 9600       # Common default; adjust based on module documentation
    
    try:
        # Open serial connection
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Sniffer started on {port} at {baud_rate} baud. Listening for wMBus messages...")
        
        while True:
            # Read incoming data
            if ser.in_waiting > 0:
                raw_data = ser.read(ser.in_waiting)  # Read all available bytes
                hex_data = raw_data.hex()            # Convert to hexadecimal string
                
                # Basic parsing (assuming standard wMBus frame: Length, C-Field, M-Field, A-Field)
                if len(raw_data) > 10:  # Minimum wMBus frame length
                    length = raw_data[0]
                    c_field = raw_data[1]
                    m_field = raw_data[2:4].hex()
                    a_field = raw_data[4:10].hex()  # Address field (meter ID)
                    print(f"Time: {time.ctime()} | Raw: {hex_data}")
                    print(f"Length: {length:02x}, C-Field: {c_field:02x}, M-Field: {m_field}, Meter ID: {a_field}")
                else:
                    print(f"Time: {time.ctime()} | Raw (short frame): {hex_data}")
            time.sleep(0.1)  # Avoid CPU overload
        
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Sniffer stopped by user.")
    finally:
        if 'ser' in locals():
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    sniffer()

