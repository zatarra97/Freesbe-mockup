# Freesbe — mockup app soci

Mockup interattivo dell'app soci Freesbe (raccolta timbri nei locali aderenti),
realizzato con Claude Design. Non è codice di produzione: è un prototipo
navigabile che serve a discutere flussi e interfaccia.

## Stato (settembre 2026)

Questo mockup è il **design di riferimento** dell'app consumer vera, che sta
nella cartella sorella `FrisbeeApp` (repo `zatarra97/frisbee-APP`, Expo). Nel
portarlo in app sono state prese tre decisioni che qui non compaiono:

- il brand è **Frisbee**, non «Freesbe»; il lessico **timbri** resta;
- **niente Login e Registrazione**: l'app è tutta pubblica, parte dalla Home;
- Home, Mappa e Dettaglio locale mostrano **locali veri** dal gestionale
  (`FrisbeeB2B`); Timbri, Carta, Punti, Missioni e Profilo restano con i dati
  finti di questo mockup finché il backend non avrà l'entità cliente. Sui locali
  veri non c'è la barra di progresso: al suo posto la raccolta in corso e il
  primo premio.

I token del design system (`_ds/`) sono stati tradotti in
`FrisbeeApp/apps/mobile/src/theme/`; le foto degli slot in
`.image-slots.state.json` sono estratte come WebP in `FrisbeeApp/apps/mobile/assets/mock/`.
Se qui cambia qualcosa, va riportato là a mano.

## Guardarlo

- **Online:** pubblicato su GitHub Pages a ogni push su `main`.
- **In locale, doppio clic** su `La Tessera - App.dc.html`.
- **In locale, via server** (necessario per aprirlo dal telefono in rete locale):

  ```
  python -m http.server 8765
  ```

  poi `http://<ip-del-pc>:8765/La%20Tessera%20-%20App.dc.html`.

Da desktop si vede la scocca dell'iPhone; sotto i 700 px di larghezza la scocca
sparisce e l'app occupa tutto lo schermo, come sul telefono vero.

## Com'è fatto

| File | Ruolo |
| --- | --- |
| `La Tessera - App.dc.html` | il mockup: template + logica delle schermate |
| `ios-frame.jsx` | la scocca iPhone (`IOSDevice`), con la soglia responsive |
| `_ds/` | design system Broadsheet (variabili, componenti, CSS) |
| `support.js` | runtime di Claude Design (generato, non modificare) |
| `image-slot.js` | slot immagine trascinabili (generato, non modificare) |
| `.image-slots.state.json` | le foto caricate negli slot |
| `offline-boot.js` | generato — vedi sotto |

### `offline-boot.js`

Aperto con doppio clic (`file://`) il browser blocca ogni `fetch()` verso file
locali, e il runtime ne usa tre: la pagina stessa, `ios-frame.jsx` e
`.image-slots.state.json`. Senza, si perdono la scocca e le foto.
`offline-boot.js` incorpora quei file e li serve tramite uno shim di `fetch`;
si attiva solo su `file://` e online non viene nemmeno scaricato.

È **generato**: rilancialo dopo aver modificato `ios-frame.jsx` o dopo aver
trascinato nuove immagini negli slot.

```
python aggiorna-offline.py
```
