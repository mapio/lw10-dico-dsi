Potete ottenere una distribuzione "pronta per l'uso" del software scaricando
(e salvando nella medesima cartella, senza scompattazione) il file:

  * http://lw10-dico-dsi.googlecode.com/files/server.zip

e, se usate Windows, il file:

  * http://lw10-dico-dsi.googlecode.com/hg/server/run.pyw

cui potete aggiungere uno dei due file:

  * http://lw10-dico-dsi.googlecode.com/files/flikr.zip, o
  * http://lw10-dico-dsi.googlecode.com/files/example.zip.

che sono due "versioni" di `data.zip` (e vanno rinominati così una volta
scaricati) che contengono, rispettivamente, alcune centinaia di immagini
scaricate da Flikr (geotaggate, ma non annotate) e tre immagini campione (con
geotag ed annotazioni). Si osserva che tali file possono anche essere
decompressi per accedere alle sole immagini che contengono.


## La versione di sviluppo ##

Potete viceversa ottenere il "sorgente" (la versione "di sviluppo") sia usando
Mercurial, con il comando

  * hg clone https://lw10-dico-dsi.googlecode.com/hg/ lw10-dico-dsi

a questo punto, usando lo script `./bin/run` potete produrre i file
necessari ed avviare il server.


**Versione beta**: c'è una versione di sviluppo (circa la quale non si
garantisce nulla) che corrispnde al branch `devel` di Mercurial, ottenibile
usando Mercurial con

  * hg clone -b devel https://lw10-dico-dsi.googlecode.com/hg/ lw10-dico-dsi-devel