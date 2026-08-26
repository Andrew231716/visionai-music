# VisionAI Music CC0 - 100 tracce

Pacchetto verificato il 2026-08-26. Contiene 100 brani reali, transcodificati in MP3 44.1 kHz stereo a 192 kbps, piu' preview fino a 30 secondi a 96 kbps.

## Prima del caricamento su Cloudflare R2

Il catalogo usa intenzionalmente questo host segnaposto:

`https://replace-with-your-r2-public-base.invalid`

Sostituiscilo con il Public Development URL o dominio CDN del bucket:

```bash
python3 tools/set_r2_base_url.py https://pub-xxxxxxxxxxxxxxxx.r2.dev
python3 tools/validate_package.py
```

Carica poi **il contenuto di questa cartella** nella radice del bucket, mantenendo i percorsi. L'URL da inserire in `secrets.properties` sara':

```properties
MUSIC_CATALOG_URL=https://pub-xxxxxxxxxxxxxxxx.r2.dev/music_catalog.json
```

## Contenuto

- `music_catalog.json`: schema VisionAI versione 1, senza campi extra.
- `audio/`: file completi suddivisi per categoria.
- `previews/`: anteprime suddivise per categoria.
- `artwork/`: predisposta ma senza immagini, quindi `artworkUrl` e' `null`.
- `metadata/license_manifest.json`: provenienza, verifica e checksum per ogni brano.
- `metadata/exclusions.json`: candidati respinti e motivazione prudenziale.
- `metadata/tracks.csv`: registro leggibile in foglio elettronico.
- `metadata/upload_manifest.csv`: chiavi R2, MIME type, cache policy, dimensioni e checksum.
- `licenses/SOURCE_VERIFICATION.md`: riepilogo delle verifiche per ciascuna fonte.
- `CHECKSUMS.sha256`: integrita' di tutti i file distribuibili.
- `tools/`: configurazione dell'host R2 e validatore offline.

## Nota legale

Sono stati inclusi soltanto file provenienti da pagine che mostrano esplicitamente CC0. La documentazione conserva comunque fonte, autore, URL della licenza e data di verifica. CC0 non elimina eventuali diritti di terzi che il concedente non possedeva; conserva sempre questo registro con la release.
