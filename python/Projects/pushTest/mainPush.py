import httplib, urllib

#from pushover import Pushover
from pushWrapper import Pushover

po = Pushover("auf2xins5qc4rf66zqz19d17t3xn8f")
po.user("ur7vvtiuy43cytxszrw3fy87m919v4")

msg = po.msg("Hello, World!")

msg.set("title", "Best title ever!!!")

po.send(msg)


