import requests
import random
import numpy as np
import datetime
import time
import json
import urllib
import urllib2




def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


headers = { 'Content-type': 'text/html', 'Connection':'close'}


sample = 100
x      = np.arange(sample)
f      = 1
Fs     = 100
daycycle = np.sin(2 * np.pi * f * x / Fs)

a = datetime.datetime(2018,1,1,0,0,0)

for kk in range(0,10):
    for ii in range(kk*4+16,kk*4+4 + 16):
        now = a + datetime.timedelta(0,5*ii*60)
        DateTimeVal = now.strftime("%Y-%m-%d %H:%M:%S")
        Temp     = round(60 + 20*daycycle[ii] + random.randint(1,150)/10,1)
        Humidity = round(20 + 15*daycycle[ii] + random.randint(1,50)/10,1)
        Pressure = round(1152 + 30*daycycle[ii] + random.randint(1,250)/10,1)
        Wind     = round(5 + 10*daycycle[ii] + random.randint(1,200)/10,1)
        WindDir  = random.randint(0,360)
        #payload = {'DateTime': DateTimeVal, 'Temp': round(Temp, 1), 'Humidity': round(Humidity, 1),'Pressure':round(Pressure, 1),'Wind':round(Wind, 1)}
        #print(payload)

        urlStr = 'http://192.168.1.144:5211/post2SQLDB.php?Pressure=' + str(Pressure) + '&WindDir=' + str(WindDir) + '&Humidity=' + str(Humidity) + '&Wind=' + str(Wind) + '&Temp=' + str(Temp) + '&DateTime=2018-01-' + DateTimeVal[8:10] + '+' + DateTimeVal[11:13] + '%3A' + DateTimeVal[14:16] + '%3A' + DateTimeVal[17:19]
        print(urlStr)
        urllib2.urlopen(urlStr)
        #resp = requests.get(urlStr)
        #print(resp.text)  # Printing response

    #    urllib.request.urlopen('http://192.168.1.144/post2SQLDB.php?Pressure=1062.0&Humidity=21.0&Wind=14.0&Temp=72.0&DateTime=2018-01-01+00%3A00%3A00')
        #try:
        #    r = requests.post('http://192.168.1.144:80/post2SQLDB.php', headers = headers, params=payload, stream=True)
        #except requests.exceptions.ConnectionError:
        #    print('connection error')
        time.sleep(.1)
        #print(ii)
        #print(r.status_code, r.reason)
        #print(r.text)
        #time.sleep(0.01)
        #print(r.request.body)
        #print(r.request.headers)

        #req = requests.Request('POST', 'http://192.168.1.144/post2SQLDB.php', headers = headers, data=payload)
        #prepared = req.prepare()

        #pretty_print_POST(prepared)
        #s = requests.Session()
        #s.send(prepared)




print("done")



#r = requests.get('http://192.168.1.144:80/index.php')
#r = requests.put('http://192.168.1.144:80/index.php', data = {'key':'value', 'test': 'bvae'})


