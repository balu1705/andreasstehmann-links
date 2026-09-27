#!/usr/bin/env python3
"""Synchronisiert Landing-Gruppen mit dem echten Repo-Zustand:
- ergänzt Nischenseiten, die auf der Landing fehlen (Gruppen-Heuristik nach Keywords)
- korrigert 'X Empfehlungen'-Anzahlen auf die reale Zahl Amazon-Links der Seite
- Titel aus <h1> der Nischenseite
"""
import os, re, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NIC = os.path.join(ROOT, 'niches')
GRP_MAP = [  # (keyword-liste, gruppe) — Reihenfolge entscheidet
    (['k_che', 'kuche', 'koch', 'esstisch', 'heissluft', 'kaffee', 'aufbewahrung_k'], 'Küche & Haushalt'),
    (['bad', 'schlaf', 'wohn', 'deko', 'wand', 'licht', 'pflanze', 'gemuet', 'kleine_wohn', 'flur'], 'Zuhause'),
    (['parfum', 'duft', 'beauty', 'haut', 'haare', 'makeup', 'selfcare', 'massage', 'wellness', 'routinen'], 'Schönheit & Wohlbefinden'),
    (['geschenke', 'lego', 'spiel', 'advent', 'weihnacht', 'basteln', 'papa', 'mama', 'paar'], 'Geschenke & Hobby'),
    (['smart', 'tapo', 'strom', 'saugroboter', 'govee'], 'Zuhause'),
    (['fitness', 'sport', 'yoga', 'lauf'], 'Fitness & Sport'),
    (['hund', 'katze', 'haustier', 'pet'], 'Geschenke & Hobby'),
    (['kaffee', 'tee', 'gaeste'], 'Küche & Haushalt'),
    (['unterwegs', 'reise', 'tasche', 'waesche', 'ordnung', 'kleiderschrank'], 'Praktisch & Unterwegs'),
    (['garten', 'balkon', 'terrasse'], 'Praktisch & Unterwegs'),
    (['herbst', 'kuerbis', 'pilz', 'kaeschere', 'gemuetlich_ke'], 'Herbst-Saison'),
]

def _niche_info(slug):
    p = os.path.join(NIC, slug, 'index.html')
    if not os.path.exists(p):
        return None
    t = open(p, encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    title = H.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else slug.replace('-', ' ').title()
    n = len(re.findall(r'href="https://www\.amazon\.[^"]*/dp/', t))
    return title, n

def _gruppe(slug):
    s = slug.lower().replace('-', '_')
    for keys, g in GRP_MAP:
        if any(k in s for k in keys):
            return g
    return 'Mehr entdecken'

def sync_groups(groups):
    present = {t[0].strip('/').split('/')[-1] for _, ts in groups for t in ts}
    counts = {g[0]: g for g in groups}
    added, fixed = 0, 0
    for slug in sorted(os.listdir(NIC)):
        if not os.path.isdir(os.path.join(NIC, slug)):
            continue
        info = _niche_info(slug)
        if not info:
            continue
        title, n = info
        href = f'niches/{slug}'
        if slug not in present:
            gname = _gruppe(slug)
            tgt = counts.get(gname)
            if tgt is None:
                tgt = [gname, []]
                groups.append(tgt)
                counts[gname] = tgt
            tgt[1].append((href, title, f'{n} Empfehlungen'))
            present.add(slug)
            added += 1
        else:
            for _, ts in groups:
                for i, (a, t, s) in enumerate(ts):
                    if a.strip('/').split('/')[-1] == slug and 'Empfehlungen' in s:
                        want = f'{n} Empfehlungen'
                        if s != want:
                            ts[i] = (a, t, want)
                            fixed += 1
    print(f'niche_tool: +{added} ergänzt, {fixed} Anzahlen korrigiert')
    return groups
