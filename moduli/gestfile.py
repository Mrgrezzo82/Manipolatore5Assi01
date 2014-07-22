#!/usr/bin/python
#-*- coding: utf-8 -*

import pickle
import advice


class gestfile:
	def __init__(self):
		pass

#=======================================================================
#Procedura per salvare il file di registro

	def scrivi_file(self, nome_file, contenuto):
		try:
			f = open(nome_file,'wb') 
			pickle.dump(contenuto,f)   
			f.close()
		except:
			advice.pericolo(["File %s non disponibile!" % (nome_file)])


#=======================================================================
#Procedura per caricare il file di registro

	def leggi_file(self, nome_file):
		reg = []
		try:
			f = open(nome_file,'r')  
			reg = pickle.load(f)	
		except:
			advice.pericolo("File non valido!")
		finally:	 
			f.close()		
		return reg

