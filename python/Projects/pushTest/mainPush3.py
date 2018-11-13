import http.client, urllib
conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "auf2xins5qc4rf66zqz19d17t3xn8f",
    "user": "ur7vvtiuy43cytxszrw3fy87m919v4",
    "message": "hello world",
  }), { "Content-type": "application/x-www-form-urlencoded" })
print(conn.getresponse())