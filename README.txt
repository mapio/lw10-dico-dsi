Learning Week DiCO DSI (2009)
=============================

Al momento non ho tempo di scrivere un readme decente, dico solo che per far
girare tutto servono due file, idealmete server.zip contiene il sw e le
risorse readonly, mentre data.zip è quello che dovrebbe contenere le immagini,
i metadati e il codice scritto dagli studenti.

Dopo aver fatto

	hg clone https://mapio@bitbucket.org/mapio/lw09-dico-dsi

(o, se non avete Mercurial installato, aver scaricato

	http://bitbucket.org/mapio/lw09-dico-dsi/get/tip.zip

e debitamente scompattato)

basta fare:

	cp data/example.zip data.zip
	
oppure

	cp data/flikr.zip data.zip

e quindi

	./bin/run

e (dovrebbe) partire un server web che risponde all'URL

	http://localhost:8000/

da cui è possibile far partire diverse applicazioni "built-in" e alcuni esempi
di codice "editabile".

Alla fine dell'uso, per arrestare il server fate

	http://localhost:8000/halt

(viene anche trap-pato anche ctrl-c, ma potrebbe essere che non esca pultio e
sputtanti data.zip, sempre meglio fermarlo con l'URL qui sopra):

Non c'è logging e gestione dell'errore, o ripulitura dell'input dell'utente…
prima di darlo in mano agli studenti va molto ripulito.


Sotto Windows
-------------

Preparare la "distribuzione" con 

	./bin/dist

quindi scaricare sulla macchina Windows il file 

	./dist.zip
	
e scompattarlo, questo dovrebbe creare tre file:

 	server.zip, data.zip run.bat 

in una stessa directory; per eseguire il server basta fare doppio click su

	run.bat


User Applications
-----------------

Per creare una "user app" di nome NOME_APP si devono fare i seguenti passi:

1) creare un template in server/resources/template [opzionale];

2) creare il codice javascript in server/resource/code/NOME_APP.js;

3) aggiungere una sezione NOME_APP che la descriva in
   server/resources/userapps.cfg;

La sezione di descrizione deve contenere i campi "title" e "template" (che
deve riferirsi al template da usare per il body, eventualmente creato al punto
1) e opzionalmente il campo "javascript".

Tale campo contiene i file JS che devono essere caricati (cui, di default,
vengono aggiunti server/static/applib.js e server/code/NOME_APP.js), per tale
sezione sono previste le macro %(GMAP_JS)s e %(GCHART_JS)s rispettivamente per
le mappe e i grafici delle API di Google.


Librerie
--------

Questo software è basato, ed include, le seguenti librerie:

EXIF.py, available at http://sourceforge.net/projects/exif-py/
Javascipt Shell, available at http://www.squarefree.com/shell/
CodeMirror, available at http://marijn.haverbeke.nl/codemirror/

