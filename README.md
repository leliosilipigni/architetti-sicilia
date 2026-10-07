# Architetti di Sicilia — mappa commerciale

Pagina web con **64 studi di architettura di tutta la Sicilia** (9 province) selezionati
per visite commerciali, con specializzazione, referenti, progetti noti e
**quali prodotti proporre** a ciascuno.

A cura di **Ellesse Rappresentanze** (Letterio Silipigni) — serramenti, porte,
pavimenti resilienti, schermature solari, chiusure automatiche e legno su 9 mandanti:
Biemme, Internorm, Ditec, Novoferm, Ferrero Legno, Gerflor, Cherubini, Roto, Navello.

## Contenuto

**64 studi** divisi in tre livelli di priorità (23 / 25 / 16), raggruppati per provincia:

| provincia | studi |
|---|---|
| Palermo | 24 |
| Catania | 11 |
| Ragusa | 7 |
| Trapani | 7 |
| Agrigento | 6 |
| Caltanissetta | 3 |
| Siracusa | 3 |
| Messina | 2 |
| Enna | 1 |

Per ogni studio: anno di fondazione, referenti, specializzazione, progetti citati,
sito ufficiale, motivazione della visita, prodotti consigliati.

La pagina ha **filtro per priorità**, **filtro per provincia** e **ricerca libera**
(per nome, città o prodotto).

## Come vengono assegnate le priorità

Le priorità sono calate sul **fit con i nove mandanti**, non su una classifica
assoluta di prestigio:

- **Priorità 1** — più volume potenziale e miglior incrocio con i prodotti
  (hospitality, opere pubbliche, restauro, grandi residenziale)
- **Priorità 2** — buon fit sulle ristrutturazioni
- **Priorità 3** — realtà da esplorare, spesso più facili da aprire come nuovo fornitore

## File

| file | cosa è |
|---|---|
| `index.html` | la pagina (autonoma, nessuna dipendenza esterna) |
| `dati.json` | tutti i 64 studi in formato strutturato |
| `dati-palermo.json` | origine: i 25 studi della mappa di Palermo |
| `dati-nuovi-raw.json` | origine: gli studi delle altre province, come raccolti |

## Pubblicazione

GitHub Pages, branch `main`, cartella radice:

**https://leliosilipigni.github.io/architetti-sicilia/**

## Fonti

Riviste e portali di settore (Archi&Interiors, Divisare, Archilovers, Archello,
Domus, Elle Decor, The Plan), siti ufficiali degli studi, Ordini degli Architetti
provinciali. Informazioni tratte da fonti pubbliche.

⚠️ **19 studi su 64 non hanno un sito ufficiale verificabile**: in quei casi il campo
è marcato "da verificare in visita" e il recapito va recuperato dall'Ordine provinciale
o alla prima visita. Nessun contatto è stato inventato.

## Rigenerare la pagina

```
python3 scripts/genera_pagina_sicilia.py     # legge dati.json e riscrive index.html
```

Per aggiungere studi: modificare `dati.json` (o gli script di raccolta e unione)
e rilanciare il generatore.
