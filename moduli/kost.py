#!/usr/bin/python
#-*- coding: utf-8 -*-

#=======================================================================
#Raccolta di tutti i messaggi
        
avvisi = {"Err-com": "Errore nella comunicazione!",
		 }
        
messaggi = {'Conn-OnL': "Connessione: on-line",
			'Conn-OfL': "Connessione: off-line",
			"Npos": "N°posizioni:",
			"Nuovo" : "Nuovo",
			"Carica" : "Carica",
			"Salva" : "Salva",
			"FneTab" : "Fine tabella.",
			"CtrRbt" : 'Controllo Robot',
			}

intestazione =["ASSE A","ASSE B","ASSE C","ASSE D","ASSE E","VELOCITA'"]

axis = dict() #dizionario assi
axis[1] = 'A'
axis[2] = 'B'
axis[3] = 'C'
axis[4] = 'D'
axis[5] = 'E'
