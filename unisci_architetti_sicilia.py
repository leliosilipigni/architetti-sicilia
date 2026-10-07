#!/usr/bin/env python3
"""Unisce Palermo + i tre elenchi raccolti + le aggiunte CL/EN in dati.json."""
import json
import re

BASE = '/data/architetti-sicilia'

# ------------------------------------------------------------------ 1. NUOVI (dai 3 sub-agent)
NUOVI = json.load(open(f'{BASE}/dati-nuovi-raw.json', encoding='utf-8'))

# ------------------------------------------------------------------ 2. AGGIUNTE CL / EN (ricerca diretta)
CL_EN = [
    dict(n="Davide Cammarata Architetto", citta="Caltanissetta", prov="Caltanissetta",
         anno="1999", chi="Davide Cammarata",
         spec="Residenziale, centri storici, progettazione di pregio",
         note="Attivo tra Caltanissetta e Palermo dal 1999. Premiato al Premio di Architettura ANCE Catania per una casa unifamiliare a Caltanissetta. Regesto progetti e riconoscimenti pubblicato sul suo sito.",
         sito="https://www.davidecammarata.it",
         proponi=["Internorm", "Biemme", "Ferrero Legno", "Gerflor"],
         perche="Il profilo più premiato della provincia di Caltanissetta: case unifamiliari di pregio dove serramento e finiture contano.",
         t=2),
    dict(n="Rumeo Arch. Giuseppe", citta="Caltanissetta", prov="Caltanissetta",
         anno=None, chi="Giuseppe Rumeo",
         spec="Progettazione edile, residenziale",
         note="Studio di progettazione edile a Caltanissetta.",
         sito="https://www.studiorumeo.com",
         proponi=["Biemme", "Gerflor", "Ferrero Legno"],
         perche="Studio tecnico radicato sul territorio: presidio utile per ristrutturazioni e nuove costruzioni.",
         t=3),
    dict(n="C+C Cucuzza Cavallaro Architetti", citta="Gela", prov="Caltanissetta",
         anno=None, chi="Cucuzza e Cavallaro",
         spec="Architettura e interior design, edifici residenziali",
         note="Studio di architettura e interior design attivo a Gela su progettazione residenziale. Sito ufficiale non individuato; presente su piattaforme di settore.",
         sito=None,
         proponi=["Gerflor", "Ferrero Legno", "Biemme"],
         perche="Riferimento sull'area di Gela per residenziale e interni: da agganciare alla prima visita.",
         t=3),
    dict(n="Studio Architetto Ciantia", citta="Piazza Armerina", prov="Enna",
         anno=None, chi="Arch. Ciantia",
         spec="Architettura e progettazione",
         note="Piazza Armerina, Via Mons. La Vaccara 24 — 94015 Enna. Tel. 370 1212833.",
         sito=None,
         proponi=["Biemme", "Gerflor", "Ferrero Legno"],
         perche="Uno dei pochi studi strutturati dell'ennese, su un territorio con forte patrimonio storico da recuperare.",
         t=3),
]

# ------------------------------------------------------------------ 3. PRIORITÀ per i nuovi
TIER = {
    # --- priorità 1 ---
    "Architrend Architecture": 1, "Moncada Rangel": 1, "Vincenzo Latina Architetto": 1,
    "Maria Giuseppina Grasso Cannizzo": 1, "Giuseppe Gurrieri Studio": 1,
    "Cottone+Indelicato Architetti": 1, "DFG Architetti Associati": 1,
    "Iraci Architetti": 1, "LAVICA studio": 1, "UZISA Hospitality Design": 1,
    "Studio GUM": 1, "Noi Studio Architettura": 1, "DAAA Haus": 1,
    # --- priorità 2 ---
    "bureau69 architects": 2, "ACA Amore Campione Architettura": 2, "Evolutive Studio": 2,
    "Studio Michele Sclafani": 2, "Sebastiano Adragna Architetti": 2, "Gilles+Arch": 2,
    "LineaTstudio": 2, "Bruno Messina": 2, "A.R.I.A. Progetti": 2,
    "Darch2": 2, "Architecture Lab Studio": 2, "Madremateria": 2,
    "Ad'A Atelier d'Architettura": 2, "Studio BOMA - Maurizio Oddo": 2,
    # --- priorità 3 ---
    "M+C De Francesco Architetti": 3, "N38lab - N38 Laboratorio di Architettura": 3,
    "AalCubo Studio": 3, "Studio D'Aleo S.r.l.": 3, "OpenWorks Architetture": 3,
    "LAB.DESIGN": 3, "Salvatore Catanzaro Architetto": 3, "Kudra Srl - Giuseppe Grizzaffi": 3,
}
PROV_CLEAN = re.compile(r'\s*\([A-Z]{2}\)\s*$')
DUPLICATI = {"ACA - Amore Campione Architettura"}   # duplicato di ACA Amore Campione

# ------------------------------------------------------------------ 4. UNIONE
palermo = json.load(open(f'{BASE}/dati-palermo.json', encoding='utf-8'))
tutti = list(palermo)
visti = {re.sub(r'\W+', '', s['n'].lower()) for s in palermo}
scartati = []

for s in NUOVI:
    nome = s['nome'].strip()
    if nome in DUPLICATI:
        scartati.append(nome); continue
    chiave = re.sub(r'\W+', '', nome.lower())
    if chiave in visti:
        scartati.append(nome); continue
    visti.add(chiave)
    tutti.append(dict(
        n=nome,
        citta=s.get('citta') or s.get('provincia', ''),
        prov=PROV_CLEAN.sub('', s.get('provincia') or s.get('prov', '')).strip(),
        anno=s.get('anno') or None,
        chi=s.get('chi', ''), spec=s.get('spec', ''), note=s.get('note', ''),
        sito=s.get('sito'), proponi=(s.get('proponi') or [])[:4],
        perche=s.get('perche', ''), t=TIER.get(nome, 3),
    ))

for s in CL_EN:
    tutti.append(s)

tutti.sort(key=lambda x: (x['prov'], x.get('t', 3), x['n']))
json.dump(tutti, open(f'{BASE}/dati.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

import collections
per = collections.Counter(s['prov'] for s in tutti)
tier = collections.Counter(s.get('t', 3) for s in tutti)
print(f"TOTALE: {len(tutti)} studi")
print(f"Palermo {len(palermo)} + nuovi {len(tutti)-len(palermo)} (scartati {len(scartati)}: {scartati})")
print("\nper provincia:")
for p, c in sorted(per.items(), key=lambda x: -x[1]):
    print(f"  {p:<14} {c:>3}")
print("\nper priorità:", dict(sorted(tier.items())))
print("senza sito:", sum(1 for s in tutti if not s['sito']))
print("senza anno:", sum(1 for s in tutti if not s.get('anno')))
