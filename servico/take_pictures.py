import os
import glob
import datetime
import time
import sys
import cv2
import base64
import urllib2
import numpy as np
import logging
from urllib2 import Request, URLError, HTTPError

logging.basicConfig(filename='/usr/local/bin/plateservice/plate_log.log',level=logging.DEBUG)

dataAtual = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")

dirRemoto = '/home/pi/img/cameras'

def take(estab, codOp, etq, placa, curl, cam):
	caminho = dirRemoto + "/" + estab + "/" + codOp + "/" + etq
	url = curl
	username = 'admin'
	password = '123'
	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	#url = 'http://177.202.199.87:81/video.mjpg'
	try:
	    stream=urllib2.urlopen(request, timeout=3)
	    bytes=''
	    condicao = True
	    if not os.path.exists(caminho):
		os.makedirs(caminho)
	    while True:
		    bytes+=stream.read(1024)
		    a = bytes.find('\xff\xd8')
		    b = bytes.find('\xff\xd9')
		    if a!=-1 and b!=-1:
			jpg = bytes[a:b+2]
			bytes= bytes[b+2:]
			i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
			cv2.imwrite(caminho+'/'+placa+'_Cam'+cam+'.jpg', i)
			time.sleep(3)
		    #if cv2.waitKey(1) == 27:
			if os.path.exists(caminho+'/'+placa+'_Cam'+cam+'.jpg'):
				condicao = False
				print('File Save Success - Wait 3 seconds')
				time.sleep(3)
				break
	except URLError as e:
	    print('Problema na Camera ' + cam)
	    logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + 'Problema na Camera ' + cam)
	except HTTPError as e:
	    print('Problema na Camera ' + cam)
	    logging.info(datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + 'Problema na Camera ' + cam)

#take('2', 'MDA123', '2')
