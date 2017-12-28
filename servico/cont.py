import sys
import take_pictures

op = sys.argv[1]
plate = sys.argv[2]

arrayUrl = [
'http://admin:3566@192.168.255.81/axis-cgi/mjpg/video.cgi?camera1',
'http://admin:3566@192.168.255.82/axis-cgi/mjpg/video.cgi?camera1',
'http://admin:3566@192.168.255.83/axis-cgi/mjpg/video.cgi?camera1',
'http://admin:3566@192.168.255.84/axis-cgi/mjpg/video.cgi?camera1',
'http://admin:3566@192.168.255.85/axis-cgi/mjpg/video.cgi?camera1']

for i in range(5):
	print(i)
    take_pictures.take(str(op), str(plate), arrayUrl[i], str(i))