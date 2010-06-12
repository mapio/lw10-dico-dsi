Learning Week DiCO DSI (2009)
=============================

Potete ottenere una distribuzione "pronta per l'uso" del software scaricando
il pacchetto

	dist.zip
	
dall'indirizzo

	http://bitbucket.org/mapio/lw09-dico-dsi/downloads
	
(oppure potete ottenere il "sorgente" usando mercurial a partire dal repository

	hg clone https://mapio@bitbucket.org/mapio/lw09-dico-dsi

oppure scaricando l'ultima versione

	http://bitbucket.org/mapio/lw09-dico-dsi/get/tip.zip

a questo punto, usando lo script

	./bin/dist
	
potete produrre il file di distribuzione descritto in seguito).

Il pacchetto si basa su tre zip file

	server.zip
	data.zip
	code.zip

(di cui il primo è da non modificare, mentre gli ultimi due sono opzionali)
che contengono rispettivamente:

	il codice dell'applicazione (ed alcune applicazioni utente di esempio)
	le immagini ed i metadati relativi
	il codice delle *applicazioni utente* e le relative configurazioni

Nel file dist.zip, oltre a server.zip, sono presenti i file

	run.bat

che serve ad eseguire l'applicazione sotto Windows ed i file

	flikr.zip
	example.zip

che sono due "versioni" di data.zip che contengono, rispettivamente, alcune
centinaia di immagini scaricate da Flikr (geotaggate, ma non annotate) e tre
immagini campione (con geotag ed annotazioni); se si intende usare uno di
questi insiemi di immagini è sufficiente rinominare il relativo file come
data.zip. Tali file possono anche essere decompressi per accedere alle sole
immagini che contengono.

Per eseguire il server è sufficiente aver installato Python 2.6, mettere tutti
i file necessari descritti sopra nella stessa cartella e

-) usando Windows, fare doppio click sull'icona di run.bat,
-) usando Linux, dare il comando "python2.6 server.zip" (senza virgolette).

Una volta posto in esecuzione il server, tutte le operazioni possono essere
effettuate puntando un browser (Firefox, o Chrome) all'indirizzo

	http://localhost:8000/

al termine del lavoro è necessario arrestare il server usando l'apposito link
presente su tale pagina, il che corrisponde ad accedere all'indirizzo

	http://localhost:8000/halt

Al termine dell'esecuzione del server vengono salvate in data.zip le immagini
(e metadati) aggiunti tramite l'applicazione di tagging, mentre in code.zip
viene salvato il codice (e configurazioni) delle applicazioni utente.

Si osservi che il codice e le configurazioni delle applicazioni utente
presenti in code.zip *adombrano* le rispettive versioni "originali" contenute
in server.zip; per "ripristinare" queste ultime è però sufficiente eliminare
(o rinominare), il file code.zip.


Applicazioni utente
-------------------

Il meccanismo delle applicazioni utente è molto limitatamente estensibile.

Vengono fornite una serie di applicazioni di esempio (in server.zip) il cui
codice Javascript può essere semplicemente modificato tramite il server.

Se si vuole aggiungere una nuova applicazione, si possono presentare due casi:

-) l'applicazione si bassa su un template esistente,
-) l'applicazione necessita di un template apposito.

Nel primo caso, è sufficiente manipolare code.zip (ossia basta decomprimerlo,
effettuare le modifiche descritte di seguito, e ricomprimerlo) come segue:

1) va aggiunto un file 

	code/<nome_app>.js

contenente la versione iniziale (eventualmente vuota) del codice
dell'applicazione,

2) va aggiunta una sezione [nome_app] al file di configurazione code/apps.cfg
che contenga i seguenti campi:

- title: una breve descrizione dell'applicazion
- template: il nome del template per il body della pagina html dell'applicazione
- javascript: un elenco (opzionale, separato da spazi) di file di codice

Il template è da indicare come basename di uno dei file presenti in

	resources/templates

di server.zip, mentre i file di codice da elencare devono essere indicati come
basename di file presenti in 

	code/

di code.zip (oppure di resources/ in server.zip); in particolare sono inclusi
di default nell'elenco il file di codice dell'applicazione (di cui al punto 1)
e la liberria

	resources/static/applib.js

e sono messe a disposizione due macro %(GMAP_JS)s e %(GCHART_JS)s che indicano
rispettivamente il codice per le mappe e i grafici delle API di Google.

Nel secondo caso, in cui non si voglia usare uno tra i template predisposti, è
necessario aggiungere ai passi precedenti la seguente manipolazione del file
server.zip (sempre ottenibile decomprimendo e quindi ricomprimendo il file):

0) va aggiunto un file

	resources/tempaltes/<nome_template>.html

contenente un template (nel senso di uno string.Template di Python) per il
body dell'applicazione.


Applib e template
-----------------

La libreria applib.js ed i template io.html e map.html consentono di
sviluppore semplici applicazioni che svolgnono rispettivamente I/O di testo
(tramite una form html) e che manipolano una Google map.

Si suggerisce di fare riferimento alle applicazioni di esempio per avere
qualche informazione sul loro funzionamento. Al momento manca una
documentazione più specifica.


Librerie esterne
----------------

Questo software è basato, ed include, le seguenti librerie:

CodeMirror, available at http://marijn.haverbeke.nl/codemirror/
EXIF.py, available at http://sourceforge.net/projects/exif-py/
fvlogger, abailable at http://www.fivevoltlogic.com/code/fvlogger/
Javascipt Shell, available at http://www.squarefree.com/shell/

