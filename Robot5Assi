#!/usr/bin/python
#-*- coding: utf-8 -*-

'''==================================================================================================================
SOFWARE PER LA PROGRAMMAZIONE DELLA MOVIMENTAZIONE DI UN MANIPOLATORE 5 ASSI 
TRAMITE COMUNICAZIONE SERIALE AD UNA SCHEDA ARDUINO UNO
ARCHETTI IVAN 07/2014
====================================================================================================================='''


import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import time 
from pymouse import PyMouse
import sys
import os

#inizializzo la cartella di lavoro dei moduli creati ad hoc
sys.path.append(sys.path[0] + os.sep + 'moduli')

import kost
from gestfile import *
from advice import *
from arduinodev import *
from calcmoto import *
from programviewer import *
from finestra_info import *




class robot5assi:
#===========================================================================================================================	
#Procedure di inzializzazione dell'interfaccia del main del programma

	def __init__(self):
		self.percorso_form = sys.path[0] + os.sep + "form" + os.sep	  
		gladeFile = gtk.glade.XML(fname = self.percorso_form+'mainwin.glade')
		
		#inizializzo arduino
		self.arduino = arduinodev()
		
		#inizializzo la gestione file
		self.gfile = gestfile()
		
		#inizializzo le procedure di calcolo
		self.calcm = calcmoto()
		
		#inizializzo gli avvisi
		self.advice = advice()
		
		callbacks = {
		'on_mainwin_delete_event' : self.mainwin_delete_event,
		'on_mainwin_key_press_event' : self.mainwin_key_press_event,
		'on_tb_connetti_clicked' : self.tb_connetti_clicked,
		'on_tb_salva_step_clicked' : self.tb_salva_step_clicked,
		'on_tb_salva_clicked' : self.tb_salva_clicked,
		'on_tb_salva_come_clicked' : self.tb_salva_come_clicked,
		'on_tb_programmazione_clicked' : self.tb_programmazione_clicked,
		'on_tb_nuovo_clicked' : self.tb_nuovo_clicked,
		'on_tb_carica_clicked' : self.tb_carica_clicked,
		'on_tb_cancella_clicked' : self.tb_cancella_clicked,
		'on_sp1_value_changed' : self.sp1_value_changed,
		'on_sp6_value_changed' : self.sp6_value_changed,
		'on_sp11_value_changed' : self.sp11_value_changed,
		'on_sp2_value_changed' : self.sp2_value_changed,
		'on_sp7_value_changed' : self.sp7_value_changed,
		'on_sp12_value_changed' : self.sp12_value_changed,
		'on_sp3_value_changed' : self.sp3_value_changed,
		'on_sp8_value_changed' : self.sp8_value_changed,
		'on_sp13_value_changed' : self.sp13_value_changed,
		'on_sp4_value_changed' : self.sp4_value_changed,
		'on_sp9_value_changed' : self.sp9_value_changed,
		'on_sp14_value_changed' : self.sp14_value_changed,
		'on_sp5_value_changed' : self.sp5_value_changed,
		'on_sp10_value_changed' : self.sp10_value_changed,
		'on_sp15_value_changed' : self.sp15_value_changed,
		'on_hs_1_change_value' : self.hs_1_change_value,
		'on_hs_2_change_value' : self.hs_2_change_value,
		'on_hs_3_change_value' : self.hs_3_change_value,
		'on_hs_4_change_value' : self.hs_4_change_value,
		'on_hs_5_change_value' : self.hs_5_change_value,
		'on_item_info_button_press_event' : self.item_info_button_press_event,
		'on_item_nuovo_button_press_event' : self.item_nuovo_button_press_event,
		'on_item_apri_button_press_event' : self.item_apri_button_press_event,
		'on_item_salva_button_press_event' : self.item_salva_button_press_event,
		'on_item_salva_come_button_press_event' : self.item_salva_come_button_press_event,
		'on_item_esci_button_press_event' : self.item_esci_button_press_event,
		}
	
		gladeFile.signal_autoconnect(callbacks)
		
		self.m = PyMouse()
		self.pos = self.m.position()[0] #inizializzo posizione di partenza del mouse

		self.axis_start = [90,90,90,90,90,5]
		self.axis_rot = self.axis_start[:] #inizializzo la posizione degli assi e velocità
		self.axis_min = [0,0,0,0,0]
		self.axis_max = [180,180,180,180,180]
		self.registro = [] #raccolta di tutte le posizioni salvate (lista di liste)
		self.flag_salvato = True #flag stato di salvataggio
		self.simulation = True

		#definisco gli oggetti grafici
		self.mainwin = gladeFile.get_widget('mainwin')
		self.sb_info = gladeFile.get_widget('sb_info')
		self.sp_vel = gladeFile.get_widget('sp_vel')
		
		
		self.toolbar = [
						gladeFile.get_widget('tb_connetti'),
						gladeFile.get_widget('tb_nuovo'),
						gladeFile.get_widget('tb_carica'),
						gladeFile.get_widget('tb_salva'),
						gladeFile.get_widget('tb_salva_come'),
						gladeFile.get_widget('tb_salva_step'),
						gladeFile.get_widget('tb_cancella'),
						gladeFile.get_widget('tb_programmazione'),
						]

		self.axsw  = []
		for i in range(1,len(kost.axis)+1):
			self.axsw.append([
							gladeFile.get_widget('hs_%01u' % (i)),
							gladeFile.get_widget('sp%01u' % (i)), #partenza
							gladeFile.get_widget('sp%01u' % (i+5)), #min 
							gladeFile.get_widget('sp%01u' % (i+10)), #max
							gladeFile.get_widget('lb%01u' % (i))
							])

		#inizializzo il filtro per il file_chooser
		self.filtro = gtk.FileFilter()
		self.filtro.set_name("rbt") 
		self.filtro.add_mime_type("rbt") 
		self.filtro.add_pattern('*.rbt')

		#inizializzo il nome file
		self.nomefile = kost.messaggi["Nuovo"]
		self.mainwin.set_title(self.nomefile)
		
		#setto tutti i widget relativi ai vari assi
		for i,k in zip(self.axsw,self.axis_rot):
			i[3].set_increments(1,0);
			i[3].set_range(0,180)
			i[3].set_value(self.axis_max[0])
			i[2].set_increments(1,0);
			i[2].set_range(0,180)
			i[2].set_value(self.axis_min[0])
			i[1].set_increments(1,0);
			i[1].set_range(0,180)
			i[1].set_value(k)
			i[0].set_range(0,180)
			i[0].set_value(k)
	
		#setto speedbutton velocità
		self.sp_vel.set_increments(1,0);
		self.sp_vel.set_range(1,10)
		self.sp_vel.set_value(5)
	
		#setto i bottoni attivi sulla toolbar
		self.set_toolbar([1,1,1,1,1,1,0,0])
	
		#aggiorno lo stato
		self.aggiorna_stato(self.registro)
	
		#attivo finestra
		self.mainwin.show()
		gtk.main()


