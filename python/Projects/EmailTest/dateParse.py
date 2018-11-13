from datetime import datetime
exDate = '12 Nov 2018 07:32:16'
#
#
datetimeEmail = datetime.strptime(exDate, '%d %b %Y %H:%M:%S')
datetimeNow = datetime.utcnow()

difftime = datetimeNow - datetimeEmail
print(difftime)

print(difftime.total_seconds())
