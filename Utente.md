Il meccanismo delle **applicazioni utente** è limitatamente estensibile.

Vengono fornite una serie di applicazioni di esempio (in `server.zip`) il
cui codice Javascript può essere semplicemente modificato tramite il server.

Se si vuole aggiungere una nuova applicazione, si possono presentare due casi:

  * l'applicazione si bassa su un template esistente,
  * l'applicazione necessita di un template apposito.

Nel primo caso, è sufficiente manipolare `code.zip` (ossia basta
decomprimerlo, effettuare le modifiche descritte di seguito, e ricomprimerlo)
come segue:

  * va aggiunto un file
> > `code/<nome_app>.js`

> contenente la versione iniziale (eventualmente vuota) del codice dell'applicazione,
  * va aggiunta una sezione `[nome_app]` al file di configurazione `code/apps.cfg` che contenga i seguenti campi:
    * `title`: una breve descrizione dell'applicazione,
    * `template`: il nome del template per il body della pagina html dell'applicazione,
    * `javascript`: un elenco (opzionale, separato da spazi) di file di codice.
> Il template è da indicare come basename di uno dei file presenti nella directory
> > `resources/templates/`

> contenuta in `server.zip`, mentre i file di codice da elencare devono
> essere indicati come basename di file presenti nella directory
> > `code/`

> contenuta in `code.zip` (oppure di `resources/` in `server.zip`); in
> particolare sono inclusi di default nell'elenco il file di codice
> dell'applicazione (di cui al punto 1) e la libreria
> > `resources/static/applib.js`

> In fine, sono messe a disposizione due macro `%(GMAP_JS)s` e
> `%(GCHART_JS)s` che espandono rispettivamente al codice per le mappe e i
> grafici delle API di Google.

Nel secondo caso, in cui non si voglia usare uno tra i template predisposti, è
necessario aggiungere ai passi precedenti la seguente manipolazione del file
`server.zip` (sempre ottenibile decomprimendo e quindi ricomprimendo il
medesimo):

  * va aggiunto un file
> > `resources/tempaltes/<nome_template>.html`

> contenente un template (nel senso di uno `string.Template` di Python) per
> il body dell'applicazione.

**Aggiunta automatica**: è prevista la possibilità di aggiungere una
applicazione basata sul template `io` tramite il server stesso, si osserva
però che una volta fatta l'aggiunta le successive modifiche (fatta esclusione
per il codice dell'applicazione che è editabile via server) dovranno essere
fatte manualmente tramite la manipolazioni del file `code.zip` descritte in
precedenza.