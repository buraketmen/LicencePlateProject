import os
hostname = "rtsp://root:root@192.168.10.34/axis-media/media.amp"
response = os.system("ping -c 1 " + hostname)

#and then check the response...
if response == 0:
  print (hostname, 'is up!')
else:
  print (hostname, 'is down!')