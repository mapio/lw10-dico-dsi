Per creare una "user app" di nome NOME_APP si devono fare i seguenti passi:

1) creare un template in server/resources/template [opzionale];

2) creare il codice javascript in server/resource/code/NOME_APP.js;

3) aggiungere una sezione NOME_APP che la descriva in
   server/resources/userapps.cfg;

4) aggiungere NOME_APP al campo list della sezione "User Applications" in
   server/resources/userapps.cfg;

La sezione di descrizione deve contenere i campi "title" e "template" (che
deve riferirsi al template da usare per il body, eventualmente creato al punto
1) e opzionalmente il campo "javascript". 

Tale campo contiene i file JS che devono essere caricati, di default vengono
aggiunti server/static/applib.js e server/code/NOME_APP.js, in più sono
previste le macro %(GMAP_JS)s e %(GCHART_JS)s rispettivamente per le mappe e i
grafici delle api di Google.