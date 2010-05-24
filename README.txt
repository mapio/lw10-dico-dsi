Learning Week DiCO DSI (2009)
=============================

Al momento non ho tempo di scrivere un readme decente, dico solo che per far
girare tutto servono due file, idealmete server.zip contiene il sw e le
risorse readonly, mentre data.zip è quello che dovrebbe contenere le immagini,
i metadati e il codice scritto dagli studenti.

Dopo aver fatto 

	hg clone https://mapio@bitbucket.org/mapio/lw09-dico-dsi

basta fare:

	cp data-example.zip data.zip
	./run

e (dovrebbe) partire un server web le cui URL vive sono

	http://localhost:8000/tag

per upload-are ed annotare le immagini,

	http://localhost:8000/shell

per eseguire una semplice shell JavaSript,

	http://localhost:8000/edit/<applicazione>
	http://localhost:8000/run/<applicazione>

per editare ed eseguire le varie applicazioni, al momento ce ne sono due
"somma" (che fa la somma tra due interi in una form) e "semplice" (che usa
gmap) e

	http://localhost:8000/halt

per arrestare il server (viene anche trap-pato anche ctrl-c, ma potrebbe
essere che non esca pultio e sputtanti data.zip, sempre meglio fermarlo con
l'URL qui sopra):

Non c'è logging e gestione dell'errore, o ripulitura dell'input dell'utente…
prima di darlo in mano agli studenti va molto ripulito.
