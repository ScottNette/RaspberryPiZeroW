from threading import Thread
from Queue import Queue
import time
import bluetooth
from bt_proximity import BluetoothRSSI


AllowList = [('Pixel2', '40:4E:36:47:A5:35'), ('Altima', '40:4E:36:47:A5:35')]
RSSIThreshold = (-30, 10)
q = Queue()

def main():
    scanDevice = 'Pixel'

    worker = Thread(target=threadScan, args=(q,))
    worker.setDaemon(True)
    worker.start()


    q.put(AllowList[1])
    count = 0
    while True:


        if (count % 10 == 0):
            q.put(AllowList[0])

        print('main')
        time.sleep(1)



def threadScan(q):

    scanVar =q.get()
    while True:
        try:
            scanVar = q.get(False)
            print scanVar
        except:
            print('no data')

        print(checkAllow([scanVar]))
        time.sleep(1)



def checkAllow(AllowList):
    RSSIThreshold = [-10, 10]

    for deviceName,deviceAddr in AllowList:

        rssi_val = getRSSI(deviceAddr)
        if RSSIThreshold[0] < rssi_val < RSSIThreshold[1]:
            deviceOut = deviceName
            break
        else:
            deviceOut = None
            print 'None'

    return deviceOut



def getRSSI(Target_MAC):
    btrssi = BluetoothRSSI(addr=Target_MAC)
    return btrssi.get_rssi()


def discoverDevice():

    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=1, flush_cache=1)
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))

def BTName(deviceAddr):
    name = bluetooth.lookup_name(deviceAddr)
    #print name
    return name



if __name__ == '__main__':
    main()