import collections
from bitfield import *

numbytes = 13
valDef = [
          ("year"     , [4,  1      ,    0,    1     ]),
          ("month"    , [4,  1      ,    0,    2     ]),
          ("day"      , [5,  1      ,    0,    3     ]),
          ("hour"     , [5,  1      ,    0,    10    ]),
          ("minute"   , [6,  1      ,    0,    37    ]),
          ("second"   , [6,  1      ,    0,    54    ]),
          ("dir"      , [4,  1      ,    0,    10    ]),
          ("speed"    , [10, 8.9737 ,    0,    35.8  ]),
          ("gustMax"  , [10, 1      ,    0,    42.2  ]),
          ("temp"     , [10, 10.7684,  -30,    23.5  ]),
          ("press"    , [10, 5.115  ,  900,    1002.2]),
          ("humid"    , [10, 10.23  ,    0,      56.2]),
          ("batteryV" , [8,  212.5  ,    3,    3.87  ]),
          ("batteryP" , [8,  2.55   ,    0,    68.4 ] ),
          ("checksum" , [8,  1      ,    0,     0    ])
]

wxDataRaw = collections.OrderedDict(valDef)

data = 0
count = 0
strData = ""
for x in wxDataRaw:
    print(x)
    if count == 0:
        data = (int(round((wxDataRaw[x][3] - wxDataRaw[x][2]) * wxDataRaw[x][1])) & ((2 ** wxDataRaw[x][0]) - 1))
        strData = str(data)
        count = 1
    else:
        tempData = (int(round((wxDataRaw[x][3] - wxDataRaw[x][2]) * wxDataRaw[x][1])) & ((2 ** wxDataRaw[x][0]) - 1)) << wxDataRaw[x][0]
        data = data + tempData
        strData = strData + str(tempData)
    print( strData)

#print strData
print strData
print bin(strData)
#print bytearray(data)
## decode

#for x in xrange(1,numbytes):






