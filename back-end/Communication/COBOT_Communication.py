from Server import get_communication_mode
from Communication.PLC import write_tag, read_tag

def determine_cobot_comms():
    mode =  int(get_communication_mode())
    if mode == 1:
        write_tag("COBOT_OPC_MODE", 1)
    elif mode == 0:
        write_tag("COBOT_OPC_MODE", 0)
    
if __name__ == "__main__":
    determine_cobot_comms()