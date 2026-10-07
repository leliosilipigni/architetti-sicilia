#!/usr/bin/env python3
"""Genera la pagina 'Architetti di Sicilia' (data-driven).

Legge /data/architetti-sicilia/dati.json — lista di studi con schema:
  n, citta, prov, chi, anno, spec, note, sito, proponi[], perche, t
"""
import json
import os
import collections

BASE = '/data/architetti-sicilia'
STUDI = json.load(open(f'{BASE}/dati.json', encoding='utf-8'))

MANDANTI = ["Biemme", "Internorm", "Ditec", "Novoferm", "Ferrero Legno",
            "Gerflor", "Cherubini", "Roto", "Navello"]
COLORI = {"Biemme": "#4f8cff", "Internorm": "#ff8a4c", "Ditec": "#3ddc97", "Novoferm": "#f6c453",
          "Ferrero Legno": "#b98a5a", "Gerflor": "#8b7cff", "Cherubini": "#ff6b9d",
          "Roto": "#5ad1e6", "Navello": "#c9d24b"}

ORDINE = dict(
    nome="Consiglio Nazionale + i 9 Ordini provinciali siciliani",
    indirizzo="Palermo · Catania · Messina · Siracusa · Ragusa · Trapani · Agrigento · Caltanissetta · Enna",
    tel="", email="", sito="https://www.ordinearchitettipalermo.it",
)

studi = STUDI
n_tot = len(studi)
n1 = sum(1 for s in studi if s.get('t') == 1)
province = sorted({s['prov'] for s in studi}, key=lambda p: -sum(1 for x in studi if x['prov'] == p))
n_prov = len(province)

per_prov = collections.OrderedDict()
for p in province:
    per_prov[p] = [s for s in studi if s['prov'] == p]


def card(s):
    chips = "".join(
        f'<span class="chip" style="--c:{COLORI.get(m, "#889")}">{m}</span>' for m in s['proponi'])
    sito = (f'<a class="sito" href="{s["sito"]}" target="_blank" rel="noopener">'
            f'{s["sito"].replace("https://", "").replace("www.", "").rstrip("/")}</a>'
            if s['sito'] else '<span class="nosito">sito da verificare in visita</span>')
    anno = s['anno'] if s.get('anno') else '—'
    return f"""
    <article class="card" data-prov="{s['prov']}" data-tier="{s.get('t', 3)}"
      data-cerca="{s['n'].lower()} {s['citta'].lower()} {s['spec'].lower()} {' '.join(m.lower() for m in s['proponi'])}">
      <div class="c-head">
        <h3>{s['n']}</h3>
        <span class="tier t{s.get('t', 3)}">Priorità {s.get('t', 3)}</span>
      </div>
      <div class="citta">📍 {s['citta']}{'' if s['citta'].startswith(s['prov']) else ' · ' + s['prov']}</div>
      <dl class="meta">
        <div><dt>Dal</dt><dd>{anno}</dd></div>
        <div><dt>Chi</dt><dd>{s['chi']}</dd></div>
      </dl>
      <p class="spec">{s['spec']}</p>
      <p class="note">{s['note']}</p>
      <div class="why"><span>Perché vale una visita</span>{s['perche']}</div>
      <div class="proponi"><span class="lbl">Cosa proporre</span>{chips}</div>
      <div class="foot">{sito}</div>
    </article>"""


sezioni = []
for p in province:
    gruppo = per_prov[p]
    n_p1 = sum(1 for x in gruppo if x.get('t') == 1)
    cards = "\n".join(card(s) for s in sorted(gruppo, key=lambda x: (x.get('t', 3), x['n'])))
    sezioni.append(f"""
  <section class="prov-block" data-prov="{p}">
    <h2>{p}<span class="line"></span>
      <span class="h-count">{len(gruppo)} studi · {n_p1} di priorità alta</span>
    </h2>
    <div class="grid">
{cards}
    </div>
  </section>""")

