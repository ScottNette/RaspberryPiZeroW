import bluetooth
from bt_proximity import BluetoothRSSI
import time
import sys


AllowList = [('Pixel2', '40:4E:36:47:A5:35'), ('Altima', '40:4E:36:47:A5:35')]
RSSIThreshold = (-30, 10)


def main():
    discoverDevice()
    print ('here')





def checkAllow():
    global AllowList, RSSIThreshold

    for device in AllowList:
        deviceName, deviceAddr, deviceEmail = device
        rssi_val = getRSSI(deviceAddr)
        if RSSIThreshold[0] < rssi_val < RSSIThreshold[1]:
            deviceOut = deviceName
            break
        else:
            deviceOut = None

    return deviceOut, deviceEmail



def getRSSI(Target_MAC):
    btrssi = BluetoothRSSI(addr=Target_MAC)
    return btrssi.get_rssi()


def discoverDevice():

    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=1, flush_cache=1)
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))





if __name__ == '__main__':
    main()