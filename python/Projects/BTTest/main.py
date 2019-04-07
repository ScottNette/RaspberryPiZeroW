import bluetooth
from bt_proximity import BluetoothRSSI
import time
import sys


#AllowList = [('Pixel2', '40:4E:36:47:A5:35','email.com'), ('Altima', 'E0:AE:5E:FD:49:26','email.com')]

AllowList = [             ['Altima', 'E0:AE:5E:FD:49:26', '2038038060@vtext.com'],
                          ['Kristen', '4C:74:BF:B0:1E:B4', '+16233268643@tmomail.net']]

RSSIThreshold = (-30, 10)


def main():
    checkAllow()
    print ('here')





def checkAllow():
    global AllowList, RSSIThreshold

    for device in AllowList:
        deviceName, deviceAddr, deviceEmail = device
        print deviceAddr
        rssi_val = getRSSI(deviceAddr)

        if RSSIThreshold[0] < rssi_val < RSSIThreshold[1]:
            deviceOut = deviceName
            print deviceOut
            break
        else:
            deviceOut = None
            print deviceOut

    return deviceOut, deviceEmail



def getRSSI(Target_MAC):
    btrssi = BluetoothRSSI(addr=Target_MAC)
    return btrssi.get_rssi()


def discoverDevice():

    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=1, flush_cache=1)
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))


def discoverName():
    print(bluetooth.lookup_name(AllowList[0][1]))


if __name__ == '__main__':
    main()