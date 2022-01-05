from Functions.Collect import *
from Functions.Status import getBatteryStatus
from time import sleep

if __name__ == '__main__':
    device_connect()
    config_block_iq()
    print(getBatteryStatus())