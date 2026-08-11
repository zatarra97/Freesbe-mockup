"""Rigenera offline-boot.js.

Perche' serve: quando il .dc.html viene aperto con doppio clic (protocollo
file://) Chrome blocca ogni fetch() verso file locali. Il runtime di Claude
Design usa fetch() per tre cose: 

  1. la propria pagina (refresh live in fase di editing)   -> inutile in locale
  2. ./ios-frame.jsx  (il componente della scocca iPhone)  -> senza, niente frame
  3. .image-slots.state.json (le foto trascinate negli slot) -> senza, niente foto

offline-boot.js incorpora 2 e 3 e li serve tramite uno shim di fetch(), e
disattiva 1. Si attiva SOLO su file://: servito via http:// non fa nulla e il
runtime lavora come sempre, leggendo i file veri dal disco.

Rilancialo ogni volta che modifichi ios-frame.jsx o trascini nuove immagini
negli slot:

    python aggiorna-offline.py
"""

import json
import pathlib

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "offline-boot.js"

# nome logico usato nel markup -> file su disco
EMBEDDED = {
    "./ios-frame.jsx": ("ios-frame.jsx", "text/jsx"),
    ".image-slots.state.json": (".image-slots.state.json", "application/json"),
}

TEMPLATE = """/* GENERATO AUTOMATICAMENTE — non modificare a mano.
   Rigenera con:  python aggiorna-offline.py

   Fa funzionare il mockup aperto con doppio clic (file://), dove il browser
   blocca fetch() sui file locali. Su http:// questo script non fa nulla. */
(function () {
  if (location.protocol !== 'file:') return;

  /* Il runtime rilegge la propria pagina via fetch() per l'editing live:
     su file:// fallisce e sporca la console. Un __resources gia' presente
     glielo fa saltare (e non rimappa nulla, essendo vuoto). */
  window.__resources = window.__resources || {};

  var FILES = __FILES__;

  var nativeFetch = typeof window.fetch === 'function' ? window.fetch.bind(window) : null;

  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : (input && input.url) || '';
    var clean = url.split('?')[0].split('#')[0];
    for (var name in FILES) {
      if (clean === name || clean.slice(-(name.length + 1)) === '/' + name.replace(/^\\.\\//, '')) {
        return Promise.resolve(new Response(FILES[name].body, {
          status: 200,
          headers: { 'Content-Type': FILES[name].type },
        }));
      }
    }
    return nativeFetch ? nativeFetch(input, init) : Promise.reject(new Error('fetch non disponibile'));
  };
})();
"""


def main():
    files = {}
    for name, (relpath, mime) in EMBEDDED.items():
        src = BASE / relpath
        if not src.exists():
            raise SystemExit("manca " + relpath)
        files[name] = {"type": mime, "body": src.read_text(encoding="utf-8")}

    payload = json.dumps(files, ensure_ascii=False, indent=None)
    OUT.write_text(TEMPLATE.replace("__FILES__", payload), encoding="utf-8")

    kb = OUT.stat().st_size / 1024
    print("scritto %s (%.0f KB) con: %s" % (OUT.name, kb, ", ".join(EMBEDDED)))


if __name__ == "__main__":
    main()
