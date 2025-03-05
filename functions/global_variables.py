import threading

asset_selected_details=[]

acquisition_started = False
acquisition_is_running = False


stop_event= threading.Event()

connection_status = 0
current_mode = None
sniffer_mode_condition = False
test_mode_condition = False
monitoring_mode_condtition = False



