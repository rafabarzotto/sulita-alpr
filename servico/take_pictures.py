import os
import glob
import datetime
import time
import sys
import cv2
import urllib2
import numpy as np
import logging
from urllib2 import Request, URLError, HTTPError

logging.basicConfig(filename='/usr/local/bin/plateservice/plate_log.log',level=logging.DEBUG)

dataAtual = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")

def take(codOp, placa, cam):
	#url = 'http://admin:3566@192.168.255.87/axis-cgi/mjpg/video.cgi?camera1'
	url = 'http://192.168.250.98:81/video.mjpg'
	#url = 'http://177.202.199.87:81/video.mjpg'
	try:
	    stream=urllib2.urlopen(url, timeout=3)
	    bytes=''
	    condicao = True
	    while True:
		    bytes+=stream.read(1024)
		    a = bytes.find('\xff\xd8')
		    b = bytes.find('\xff\xd9')
		    if a!=-1 and b!=-1:
			jpg = bytes[a:b+2]
			bytes= bytes[b+2:]
			i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
			cv2.imwrite('/home/pi/img/cameras/'+codOp+'_'+placa+'_'+dataAtual+'_Cam'+cam+'.jpg', i)
			time.sleep(3)
		    #if cv2.waitKey(1) == 27:
			if os.path.exists('/home/pi/img/cameras/'+codOp+'_'+placa+'_'+dataAtual+'_Cam'+cam+'.jpg'):
				condicao = False
				print('File Save Success - Wait 4 seconds')
				time.sleep(4)
				break
	except URLError as e:
	    print('Problema na Camera ')
	    logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + 'Problema na Camera ')
	except HTTPError as e:
	    print('Problema na Camera ')
	    logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + 'Problema na Camera')

#take('2', 'MDA123', '2')
