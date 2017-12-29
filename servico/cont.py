import sys
import take_pictures

estab = sys.argv[1]
op = sys.argv[2]
etq = sys.argv[3]
plate = sys.argv[4]

arrayUrl = [
'http://192.168.255.81/axis-cgi/mjpg/video.cgi?camera1',
'http://192.168.255.82/axis-cgi/mjpg/video.cgi?camera1',
'http://177.202.199.87:81/video.mjpg',
'http://192.168.255.84/axis-cgi/mjpg/video.cgi?camera1',
'http://192.168.255.85/axis-cgi/mjpg/video.cgi?camera1']

for i in range(5):
	print(i)
	take_pictures.take(str(estab), str(op), str(etq), str(plate), str(arrayUrl[i]), str(i))
