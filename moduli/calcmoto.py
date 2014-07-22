#!/usr/bin/python
#-*- coding: utf-8 -*



class calcmoto:
	def __init__(self):
		pass
			
			
#=======================================================================
#verifico il movimento di un dispositivo (e.g. mouse) e lo converto nel moto dei motori

	def move_axes(self, ang,pos,old_pos,min,max):
		inc = pos - old_pos #confronto la nuova posizione del mouse con quella vecchia
		if inc > 0: #se la posizione e' aumentata, aumenta l'angolo
			if ang < max: #definisco l'escursione massima
				ang = ang + 1
		elif inc < 0: #se la posizione e' diminuita, dmininuisce l'angolo
			if ang > min: #definisco l'escursione minima
				ang = ang - 1
		return ang,pos #passo i valori in modo che vengano memorizzate posizioni e angoli


#=======================================================================
#leggo il registro ed eseguo sequenza dopo sequenza

	def moto_robot(self, reg):
		output = []
		ritardo = 2520 #definisco il tempo di campionamento MCD tra 1-10
		delta = int(ritardo/reg[0][-1]) #definisco un incrementale
		for j in range(delta): #scorro l'incrementale
			pos = []
			for i in range(len(reg[0])-1): #scorro il vettore 
				inc = round(reg[0][:-1][i]+(reg[1][:-1][i]-reg[0][:-1][i])/delta*j) #incremento dalla posizioni di partenza all'arrivo
				pos.insert(i,inc) #aggiorno con le nuove posizioni calcolate
			pos.insert(len(reg[0]),reg[0][-1]) #inserisco la velocità
			output.insert(j,pos)#compongo il vettore in uscita con tutti i sottovettori	
		return output
