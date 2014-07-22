#!/usr/bin/env python
#
#       Finestra_info.py
#       
#       Copyright 2009 ivan <ivan@ivan-desktop>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import sys
import os



class finestra_info:
   def __init__ (self, path):
      self.ui = gtk.glade.XML (path + 'finestra_info.glade')
      self.callbacks = {
                       'on_finestra_info_response' : self.finestra_info_response, 
                       }
      self.ui.signal_autoconnect(self.callbacks)
      self.finestra_info = self.ui.get_widget ('finestra_info')
     # self.finestra_info.set_version(kost.versione)
      #self.finestra_info.set_program_name('')
      
#-----------------------------------------------------------------------

   def finestra_info_response(self, widget, response):
       if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CANCEL:
          self.finestra_info.destroy()
		
#-----------------------------------------------------------------------

   def show_info(self):
       self.finestra_info.show_all()



