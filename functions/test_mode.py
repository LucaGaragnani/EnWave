import serial
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger()

def initialize_module(ser, baud_rate):
    """Initialize the Mimas-I module."""
    try:
        logger.info("Initializing module...")
        ser.write(b"AT\r\n")  # Check AT support
        time.sleep(0.5)
        if ser.in_waiting > 0:
            logger.info(f"AT response: {ser.read(ser.in_waiting).decode(errors='ignore')}")
        
        ser.write(b"AT+RX\r\n")  # Enable RX for responses (adjust per manual)
        time.sleep(0.5)
        if ser.in_waiting > 0:
            logger.info(f"RX mode response: {ser.read(ser.in_waiting).decode(errors='ignore')}")
    except Exception as e:
        logger.error(f"Initialization error: {e}")

def parse_meters_and_more_frame(raw_data):
    """Parse a wMBus frame with Meters and More protocol."""
    if len(raw_data) < 11:  # Minimum: L, C, M (2), A (6), CI
        return None
    
    frame = {
        "length": raw_data[0],
        "c_field": raw_data[1],
        "m_field": raw_data[2:4].hex(),  # Manufacturer ID
        "a_field": raw_data[4:10].hex(),  # Address
        "ci_field": raw_data[10] if len(raw_data) > 10 else None,  # Control Information
        "data": raw_data[11:].hex() if len(raw_data) > 11 else ""  # Payload
    }
    
    ci_meaning = {
        0x72: "Short Data Frame",
        0x78: "Long Data Frame",
        0x7A: "Extended Link Layer"
    }
    frame["ci_description"] = ci_meaning.get(frame["ci_field"], "Unknown CI-Field")
    
    c_meaning = {
        0x44: "SND-NR (Send, No Reply)",
        0x46: "SND-IR (Send, Installation Request)",
        0x7B: "SND-UD (Send User Data)",
        0x5B: "RSP-UD (Response User Data)"
    }
    frame["c_description"] = c_meaning.get(frame["c_field"], "Unknown C-Field")
    
    return frame

def test():
    port = "/dev/ttyUSB0"
    baud_rate = 38400  # Update from manual (try 9600, 19200, 38400)
    
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baud_rate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2,  # Longer timeout for responses
            rtscts=False
        )
        logger.info(f"Test mode started on {port} at {baud_rate} baud.")
        
        initialize_module(ser, baud_rate)
        
        while True:
            try:
                command = input("Enter hex command (e.g., '0B' for CMD_SERIALNO_REQ, '107B...' for SND-UD) or 'q' to quit: ").strip()
                if command.lower() == 'q':
                    break
                
                # Convert and send command
                try:
                    command_bytes = bytes.fromhex(command)
                    ser.write(command_bytes)  # Raw hex (adjust if AT+SEND is needed)
                    logger.info(f"Sent: {command}")
                except ValueError:
                    logger.error("Invalid hex string. Use format like '0B' or '107B2A'.")
                    continue
                
                # Wait for response
                time.sleep(1)  # Adjust based on manual or meter response time
                if ser.in_waiting > 0:
                    raw_response = ser.read(ser.in_waiting)
                    hex_response = raw_response.hex()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    logger.info(f"Raw response received: {hex_response}")
                    
                    # Parse response if it's a wMBus frame
                    frame = parse_meters_and_more_frame(raw_response)
                    if frame:
                        logger.info(f"Parsed response at {timestamp}:")
                        logger.info(f"  Length: {frame['length']:02x}")
                        logger.info(f"  C-Field: {frame['c_field']:02x} ({frame['c_description']})")
                        logger.info(f"  M-Field: {frame['m_field']}")
                        logger.info(f"  A-Field: {frame['a_field']}")
                        if frame['ci_field'] is not None:
                            logger.info(f"  CI-Field: {frame['ci_field']:02x} ({frame['ci_description']})")
                        if frame['data']:
                            logger.info(f"  Data: {frame['data']} (possibly encrypted)")
                    else:
                        logger.info(f"Unparsed response: {hex_response}")
                else:
                    logger.info("No response received.")
            
            except Exception as e:
                logger.error(f"Test loop error: {e}")
                time.sleep(1)
    
    except serial.SerialException as e:
        logger.error(f"Serial port error: {e}")
    except KeyboardInterrupt:
        logger.info("Test mode stopped by user.")
    finally:
        if 'ser' in locals():
            ser.close()
            logger.info("Serial port closed.")

if __name__ == "__main__":
    test()