#===========================================================================================================================	
#Chiusura della form

	def mainwin_delete_event(self, widget, data=None):
		while not self.flag_salvato:
			self.tb_salva_come_clicked(widget)
		if not self.simulation:	
			self.arduino.arduino_close()
		gtk.main_quit()	
	
#===========================================================================================================================	
#Permetto di muovere il robot con il movimento del mouse premendo tasti specifici della tastiera

	def mainwin_key_press_event(self, widget, event=None):
		keyboard = {"KP_1":0,"KP_2":1,"KP_3":2,"KP_4":3,"KP_5":4}
		if keyboard.has_key(gtk.gdk.keyval_name(event.keyval)):
			key = keyboard[gtk.gdk.keyval_name(event.keyval)]
			self.axis_rot[key],self.pos = self.calcm.move_axes(self.axis_rot[key],self.m.position()[0],self.pos,self.axsw[key][2].get_value(),self.axsw[key][3].get_value())
			self.axsw[key][1].set_value(self.axis_rot[key])
		self.axis_rot[5] = self.sp_vel.get_value()

#===========================================================================================================================
#Implemento le funzionalità del menù	
	
	def item_info_button_press_event(self, widget, data=None):
		informazioni = finestra_info(self.percorso_form)
		informazioni.show_info()
		
	def item_nuovo_button_press_event(self, widget, data=None):
		self.tb_nuovo_clicked(widget)
			
	def item_apri_button_press_event(self, widget, data=None):
		self.tb_carica_clicked(widget)
		
	def item_salva_button_press_event(self, widget, data=None):
		self.tb_salva_clicked(widget)
		
	def item_salva_come_button_press_event(self, widget, data=None):
		self.tb_salva_come_clicked(widget)
		
	def item_esci_button_press_event(self, widget, data=None):
		self.mainwin_delete_event(widget)
		