HTML = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Architetti di Sicilia · Mappa commerciale Ellesse Rappresentanze</title>
<meta name="description" content="{n_tot} studi di architettura in Sicilia da visitare per promuovere serramenti, porte, pavimenti, tende e chiusure automatiche. A cura di Ellesse Rappresentanze.">
<meta property="og:title" content="Architetti di Sicilia · Mappa commerciale Ellesse">
<meta property="og:description" content="{n_tot} studi di architettura siciliani, con specializzazione e prodotti da proporre.">
<meta property="og:type" content="website">
<style>
  :root {{
    --bg:#0c1220; --bg2:#121a2c; --card:#161f36; --border:rgba(255,255,255,.09);
    --txt:#eef2fa; --txt2:#a8b4cc; --dim:#7c88a3; --orange:#ff7a2f; --green:#3ddc97;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html{{-webkit-text-size-adjust:100%}}
  body{{
    background:radial-gradient(1200px 600px at 80% -10%,#1d2a4a 0%,var(--bg) 55%) no-repeat,var(--bg);
    color:var(--txt); font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
    line-height:1.55; padding-bottom:60px;
  }}
  .wrap{{max-width:1120px;margin:0 auto;padding:0 16px}}

  header{{padding:44px 0 30px;border-bottom:1px solid var(--border)}}
  .brand{{display:flex;align-items:center;gap:11px;margin-bottom:22px}}
  .mark{{width:40px;height:40px;border-radius:11px;flex:none;
    background:linear-gradient(135deg,var(--orange),#ff4d6d);
    display:grid;place-items:center;font-weight:900;font-size:15px;color:#fff;letter-spacing:-.5px}}
  .brand b{{font-size:15px;letter-spacing:.2px}}
  .brand small{{display:block;color:#9aa8c4;font-size:12px;font-weight:500}}
  h1{{font-size:clamp(26px,6vw,44px);line-height:1.1;letter-spacing:-1px;font-weight:850}}
  h1 em{{font-style:normal;color:var(--orange)}}
  .sub{{color:var(--txt2);margin-top:14px;font-size:clamp(14px,3.6vw,16.5px);max-width:68ch}}

  .kpi{{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:10px;margin-top:26px}}
  .k{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px 16px}}
  .k b{{display:block;font-size:26px;font-weight:850;letter-spacing:-.6px}}
  .k span{{color:#9aa8c4;font-size:11.5px;text-transform:uppercase;letter-spacing:.7px;font-weight:700}}

  .toolbar{{position:sticky;top:0;z-index:30;background:rgba(12,18,32,.94);
    backdrop-filter:blur(14px);border-bottom:1px solid var(--border);padding:11px 0}}
  .toolbar .wrap{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
  .f{{background:var(--card);border:1px solid var(--border);color:var(--txt2);
    padding:8px 14px;border-radius:999px;font-size:13px;font-weight:650;cursor:pointer;transition:.15s;
    font-family:inherit}}
  .f:hover{{border-color:var(--orange);color:var(--txt)}}
  .f[aria-pressed="true"]{{background:var(--orange);border-color:var(--orange);color:#fff}}
  #q{{flex:1;min-width:160px;background:var(--card);border:1px solid var(--border);color:var(--txt);
    padding:9px 15px;border-radius:999px;font-size:13.5px;font-family:inherit;outline:none}}
  #q:focus{{border-color:var(--orange)}}
  #q::placeholder{{color:#8b97b1;opacity:1}}
  .row-lbl{{width:100%;color:var(--dim);font-size:10px;font-weight:800;
    text-transform:uppercase;letter-spacing:.8px;margin-top:2px}}

  h2{{font-size:clamp(20px,4.8vw,27px);letter-spacing:-.5px;margin:44px 0 0;font-weight:850;
    display:flex;flex-wrap:wrap;align-items:baseline;gap:12px}}
  h2 .line{{display:block;height:3px;width:46px;background:var(--orange);border-radius:2px;
    margin-top:10px;flex-basis:100%;order:9}}
  .h-count{{font-size:12.5px;font-weight:600;color:var(--dim)}}
  .h-note{{color:var(--txt2);font-size:14px;margin-top:12px;max-width:72ch}}

  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:14px;margin-top:20px}}
  .card{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:18px;
    display:flex;flex-direction:column;gap:10px;transition:.18s}}
  .card:hover{{border-color:rgba(255,122,47,.42);transform:translateY(-2px)}}
  .c-head{{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}}
  .c-head h3{{font-size:16.5px;letter-spacing:-.3px;line-height:1.25;font-weight:800}}
  .tier{{font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.6px;
    padding:4px 9px;border-radius:999px;white-space:nowrap;flex:none}}
  .t1{{background:rgba(255,122,47,.16);color:#ffa06a;border:1px solid rgba(255,122,47,.34)}}
  .t2{{background:rgba(79,140,255,.14);color:#8fb4ff;border:1px solid rgba(79,140,255,.32)}}
  .t3{{background:rgba(255,255,255,.06);color:var(--dim);border:1px solid var(--border)}}
  .citta{{font-size:11.5px;color:var(--dim);font-weight:650}}
  .meta{{display:flex;flex-wrap:wrap;gap:14px;font-size:12.5px}}
  .meta dt{{color:var(--dim);font-size:10px;text-transform:uppercase;letter-spacing:.6px;font-weight:750}}
  .meta dd{{color:var(--txt2)}}
  .spec{{font-size:13.5px;color:var(--txt);font-weight:600}}
  .note{{font-size:12.8px;color:var(--txt2)}}
  .why{{font-size:12.8px;color:var(--txt2);background:rgba(61,220,151,.07);
    border-left:2px solid var(--green);border-radius:0 9px 9px 0;padding:9px 12px}}
  .why span{{display:block;color:var(--green);font-size:10px;font-weight:800;
    text-transform:uppercase;letter-spacing:.6px;margin-bottom:3px}}
  .proponi{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
  .proponi .lbl{{color:var(--dim);font-size:10px;font-weight:800;
    text-transform:uppercase;letter-spacing:.6px;width:100%}}
  .chip{{font-size:11.5px;font-weight:700;padding:3px 10px;border-radius:999px;
    color:var(--c);background:color-mix(in srgb,var(--c) 15%,transparent);
    border:1px solid color-mix(in srgb,var(--c) 38%,transparent)}}
  .foot{{margin-top:auto;padding-top:11px;border-top:1px solid var(--border)}}
  .sito{{color:var(--orange);font-size:12.5px;text-decoration:none;font-weight:650;word-break:break-all}}
  .sito:hover{{text-decoration:underline}}
  .nosito{{color:var(--dim);font-size:12px;font-style:italic}}

  .panel{{background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:20px;margin-top:20px}}
  .steps{{list-style:none;display:grid;gap:13px}}
  .steps li{{display:flex;gap:13px;font-size:14px;color:var(--txt2)}}
  .steps b{{flex:none;width:25px;height:25px;border-radius:8px;background:var(--orange);
    color:#fff;display:grid;place-items:center;font-size:12.5px;font-weight:850}}
  .mandanti{{display:flex;flex-wrap:wrap;gap:7px;margin-top:4px}}
  .ordine{{display:grid;gap:5px;font-size:14px;color:var(--txt2)}}
  .ordine a{{color:var(--orange);text-decoration:none}}

  footer{{margin-top:46px;padding-top:22px;border-top:1px solid var(--border);
    color:var(--dim);font-size:12.5px;display:grid;gap:5px}}
  footer b{{color:var(--txt2)}}
  .empty{{display:none;padding:40px 0;color:var(--dim);font-size:14px}}

  @media (max-width:560px){{ .grid{{grid-template-columns:1fr}} header{{padding:32px 0 22px}} }}
  @media print{{
    body{{background:#fff;color:#111}} .toolbar{{display:none}}
    .card,.panel,.k{{border-color:#ddd;background:#fff;break-inside:avoid}}
    .card h3,.spec{{color:#111}} .note,.why{{color:#333}} h1 em{{color:#c2410c}} .citta{{color:#666}}
  }}
</style>
</head>
<body>

<header><div class="wrap">
  <div class="brand">
    <div class="mark">ER</div>
    <div><b>Ellesse Rappresentanze</b><small>Serramenti · Porte · Pavimenti · Schermature · Chiusure</small></div>
  </div>
  <h1>Architetti di <em>Sicilia</em><br>mappa per la rete commerciale</h1>
  <p class="sub"><b>{n_tot} studi di architettura</b> in tutta la Sicilia, da andare a trovare.
    Per ciascuno: chi sono, su cosa progettano, perché vale una visita e
    <b>quali dei nostri prodotti proporre per primi</b>. Ordinati per provincia,
    con filtro per priorità e ricerca.</p>
  <div class="kpi">
    <div class="k"><b>{n_tot}</b><span>studi in mappa</span></div>
    <div class="k"><b>{n_prov}</b><span>province</span></div>
    <div class="k"><b>{n1}</b><span>priorità alta</span></div>
    <div class="k"><b>{len(MANDANTI)}</b><span>mandanti</span></div>
  </div>
</div></header>

<div class="toolbar"><div class="wrap">
  <span class="row-lbl">Priorità</span>
  <button class="f" data-t="0" aria-pressed="true">Tutte</button>
  <button class="f" data-t="1" aria-pressed="false">Priorità 1</button>
  <button class="f" data-t="2" aria-pressed="false">Priorità 2</button>
  <button class="f" data-t="3" aria-pressed="false">Priorità 3</button>
  <input id="q" type="search" placeholder="Cerca studio, città o prodotto…" autocomplete="off">
  <span class="row-lbl">Provincia</span>
  <button class="f prov" data-p="" aria-pressed="true">Tutte</button>
  {"".join(f'<button class="f prov" data-p="{p}" aria-pressed="false">{p} <small style="opacity:.6">{len(per_prov[p])}</small></button>' for p in province)}
</div></div>

<main class="wrap">

  <h2 style="margin-top:34px">Come leggere le priorità<span class="line"></span></h2>
  <p class="h-note"><b>Priorità 1</b> = più volume potenziale e miglior incrocio con i nostri prodotti
    (hospitality, opere pubbliche, restauro, grandi residenziale). <b>Priorità 2</b> = buon fit sulle
    ristrutturazioni. <b>Priorità 3</b> = realtà da esplorare, spesso più facili da aprire come nuovo fornitore.
    Le priorità sono calate sul <b>fit con i nostri nove mandanti</b>, non su una classifica assoluta di prestigio.</p>
{"".join(sezioni)}
  <div class="empty" id="empty">Nessuno studio corrisponde al filtro.</div>

  <h2>Come approcciarli<span class="line"></span></h2>
  <div class="panel">
    <ol class="steps">
      <li><b>1</b><div><b>Vai con il disegno, non con il catalogo.</b> Portagli una sezione di serramento quotata
        e una portafinestra con le misure reali: gli architetti comprano dettaglio tecnico, non brochure.</div></li>
      <li><b>2</b><div><b>Parti dal prodotto che gli manca</b>, non dal tuo listino. Bar e ristoranti → pavimento
        e schermature. Restauro e centro storico → serramento in legno su misura.</div></li>
      <li><b>3</b><div><b>Chiedi il cantiere in corso, non il progetto futuro.</b> Una ristrutturazione già aperta
        ha decisioni da prendere questa settimana.</div></li>
      <li><b>4</b><div><b>Offriti come unico interlocutore.</b> Con nove mandati copri finestra, porta interna,
        porta automatica, pavimento, tenda e legno: è il vantaggio che un rivenditore singolo non ha.</div></li>
      <li><b>5</b><div><b>Raggruppa le visite per provincia</b>, non per studio. Un giro Catania–Siracusa–Ragusa
        rende molto più di tre trasferte separate.</div></li>
      <li><b>6</b><div><b>Torna ogni 4-6 settimane</b> con un aggiornamento vero (nuova finitura, nuovo sistema,
        una referenza appena posata). La seconda visita è quella che conta.</div></li>
    </ol>
  </div>

  <h2>Dove recuperare i contatti mancanti<span class="line"></span></h2>
  <div class="panel">
    <p class="h-note" style="margin-top:0">Gli Ordini provinciali pubblicano e aggiornano l'albo dei
      professionisti: è la via più rapida per email e telefono degli studi senza sito.</p>
    <div class="ordine" style="margin-top:14px">
      <div><b>{ORDINE['nome']}</b></div>
      <div>{ORDINE['indirizzo']}</div>
      <div><a href="{ORDINE['sito']}" target="_blank" rel="noopener">ordinearchitettipalermo.it</a> — da lì si
        raggiungono anche gli altri otto Ordini.</div>
    </div>
  </div>

  <h2>I mandanti che rappresentiamo<span class="line"></span></h2>
  <div class="panel">
    <div class="mandanti">
      {"".join(f'<span class="chip" style="--c:{COLORI[m]}">{m}</span>' for m in MANDANTI)}
    </div>
    <p class="h-note" style="margin-bottom:0">Nove mandanti tra serramenti, porte, chiusure automatiche,
      pavimenti resilienti, schermature solari e legno.</p>
  </div>

  <footer>
    <div><b>Fonti:</b> riviste e portali di settore (Archi&amp;Interiors, Divisare, Archilovers, Archello),
      siti ufficiali degli studi, Ordini degli Architetti provinciali.</div>
    <div>Informazioni tratte da fonti pubbliche; i recapiti degli studi senza sito sono da verificare alla prima visita.</div>
    <div style="margin-top:8px">A cura di <b>Ellesse Rappresentanze</b> · Letterio Silipigni · ottobre 2026</div>
  </footer>

</main>

<script>
(function(){{
  var grid=document.querySelectorAll('.prov-block, .card'),
      sezioni=[].slice.call(document.querySelectorAll('.prov-block')),
      cards=[].slice.call(document.querySelectorAll('.card')),
      q=document.getElementById('q'),
      empt=document.getElementById('empty'),
      bt=[].slice.call(document.querySelectorAll('.f[data-t]')),
      bp=[].slice.call(document.querySelectorAll('.f.prov')),
      tier=0, prov='';

  function apply(){{
    var s=(q.value||'').trim().toLowerCase(), vis=0;
    cards.forEach(function(c){{
      var okT = !tier || c.dataset.tier===String(tier);
      var okP = !prov || c.dataset.prov===prov;
      var okS = !s || c.dataset.cerca.indexOf(s)>-1;
      var ok = okT && okP && okS;
      c.style.display = ok ? '' : 'none';
      if(ok) vis++;
    }});
    sezioni.forEach(function(sez){{
      var n=[].slice.call(sez.querySelectorAll('.card')).filter(function(c){{ return c.style.display!=='none'; }}).length;
      sez.style.display = n ? '' : 'none';
      var hc=sez.querySelector('.h-count');
      if(hc) hc.textContent = n + ' studi visibili';
    }});
    empt.style.display = vis ? 'none' : 'block';
  }}
  bt.forEach(function(b){{ b.addEventListener('click', function(){{
    tier=parseInt(b.dataset.t,10);
    bt.forEach(function(x){{ x.setAttribute('aria-pressed', x===b?'true':'false'); }}); apply();
  }}); }});
  bp.forEach(function(b){{ b.addEventListener('click', function(){{
    prov=b.dataset.p;
    bp.forEach(function(x){{ x.setAttribute('aria-pressed', x===b?'true':'false'); }}); apply();
  }}); }});
  q.addEventListener('input', apply);
}})();
</script>
</body>
</html>
"""

open(f'{BASE}/index.html', 'w', encoding='utf-8').write(HTML)
print(f"scritto {BASE}/index.html — {len(HTML):,} caratteri")
print(f"studi {n_tot} · province {n_prov} · priorità 1: {n1}")
for p in province:
    print(f"  {p:<14} {len(per_prov[p]):>3} studi")
