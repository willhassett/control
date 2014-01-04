import sys
import serial
import serial.tools.list_ports
import struct
import csv
import time

def find_arduino():
    # These are the vendor and product ids for the 
    # arduino's ftdi chip, I think
	ports = list(serial.tools.list_ports.grep(r'VID:PID=2341:43'))
	if not ports:
		sys.stderr.write("No Arduino found.\n")
		sys.exit(-1)
	if len(ports) > 1:
		sys.stderr.write("Too many Arduino's found.\n")
		sys.exit(-1)
	return ports[0][0]

def pb(b):
	print [ord(x) for x in b]

def main():
	ser = serial.Serial(find_arduino(), 9600)
	
	with open('output.csv', 'awb') as csvfile:
		output = csv.writer(csvfile)
		while True:
			buffer = ser.read(size=12)
			data = struct.unpack("<hhhhhh", buffer)
			
			# try and synchronise with the stream
			off_by_one = False
			for x in data:
				if x > 1024:
					off_by_one = True
					break	
			if off_by_one or 0 not in data:
				print ">>>>>>> off by one"
				ser.read(size=1)
				continue
			index = data.index(0)
			if index != 0:
				print ">>>>>>> out of sync"
				to_read = 2 * index
				ser.read(size=to_read)
				continue
			data = list(data)
			data[0] = time.time()
			# if we get to this point, we should be in sync
			print "> %s" % str(data)
		
			output.writerow(data)

if __name__ == '__main__':
    main()
