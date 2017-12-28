from openalpr import Alpr
import os
import glob
import datetime
import time
import cv2
import sys
import urllib2
import numpy as np
import logging
from urllib2 import Request, URLError, HTTPError

logging.basicConfig(filename='/usr/local/bin/plateservice/plate_log.log',level=logging.DEBUG)

alpr = Alpr("br", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")

if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(10)
alpr.set_default_region("md")

dataAtual = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")

def take():
	#url = 'http://admin:3566@192.168.255.87/axis-cgi/mjpg/video.cgi?camera1'
	url = 'http://192.168.250.98:81/video.mjpg'
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
			cv2.imwrite('/home/pi/img/i.jpg',i)
			time.sleep(3)
		    #if cv2.waitKey(1) == 27:
			if os.path.exists('/home/pi/img/i.jpg'):
				condicao = False
				reconhece()
				break
	except URLError as e:
	    print('Problema na Camera')
	    logging.info(datetime.datetime.now().strftime("%d-%m-%Y-%H:%M") + " - " + 'Problema na Camera do LPR')
	except HTTPError as e:
	    print('Problema na Camera')
	    logging.info(datetime.datetime.now().strftime("%d-%m-%Y-%H:%M") + " - " + 'Problema na Camera do LPR')		

def reconhece():
	list_of_files = glob.glob('/home/pi/img/*') # * means all if need specific format then *.csv
	if not list_of_files:
		print "Diretorio Vazio"
		arq_foto = ""
		dir_saida = ""
	else:
		arq_foto = "/home/pi/img/i.jpg"
		dir_saida = "/home/pi/out/"

		if os.path.exists(arq_foto):
			results = alpr.recognize_file(arq_foto)
			lista = []

			i = 0
			for plate in results['results']:
					i += 1
					#print("   %12s %12s" % ("Plate", "Confidence"))
					for candidate in plate['candidates']:
						prefix = "-"
						if candidate['matches_template']:
							prefix = "*"
							#print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
							lista.extend([{'placa': candidate['plate'], 'confidencia': candidate['confidence']}])

			if not lista:
				# Call when completely done to release memory
				os.remove(arq_foto)
				print 'NOK'
			else:
				certo = max(lista,key=lambda item:item['confidencia'])

				print certo['placa']

				# Call when completely done to release memory
				#alpr.unload()
				os.remove(arq_foto)
				#print datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " - " + certo['placa']

		else:
			print "Arquivo nao encontrado"

take()
#reconhece()