#===========================================================================================================================
#Gestisco lo scorrimento delle cifre nei vari speedbutton ed il movimento del robot

	def sp1_value_changed(self, widget, data=None): 
		self.set_range(kost.axis.keys()[0]-1)
		self.axsw[0][0].set_value(self.axsw[0][1].get_value())
	
	def sp6_value_changed(self, widget, data=None): 
		self.set_min(kost.axis.keys()[0]-1) #impedisco al minimo di salire sopra la partenza
		
	def sp11_value_changed(self, widget, data=None): 
		self.set_max(kost.axis.keys()[0]-1) #impedisco al massimo di scendere sotto la partenza
	
	def sp2_value_changed(self, widget, data=None): 
		self.set_range(kost.axis.keys()[0])
		self.axsw[1][0].set_value(self.axsw[1][1].get_value())

	def sp7_value_changed(self, widget, data=None): 
		self.set_min(kost.axis.keys()[0]) #impedisco al minimo di salire sopra la partenza
		
	def sp12_value_changed(self, widget, data=None): 
		self.set_max(kost.axis.keys()[0]) #impedisco al massimo di scendere sotto la partenza

	def sp3_value_changed(self, widget, data=None): 
		self.set_range(kost.axis.keys()[1])
		self.axsw[2][0].set_value(self.axsw[2][1].get_value())

	def sp8_value_changed(self, widget, data=None): 
		self.set_min(kost.axis.keys()[1]) #impedisco al minimo di salire sopra la partenza
			
	def sp13_value_changed(self, widget, data=None): 
		self.set_max(kost.axis.keys()[1]) #impedisco al massimo di scendere sotto la partenza
		
	def sp4_value_changed(self, widget, data=None): 
		self.set_range(kost.axis.keys()[2])
		self.axsw[3][0].set_value(self.axsw[3][1].get_value())

	def sp9_value_changed(self, widget, data=None): 
		self.set_min(kost.axis.keys()[2]) #impedisco al minimo di salire sopra la partenza
		
	def sp14_value_changed(self, widget, data=None): 
		self.set_max(kost.axis.keys()[2]) #impedisco al massimo di scendere sotto la partenza
		
	def sp5_value_changed(self, widget, data=None): 
		self.set_range(kost.axis.keys()[3])
		self.axsw[4][0].set_value(self.axsw[4][1].get_value())

	def sp10_value_changed(self, widget, data=None): 
		self.set_min(kost.axis.keys()[3]) #impedisco al minimo di salire sopra la partenza
		
	def sp15_value_changed(self, widget, data=None): 
		self.set_max(kost.axis.keys()[3]) #impedisco al massimo di scendere sotto la partenza

	def hs_1_change_value(self, widget, data=None, data2=None): #collego il movimento dello slider con lo spinbutton
		self.axsw[0][1].set_value(self.axsw[0][0].get_value())
	
	def hs_2_change_value(self, widget, data=None, data2=None): #collego il movimento dello slider con lo spinbutton
		self.axsw[1][1].set_value(self.axsw[1][0].get_value())	

	def hs_3_change_value(self, widget, data=None, data2=None): #collego il movimento dello slider con lo spinbutton
		self.axsw[2][1].set_value(self.axsw[2][0].get_value())			
		
	def hs_4_change_value(self, widget, data=None, data2=None): #collego il movimento dello slider con lo spinbutton
		self.axsw[3][1].set_value(self.axsw[3][0].get_value())	
			
	def hs_5_change_value(self, widget, data=None, data2=None):	#collego il movimento dello slider con lo spinbutton
		self.axsw[4][1].set_value(self.axsw[4][0].get_value())	

