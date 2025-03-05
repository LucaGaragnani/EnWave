import serial
import time

def test():
    # Configure serial port
    port = "/dev/ttyUSB0"  # Adjust as needed
    baud_rate = 9600       # Adjust as needed
    
    try:
        # Open serial connection
        ser = serial.Serial(port, baud_rate, timeout=2)  # 2-second timeout for response
        print(f"Test mode started on {port} at {baud_rate} baud.")
        
        while True:
            # Get command from user
            command = input("Enter command (hex string, e.g., '10442A' for SND-NR) or 'q' to quit: ").strip()
            if command.lower() == 'q':
                break
            
            # Convert hex string to bytes
            try:
                command_bytes = bytes.fromhex(command)
            except ValueError:
                print("Invalid hex string. Example: '10442A'")
                continue
            
            # Send command
            ser.write(command_bytes)
            print(f"Sent: {command}")
            
            # Wait for and read response
            time.sleep(1)  # Give meter time to respond
            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting).hex()
                print(f"Response: {response}")
            else:
                print("No response received.")
        
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Test stopped by user.")
    finally:
        if 'ser' in locals():
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    test()