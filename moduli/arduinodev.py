#!/usr/bin/python
#-*- coding: utf-8 -*-

import serial
from advice import *
import kost

class arduinodev:
	def __init__(self):
		self.advice = advice()

#=======================================================================
	#connetti arduino
	def arduino_connect(self):
		self.arduino = serial.Serial('/dev/ttyACM0', 9600)
		

#=======================================================================
#invio messaggio formattato ad arduino

	def write_arduino(self, ang, axes):
		try:
			self.arduino.write('%u%03u*' % (axes,ang))
		except Exception, tipo:
			self.advice.pericolo("%s\n\n %s" % (kost.avvisi["Err-com"],tipo.args))



#=======================================================================
#chiudo arduino
	def arduino_close(self):
		self.arduino.close()
		


	def pippo(self):
		print 'ciao'
