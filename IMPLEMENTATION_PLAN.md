# Master-Plan: Conversion- & SEO-Optimierung andreasstehmann-links

**Stand**: 2026-11-17  
**Status**: Phase 0 (Bestandsaufnahme) ✓ — Phase 1 (Startseite) startet jetzt

---

## Bestandsaufnahme (Phase 0) — ABGESCHLOSSEN

### Projektstruktur
- `/opt/data/andreasstehmann-links/` — Hauptprojekt
- `build_site.py` (58KB) — Statischer Site-Generator, alle Templates inline
- `daily_maintenance.py` (271 Zeilen) — Autonome tägliche Pflege (Cron: 06:00 UTC)
- `data/niche_products.json` — 94 Nischen, je 8 Produkte (ASIN, Titel, Preis, Bild, Affiliate-Link)
- `output/` — Generierte Site (110 Dateien: 94 Nischen + 7 Kategorien + 4 Legal + Index/Sitemap/Robots)
- `assets/style.css` (13KB), `assets/main.js` (2KB) — Frontend

### Aktuelle Schwachstellen
| Bereich | Problem |
|---------|---------|
| **Startseite** | Nur Hero + Kategorien-Grid + Footer — keine Vertrauens-Elemente, keine Saison/Guide/Produkt-Highlights, keine Newsletter-Conversion |
| **Produktkarten** | Minimal: Bild, Titel, Preis, CTA — keine Features, keine Problemlösung, keine Einordnung (Einsteiger/Premium), kein Affiliate-Hinweis auf Karte |
| **Kaufberatungen** | Fehlen komplett — nur Nischen-Seiten als Produkt-Listen |
| **SEO** | Title/Meta generisch, keine Breadcrumb, kein JSON-LD, keine Canonical, H1-H3 inkonsistent, Bilder ohne echte Alt-Texte |
| **Conversion** | Ein CTA pro Karte, keine Empfehlungs-Boxen, keine saisonalen Welten, keine Geschenkideen |
| **Vertrauen/Recht** | Impressum/Datenschutz Platzhalter (Musterstraße), Amazon-Hinweis nur im Impressum, keine Cookie-Info |
| **Newsletter** | Nicht vorhanden |
| **Tracking** | Nicht vorhanden |
| **Design** | Funktional, aber nicht "Premium Lifestyle Magazin" — Typografie, spacing, Bildqualität verbesserbar |

### Erhaltenswerte Infrastruktur
- ✅ `build_site.py` als Generator (Templates modularisieren, nicht neu schreiben)
- ✅ `daily_maintenance.py` + Cron-Jobs (unverändert lassen)
- ✅ `data/niche_products.json` + Affiliate-Tag `balu17051-21`
- ✅ GitHub Pages Deploy (funktioniert)
- ✅ 94 Nischen-Seiten + 7 Kategorie-Seiten (URLs beibehalten)

---

## 12-Phasen-Plan

### Phase 1: Startseite vollständig optimieren (AKTUELL)
**Ziel**: Premium-Lifestyle-Magazin-Feeling, Vertrauen, schnelle Navigation, Newsletter-Conversion
**Deliverables**: Neuer `index.html` Template in `build_site.py`
**Tests**: Build → Mobile Check → Affiliate-Links prüfen → Internal Links prüfen

### Phase 2: Produktkarten auf Conversion optimieren
**Ziel**: Hochwertige Karten mit Features, Problemlösung, Einordnung (Einsteiger/Preis-Leistung/Premium), sichtbarem Affiliate-Hinweis
**Deliverables**: Neues Produktkarten-Template + Sortier-Logik in `build_site.py`
**Tests**: Build → Nischen-Seiten prüfen → Kategorie-Seiten prüfen

### Phase 3: Hochwertige Kaufberatungen entwickeln
**Ziel**: Für jede der 7 Themenwelten 3 Kaufberatungen (insgesamt 21 Artikel)
**Deliverables**: Neue Template-Typ "Guide" in `build_site.py`, Content-Erstellung (KI-unterstützt via `generate_blog_content.py` adaptiert)
**Tests**: Build → Guide-Seiten prüfen → Interne Verlinkung prüfen

