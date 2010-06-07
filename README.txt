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

	cp data-example.zip data.zip
	./run

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
