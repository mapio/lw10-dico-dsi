La libreria `applib.js` ed i template `io` e `map` consentono di
sviluppare semplici applicazioni che svolgnono rispettivamente I/O di testo
(tramite una _form_ HTML) e manipolano una **Google Map**.

Il template `io` prevede che l'applicazione implementi almeno due funzioni:

  * `init` e
  * `main`;

la prima viene chiamata all'`onload` della pagina, mentre la seconda viene
chiamata alla pressione del bottone "Esegui il programma" presente nella
pagina (e riceve come argomento i valori presenti nella _form_, convertiti al
tipo indicato all'atto della loro creazione). C'è un meccanismo di \1
che può supportare lo sviluppo, così come \1 consentono l'uso
di semlici mappe o grafici (basati su **Google Chart**).

Il template `map` prevede che l'applicazione implementi la funzione

  * `init`

che viene chiamata all'`onload` della pagina e può fare affidamento che sia
già stata inizializzata una **Google Map** (accessibile tramite l'oggetto
`map`, o con appositi metodi di convenienza per punnti e marker).

Si suggerisce di fare riferimento alle applicazioni di esempio per avere
qualche informazione sul loro funzionamento. Al momento manca una
documentazione più specifica.