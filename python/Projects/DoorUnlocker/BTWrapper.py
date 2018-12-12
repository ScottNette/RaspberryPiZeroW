import bluetooth
from bt_proximity import BluetoothRSSI
import time


class BTWrapper:
    def __init__(self, allowList, rssiThreshold):

        self.allow = allowList
        self.rssiThres = rssiThreshold
        self.foundDevice = (None, None, None)
        self.btrssi = None

    def checkAllow(self):
        self.foundDevice = []
        for device in self.allow:
            time.sleep(0.2)
            deviceAddr = device[1]
            rssi_val = self.getRSSI(deviceAddr)
            if self.rssiThres[0] < rssi_val < self.rssiThres[1]:
                self.foundDevice.append(device)
                break
            else:
                self.foundDevice = []





    def getRSSI(self, Target_MAC):
        self.btrssi = BluetoothRSSI(addr=Target_MAC)
        return self.btrssi.get_rssi()


    def discoverDevice(self):

        nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=1, flush_cache=1)
        print("found %d devices" % len(nearby_devices))

        for addr, name in nearby_devices:
            print("  %s - %s" % (addr, name))

