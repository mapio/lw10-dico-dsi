=============================
Learning Week DiCO DSI (2009)
=============================

Come usare il server
--------------------

Il funzionamento del server **learning week** si basa su tre zip file:

- ``server.zip``,
- ``data.zip``,
- ``code.zip``,

che contengono rispettivamente:

- il materiale necessario all'esecuzione del *server*,
- le *immagini* ed i *metadati* relativi,
- il *codice* delle **applicazioni utente** e le relative *configurazioni*;

il primo è il software del server e non deve essere modificato, mentre gli
ultimi due servono ad archiviare i dati utente, possono essere inizialmente
assenti (ma vengono in ogni caso creati al termine dell'esecuzione del server)
e possono essere manualmente modificati (quando il server non è attivo, ad
esempio, scompattandoli, modificando i file che contengono e quindi
ricompattandoli).

Per facilitare l'uso del server sotto Windows viene fornito anche lo script

- ``run.pyw``

e due versioni di ``data.zip`` che contengono alcune immagini (e relativi
metadati) pronte per l'uso.

Per eseguire il server è sufficiente aver installato Python 2.6, mettere tutti
i file necessari descritti sopra nella stessa cartella e

- usando Windows, fare doppio click sull'icona di ``run.pyw``,
- usando Linux, dare il comando ``python2.6 server.zip``.

Una volta posto in esecuzione il server, tutte le operazioni possono essere
effettuate puntando un browser (Firefox, o Chrome) all'indirizzo

	http://localhost:8000/

al termine del lavoro è necessario arrestare il server usando l'apposito link
presente su tale pagina, il che corrisponde ad accedere all'indirizzo

	http://localhost:8000/halt

Al termine dell'esecuzione del server vengono salvate in ``data.zip`` le
immagini (e metadati) aggiunti tramite l'applicazione di tagging, mentre in
``code.zip`` viene salvato il codice (e configurazioni) delle applicazioni
utente.

Si osservi che il codice e le configurazioni delle applicazioni utente
presenti in ``code.zip`` *adombrano* le rispettive versioni "originali"
contenute in ``server.zip``; per "ripristinare" queste ultime è però
sufficiente eliminare (o rinominare), il file ``code.zip``.


Come ottenere il materiale
--------------------------

Potete ottenere una distribuzione "pronta per l'uso" del software scaricando
(e salvando nella medesima cartella, senza scompattazione) il file:

- http://bitbucket.org/mapio/lw09-dico-dsi/raw/default/dist/server.zip

e, se usate Windows, il file:

- http://bitbucket.org/mapio/lw09-dico-dsi/raw/default/dist/run.pyw

cui potete aggiungere uno dei due file:

- http://bitbucket.org/mapio/lw09-dico-dsi/raw/default/dist/flikr/data.zip, o
- http://bitbucket.org/mapio/lw09-dico-dsi/raw/default/dist/example/data.zip.

che sono due "versioni" di data.zip che contengono, rispettivamente, alcune
centinaia di immagini scaricate da Flikr (geotaggate, ma non annotate) e tre
immagini campione (con geotag ed annotazioni). Si osserva che tali file
possono anche essere decompressi per accedere alle sole immagini che
contengono.

La versione di sviluppo
```````````````````````

Potete viceversa ottenere il "sorgente" (la versione "di sviluppo") sia usando
Mercurial, con il comando

	``hg clone https://bitbucket.org/mapio/lw09-dico-dsi``

oppure scaricando (e scompattando) lo zip file all'indirizzo

	http://bitbucket.org/mapio/lw09-dico-dsi/get/default.zip

a questo punto, usando lo script ``./bin/run`` potete produrre i file
necessari ed avviare il server.


**Versione beta**: c'è una versione di sviluppo (circa la quale non si
garantisce nulla) che corrispnde al branch ``devel`` di Mercurial, ottenibile
usando Mercurial con

	``hg clone -b devel https://bitbucket.org/mapio/lw09-dico-dsi lw09-dico-dsi-devel``

o che può essere scaricata come zip file all'indirizzo

	http://bitbucket.org/mapio/lw09-dico-dsi/get/devel.zip


Applicazioni utente
-------------------

Il meccanismo delle *applicazioni utente* è limitatamente estensibile.

Vengono fornite una serie di applicazioni di esempio (in ``server.zip``) il
cui codice Javascript può essere semplicemente modificato tramite il server.

Se si vuole aggiungere una nuova applicazione, si possono presentare due casi:

- l'applicazione si bassa su un template esistente,
- l'applicazione necessita di un template apposito.

Nel primo caso, è sufficiente manipolare ``code.zip`` (ossia basta
decomprimerlo, effettuare le modifiche descritte di seguito, e ricomprimerlo)
come segue:

1. va aggiunto un file 

	``code/<nome_app>.js``

  contenente la versione iniziale (eventualmente vuota) del codice
  dell'applicazione,

2. va aggiunta una sezione ``[nome_app]`` al file di configurazione
   ``code/apps.cfg`` che contenga i seguenti campi:

	:title: 
		una breve descrizione dell'applicazione,
	:template: 
		il nome del template per il body della pagina html dell'applicazione,
	:javascript: 
			un elenco (opzionale, separato da spazi) di file di codice.

  Il template è da indicare come basename di uno dei file presenti nella
  directory

	``resources/templates/``

  contenuta in ``server.zip``, mentre i file di codice da elencare devono
  essere indicati come basename di file presenti nella directory

	``code/``

  contenuta in ``code.zip`` (oppure di ``resources/`` in ``server.zip``); in
  particolare sono inclusi di default nell'elenco il file di codice
  dell'applicazione (di cui al punto 1) e la libreria

	``resources/static/applib.js``

  In fine, sono messe a disposizione due macro ``%(GMAP_JS)s`` e
  ``%(GCHART_JS)s`` che espandono rispettivamente al codice per le mappe e i
  grafici delle API di Google.

Nel secondo caso, in cui non si voglia usare uno tra i template predisposti, è
necessario aggiungere ai passi precedenti la seguente manipolazione del file
``server.zip`` (sempre ottenibile decomprimendo e quindi ricomprimendo il
medesimo):

3. va aggiunto un file

	``resources/tempaltes/<nome_template>.html``

  contenente un template (nel senso di uno ``string.Template`` di Python) per
  il body dell'applicazione.

**Aggiunta automatica**: è prevista la possibilità di aggiungere una
applicazione basata sul template ``io`` tramite il server stesso, si osserva
però che una volta fatta l'aggiunta le successive modifiche (fatta esclusione
per il codice dell'applicazione che è editabile via server) dovranno essere
fatte manualmente tramite la manipolazioni del file ``code.zip`` descritte in
precedenza.


Applib e template
-----------------

La libreria ``applib.js`` ed i template ``io`` e ``map`` consentono di
sviluppare semplici applicazioni che svolgnono rispettivamente I/O di testo
(tramite una *form* HTML) e manipolano una *Google Map*.

Il template ``io`` prevede che l'applicazione implementi almeno due funzioni:

- ``init`` e
- ``main``;

la prima viene chiamata all'``onload`` della pagina, mentre la seconda viene
chiamata alla pressione del bottone "Esegui il programma" presente nella
pagina (e riceve come argomento i valori presenti nella *form*, convertiti al
tipo indicato all'atto della loro creazione). C'è un meccanismo di *logging*
che può supportare lo sviluppo, così come altri *gadget* che consentono l'uso
di semlici mappe o grafici (basati su *Google Chart*).

Il template ``map`` prevede che l'applicazione implementi la funzione 

- ``init``

che viene chiamata all'``onload`` della pagina e può fare affidamento che sia
già stata inizializzata una *Google Map* (accessibile tramite l'oggetto
``map``, o con appositi metodi di convenienza per punnti e marker).

Si suggerisce di fare riferimento alle applicazioni di esempio per avere
qualche informazione sul loro funzionamento. Al momento manca una
documentazione più specifica.


Librerie esterne
----------------

Questo software è basato, ed include, le seguenti librerie:

- CodeMirror, available at http://marijn.haverbeke.nl/codemirror/,
- EXIF.py, available at http://sourceforge.net/projects/exif-py/,
- fvlogger, abailable at http://www.fivevoltlogic.com/code/fvlogger/,
- Javascipt Shell, available at http://www.squarefree.com/shell/.
