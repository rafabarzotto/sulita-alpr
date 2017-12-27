import sys
import take_pictures

op = sys.argv[1]
plate = sys.argv[2]

for i in range(5):
	print(i)
	take_pictures.take(str(op), str(plate), str(i))