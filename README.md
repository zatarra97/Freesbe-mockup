# Freesbe — mockup app soci

Mockup interattivo dell'app soci Freesbe (raccolta timbri nei locali aderenti),
realizzato con Claude Design. Non è codice di produzione: è un prototipo
navigabile che serve a discutere flussi e interfaccia.

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
