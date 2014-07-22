#!/usr/bin/python
#-*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import sys
import os
import time 

import kost
from calcmoto import *
from arduinodev import *
from advice import *

class programviewer:
	def __init__(self, path):
		
		#inizializzo le procedure di calcolo
		self.calcm = calcmoto()
		
		#inizializzo gli avvisi
		self.advice = advice()
		
		self.gladeFile = gtk.glade.XML(fname = path+'progviewer.glade')
		self.mainwin = self.gladeFile.get_widget('winprogviewer')
		
		#inizializzo il arduino
		self.arduino = arduinodev()
		
		self.tv_program = self.gladeFile.get_widget('tv_program')
		
		self.cell = gtk.CellRendererText()
	
		callbacks = {
					'on_winprogviewer_delete_event' : self.winprogviewer_delete_event,
					'on_tb_play_clicked' : self.tb_play_clicked,
					'on_tb_home_clicked' : self.tb_home_clicked,
					'on_tb_precedente_clicked' : self.tb_precedente_clicked,
					'on_tb_successivo_clicked' : self.tb_successivo_clicked,

					}

		self.gladeFile.signal_autoconnect(callbacks)
		
		self.i = 0
		
	def winprogviewer_delete_event(self, widget, data=None):
		self.mainwin.destroy()	
	
	def program_show(self, reg, simulation):
		self.simulation = simulation
		if not self.simulation:
			self.arduino.arduino_connect()
		self.registro = reg[:]
		self.old = self.registro[0] #variabile di appoggio
		#self.model = gtk.ListStore(str, str, str, str, str, str)
		self.model = gtk.ListStore(int, int, int, int, int, int)
		self.tv_program.set_model(self.model)
		self.tv_program.set_rules_hint(1) #setta il colore alternato

		for i in self.registro: #aggiungo ai vettori 
			self.iter = self.model.append(i)
		
		for i,k in zip(kost.intestazione,range(len(kost.intestazione))):
			self.column = gtk.TreeViewColumn (i, self.cell, text = k)
			self.tv_program.append_column(self.column)
			self.column.set_resizable(True)
		
		self.mainwin.show()

#eseguo il movimento in modo continuativo
	def tb_play_clicked(self, widget, data=None):
		for k in range(len(self.registro)-1): #scorro l'intero registro	
			self.attuamovimento(self.registro[k],self.registro[k+1])
		self.tv_program.grab_focus()
		self.tv_program.set_cursor(len(self.registro)-1)
		self.old = self.registro[-1] #meorizzo l'ultima posizione
		

#procedo passo a passo (indietro) col movimento
	def tb_precedente_clicked(self, widget, data=None):
		try:
			n_vett = int(self.tv_program.get_cursor()[0][0])
			if n_vett > 0:
				self.tv_program.set_cursor(n_vett-1)
				self.attuamovimento(self.old,self.registro[n_vett-1]) #il primo vettore deve essere la posizione attuale
				self.old = self.registro[n_vett-1] #memorizzo l'ultima posizione
		except:
			pass

#procedo passo a passo (in avanti) col movimento
	def tb_successivo_clicked(self, widget, data=None):
		try:
			n_vett = int(self.tv_program.get_cursor()[0][0])
			self.tv_program.set_cursor(n_vett+1)
			self.attuamovimento(self.old,self.registro[n_vett+1]) #il primo vettore deve essere la posizione attuale
			self.old = self.registro[n_vett+1] #memorizzo l'ultima posizione
		except:
			pass
			
#ritorno alla posizione iniziale
	def tb_home_clicked(self, widget, data=None):
		model, iter = self.tv_program.get_selection().get_selected()
		tmp = []
		if iter:
			for i in range(len(model[0])):
				tmp.append(model.get_value (iter,i))
		else:
			tmp = self.registro[0][:]
		self.attuamovimento(tmp,self.registro[0])
		self.tv_program.grab_focus()
		self.tv_program.set_cursor(0)
		

			
		
#===========================================================================================================================	
# Invio i comandi ad arduino di come passare da una posizione ad un'altra
	def attuamovimento(self, patenza,arrivo):
		temp = self.calcm.moto_robot([patenza,arrivo]) #passo due vettori posizione appaiati
		for i in range(len(temp)-1): #scorro le posizioni calcolate tra l'inizio e la fine
			for j in kost.axis.keys(): #passo i singoli attuatori
				if temp[i][j-1] <> temp[i+1][j-1]: #invio solo le posizioni modificate
					if not self.simulation: 
						self.arduino.write_arduino(temp[i+1][j-1],j)
					time.sleep(0.1/temp[i][-1]) #metto un tempo di attesa in funzione della velocità	