#===========================================================================================================================
#Procedure relative ai vari speed button	
	
	def tb_connetti_clicked(self, widget, data=None):
		if self.simulation == True:
			try:
				self.arduino.arduino_connect()
				self.simulation = False
				self.toolbar[0].set_stock_id('gtk-connect') 
				self.set_toolbar([1,-1,-1,-1,-1,-1,-1])
				self.aggiorna_stato(self.registro)
			except Exception, tipo:
				self.advice.pericolo("%s\n\n %s" % (kost.avvisi["Err-com"],tipo.args))
		else:
			try:
				self.arduino_close()
				self.simulation = True
				self.toolbar[0].set_stock_id('gtk-disconnect') 
				self.set_toolbar([1,-1,-1,-1,-1,-1,-1])
				self.aggiorna_stato(self.registro)
			except Exception, tipo:
				self.advice.pericolo("%s\n\n %s" % (kost.avvisi["Err-com"],tipo.args))

	def tb_nuovo_clicked(self, widget, data=None):	
		while not self.flag_salvato:
			self.tb_salva_come_clicked(widget)	
		nomefile = kost.messaggi["Nuovo"]
		self.mainwin.set_title(nomefile)
		self.registro = []
		self.aggiorna_stato(self.registro)
		self.set_toolbar([-1,-1,-1,0,-1,-1,0,0,0]) 
	
	def tb_carica_clicked(self, widget, data=None):
		fc =  gtk.FileChooserDialog(kost.messaggi["Carica"], None, gtk.FILE_CHOOSER_ACTION_OPEN, 
											(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))    
		fc.set_select_multiple(False)  
		fc.add_filter(self.filtro)  
		fc.set_current_folder(sys.path[0])
		if fc.run() == gtk.RESPONSE_OK:
			nomefile = fc.get_filename()
			self.mainwin.set_title(nomefile.rpartition(os.sep)[2])
			self.registro = self.gfile.leggi_file(nomefile)[:]
			self.aggiorna_stato(self.registro)	
		fc.destroy()
		self.set_toolbar([-1,-1,-1,0,-1,-1,1,1])
		self.flag_salvato = True

	def tb_salva_clicked(self, widget, data=None):
		if not self.flag_salvato:
			self.gfile.scrivi_file(self.nomefile.rpartition(os.sep)[2],self.registro) #salvo le posizioni registrate
			self.set_toolbar([-1,-1,-1,0,-1,-1,-1,-1])
		elif (not self.flag_salvato and self.nomefile == kost.messaggi["Nuovo"]):
			tb_salva_come_clicked(widget)

	def tb_salva_come_clicked(self, widget, data=None):
		fc =  gtk.FileChooserDialog(kost.messaggi["Salva"], None, gtk.FILE_CHOOSER_ACTION_SAVE, 
											(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))    
		fc.set_select_multiple(False) 
		fc.set_current_folder(sys.path[0]) 
		fc.set_filter(self.filtro)
		if fc.run() == gtk.RESPONSE_OK:
			if fc.get_filename() [-3:] == self.filtro.get_name(): 
				nomefile = fc.get_filename() 
			else:
				nomefile = fc.get_filename() + '.' + self.filtro.get_name()
			self.gfile.scrivi_file(nomefile,self.registro)
			self.mainwin.set_title(nomefile.rpartition(os.sep)[2])    
			self.set_toolbar([-1,-1,-1,0,-1,-1,-1,-1])     
		fc.destroy()
		self.flag_salvato = True
	
	def tb_salva_step_clicked(self, widget, data=None):
		self.set_toolbar([-1,-1,-1,1,1,-1,1,1])
		self.registro.append(self.axis_rot[:])#salvo le posizioni in un registro 
		self.aggiorna_stato(self.registro)
		self.flag_salvato = False	

	def	tb_cancella_clicked(self, widget, data=None):
		if len(self.registro) > 0:
			self.set_toolbar([-1,-1,-1,1,-1,-1,1,1])
			self.registro.pop()
			if len(self.registro) == 0:
				self.set_toolbar([-1,-1,-1,-1,1,-1,-1,0,0])
			self.flag_salvato = False
		self.aggiorna_stato(self.registro)
	
	def tb_programmazione_clicked(self, widget, data=None):
		program = programviewer(self.percorso_form)
		program.program_show(self.registro,self.simulation)


#===========================================================================================================================	
#Procedure di appoggio

#definisco il range di rotazione
	def set_range(self, axes): 
		if self.axsw[axes][1].get_value() < self.axsw[axes][2].get_value() or self.axsw[axes][1].get_value() > self.axsw[axes][3].get_value():
			self.axsw[axes][1].set_range(self.axsw[axes][2].get_value(),self.axsw[axes][3].get_value())
		self.axis_rot[axes] = self.axsw[axes][1].get_value()
		if not self.simulation:
			self.arduino.write_arduino(self.axis_rot[axes], kost.axis.keys()[axes])

 #il minimo non sale sopra partenza
	def set_min(self, axes):
		if self.axsw[axes][2].get_value() > self.axsw[axes][1].get_value():
			self.axsw[axes][2].set_value(self.axsw[axes][1].get_value())
		self.axsw[axes][1].set_range(self.axsw[axes][2].get_value(),self.axsw[axes][3].get_value())

#il massimo non scende sotto la partenza
	def set_max(self, axes): 
		if self.axsw[axes][3].get_value() < self.axsw[axes][1].get_value(): 
			self.axsw[axes][3].set_value(self.axsw[axes][1].get_value())		
		self.axsw[axes][1].set_range(self.axsw[axes][2].get_value(),self.axsw[axes][3].get_value())	

#aggiorno la barra di stato con le varie info
	def aggiorna_stato(self, posizioni):
		self.sb_info.pop(0)
		if not self.simulation:
			a = kost.messaggi["Conn-OnL"].ljust(30)
		else:
			a = kost.messaggi["Conn-OfL"].ljust(30)
		b = ("%s %s" % (kost.messaggi["Npos"],len(posizioni)))
		b = b.ljust(20)
		if len(posizioni) == 0:
			posizioni = [[]]
		c = ("%s" % (posizioni[-1]))	
		c = c.ljust(20)
		self.sb_info.push(0, a+b+c)

#accendo o spengo i vari tasti della toolbar            
	def set_toolbar(self, stato):
		for i,k in zip(self.toolbar,stato): #0 = False / 1 = True / -1 = non variare
			if k > -1:
				i.set_sensitive(k)

#===========================================================================================================================	
#Programma principale

if __name__ == '__main__':
   sample = robot5assi()
 




