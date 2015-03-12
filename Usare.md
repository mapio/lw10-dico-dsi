Il funzionamento del server **learning week** si basa su tre zip file:

  * `server.zip`,
  * `data.zip`,
  * `code.zip`,

che contengono rispettivamente:

  * il materiale necessario all'esecuzione del _server_,
  * le _immagini_ ed i _metadati_ relativi,
  * il _codice_ delle **applicazioni utente** e le relative _configurazioni_;

il primo è il software del server e non deve essere modificato, mentre gli
ultimi due servono ad archiviare i dati utente, possono essere inizialmente
assenti (ma vengono in ogni caso creati al termine dell'esecuzione del server)
e possono essere manualmente modificati (quando il server non è attivo, ad
esempio, scompattandoli, modificando i file che contengono e quindi
ricompattandoli).

Per facilitare l'uso del server sotto Windows viene fornito anche lo script

  * `run.pyw`

e due versioni di `data.zip` che contengono alcune immagini (e relativi
metadati) pronte per l'uso.

Per eseguire il server è sufficiente aver installato Python 2.6, mettere tutti
i file necessari descritti sopra nella stessa cartella e

  * usando Windows, fare doppio click sull'icona di `run.pyw`,
  * usando Linux, dare il comando `python2.6 server.zip`.

Una volta posto in esecuzione il server, tutte le operazioni possono essere
effettuate puntando un browser (Firefox, o Chrome) all'indirizzo

> http://localhost:8000/

al termine del lavoro è necessario arrestare il server usando l'apposito link
presente su tale pagina, il che corrisponde ad accedere all'indirizzo

> http://localhost:8000/halt

Al termine dell'esecuzione del server vengono salvate in `data.zip` le
immagini (e metadati) aggiunti tramite l'applicazione di tagging, mentre in
`code.zip` viene salvato il codice (e configurazioni) delle applicazioni
utente.

Si osservi che il codice e le configurazioni delle applicazioni utente
presenti in `code.zip` _adombrano_ le rispettive versioni "originali"
contenute in `server.zip`; per "ripristinare" queste ultime è però
sufficiente eliminare (o rinominare), il file `code.zip`.