import bluetooth
#from bt_proximity import BluetoothRSSI
import time


class BTWrapper:
    def __init__(self, allowList, rssiThreshold):

        self.allow = allowList
        self.rssiThres = rssiThreshold
        self.foundDevice = []
        self.btrssi = None

    def checkAllow(self):
        self.foundDevice = []
        for idx, device in enumerate(self.allow):
            time.sleep(0.2)
            deviceAddr = device[1]
            #rssi_val = self.getRSSI(deviceAddr)
           # print(rssi_val)
           # if self.rssiThres[0] < rssi_val < self.rssiThres[1]:
            #print(deviceAddr)
            name = bluetooth.lookup_name(deviceAddr)
            #print(name)
            #print(list[3])

            if (name == device[3]):
                self.foundDevice = device
                break
            else:
                self.foundDevice = []

    def checkList(self, list):
        self.foundDevice = []
        for idx, device in enumerate(list):
            time.sleep(0.2)
            deviceAddr = device[1]
            name = bluetooth.lookup_name(deviceAddr)
            if (name == device[3]):
            #rssi_val = self.getRSSI(deviceAddr)
            #print(rssi_val)
            #if self.rssiThres[0] < rssi_val < self.rssiThres[1]:
                self.foundDevice = device
                break
            else:
                self.foundDevice = []


    def checkSingle(self, list):
        self.foundDevice = []
        print(list[1])
        device = list[1]
        deviceAddr = device
        name = bluetooth.lookup_name(deviceAddr)
        #rssi_val = self.getRSSI(deviceAddr)
        #print(rssi_val)
        #if self.rssiThres[0] < rssi_val < self.rssiThres[1]:
        #print(name)
        #print(list[3])
        if (name == list[3]):
            self.foundDevice = list
        else:
            self.foundDevice = []


    #def getRSSI(self, Target_MAC):
       # self.btrssi = BluetoothRSSI(addr=Target_MAC)
    #    return self.btrssi.get_rssi()


    def discoverDevice(self):

        nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=1, flush_cache=1)
        print("found %d devices" % len(nearby_devices))

        for addr, name in nearby_devices:
            print("  %s - %s" % (addr, name))

