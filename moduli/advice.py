#!/usr/bin/python
#-*- coding: utf-8 -*

import gtk
import kost


class advice:
	def __init__(self):
		pass		
#=======================================================================
#invio un segnale di pericolo
	def pericolo(self, eccezione):
		message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE, eccezione)
		message.set_title(kost.messaggi["CtrRbt"])
		message.show()
		resp = message.run()
		if resp == gtk.RESPONSE_CLOSE:
			message.destroy()

#invio un segnale di informazione
	def info(self, eccezione):
		message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE, eccezione)
		message.set_title(kost.messaggi["CtrRbt"])
		message.show()
		resp = message.run()
		if resp == gtk.RESPONSE_CLOSE:
			message.destroy()