### Phase 4: SEO & technische Optimierung
**Ziel**: Individuelle Title/Meta, H1-H3 Struktur, Breadcrumb, JSON-LD (Product, Article, BreadcrumbList), Canonical, Bild-Optimierung, Core Web Vitals
**Deliverables**: SEO-Modul in `build_site.py`, aktualisierte Templates
**Tests**: Build → Lighthouse/PageSpeed → Structured Data Testing Tool → Sitemap/Robots prüfen

### Phase 5: Conversion-Strategie umsetzen
**Ziel**: Empfehlungs-Boxen in Artikeln, saisonale Produktwelten, Geschenkideen, situative Listen, Newsletter-Integration
**Deliverables**: Komponenten in `build_site.py`, Daten-Struktur für Saisons/Anlässe
**Tests**: Build → User-Flow prüfen → Affiliate-Klick-Pfade validieren

### Phase 6: Vertrauen & Rechtssicherheit
**Ziel**: Echtes Impressum, vollständige Datenschutz, Cookie-Hinweis, Amazon-Partner-Hinweis prominent, Werbekennzeichnung auf jeder Karte
**Deliverables**: Legal-Templates aktualisieren, Cookie-Banner (optional, da keine Cookies), Affiliate-Disclosure auf allen kommerziellen Seiten
**Tests**: Rechtliche Prüfung → Mobile Darstellung Legal-Seiten

### Phase 7: Newsletter & Kundenbindung
**Ziel**: Anmelde-Formular (Double-Opt-In ready), Lead-Magnet (z.B. "Wochenend-Inspiration"), Versand-Vorbereitung
**Deliverables**: Newsletter-Section auf Startseite + Nischen-Seiten, Formular-Endpoint-Vorbereitung
**Tests**: Formular-Funktion → Datenschutz-Konformität

### Phase 8: Messbarkeit & Analyse
**Ziel**: Datenschutzkonformes Tracking (Matomo/Plausible selbstgehostet oder GA4 minimal), Event-Tracking für Affiliate-Klicks, Newsletter-Anmeldungen
**Deliverables**: Tracking-Snippet in `build_site.py`, Event-Data-Layer
**Tests**: Netzwerk-Tab prüfen → Events feuern → Report-Integration vorbereiten

### Phase 9: Design & technische Qualität
**Ziel**: Mobile First Excellence, Performance (kein unnötiges JS, kritisches CSS inline), Barrierefreiheit (WCAG AA), konsistentes Design-System
**Deliverables**: `style.css` Refactor (Custom Properties, Fluid Typography, Container Queries), `main.js` minimieren
**Tests**: Lighthouse ≥ 90 alle Kategorien → Axe Accessibility → Cross-Device

### Phase 10: Tests & Deployment
**Ziel**: Vollständiger Regressionstest, bestehender Daily-Maintenance-Lauf erfolgreich
**Tests**: 
- Build ohne Fehler
- Alle 94 Nischen-Seiten rendern
- Alle 7 Kategorie-Seiten rendern
- Alle 21 Guide-Seiten rendern (neu)
- 4 Legal-Seiten rendern
- Sitemap/Robots korrekt
- Affiliate-Links enthalten Tag `balu17051-21`
- Interne Links keine 404
- Mobile Darstellung iPhone/Safari
- Daily Maintenance Script läuft durch (trocken)
- Git Push → GitHub Pages live

---

## Backup-Strategie (vor Phase 1)
```bash
cp -r /opt/data/andreasstehmann-links /opt/data/andreasstehmann-links.backup.$(date +%Y%m%d)
git -C /opt/data/andreasstehmann-links commit -am "Backup vor Master-Prompt Optimierung"
```

---

## Arbeitsweise
1. **Eine Phase nach der anderen** — Build & Test nach jeder Phase
2. **Modulare Änderungen** — Templates in `build_site.py` isoliert anpassen
3. **Keine Breaking Changes** — Bestehende URLs, Daten, Cron-Jobs unberührt
4. **Dokumentation** — Geänderte Dateien & Begründung in diesem Plan festhalten

---

## Nächster Schritt
**Phase 1 starten**: Startseite-Template in `build_site.py` vollständig neu gestalten gemäß Master-Prompt Anforderungen (12 Punkte: Hero, Headlines, CTAs, 7 Themenwelten, Saison, Guides, Produkt-Highlights, Vertrauen, Newsletter, Footer).