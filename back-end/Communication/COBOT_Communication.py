from Server import get_communication_mode, remove_cart
from Communication.PLC import write_tag, read_tag
from time import sleep

def determine_cobot_comms():
    mode =  int(get_communication_mode())
    if mode == 1:
        write_tag("COBOT_OPC_MODE", 1)
    elif mode == 0:
        write_tag("COBOT_OPC_MODE", 0)
    
def get_cobot_watchdog():
    return read_tag("COBOT_WATCHDOG")

def reset_cobot_watchdog():
    write_tag("COBOT_WATCHDOG", 0)

def cobot_watchdog():
    mode = int(read_tag("COBOT_OPC_MODE"))
    while (mode == 1):
        write_tag("COBOT_WATCHDOG", 1)
        sleep(2)
        if read_tag("COBOT_WATCHDOG") == 1:
            return print("COBOT COMMUNICATIONS LOST")
        mode = int(read_tag("COBOT_OPC_MODE"))

def remove_cart(barcode, area):
    write_tag("COBOT_AREA", area)
    write_tag("COBOT_CART_ID", barcode)


if __name__ == "__main__":
    determine_cobot_comms()
    cobot_watchdog()