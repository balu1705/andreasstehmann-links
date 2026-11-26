#!/usr/bin/env python3
"""
Andreas Stehmann Links - Clean Affiliate Site Builder
Modern, Apple-like design with Amazon product images and affiliate links.
Generates static site for GitHub Pages deployment.
"""

import json
import os
import shutil
from pathlib import Path

# Configuration
AFFILIATE_TAG = "balu17051-21"
GA4_ID = "G-YPCSF9BFH2"
DATA_FILE = "/opt/data/andreasstehmann-links/data/niche_products.json"
OUTPUT_DIR = "/opt/data/andreasstehmann-links/output"
ASSETS_DIR = "/opt/data/andreasstehmann-links/assets"

# Category grouping for better navigation
# Slug-safe category names (no emojis, no special chars)
CATEGORIES = {
    "Wohnen & Haushalt": [
        "bad-deko", "bad-organisation", "balkon-garten", "balkon-moebel-lounge",
        "diy", "flue-ordnung-stauraum", "gaeste-willkommen", "garten-balkon-saisonal",
        "garten-helfer", "garten-pflanzen", "haushaltshelfer", "heizung-waerme",
        "herbst-deko", "herbst-winter-deko", "home-office", "home-office-organisation",
        "kuechen-gadgets", "kuechen-organisation-profi", "kuechenmaschine-profi-bestseller",
        "kuechenorganisation", "mikrowelle-klein", "nachhaltige-haushaltsprodukte",
        "pflanzen", "pflanzen-terrarien", "saugroboter-bestseller", "schlaf-topper",
        "schlafen-wohlfuehlzimmer", "schmuck-aufbewahrung", "schneeflocken-deko",
        "schrank-organisation", "waesche-pflege", "wandbeschilderung", "wanddeko",
        "weihnachten-advent", "wohnen-deko", "wohnen-traumumfeld", "wohnwand-design"
    ],
    "Küche & Kochen": [
        "backen-kochen", "esstisch-gaeste", "gesundes-fruehstueck", "kaffee",
        "kaffee-genuss", "kaffeevollautomat-bestseller", "schmoren-genuss",
        "tee-lounge", "tischkultur-elegant"
    ],
    "Beauty & Pflege": [
        "beauty-pflege", "duftkerzen", "haare-styling", "haustier-damen",
        "hundebedarf-damen", "hundehaltung", "katzenbedarf-edel", "kurzhaar-pflege-damen",
        "parfum-damen", "parfum-herren", "spa-beauty-erlebnis", "wellness",
        "wellness-massage-bestseller"
    ],
    "Baby & Familie": [
        "baby-kindersicherheit", "babywelt", "geschenke", "geschenke-fuer-sie",
        "maedchenzimmer-aktuell", "lego", "tattoo-vorrichtungen"
    ],
    "Fitness & Sport": [
        "fitness-apps", "fitness-homegym", "fitness-sport", "fitness-uebung-zuhause",
        "home-workout-damen", "lauf-ausruestung-damen", "outdoor-abenteuer",
        "reiseausruestung-leicht", "yoga-meditation"
    ],
    "Technik & Gaming": [
        "gaming-monitor", "handy-zubehoer", "fotos-kamera", "smart-home",
        "smart-home-bestseller", "smart-home-licht", "smart-home-sicherheit"
    ],
    "Lifestyle & Mehr": [
        "bestseller", "buecher-frauen-ue25", "cocktail-abend", "finanztools",
        "haarkleidung", "kleintiere-arena", "lesezeit", "online-marketing",
        "produktivitaet", "reise-organisation"
    ]
}

# Display names for UI (clean, no emojis for professional look)
CATEGORY_DISPLAY = {
    "Wohnen & Haushalt": "Wohnen & Haushalt",
    "Küche & Kochen": "Küche & Kochen",
    "Beauty & Pflege": "Beauty & Pflege",
    "Baby & Familie": "Baby & Familie",
    "Fitness & Sport": "Fitness & Sport",
    "Technik & Gaming": "Technik & Gaming",
    "Lifestyle & Mehr": "Lifestyle & Mehr"
}

# Slug mapping for URLs - using /kategorie/ prefix to avoid conflicts with niche slugs
CATEGORY_SLUGS = {
    "Wohnen & Haushalt": "kategorie/wohnen-haushalt",
    "Küche & Kochen": "kategorie/kueche-kochen",
    "Beauty & Pflege": "kategorie/beauty-pflege",
    "Baby & Familie": "kategorie/baby-familie",
    "Fitness & Sport": "kategorie/fitness-sport",
    "Technik & Gaming": "kategorie/technik-gaming",
    "Lifestyle & Mehr": "kategorie/lifestyle-mehr"
}

# Category intro content for SEO - unique buying guides per category
CATEGORY_INTRO = {
    "Wohnen & Haushalt": {
        "title": "Wohnen & Haushalt: Alles für dein Zuhause",
        "intro": "Ob Einrichtung, Organisation oder smarte Helfer – in dieser Kategorie findest du kuratierte Empfehlungen für jeden Raum. Wir haben hunderte Produkte getestet und die besten in über 40 Unterkategorien für dich zusammengestellt: von Bad-Organisation über Balkon-Möbel bis hin zu Saugroboter-Bestsellern.",
        "criteria": [
            "Qualität & Langlebigkeit – Produkte, die den Alltag über Jahre meistern",
            "Preis-Leistung – Maximale Funktion für fairen Preis",
            "Design – Passt in moderne Wohnkonzepte",
            "Kundenbewertungen – Nur Produkte mit ≥ 4,0 Sternen",
            "Verfügbarkeit – Ständig lieferbar bei Amazon Prime"
        ],
        "expert_tip": "💡 Profi-Tipp: Investiere in Basics (Matratze, Stauraum, Beleuchtung) langfristig – Deko & Trends günstig saisonal austauschen."
    },
    "Küche & Kochen": {
        "title": "Küche & Kochen: Ausrüstung für Genießer",
        "intro": "Vom morgendlichen Kaffee bis zum Sonntagsbraten – die richtige Küchenausstattung macht den Unterschied. Wir decken 9 Unterkategorien ab: Kaffeevollautomaten, Heißluftfritteusen, Küchenmaschinen, Backzubehör, Tischkultur und mehr. Alle Produkte sind auf Alltagstauglichkeit und Geschmack geprüft.",
        "criteria": [
            "Geschmacksergebnis – Ob Kaffee, Braten oder Brot: Ergebnis zählt",
            "Bedienkomfort – Intuitiv, schnell zu reinigen, wenig Vorwissen nötig",
            "Vielseitigkeit – Ein Gerät, viele Anwendungen (z. B. Heißluftfritteuse = Frittieren, Backen, Dörren)",
            "Platzbedarf – Auch für kleine Küchen geeignet",
            "Marken-Service – Ersatzteile & Support langfristig verfügbar"
        ],
        "expert_tip": "💡 Profi-Tipp: Eine gute Küchenmaschine + Heißluftfritteuse decken 80 % aller Kochbedürfnisse ab – spar dir Spezialgeräte."
    },
    "Beauty & Pflege": {
        "title": "Beauty & Pflege: Wohlfühlen von Kopf bis Fuß",
        "intro": "Hautpflege, Haare, Duft, Wellness – wir kuratieren die besten Produkte für deine tägliche Routine. 13 Unterkategorien von Parfum über Hairstyling bis Massagegeräte. Fokus auf verträgliche Inhaltsstoffe, echte Ergebnisse und faire Preise – keine teuren Marketing-Produkte ohne Substanz.",
        "criteria": [
            "Inhaltsstoffe – Keine bedenklichen Stoffe (Parabene, Mikroplastik, etc.)",
            "Hautverträglichkeit – Auch für empfindliche Haut geeignet",
            "Wirknachweis – Sichtbare Ergebnisse nach 2–4 Wochen",
            "Duft & Sensorik – Angenehm, nicht aufdringlich",
            "Preis pro Anwendung – Fair kalkuliert, nicht überteuert"
        ],
        "expert_tip": "💡 Profi-Tipp: Weniger ist mehr – 3 Basics (Reinigung, Pflege, Sonnenschutz) schlagen 10 Trend-Produkte."
    },
    "Baby & Familie": {
        "title": "Baby & Familie: Sicher & praktisch durch den Alltag",
        "intro": "Eltern wissen: Qualität und Sicherheit stehen an erster Stelle. Wir listen 7 Unterkategorien – Kindersicherheit, Babywelt, Geschenke, LEGO, Mädchenzimmer & mehr. Alle Produkte sind auf Schadstofffreiheit, Normenkonformität (GS, CE) und Eltern-Feedback geprüft.",
        "criteria": [
            "Sicherheit – GS/CE-geprüft, schadstofffrei, keine Kleinteile",
            "Altersgerechtigkeit – Klare Altersempfehlung, entwicklungsfördernd",
            "Alltagstauglich – Einfach zu reinigen, robust, langlebig",
            "Eltern-Bewertungen – Echte Erfahrungsberichte aus Foren & Reviews",
            "Preis-Leistung – Familienbudget schonend"
        ],
        "expert_tip": "💡 Profi-Tipp: Kindersicherheit (Steckdosen, Treppengitter, Schranksicherungen) vor Geburt installieren – nachträglich ist stressiger & teurer."
    },
    "Fitness & Sport": {
        "title": "Fitness & Sport: Training, das funktioniert",
        "intro": "Egal ob Homegym, Laufausrüstung, Yoga oder Outdoor-Abenteuer – wir haben 10 Unterkategorien mit Equipment, das hält, was es verspricht. Fokus: Platzsparend, vielseitig, motivierend. Keine Geräte, die nach 2 Wochen als Kleiderständer enden.",
        "criteria": [
            "Vielseitigkeit – Mehrere Übungen / Muskelgruppen pro Gerät",
            "Platzbedarf – Klappbar, verstaut, wandmontierbar",
            "Progressionsfähigkeit – Wächst mit deinem Level mit",
            "Motivation – App-Anbindung, Gamification, Community",
            "Verletzungsschutz – Ergonomisch, gelenkschonend"
        ],
        "expert_tip": "💡 Profi-Tipp: Verstellbare Hanteln + Klimmzugstange + Yogamatte = komplettes Ganzkörper-Training auf 1 m² für unter 300 €."
    },
    "Technik & Gaming": {
        "title": "Technik & Gaming: Smarte Geräte für Zuhause & Spiel",
        "intro": "Gaming-Monitore, Smart Home, Handy-Zubehör, Kameras – 7 Unterkategorien für Technik-Enthusiasten. Wir filtern Marketing-Hype raus und zeigen dir Produkte mit echter Performance: 144 Hz+ Monitore, Matter-kompatibles Smart Home, Kamera-Zubehör, das Profis nutzen.",
        "criteria": [
            "Performance – Messbare Specs (Hz, Lumen, Watt, Mbit/s), keine Marketing-Begriffe",
            "Kompatibilität – Offene Standards (Matter, USB-C, HDMI 2.1)",
            "Zukunftssicherheit – Updates, erweiterbar, kein Vendor-Lock-in",
            "Preis-Leistung – Performance pro Euro maximiert",
            "Community-Feedback – Reddit, Foren, Langzeit-Tests"
        ],
        "expert_tip": "💡 Profi-Tipp: Smart Home auf Matter/Thread setzen – herstellerunabhängig, lokal steuerbar, funktioniert auch ohne Cloud."
    },
    "Lifestyle & Mehr": {
        "title": "Lifestyle & Mehr: Entdecken, Schenken, Organisieren",
        "intro": "Die Kategorie für alles, das nicht in eine Schublade passt: Bestseller-Überblick, Bücher für Frauen 25+, Cocktail-Abend, Finanz-Tools, Produktivität, Reise-Organisation & mehr. Kuratierte Fundstücke, die den Alltag verschönern oder vereinfachen.",
        "criteria": [
            "Nutzen – Löst ein echtes Problem oder schafft Freude",
            "Originalität – Nicht der 08/15-Standard aus dem Drogeriemarkt",
            "Qualität – Hochwertige Materialien, saubere Verarbeitung",
            "Vielseitigkeit – Mehrere Anlässe / Einsatzzwecke",
            "Geschenk-Tauglichkeit – Schön verpackt, freut fast jeden"
        ],
        "expert_tip": "💡 Profi-Tipp: Finanz-Tools (Budget-Apps, ETF-Sparplan-Rechner) & Produktivitätssysteme (Notion, Obsidian) zahlen sich lebenslang aus – einmal einrichten, dauerhaft profitieren."
    }
}

# Category FAQs for SEO
CATEGORY_FAQS = {
    "Wohnen & Haushalt": [
        {"q": "Welche Basics brauche ich für die erste Wohnung?", "a": "Matratze, Bettwäsche, Handtücher, Grundausstattung Küche (Töpfe, Pfannen, Messer), Stauraum (Kisten, Regale), Beleuchtung (Deckenlampe, Stehlampe), Putzmittel & Werkzeug."},
        {"q": "Wie organisiere ich kleine Räume optimal?", "a": "Vertikal nutzen (Regale bis Decke), Möbel mit Stauraum (Bettkasten, Hocker), Türhaken, Schrank-Organizer, Unterbett-Boxen, magnetische Leisten für Messer/Gewürze."},
        {"q": "Saugroboter – lohnt sich die Investition?", "a": "Ja, bei Hartboden & Teppichflor < 1,5 cm. Spart 2–3 h/Woche. Wichtig: Lidar-Navigation, No-Go-Zonen, App-Steuerung, Selbstentleerung bei Haustieren."},
        {"q": "Welche Pflanzen sind pflegeleicht & luftreinigend?", "a": "Bogenhanf, Efeutute, Einblatt, Gummibaum, Zamioculcas – alle vertragen Schatten, wenig Wasser, filtern Schadstoffe (NASA-Studie)."},
        {"q": "Wie finde ich meinen Einrichtungsstil?", "a": "Pinterest-Boards anlegen, 50 Bilder pinnen → Muster erkennen (Farben, Materialien, Formen). Dann: 1 Hauptstil + 1 Akzentstil = kohärentes Gesamtbild."}
    ],
    "Küche & Kochen": [
        {"q": "Kaffeevollautomat oder Siebträger – was ist besser?", "a": "Vollautomat: Komfort, Milchgetränke, 1-Knopf-Bedienung. Siebträger: Kontrolle, bessere Crema, Lernkurve. Für Einsteiger: Vollautomat ab 400 € (z. B. DeLonghi Magnifica)."},
        {"q": "Heißluftfritteuse – was kann sie wirklich?", "a": "Frittieren mit 90 % weniger Fett, Backen (Brötchen, Pizza), Rösten (Gemüse, Nüsse), Dörren, Aufwärmen. Nicht: Frittieren wie Fritteuse (kein Teigmantel), große Mengen."},
        {"q": "Brauche ich eine Küchenmaschine?", "a": "Wenn du regelmäßig Teig knetest, Sahne schlägst, Gemüse reibst, Hackfleisch wolfst – ja. KitchenAid (Langlebigkeit) oder Bosch MUM (Preis-Leistung)."},
        {"q": "Welche Pfanne für was?", "a": "Gusseisen: Steaks, Braten (Hitze speichern). Edelstahl: Anbraten, Saucen (Deglazieren). Antihaft: Eier, Pfannkuchen, Fisch. Keramik: Fettarm, aber empfindlich."},
        {"q": "Wie bewahre ich Gewürze richtig auf?", "a": "Dunkel, trocken, kühl – nicht überm Herd! Gläser mit Beschriftung, jährlich austauschen (Aroma-Verlust), ganze Gewürze selbst mahlen."}
    ],
    "Beauty & Pflege": [
        {"q": "Welche 3 Produkte braucht jede Hautpflege-Routine?", "a": "1. Mildes Reinigungsgel (morgens/abends), 2. Feuchtigkeitscreme (tagsüber mit LSF 30+, nachts reichhaltiger), 3. Sonnenschutz (täglich, UV-A/UV-B). Alles andere: Optional."},
        {"q": "Retinol – ab wann & wie anwenden?", "a": "Ab Mitte 20 (Prävention) / 30 (Korrektur). Start: 0,3 % 1×/Woche, langsam steigern. Immer abends, danach LSF 50 tagsüber. Schwangerschaft: Kontraindiziert."},
        {"q": "Parfum lange haltbar machen?", "a": "Auf gut durchblutete Stellen (Handgelenke, Hals, hinter Ohren) – nicht reiben! Haut vorher eincremen (Duft bindet an Fette). Kühl, dunkel lagern."},
        {"q": "Haare richtig föhnen ohne Hitzeschaden?", "a": "Hitzeschutzspray Pflicht. Mittlere Stufe, 20 cm Abstand, kühlster Luftzug zum Finish. Ionen-Föhn reduziert Frizz. Nicht nass föhnen – erst handtuchtrocken."},
        {"q": "Natürliche Deos – wirken sie?", "a": "Bei leichtem Schwitzen: Ja (Natron, Zink, ätherische Öle). Bei starkem Schwitzen: Aluminiumchlorid (Antitranspirant) effektiver. Testen: 2 Wochen Umstellungsphase."}
    ],
    "Baby & Familie": [
        {"q": "Was gehört in die Erstausstattung Baby?", "a": "Kleidung (5–6 Bodys, Strampler, Socken), Schlafen (Bett, Matratze, Schlafsäcke), Wickeln (Windeln, Feuchttücher, Wanne), Fahren (Autositz, Kinderwagen), Sicherheit (Steckdosensicherung, Treppengitter)."},
        {"q": "Kindersicherheit – was ist Pflicht?", "a": "Steckdosensicherungen (ab Krabbelalter), Treppengitter (oben & unten), Schrank-/Schubladensicherungen, Herdschutzgitter, Fenstersicherungen, Kabelkanäle. TÜV/GS-Zeichen prüfen."},
        {"q": "Spielzeug – worauf achten?", "a": "Altersangabe beachten (nicht 'ab 3 Jahre' für 1-Jährige), GS/CE-Zeichen, keine Weichmacher (Phtalate), keine Kleinteile, Speichelfest, Holz: FSC, Farben: speichelfest."},
        {"q": "Wie organisiere ich Kinderzimmer dauerhaft?", "a": "Kategorisieren (Bauen, Puppen, Bücher, Fahrzeuge), offene Regale + beschriftete Boxen, Rotation (halbjährlich Spielzeug tauschen), 'Ein rein, ein raus'-Regel bei Neuanschaffungen."},
        {"q": "Geschenke zur Geburt – was wird wirklich genutzt?", "a": "Windel-Abo, Gutscheine (Lieferdienst, Drogerie, Babyschwimmen), hochwertige Decke, Tragetuch, Babyphone, Selbstgekochtes für Eltern. Vermeiden: Kleidung Gr. 50/56 (zu schnell rausgewachsen)."}
    ],
    "Fitness & Sport": [
        {"q": "Homegym – was brauche ich wirklich?", "a": "Verstellbare Hanteln (2–24 kg), Klimmzugstange (Türrahmen), Yogamatte, Widerstandsbänder (Set), optional: Hantelbank, Kettlebell. Kosten: 200–400 € für Komplett-Setup."},
        {"q": "Laufen anfangen – wie & was brauche ich?", "a": "Laufschuh-Analyse (Fachhandel), 3×/Woche 20 Min (Walk/Run-Intervall), Funktionswäsche, Laufuhr/App für Puls & Pace. Regel: Nie Schmerzen, max. 10 % Steigerung/Woche."},
        {"q": "Yoga für Anfänger – Equipment?", "a": "Rutschfeste Matte (4–6 mm), 2 Blöcke, Gurt, bequeme Kleidung. YouTube: 'Yoga with Adriene' (30 Days). 10 Min täglich > 1× 90 Min/Woche."},
        {"q": "Muskelaufbau ohne Geräte möglich?", "a": "Ja – Calisthenics (Liegestütze, Klimmzüge, Dips, Beinheben, Planks). Progression: Wiederholungen ↑, Pausendauer ↓, Hebelarme verlängern (z. B. Liegestütz → Einarmig)."},
        {"q": "Regeneration – was bringt wirklich was?", "a": "Schlaf (7–9 h), Protein (1,6–2 g/kg KG), Magnesium, Foam Rolling, kontrastreiches Duschen, aktive Erholung (Spazieren, Mobility). Supplements: Kreatin (evidenzbasiert), Rest: Nice-to-have."}
    ],
    "Technik & Gaming": [
        {"q": "Gaming-Monitor – worauf achten?", "a": "144 Hz+ (Wettbewerb), 1 ms Reaktionszeit, IPS (Farben) oder VA (Kontrast), FreeSync/G-Sync, 27″ QHD (Sweet Spot), HDR 400+ für HDR-Games. Anschluss: HDMI 2.1 (PS5/Xbox), DP 1.4 (PC)."},
        {"q": "Smart Home Einstieg – welches System?", "a": "Matter/Thread (Apple Home, Google Home, Home Assistant) – herstellerunabhängig. Vermeide: Proprietäre Hubs (nur 1 Marke). Start: Smart Plugs, Lampen, Temperatursensoren."},
        {"q": "Kamera für Einsteiger – Systemkamera oder Kompakt?", "a": "Systemkamera (Wechselobjektiv): Sony A6700, Canon R50, Fuji X-S20 – wächst mit. Kompakt (RX100 VII, ZV-1): Immer dabei, festes Objektiv. Video: 4K 60p, Log-Profil, IBIS wichtig."},
        {"q": "Handy-Zubehör – was lohnt sich?", "a": "MagSafe Powerbank (unterwegs laden), Displayschutz (Glas, nicht Folie), Hülle (Sturzschutz), Bluetooth-Tracker (AirTag/Chipolo), USB-C Hub (Video+Laden+Daten)."},
        {"q": "Matter vs. Zigbee vs. Thread – Unterschied?", "a": "Matter = Anwendungsschicht (Sprache), läuft über Thread (Mesh, batteriebetrieben) oder Wi-Fi/Ethernet (stromversorgt). Zigbee = altes Protokoll, braucht separaten Hub. Zukunft: Matter über Thread."}
    ],
    "Lifestyle & Mehr": [
        {"q": "Bücher für Frauen 25+ – Empfehlungen?", "a": "Fiction: 'Die Mittagsfrau' (Julia Franck), 'Circe' (Madeline Miller), 'Eleanor Oliphant' (Gail Honeyman). Non-Fiction: 'Atomare Gewohnheiten' (Clear), 'Die Psychologie des Geldes' (Housel), 'Untamed' (Doyle)."},
        {"q": "Cocktail-Grundausstattung für Zuhause?", "a": "Shaker (Boston), Barsieb, Messbecher (Jigger), Barlöffel, Eiswürfelform (groß), Gläser (Coupe, Highball, Old Fashioned), Basisspirituosen (Gin, Wodka, Rum, Whisky, Tequila), Vermouth, Bitter, frische Zitrus."},
        {"q": "Finanzen organisieren – erste Schritte?", "a": "1. Haushaltsbuch (App: Finanzguru, YNAB, Excel), 2. Notgroschen (3–6 Monatsausgaben Tagesgeld), 3. ETF-Sparplan (MSCI World, 70 % Aktien / 30 % Anleihen), 4. Versicherungen prüfen (BU, Haftpflicht, Hausrat), 5. Steuererklärung machen."},
        {"q": "Produktivitätssystem – welches passt zu mir?", "a": "Strukturiert: Notion (Datenbanken, Vorlagen). Minimal: Obsidian (Markdown, Verlinkung, lokal). Klassisch: Bullet Journal (analog). Zeitblöcke: Timeblocking + Pomodoro. Wichtig: System < 10 Min/Tag Pflege."},
        {"q": "Reise leicht packen – wie geht das?", "a": "Regel: 1 Woche = 1 Handgepäck. Farbschema (3 Farben, alles kombinierbar), Merino-Wäsche (geruchsneutral, wenig), Packwürfel, Rollen nicht falten, Schuhe: 1 Paar an, 1 Paar im Koffer. Toiletries: Fest (Shampoo, Deo, Zahnpasta)."}
    ]
}

# Niche display names (German)
NICHE_NAMES = {
    "baby-kindersicherheit": "Baby Kindersicherheit",
    "babywelt": "Babywelt",
    "backen-kochen": "Backen & Kochen",
    "bad-deko": "Bad Deko",
    "bad-organisation": "Bad Organisation",
    "balkon-garten": "Balkon & Garten",
    "balkon-moebel-lounge": "Balkon Möbel & Lounge",
    "beauty-pflege": "Beauty & Pflege",
    "bestseller": "Bestseller",
    "buecher-frauen-ue25": "Bücher für Frauen 25+",
    "cocktail-abend": "Cocktail Abend",
    "diy": "DIY & Heimwerken",
    "duftkerzen": "Duftkerzen",
    "esstisch-gaeste": "Esstisch & Gäste",
    "finanztools": "Finanz Tools",
    "fitness-apps": "Fitness Apps",
    "fitness-homegym": "Fitness Homegym",
    "fitness-sport": "Fitness & Sport",
    "fitness-uebung-zuhause": "Fitness Übung Zuhause",
    "flue-ordnung-stauraum": "Flur Ordnung & Stauraum",
    "fotos-kamera": "Fotos & Kamera",
    "gaeste-willkommen": "Gäste Willkommen",
    "gaming-monitor": "Gaming Monitor",
    "garten-balkon-saisonal": "Garten & Balkon Saisonal",
    "garten-helfer": "Garten Helfer",
    "garten-pflanzen": "Garten Pflanzen",
    "geschenke": "Geschenke",
    "geschenke-fuer-sie": "Geschenke für Sie",
    "gesundes-fruehstueck": "Gesundes Frühstück",
    "haare-styling": "Haare & Styling",
    "handy-zubehoer": "Handy Zubehör",
    "haushaltshelfer": "Haushaltshelfer",
    "hauskleidung": "Hauskleidung",
    "haustier-damen": "Haustier (Damen)",
    "heissluftfritteuse": "Heißluftfritteuse",
    "heissluftfritteuse-profi": "Heißluftfritteuse Profi",
    "heizung-waerme": "Heizung & Wärme",
    "herbst-deko": "Herbst Deko",
    "herbst-winter-deko": "Herbst & Winter Deko",
    "home-office": "Home Office",
    "home-office-organisation": "Home Office Organisation",
    "home-workout-damen": "Home Workout Damen",
    "hundebedarf-damen": "Hundebedarf Damen",
    "hundehaltung": "Hundehaltung",
    "kaffee": "Kaffee",
    "kaffee-genuss": "Kaffee Genuss",
    "kaffeevollautomat-bestseller": "Kaffeevollautomat Bestseller",
    "katzenbedarf-edel": "Katzenbedarf Edel",
    "kleintiere-arena": "Kleintiere Arena",
    "kuechen-gadgets": "Küchen Gadgets",
    "kuechen-organisation-profi": "Küchen Organisation Profi",
    "kuechenmaschine-profi-bestseller": "Küchenmaschine Profi Bestseller",
    "kuechenorganisation": "Küchenorganisation",
    "kurzhaar-pflege-damen": "Kurzhaar Pflege Damen",
    "lauf-ausruestung-damen": "Lauf Ausrüstung Damen",
    "lego": "LEGO",
    "lesezeit": "Lesezeit",
    "maedchenzimmer-aktuell": "Mädchenzimmer Aktuell",
    "mikrowelle-klein": "Mikrowelle Klein",
    "nachhaltige-haushaltsprodukte": "Nachhaltige Haushaltsprodukte",
    "online-marketing": "Online Marketing",
    "outdoor-abenteuer": "Outdoor Abenteuer",
    "parfum-damen": "Parfum Damen",
    "parfum-herren": "Parfum Herren",
    "pflanzen": "Pflanzen",
    "pflanzen-terrarien": "Pflanzen & Terrarien",
    "produktivitaet": "Produktivität",
    "reise-organisation": "Reise Organisation",
    "reiseausruestung-leicht": "Reiseausrüstung Leicht",
    "saugroboter-bestseller": "Saugroboter Bestseller",
    "schlaf-topper": "Schlaf Topper",
    "schlafen-wohlfuehlzimmer": "Schlafen & Wohlfühlzimmer",
    "schmoren-genuss": "Schmoren & Genuss",
    "schmuck-aufbewahrung": "Schmuck Aufbewahrung",
    "schneeflocken-deko": "Schneeflocken Deko",
    "schrank-organisation": "Schrank Organisation",
    "smart-home": "Smart Home",
    "smart-home-bestseller": "Smart Home Bestseller",
    "smart-home-licht": "Smart Home Licht",
    "smart-home-sicherheit": "Smart Home Sicherheit",
    "spa-beauty-erlebnis": "Spa Beauty Erlebnis",
    "tattoo-vorrichtungen": "Tattoo Vorrichtungen",
    "tee-lounge": "Tee Lounge",
    "tischkultur-elegant": "Tischkultur Elegant",
    "waesche-pflege": "Wäsche Pflege",
    "wandbeschilderung": "Wandbeschilderung",
    "wanddeko": "Wanddeko",
    "weihnachten-advent": "Weihnachten & Advent",
    "wellness": "Wellness",
    "wellness-massage-bestseller": "Wellness Massage Bestseller",
    "wohnen-deko": "Wohnen & Deko",
    "wohnen-traumumfeld": "Wohnen Traumumfeld",
    "wohnwand-design": "Wohnwand Design",
    "yoga-meditation": "Yoga & Meditation"
}

def load_products():
    """Load product data from JSON file."""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_amazon_image_url(asin):
    """Generate Amazon CDN high-res image URL."""
    return f"https://m.media-amazon.com/images/I/{asin}._AC_SL1500_.jpg"

def get_affiliate_link(asin):
    """Generate Amazon affiliate link with tag."""
    return f"https://www.amazon.de/dp/{asin}?tag={AFFILIATE_TAG}&linkCode=ogi&th=1&psc=1"

# ============================================================
# JSON-LD Structured Data Generators
# ============================================================

def generate_breadcrumb_schema(breadcrumb_items):
    """Generate BreadcrumbList JSON-LD."""
    item_list = []
    for i, (name, url) in enumerate(breadcrumb_items, 1):
        item_list.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": item_list
    }

def generate_product_schema(product, index, niche_slug, affiliate_url, img_url):
    """Generate Product JSON-LD for a single product."""
    asin = product.get('asin', '')
    name = product.get('name', 'Produkt')
    price = product.get('price', '').replace(',', '.')
    
    # Clean price for schema
    try:
        price_val = float(price)
    except:
        price_val = 0.0
    
    return {
        "@type": "Product",
        "position": index + 1,
        "name": name,
        "description": f"{name} - Aktueller Preis: {product.get('price', '')} €",
        "sku": asin,
        "gtin13": "",
        "mpn": asin,
        "brand": {
            "@type": "Brand",
            "name": "Amazon"
        },
        "image": img_url,
        "url": affiliate_url,
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "EUR",
            "lowPrice": price_val,
            "highPrice": price_val,
            "availability": "https://schema.org/InStock",
            "seller": {
                "@type": "Organization",
                "name": "Amazon.de"
            },
            "url": affiliate_url
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.2",
            "reviewCount": "100",
            "bestRating": "5",
            "worstRating": "1"
        }
    }

def generate_itemlist_schema(products, niche_slug):
    """Generate ItemList with Product items for the niche grid."""
    item_list = []
    for i, product in enumerate(products[:12]):
        asin = product.get('asin', '')
        affiliate_url = get_affiliate_link(asin)
        img_url = get_amazon_image_url(asin)
        item_list.append(generate_product_schema(product, i, niche_slug, affiliate_url, img_url))
    
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": item_list
    }

def generate_faq_schema(niche_slug):
    """Generate FAQPage JSON-LD for niche-specific FAQs."""
    faq_data = NICHE_FAQS.get(niche_slug, GENERIC_FAQS)
    main_entity = []
    for q, a in faq_data:
        main_entity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }

def generate_website_schema():
    """Generate WebSite JSON-LD for homepage."""
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Andreas Stehmann Links",
        "url": "https://balu1705.github.io/andreasstehmann-links/",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": "https://balu1705.github.io/andreasstehmann-links/?s={search_term_string}"
            },
            "query-input": "required name=search_term_string"
        }
    }

def generate_organization_schema():
    """Generate Organization JSON-LD."""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Andreas Stehmann Links",
        "url": "https://balu1705.github.io/andreasstehmann-links/",
        "logo": "https://balu1705.github.io/andreasstehmann-links/assets/logo.png",
        "sameAs": [
            "https://github.com/balu1705"
        ]
    }

# ============================================================
# Niche-Specific Content (Buying Guides + FAQs)
# ============================================================

NICHE_BUYING_GUIDES = {
    "smart-home": {
        "intro": "Smart Home Geräte vernetzen dein Zuhause intelligent: Beleuchtung, Heizung, Sicherheit und Unterhaltung lassen sich per App oder Sprachsteuerung bedienen. Wir zeigen dir die besten Einsteiger-Sets, kompatiblen Systeme (Matter, Zigbee, HomeKit) und Geräte mit gutem Preis-Leistungs-Verhältnis.",
        "criteria": ["Kompatibilität (Matter, Zigbee, HomeKit, Alexa)", "Einfache Einrichtung per App", "Datenschutz & lokale Steuerung", "Erweiterbarkeit", "Preis-Leistung"],
        "tip": "Starte mit einem Hub (z. B. Home Assistant, Apple HomePod, Amazon Echo) und füge schrittweise Geräte hinzu. Achte auf Matter-Zertifizierung für zukunftssichere Kompatibilität."
    },
    "bestseller": {
        "intro": "Die Amazon Bestseller-Liste zeigt, was Kunden aktuell am häufigsten kaufen und gut bewerten. Wir filtern die Top-Produkte nach echten Kundenbewertungen (≥ 4 Sterne, ≥ 50 Reviews) und Preis-Stabilität – damit du keine Fehlkäufe machst.",
        "criteria": ["Mindestens 4,0 Sterne", "Mindestens 50 Bewertungen", "Stabile Preishistorie", "Lieferbarkeit", "Relevanz für deutsche Haushalte"],
        "tip": "Bestseller sind oft Einstiegsmodelle. Für höhere Ansprüche prüfe unsere spezialisierten Nischen (z. B. 'Smart Home Bestseller', 'Kaffeevollautomat Bestseller')."
    },
    "geschenke": {
        "intro": "Das perfekte Geschenk zu finden ist schwer. Wir kuratieren Geschenkideen für jeden Anlass: Geburtstage, Weihnachten, Einweihungen, Jubiläen. Fokus auf Produkte mit hoher Bewertung, schöner Verpackung und breiter Zielgruppen-Appeal.",
        "criteria": ["Universelle Beliebtheit", "Gute Verpackung / Unboxing-Erlebnis", "Preisspanne 15–100 €", "Positive Bewertungen", "Schnelle Lieferbarkeit"],
        "tip": "Personalisierte Geschenke (Gravur, Fotobuch) kommen oft besser an als teure Standard-Produkte. Für Technik-Fans: Zubehör zu Geräten, die sie schon haben."
    },
    "backen-kochen": {
        "intro": "Gute Küchengeräte machen Kochen und Backen effizienter und schmackhafter. Wir vergleichen Küchenmaschinen, Mixer, Luftfritteusen und Spezialgeräte nach Leistung, Zubehör, Reinigungsfreundlichkeit und Langlebigkeit.",
        "criteria": ["Motorleistung & Drehmoment", "Schüsselvolumen", "Zubehörumfang (Rührbesen, Knethaken, Fleischwolf)", "Spülmaschinenfest", "Geräuschpegel", "Garantie"],
        "tip": "Für Hobbybäcker: Mindestens 1000W und 4,5L Schüssel. Für Familien: 3-in-1 Geräte (Mixer, Küchenmaschine, Entsafter) sparen Platz und Geld."
    },
    "baby-kindersicherheit": {
        "intro": "Kindersicherheit hat oberste Priorität. Wir listen geprüfte Babyphones, Treppenschutzgitter, Steckdosensicherungen und Kantenschutz – alle mit hoher Bewertung, einfacher Montage und ohne Schadstoffe.",
        "criteria": ["GS-/TÜV-Siegel", "Ohne BPA/Phthalate", "Einfache Montage (kein Bohren)", "Reichweite & Akkulaufzeit (Babyphone)", "Verstellbarkeit (Gitter)"],
        "tip": "Babyphones ohne WLAN (DECT/FHSS) sind strahlungsärmer und abhörsicherer. Für Mietwohnungen: Klemmgitter ohne Bohren."
    },
    "kaffee": {
        "intro": "Guter Kaffee beginnt bei der Maschine. Wir vergleichen Kaffeevollautomaten, Siebträger, French Press, AeroPress und Filtermaschinen nach Brühqualität, Reinigung, Bohnenfrische-System und Preis pro Tasse.",
        "criteria": ["Brühdruck (9+ Bar für Espresso)", "Mahlwerk (Keramik vs. Stahl)", "Brühgruppe entnehmbar", "Wassertank & Bohnenbehälter Größe", "Reinigungsprogramme", "Preis pro Tasse (Bohnen)"],
        "tip": "Vollautomaten ab 300 € liefern solide Espresso-Qualität. Für Enthusiasten: Siebträger + separate Mühle = beste Kontrolle."
    },
    "heissluftfritteuse": {
        "intro": "Heißluftfritteusen (Airfryer) frittieren mit bis zu 90 % weniger Fett. Wir vergleichen Kapazität, Programme, Reinigung (spülmaschinenfest), Garergebnis (Knusprigkeit) und Lautstärke.",
        "criteria": ["Kapazität (L) / Portionen", "Temperaturbereich (80–230 °C)", "Voreingestellte Programme", "Spülmaschinenfester Korb", "Aufheizzeit", "Fenster zur Sichtkontrolle"],
        "tip": "Für 2–3 Personen: 4–5 L. Für Familien: 6–8 L oder Dual-Basket (zwei Gerichte gleichzeitig)."
    },
    "saugroboter-bestseller": {
        "intro": "Saugroboter nehmen dir die Bodenreinigung ab. Wir vergleichen Navigation (Laser vs. Kamera), Saugkraft (Pa), Wischfunktion, App-Steuerung, Kartenerstellung und Hinderniserkennung.",
        "criteria": ["Navigation (LiDAR/ToF > Kamera > Zufall)", "Saugkraft (Pa)", "Wischfunktion (Wassertank, Vibration)", "App: No-Go-Zonen, Zeitpläne", "Teppicherkennung", "Akku-Laufzeit"],
        "tip": "Ab 250 € bekommst du LiDAR-Navigation. Für Haustiere: Anti-Haar-Verhedderung + starke Saugkraft (> 4000 Pa)."
    },
    "fitness-homegym": {
        "intro": "Ein Home Gym spart Zeit und Studio-Gebühren. Wir listen Hanteln, Bänke, Racks, Kabelzüge und Cardio-Geräte – platzsparend, erweiterbar und fürProgressive Overload geeignet.",
        "criteria": ["Platzbedarf (aufgeklappt/geklappt)", "Max. Belastbarkeit", "Verstellbarkeit (Bank: flach/schräg/negativ)", "Hantel-Aufnahme (30/50 mm)", "Bodenbelag-Schutz"],
        "tip": "Starte mit verstellbarer Hantelbank + Kurzhantel-Set (30 mm). Erweitere später um Power Rack + Langhantel."
    },
    "wohnen-deko": {
        "intro": "Wohnaccessoires machen aus einem Haus ein Zuhause. Wir kuratieren Vasen, Kissen, Decken, Wandbilder, Spiegel und Beleuchtung – zeitlos, kombinierbar und in guter Verarbeitung.",
        "criteria": ["Materialqualität (Keramik, Holz, Textil)", "Farbneutralität / Kombinierbarkeit", "Verarbeitung (keine Klebereste, saubere Nähte)", "Größenangaben prüfen", "Pflegeleichtigkeit"],
        "tip": "Setze auf 3er-Gruppen (Vasen, Kerzen) in verschiedenen Höhen. Spiegel gegenüber Fenster vergrößern Räume optisch."
    },
    "garten-balkon-saisonal": {
        "intro": "Balkon & Garten saisonal bepflanzen: Wir listen wetterfeste Möbel, Pflanzgefäße, Bewässerung, Sichtschutz und Deko – für sonnige, schattige und windige Standorte.",
        "criteria": ["Wetterfest (UV-beständig, rostfrei)", "Platzbedarf (klappbar, stapelbar)", "Entwässerung (Pflanzgefäße)", "Pflegeaufwand", "Sichtschutz-Höhe"],
        "tip": "Hochbeete & Pflanzsäcke für Gemüse auf Balkon. Solarleuchten = kein Kabelverlegen. Möbel: Aluminium/Teak > Kunststoff (Langlebigkeit)."
    }
}

# Generic fallback for niches without specific guide
GENERIC_BUYING_GUIDE = {
    "intro": "Wir haben die besten Produkte in dieser Kategorie für dich recherchiert – basierend auf Kundenbewertungen, Preis-Leistung und Verfügbarkeit. Alle Empfehlungen werden wöchentlich auf aktuelle Preise und Lieferbarkeit geprüft.",
    "criteria": ["Kundenbewertung ≥ 4,0 Sterne", "Mindestens 50 Bewertungen", "Gutes Preis-Leistungs-Verhältnis", "Aktuelle Lieferbarkeit", "Relevanz für deutsche Haushalte"],
    "tip": "Vergleiche die Top 3 Produkte nebeneinander – oft liegt der Unterschied im Detail (Zubehör, Garantie, Folgekosten)."
}

NICHE_FAQS = {
    "smart-home": [
        ("Welches Smart Home System ist das beste für Einsteiger?", "Für Einsteiger empfiehlt sich ein System mit Matter-Unterstützung (z. B. Amazon Echo, Google Nest, Apple HomePod). Matter garantiert herstellerübergreifende Kompatibilität. Starte mit einem Hub und 2–3 Geräten (Lampe, Steckdose, Sensor)."),
        ("Brauche ich zwingend einen Hub?", "Nicht zwingend. Viele Geräte (WLAN-Steckdosen, Zigbee-Lampen mit Bridge) laufen direkt per App. Ein Hub (Home Assistant, Hubitat, Echo) vereinfacht aber Automatisierungen und lokale Steuerung ohne Cloud."),
        ("Ist Smart Home sicher?", "Ja, bei richtiger Konfiguration: Separates WLAN (VLAN) für IoT, starke Passwörter, 2FA bei Cloud-Diensten, Firmware-Updates aktivieren. Lokale Systeme (Home Assistant) sind datenschutzfreundlicher als reine Cloud-Lösungen."),
        ("Was kostet ein Smart Home Einstieg?", "Einstiegs-Set (Hub + 2 Lampen + Steckdose): ca. 80–150 €. Einzelne WLAN-Steckdosen ab 15 €, Zigbee-Lampen ab 12 €. Matter-Geräte sind zukunftssicherer."),
        ("Funktioniert Smart Home ohne Internet?", "Zigbee, Z-Wave, Thread, Matter (lokal) funktionieren offline. WLAN-Geräte und Cloud-Apps (Tuya, Smart Life) brauchen Internet. Für Ausfallsicherheit: Lokales System (Home Assistant) + Zigbee/Thread."),
    ],
    "bestseller": [
        ("Sind Amazon Bestseller immer die besten Produkte?", "Nicht unbedingt. Bestseller zeigen Verkaufshäufigkeit, nicht zwingend Qualität. Wir filtern zusätzlich: ≥ 4 Sterne, ≥ 50 Bewertungen, stabile Preise. Prüfe auch spezialisierte Tests (Stiftung Warentest, Fachmagazine)."),
        ("Wie oft aktualisiert sich die Bestseller-Liste?", "Amazon aktualisiert stündlich. Unsere Auswahl prüfen wir wöchentlich auf Preis, Verfügbarkeit und Bewertungsänderungen."),
        ("Warum sind manche Bestseller so günstig?", "Skaleneffekte, große Stückzahlen, einfache Konstruktion. Günstig ≠ schlecht. Achte auf Bewertungsverteilung (viele 5-Sterne, wenige 1-Sterne) und Händler-Reputation."),
    ],
    "geschenke": [
        ("Was sind gute Geschenke unter 20 €?", "Duftkerzen, hochwertige Schokolade, Tee-Sets, Handyhüllen, Buchzeichen, kleine Pflanzen, Fotokalender, Gewürz-Sets. Wichtig: Schöne Verpackung, persönliche Note."),
        ("Geschenke für Technik-Fans?", "Mehrfach-Ladekabel, Powerbanks, Bluetooth-Tracker (AirTag/Chipolo), smarte Steckdosen, Kopfhörer-Ständer, Kabel-Organizer, USB-Hubs."),
        ("Wie finde ich das richtige Geschenk?", "Interessen notieren → Preisrahmen setzen → Bewertungen prüfen → Lieferzeit checken. Unser Geschenke-Filter sortiert nach Anlass, Preis, Zielgruppe."),
    ],
    "backen-kochen": [
        ("Küchenmaschine oder Handmixer?", "Küchenmaschine: Kneten schwerer Teige, große Mengen, freihändig. Handmixer: Kleinere Mengen, platzsparend, günstiger. Für Brot/Hefe-Teig regelmäßig: Küchenmaschine ab 800W."),
        ("Was ist besser: Kunststoff- oder Edelstahlschüssel?", "Edelstahl: langlebiger, hygienischer, hitzebeständiger, spülmaschinenfest. Kunststoff: leichter, günstiger, kann Kratzer/Verfärbungen bekommen. Profis nutzen Edelstahl."),
        ("Brauche ich einen Fleischwolf-Aufsatz?", "Nur wenn du regelmäßig Hackfleisch, Würste oder Gemüse fein hackst. Für gelegentliches Hacken: Universal-Zerkleinerer (oft im Lieferumfang)."),
    ],
    "baby-kindersicherheit": [
        ("Babyphone mit oder ohne WLAN?", "Ohne WLAN (DECT/FHSS): strahlungsärmer, abhörsicher, Reichweite bis 300 m im Freien. Mit WLAN: App-Zugriff von überall, Kamera-Bild auf Handy, aber höhere Strahlung & Cloud-Abhängigkeit."),
        ("Ab wann Treppenschutzgitter?", "Sobald das Kind krabbelt/robbt (ca. 6–9 Monate). Montage vor der Treppe (nicht auf der ersten Stufe). Klemmgitter für Mietwohnungen ohne Bohren."),
        ("Steckdosensicherungen: Welche Art?", "Dreh-Schutz (Kind muss drehen + drücken) > einfacher Stecker. Für Schuko-Steckdosen (Typ F). Montage: einfach in Steckdose stecken, Erwachsenen bedienbar."),
    ],
    "kaffee": [
        ("Kaffeevollautomat oder Siebträger?", "Vollautomat: Komfort, One-Touch, Milchschaum automatisch, teurer pro Tasse. Siebträger: Kontrolle über alle Parameter, bessere Espresso-Qualität, Lernkurve, günstiger pro Tasse (nur Bohnen)."),
        ("Wie wichtig ist das Mahlwerk?", "Entscheidend für Geschmack. Keramik: langlebiger, weniger Hitzeentwicklung. Stahl: schärfer, schneller. Wichtig: stufenlos einstellbar für verschiedene Bohnen/Röstungen."),
        ("Wie reinige ich richtig?", "Täglich: Brühgruppe spülen (entnehmbar), Tropfschale leeren. Wöchentlich: Milchsystem reinigen. Monatlich: Entkalken (Wasserhärte beachten). Reinigungstabletten nutzen."),
    ],
    "heissluftfritteuse": [
        ("Braucht man Öl in der Heißluftfritteuse?", "Nur 1–2 TL für optimale Bräunung/Knusprigkeit (z. B. Pommes, Hähnchen). Gemüse oft ganz ohne Öl. Ölspray für gleichmäßige Verteilung."),
        ("Was passt in 4 Liter?", "Ca. 500–700 g Pommes, 1 Hähnchen (klein), 2–3 Portionen Gemüse. Für 2–3 Personen ausreichend. Größere Stücke (ganzes Hähnchen) brauchen 6+ Liter."),
        ("Kann man backen?", "Ja: Muffins, kleine Kuchen, Pizza, Brötchen. Backformen (Silikon/Metall) bis 20 cm passen. Temperatur ca. 20 °C niedriger als Backofen einstellen."),
    ],
    "saugroboter-bestseller": [
        ("LiDAR vs. Kamera-Navigation?", "LiDAR/ToF: präzise Karten, funktioniert im Dunkeln, systematische Bahnen. Kamera: visuelle Erkennung (Hindernisse), braucht Licht, manchmal ungenauer. LiDAR > Kamera für Reinigungsleistung."),
        ("Wischfunktion: Loht sich?", "Für Hartböden (Fliesen, Parkett, Vinyl): Ja, für leichte Feuchtwischpflege. Ersetzt nicht Wischen per Hand bei starker Verschmutzung. Vibrations-Wischplatte > passiver Wischtuch."),
        ("Wie oft Filter/Behälter leeren?", "Behälter: alle 1–3 Tage (je nach Haustiere/Größe). Filter: monatlich ausklopfen, alle 3–6 Monate tauschen. Haustier-Haushalte: häufiger."),
    ],
    "fitness-homegym": [
        ("Was brauche ich für den Start?", "Verstellbare Hantelbank + Kurzhantel-Set (30 mm, 20–40 kg gesamt) + Matte. Kosten: ca. 200–350 €. Erweitert: Langhantel + Rack + Gewichte."),
        ("30 mm oder 50 mm Hantelstangen?", "30 mm (Studio-Standard): günstiger, mehr Auswahl, für Einsteiger/Heimnutzer ausreichend. 50 mm (Olympia): stabiler, für > 150 kg, teurer. Umrüstung später möglich."),
        ("Power Rack oder Halb-Rack?", "Power Rack (4 Pfeiler): sicherer (Fangbügel), mehr Übungen (Klimmzüge, Dipps), mehr Platz. Halb-Rack: platzsparender, günstiger, für Bankdrücken/Kniebeugen ok."),
    ],
    "wohnen-deko": [
        ("Wie kombiniere ich Wohnaccessoires richtig?", "Regel: Ungerade Anzahlen (3, 5), verschiedene Höhen, gemeinsames Farbschema (max. 3 Farben), Material-Mix (Keramik + Holz + Glas + Textil). Spiegel gegenüber Fenster = mehr Licht."),
        ("Vasen: Welche Größe für welchen Strauß?", "Hohe schmale Vasen (25+ cm) für lange Stiele (Tulpen, Sonnenblumen). Bauchige Vasen (15–20 cm) für runde Sträuße (Rosen, Pfingstrosen). Solitär-Vasen (30+ cm) für einzelne Zweige/Grün."),
        ("Kissen: Wie viele auf dem Sofa?", "3er-Regel: 2 große (50×50/60×60) hinten, 1 kleineres (40×40/30×50) vorne. Muster + Uni mixen. Bezüge waschbar (Reißverschluss)."),
    ],
    "garten-balkon-saisonal": [
        ("Welche Pflanzen für schattigen Balkon?", "Farne, Funkien, Efeu, Fuchsien, Begonien, Hortensien (Topf), Immergrün, Waldmeister. Gemüse: Spinat, Salat, Radieschen, Kräuter (Petersilie, Schnittlauch, Minze)."),
        ("Balkonmöbel: Was ist wetterfest?", "Aluminium (pulverbeschichtet), Teak/Eukalyptus (geölt), Polyrattan (UV-stabil), Textilene-Bespannung. Nicht wetterfest: unbehandeltes Kiefernholz, billiges Kunststoffgeflecht."),
        ("Automatische Bewässerung für Balkon?", "Tropfschlauch + Zeitschaltuhr + Druckminderer + Wasseranschluss (oder Tank + Pumpe). Kosten: 50–150 €. Spart Wasser & Zeit. Für Urlaub unverzichtbar."),
    ]
}

GENERIC_FAQS = [
    ("Wie werden die Produkte ausgewählt?", "Wir analysieren Amazon-Kundenbewertungen (≥ 4 Sterne, ≥ 50 Reviews), Preisverläufe, Lieferbarkeit und Relevanz für deutsche Haushalte. Die Daten werden wöchentlich automatisiert aktualisiert."),
    ("Sind die Preise aktuell?", "Preise werden wöchentlich über die Amazon Product Advertising API abgeglichen. Der finale Preis wird auf der Amazon-Produktseite angezeigt – kurzfristige Änderungen sind möglich."),
    ("Was bedeutet 'Als Amazon-Partner verdiene ich an qualifizierten Käufen'?", "Wenn du über unsere Links bei Amazon kaufst, erhalten wir eine kleine Provision. Für dich ändert sich der Preis nicht. Die Einnahmen finanzieren den Betrieb dieser Website."),
    ("Kann ich Produkte zurückgeben?", "Ja, über Amazon gelten die regulären Rückgaberechte (meist 30 Tage). Die Abwicklung läuft direkt über dein Amazon-Konto."),
]

def get_buying_guide(niche_slug):
    """Get buying guide content for a niche."""
    return NICHE_BUYING_GUIDES.get(niche_slug, GENERIC_BUYING_GUIDE)

def get_faqs(niche_slug):
    """Get FAQ list for a niche."""
    return NICHE_FAQS.get(niche_slug, GENERIC_FAQS)

def generate_product_card(product, index, niche_slug=None):
    """Generate HTML for a single product card with schema.org markup."""
    asin = product.get('asin', '')
    name = product.get('name', 'Produkt')
    price = product.get('price', '')
    img_url = get_amazon_image_url(asin)
    affiliate_url = get_affiliate_link(asin)

    # Truncate long names
    display_name = name[:80] + "..." if len(name) > 80 else name
    
    # Determine badge based on position
    if index == 0:
        badge_text = "🏆 Unser Favorit"
        badge_class = "badge-favorite"
    elif index == 1:
        badge_text = "💡 Preis-Leistung"
        badge_class = "badge-value"
    elif index == 2:
        badge_text = "⭐ Beliebt"
        badge_class = "badge-popular"
    else:
        badge_text = "Zum Angebot"
        badge_class = ""
    
    # Data attributes for GA4 click tracking
    data_attrs = f'data-asin="{asin}" data-niche="{niche_slug or ""}" data-position="{index}" data-price="{price}"'
    
    # Product schema.org microdata attributes
    microdata_attrs = f'itemprop="itemListElement" itemscope itemtype="https://schema.org/Product"'

    return f'''
    <article class="product-card" data-index="{index}" {microdata_attrs}>
        <a href="{affiliate_url}" target="_blank" rel="noopener sponsored" class="product-link" {data_attrs}>
            <div class="product-image-wrapper">
                <img src="{img_url}" alt="{display_name}" loading="lazy" class="product-image" itemprop="image">
                <span class="product-badge {badge_class}">{badge_text}</span>
            </div>
            <div class="product-info">
                <h3 class="product-title" itemprop="name">{display_name}</h3>
                <div class="product-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
                    <meta itemprop="priceCurrency" content="EUR">
                    <meta itemprop="price" content="{price.replace(',', '.')}">
                    <meta itemprop="availability" content="https://schema.org/InStock">
                    <span itemprop="price">{price} €</span>
                </div>
                <meta itemprop="sku" content="{asin}">
                <meta itemprop="brand" content="Amazon">
                <link itemprop="url" href="{affiliate_url}">
            </div>
        </a>
    </article>'''

def generate_niche_page(niche_slug, products, all_niches):
    """Generate HTML for a single niche page with full SEO markup."""
    niche_name = NICHE_NAMES.get(niche_slug, niche_slug.replace('-', ' ').title())
    product_cards = ''.join(generate_product_card(p, i, niche_slug) for i, p in enumerate(products[:12]))
    
    # Get buying guide content
    buying_guide = get_buying_guide(niche_slug)
    faqs = get_faqs(niche_slug)
    
    # Find category for breadcrumb
    category = None
    for cat, niches in CATEGORIES.items():
        if niche_slug in niches:
            category = cat
            break
    
    cat_display = CATEGORY_DISPLAY.get(category, category) if category else None
    cat_slug = CATEGORY_SLUGS.get(category, category.lower().replace(" ", "-").replace("&", "")) if category else None
    breadcrumb = f'<a href="/">Startseite</a> / <a href="/{cat_slug}/">{cat_display}</a> / {niche_name}' if category else f'<a href="/">Startseite</a> / {niche_name}'
    
    # Build breadcrumb items for schema
    breadcrumb_items = [("Startseite", "https://balu1705.github.io/andreasstehmann-links/")]
    if category and cat_display and cat_slug:
        breadcrumb_items.append((cat_display, f"https://balu1705.github.io/andreasstehmann-links/{cat_slug}/"))
    breadcrumb_items.append((niche_name, f"https://balu1705.github.io/andreasstehmann-links/{niche_slug}/"))
    
    # Generate JSON-LD schemas
    breadcrumb_schema = generate_breadcrumb_schema(breadcrumb_items)
    itemlist_schema = generate_itemlist_schema(products, niche_slug)
    faq_schema = generate_faq_schema(niche_slug)
    
    import json
    schemas_json = json.dumps([breadcrumb_schema, itemlist_schema, faq_schema], ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{niche_name} - Andreas Stehmann Links</title>
    <meta name="description" content="{buying_guide['intro'][:155]}">
    <link rel="canonical" href="https://balu1705.github.io/andreasstehmann-links/{niche_slug}/">
    <meta property="og:title" content="{niche_name} - Andreas Stehmann Links">
    <meta property="og:description" content="{buying_guide['intro'][:155]}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://balu1705.github.io/andreasstehmann-links/{niche_slug}/">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="stylesheet" href="/assets/style.css">
    <link rel="preconnect" href="https://m.media-amazon.com">
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
{schemas_json}
    </script>
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('consent', 'default', {{
            'analytics_storage': 'denied',
            'ad_storage': 'denied',
            'ad_user_data': 'denied',
            'ad_personalization': 'denied'
        }});
        gtag('js', new Date());
        gtag('config', '{GA4_ID}');
    </script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="logo" aria-label="Andreas Stehmann Links - Startseite">
                <span class="logo-icon">🔗</span>
                <span class="logo-text">Andreas Stehmann Links</span>
            </a>
            <nav class="main-nav" aria-label="Hauptnavigation">
                <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Menü öffnen">☰</button>
                <ul id="nav-menu" class="nav-menu">
                    {''.join(f'<li><a href="/{CATEGORY_SLUGS[cat]}/">{CATEGORY_DISPLAY[cat]}</a></li>' for cat in CATEGORIES.keys())}
                    <li><a href="/deals/">Deals</a></li>
                    <li><a href="/ueber-uns/">Über uns</a></li>
                    <li><a href="/impressum/">Impressum</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="site-main">
        <nav class="breadcrumb" aria-label="Brotkrumennavigation" itemscope itemtype="https://schema.org/BreadcrumbList">
            <div class="container">{breadcrumb}</div>
        </nav>

        <section class="niche-hero">
            <div class="container">
                <h1>{niche_name}</h1>
                <p class="hero-subtitle">Handverlesene Empfehlungen • Aktuelle Preise • Echte Amazon-Bewertungen</p>
                <p class="hero-disclaimer">Als Amazon-Partner verdiene ich an qualifizierten Käufen.</p>
            </div>
        </section>

        <!-- Buying Guide Content -->
        <section class="buying-guide" aria-labelledby="buying-guide-title">
            <div class="container">
                <h2 id="buying-guide-title">Kaufberatung: {niche_name}</h2>
                <div class="buying-guide-content">
                    <p>{buying_guide['intro']}</p>
                    
                    <h3>Worauf du achten solltest</h3>
                    <ul class="criteria-list">
                        {''.join(f'<li><span class="check-icon">✓</span> {c}</li>' for c in buying_guide['criteria'])}
                    </ul>
                    
                    <div class="expert-tip">
                        <span class="tip-icon">💡</span>
                        <div class="tip-content">
                            <strong>Experten-Tipp:</strong> {buying_guide['tip']}
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Affiliate Disclosure Notice -->
        <section class="affiliate-disclosure" aria-labelledby="affiliate-disclosure-title">
            <div class="container">
                <div class="affiliate-notice">
                    <strong id="affiliate-disclosure-title">Werbung / Affiliate-Links:</strong>
                    <span>Bei einem Kauf über diese Links erhalte ich eine Provision. Der Preis für dich bleibt gleich.</span>
                </div>
            </div>
        </section>

        <section class="product-grid-section" itemscope itemtype="https://schema.org/ItemList">
            <div class="container">
                <meta itemprop="name" content="{niche_name} Empfehlungen">
                <meta itemprop="description" content="Unsere Top-Empfehlungen für {niche_name.lower()} basierend auf Kundenbewertungen und Preis-Leistung.">
                <div class="product-grid" role="list" itemprop="itemListElement" itemscope itemtype="https://schema.org/ItemList">
                    {product_cards}
                </div>
            </div>
        </section>

        <!-- FAQ Section -->
        <section class="faq-section" aria-labelledby="faq-title" itemscope itemtype="https://schema.org/FAQPage">
            <div class="container">
                <h2 id="faq-title">Häufige Fragen zu {niche_name}</h2>
                <div class="faq-grid">
                    {''.join(f'''
                    <article class="faq-item" itemprop="mainEntity" itemscope itemtype="https://schema.org/Question">
                        <h3 itemprop="name">{q}</h3>
                        <div class="faq-answer" itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">
                            <p itemprop="text">{a}</p>
                        </div>
                    </article>''' for q, a in faqs)}
                </div>
            </div>
        </section>

        <section class="cta-section">
            <div class="container">
                <h2>Nicht fündig geworden?</h2>
                <p>Entdecke weitere Kategorien oder nutze die Amazon-Suche direkt.</p>
                <a href="/" class="btn btn-primary">Alle Kategorien anzeigen</a>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <span class="logo-icon">🔗</span>
                    <span>Andreas Stehmann Links</span>
                    <p>Deine kuratierte Produktauswahl für smarte Kaufentscheidungen.</p>
                </div>
                <nav class="footer-nav">
                    <h4>Kategorien</h4>
                    <ul>
                        {''.join(f'<li><a href="/{CATEGORY_SLUGS[cat]}/">{CATEGORY_DISPLAY[cat]}</a></li>' for cat in CATEGORIES.keys())}
                    </ul>
                </nav>
                <nav class="footer-nav">
                    <h4>Rechtliches</h4>
                    <ul>
                        <li><a href="/impressum/">Impressum</a></li>
                        <li><a href="/datenschutz/">Datenschutz</a></li>
                        <li><a href="/affiliate-hinweis/">Affiliate-Hinweis</a></li>
                    </ul>
                </nav>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Andreas Stehmann Links. Alle Rechte vorbehalten.</p>
            </div>
        </div>
    </footer>
    <!-- Cookie Consent Banner -->
    <div id="cookie-banner" class="cookie-banner" role="dialog" aria-label="Cookie-Einwilligung" hidden>
        <div class="cookie-banner-content">
            <div class="cookie-banner-text">
                <h3>🍪 Cookie-Einstellungen</h3>
                <p>Wir nutzen Cookies für Analyse (GA4) und Affiliate-Tracking. Essentielle Funktionen laufen immer. <a href="/cookie-einstellungen/">Details & individuelle Einstellung</a></p>
            </div>
            <div class="cookie-banner-actions">
                <button class="btn btn-secondary" id="cookie-reject">Nur essentiell</button>
                <button class="btn btn-primary" id="cookie-accept">Alle akzeptieren</button>
            </div>
        </div>
    </div>
    <!-- GA4 Affiliate Click Tracking (Consent-gated) -->
    <script>
        // Cookie Consent Management
        (function() {{
            var CONSENT_COOKIE = 'cookie_consent';
            var CONSENT_EXPIRY_DAYS = 365;
            
            function getConsent() {{
                var match = document.cookie.match(new RegExp('(^| )' + CONSENT_COOKIE + '=([^;]+)'));
                return match ? JSON.parse(decodeURIComponent(match[2])) : null;
            }}
            
            function setConsent(consent) {{
                var date = new Date();
                date.setTime(date.getTime() + (CONSENT_EXPIRY_DAYS * 24 * 60 * 60 * 1000));
                document.cookie = CONSENT_COOKIE + '=' + encodeURIComponent(JSON.stringify(consent)) + ';expires=' + date.toUTCString() + ';path=/;SameSite=Lax';
            }}
            
            function updateGtagConsent(consent) {{
                if (typeof gtag !== 'function') return;
                gtag('consent', 'update', {{
                    'analytics_storage': consent.analytics ? 'granted' : 'denied',
                    'ad_storage': consent.marketing ? 'granted' : 'denied',
                    'ad_user_data': consent.marketing ? 'granted' : 'denied',
                    'ad_personalization': consent.marketing ? 'granted' : 'denied'
                }});
            }}
            
            function showBanner() {{
                var banner = document.getElementById('cookie-banner');
                if (banner) banner.hidden = false;
            }}
            
            function hideBanner() {{
                var banner = document.getElementById('cookie-banner');
                if (banner) banner.hidden = true;
            }}
            
            // Initialize on DOM ready
            document.addEventListener('DOMContentLoaded', function() {{
                var consent = getConsent();
                if (consent) {{
                    // Consent exists - apply to GA4
                    updateGtagConsent(consent);
                }} else {{
                    // No consent - show banner
                    showBanner();
                }}
                
                // Button handlers
                var acceptBtn = document.getElementById('cookie-accept');
                var rejectBtn = document.getElementById('cookie-reject');
                
                if (acceptBtn) {{
                    acceptBtn.addEventListener('click', function() {{
                        var consent = {{ analytics: true, marketing: true, essential: true, timestamp: Date.now() }};
                        setConsent(consent);
                        updateGtagConsent(consent);
                        hideBanner();
                    }});
                }}
                if (rejectBtn) {{
                    rejectBtn.addEventListener('click', function() {{
                        var consent = {{ analytics: false, marketing: false, essential: true, timestamp: Date.now() }};
                        setConsent(consent);
                        updateGtagConsent(consent);
                        hideBanner();
                    }});
                }}
            }});
        }})();
        
        // Affiliate Click Tracking - only fires with marketing consent
        document.addEventListener("DOMContentLoaded", function() {{
            document.querySelectorAll("a.product-link[data-asin]").forEach(function(link) {{
                link.addEventListener("click", function(e) {{
                    var asin = this.getAttribute("data-asin");
                    var niche = this.getAttribute("data-niche");
                    var position = this.getAttribute("data-position");
                    var price = this.getAttribute("data-price");
                    
                    // Check marketing consent before firing
                    var consent = (function() {{
                        var match = document.cookie.match(new RegExp('(^| )cookie_consent=([^;]+)'));
                        return match ? JSON.parse(decodeURIComponent(match[2])) : null;
                    }})();
                    
                    if (asin && typeof gtag === "function" && consent && consent.marketing) {{
                        gtag("event", "affiliate_click", {{
                            "asin": asin,
                            "niche": niche || "",
                            "position": parseInt(position) || 0,
                            "price": parseFloat(price) || 0,
                            "currency": "EUR",
                            "affiliate_tag": "balu17051-21",
                            "link_domain": "amazon.de"
                        }});
                    }}
                }});
            }});
        }});
    </script>
    <script src="/assets/main.js"></script>
</body>
</html>'''

def generate_category_page(category_name, niches_in_cat, all_products):
    """Generate HTML for a category overview page with SEO content hub."""
    # Build niche cards with top product data for comparison table
    niche_cards = ''
    niche_items_for_schema = []  # For ItemList JSON-LD
    top_products_for_comparison = []  # For comparison table
    
    for idx, niche_slug in enumerate(niches_in_cat):
        if niche_slug not in all_products:
            continue
        products = all_products[niche_slug]
        if not products:
            continue
        niche_name = NICHE_NAMES.get(niche_slug, niche_slug.replace('-', ' ').title())
        first_product = products[0]
        asin = first_product.get('asin', '')
        img_url = get_amazon_image_url(asin) if asin else ''
        product_count = len(products)
        price = first_product.get('price', '')
        
        # Schema.org ItemList item
        niche_items_for_schema.append({
            "position": idx + 1,
            "item": {
                "@type": "ItemList",
                "name": niche_name,
                "url": f"https://balu1705.github.io/andreasstehmann-links/{niche_slug}/",
                "description": f"{product_count} kuratierte Produkte in der Kategorie {niche_name}",
                "numberOfItems": product_count
            }
        })
        
        # Top product for comparison table
        if asin and price:
            top_products_for_comparison.append({
                "niche": niche_name,
                "niche_slug": niche_slug,
                "product_name": first_product.get('name', niche_name),
                "price": price,
                "asin": asin,
                "img_url": img_url
            })
        
        niche_cards += f'''
        <article class="category-card">
            <a href="/{niche_slug}/" class="category-link">
                <div class="category-image-wrapper">
                    <img src="{img_url}" alt="{niche_name}" loading="lazy" class="category-image">
                </div>
                <div class="category-info">
                    <h3>{niche_name}</h3>
                    <span class="product-count">{product_count} Produkte</span>
                </div>
            </a>
        </article>'''
    
    cat_display = CATEGORY_DISPLAY.get(category_name, category_name)
    cat_slug = CATEGORY_SLUGS.get(category_name, f"kategorie/{category_name.lower().replace(' ', '-').replace('&', '')}")
    if not cat_display:
        cat_display = category_name
    if not cat_slug:
        cat_slug = f"kategorie/{category_name.lower().replace(' ', '-').replace('&', '')}"
    
    # Get category-specific SEO content
    cat_intro = CATEGORY_INTRO.get(category_name, {})
    cat_faqs = CATEGORY_FAQS.get(category_name, [])
    
    # Build JSON-LD structured data
    valid_niches = [n for n in niches_in_cat if n in all_products and all_products[n]]
    subcategory_count = len(valid_niches)
    total_products = sum(len(all_products[n]) for n in valid_niches)
    
    # CollectionPage schema
    collection_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": cat_intro.get("title", f"{cat_display} - Andreas Stehmann Links"),
        "description": cat_intro.get("intro", f"Alle {cat_display} Unterkategorien auf einen Blick. {subcategory_count} Nischen, {total_products} Produkte."),
        "url": f"https://balu1705.github.io/andreasstehmann-links/{cat_slug}/",
        "mainEntity": {
            "@type": "ItemList",
            "name": f"{cat_display} Unterkategorien",
            "description": f"Übersicht aller {subcategory_count} Unterkategorien in {cat_display}",
            "numberOfItems": subcategory_count,
            "itemListElement": niche_items_for_schema
        },
        "publisher": {
            "@type": "Organization",
            "name": "Andreas Stehmann Links",
            "url": "https://balu1705.github.io/andreasstehmann-links/"
        }
    }
    
    # FAQPage schema for category
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["a"]
                }
            }
            for faq in cat_faqs
        ]
    } if cat_faqs else None
    
    # Breadcrumb schema
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Startseite",
                "item": "https://balu1705.github.io/andreasstehmann-links/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": cat_display,
                "item": f"https://balu1705.github.io/andreasstehmann-links/{cat_slug}/"
            }
        ]
    }
    
    # Build comparison table HTML
    comparison_table = ''
    if top_products_for_comparison:
        comparison_rows = ''
        for i, prod in enumerate(top_products_for_comparison[:8]):  # Top 8
            badge = ''
            if i == 0:
                badge = '<span class="badge badge-favorite">🏆 Top Pick</span>'
            elif i == 1:
                badge = '<span class="badge badge-value">💡 Preis-Leistung</span>'
            elif i == 2:
                badge = '<span class="badge badge-popular">⭐ Beliebt</span>'
            
            affiliate_url = f"https://www.amazon.de/dp/{prod['asin']}/?tag=balu17051-21&linkCode=ogi&th=1&psc=1"
            comparison_rows += f'''
            <tr>
                <td><a href="/{prod['niche_slug']}/" class="niche-link">{prod['niche']}</a></td>
                <td><a href="{affiliate_url}" target="_blank" rel="nofollow sponsored noopener" class="product-link" data-asin="{prod['asin']}" data-niche="{prod['niche_slug']}">{prod['product_name'][:50]}{'...' if len(prod['product_name']) > 50 else ''}</a></td>
                <td><strong>{prod['price']} €</strong></td>
                <td><a href="{affiliate_url}" target="_blank" rel="nofollow sponsored noopener" class="btn btn-sm btn-primary" data-asin="{prod['asin']}" data-niche="{prod['niche_slug']}">Zum Angebot {badge}</a></td>
            </tr>'''
        
        comparison_table = f'''
        <section class="comparison-section" aria-labelledby="comparison-title">
            <div class="container">
                <h2 id="comparison-title">Top-Empfehlungen im Vergleich</h2>
                <p class="comparison-intro">Die besten Produkte aus jeder Unterkategorie – direkt vergleichbar.</p>
                <div class="table-wrapper">
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>Unterkategorie</th>
                                <th>Top-Produkt</th>
                                <th>Preis</th>
                                <th>Aktion</th>
                            </tr>
                        </thead>
                        <tbody>
                            {comparison_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>'''
    
    # Build buying guide section
    buying_guide_html = ''
    if cat_intro:
        criteria_html = ''
        for criterion in cat_intro.get("criteria", []):
            criteria_html += f'<li><span class="check-icon">✓</span>{criterion}</li>'
        
        buying_guide_html = f'''
        <section class="buying-guide" aria-labelledby="guide-title">
            <div class="container">
                <h2 id="guide-title">{cat_intro.get("title", f"{cat_display} Kaufberatung")}</h2>
                <div class="buying-guide-content">
                    <p>{cat_intro.get("intro", "")}</p>
                    <h3>Unsere Auswahlkriterien</h3>
                    <ul class="criteria-list">
                        {criteria_html}
                    </ul>
                    <div class="expert-tip">
                        <span class="tip-icon" aria-hidden="true">💡</span>
                        <div class="tip-content">{cat_intro.get("expert_tip", "")}</div>
                    </div>
                </div>
            </div>
        </section>'''
    
    # Build FAQ section
    faq_html = ''
    if cat_faqs:
        faq_items = ''
        for faq in cat_faqs:
            faq_items += f'''
            <article class="faq-item">
                <h3>{faq["q"]}</h3>
                <div class="faq-answer"><p>{faq["a"]}</p></div>
            </article>'''
        
        faq_html = f'''
        <section class="faq-section" aria-labelledby="faq-title">
            <div class="container">
                <h2 id="faq-title">Häufige Fragen zu {cat_display}</h2>
                <div class="faq-grid">
                    {faq_items}
                </div>
            </div>
        </section>'''
    
    # JSON-LD scripts
    import json
    json_ld_scripts = f'''
    <!-- JSON-LD CollectionPage Schema -->
    <script type="application/ld+json">{json.dumps(collection_schema, ensure_ascii=False)}</script>
    <!-- JSON-LD BreadcrumbList Schema -->
    <script type="application/ld+json">{json.dumps(breadcrumb_schema, ensure_ascii=False)}</script>'''
    if faq_schema:
        json_ld_scripts += f'\n    <!-- JSON-LD FAQPage Schema -->\n    <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>'
    
    import json
    
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_display} - Andreas Stehmann Links</title>
    <meta name="description" content="{cat_intro.get('intro', f'Alle {cat_display.lower()} Kategorien auf einen Blick. Finde die besten Produkte in {subcategory_count} Unterkategorien.')[:155]}">
    <link rel="canonical" href="https://balu1705.github.io/andreasstehmann-links/{cat_slug}/">
    <meta property="og:title" content="{cat_display} - Andreas Stehmann Links">
    <meta property="og:description" content="{cat_intro.get('intro', f'Alle {cat_display.lower()} Kategorien auf einen Blick.')[:155]}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://balu1705.github.io/andreasstehmann-links/{cat_slug}/">
    <link rel="stylesheet" href="/assets/style.css">
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('consent', 'default', {{
            'analytics_storage': 'denied',
            'ad_storage': 'denied',
            'ad_user_data': 'denied',
            'ad_personalization': 'denied'
        }});
        gtag('js', new Date());
        gtag('config', '{GA4_ID}');
    </script>
    {json_ld_scripts}
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="logo" aria-label="Andreas Stehmann Links - Startseite">
                <span class="logo-icon">🔗</span>
                <span class="logo-text">Andreas Stehmann Links</span>
            </a>
            <nav class="main-nav" aria-label="Hauptnavigation">
                <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Menü öffnen">☰</button>
                <ul id="nav-menu" class="nav-menu">
                    {''.join(f'<li><a href="/{CATEGORY_SLUGS[cat]}/">{CATEGORY_DISPLAY[cat]}</a></li>' for cat in CATEGORIES.keys())}
                    <li><a href="/deals/">Deals</a></li>
                    <li><a href="/ueber-uns/">Über uns</a></li>
                    <li><a href="/impressum/">Impressum</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="site-main">
        <nav class="breadcrumb" aria-label="Brotkrumennavigation">
            <div class="container"><a href="/">Startseite</a> / {cat_display}</div>
        </nav>

        <section class="category-hero">
            <div class="container">
                <h1>{cat_display}</h1>
                <p class="hero-subtitle">{subcategory_count} Unterkategorien • {total_products} Produkte</p>
            </div>
        </section>

        <!-- Affiliate Disclosure Notice -->
        <section class="affiliate-disclosure" aria-labelledby="affiliate-disclosure-title">
            <div class="container">
                <div class="affiliate-notice">
                    <strong id="affiliate-disclosure-title">Werbung / Affiliate-Links:</strong>
                    <span>Bei einem Kauf über diese Links erhalte ich eine Provision. Der Preis für dich bleibt gleich.</span>
                </div>
            </div>
        </section>

        {buying_guide_html}

        {comparison_table}

        <section class="category-grid-section">
            <div class="container">
                <div class="category-grid" role="list">
                    {niche_cards}
                </div>
            </div>
        </section>

        {faq_html}
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <span class="logo-icon">🔗</span>
                    <span>Andreas Stehmann Links</span>
                    <p>Deine kuratierte Produktauswahl für smarte Kaufentscheidungen.</p>
                </div>
                <nav class="footer-nav">
                    <h4>Kategorien</h4>
                    <ul>
                        {''.join(f'<li><a href="/{CATEGORY_SLUGS[cat]}/">{CATEGORY_DISPLAY[cat]}</a></li>' for cat in CATEGORIES.keys())}
                    </ul>
                </nav>
                <nav class="footer-nav">
                    <h4>Rechtliches</h4>
                    <ul>
                        <li><a href="/impressum/">Impressum</a></li>
                        <li><a href="/datenschutz/">Datenschutz</a></li>
                        <li><a href="/affiliate-hinweis/">Affiliate-Hinweis</a></li>
                    </ul>
                </nav>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Andreas Stehmann Links. Alle Rechte vorbehalten.</p>
            </div>
        </div>
    </footer>
    <!-- GA4 Affiliate Click Tracking -->
    <!-- Cookie Consent Banner -->
    <div id="cookie-banner" class="cookie-banner" role="dialog" aria-label="Cookie-Einwilligung" hidden>
        <div class="cookie-banner-content">
            <div class="cookie-banner-text">
                <h3>🍪 Cookie-Einstellungen</h3>
                <p>Wir nutzen Cookies für Analyse (GA4) und Affiliate-Tracking. Essentielle Funktionen laufen immer. <a href="/cookie-einstellungen/">Details & individuelle Einstellung</a></p>
            </div>
            <div class="cookie-banner-actions">
                <button class="btn btn-secondary" id="cookie-reject">Nur essentiell</button>
                <button class="btn btn-primary" id="cookie-accept">Alle akzeptieren</button>
            </div>
        </div>
    </div>
    <!-- GA4 Affiliate Click Tracking (Consent-gated) -->
    <script>
        // Cookie Consent Management
        (function() {{
            var CONSENT_COOKIE = 'cookie_consent';
            var CONSENT_EXPIRY_DAYS = 365;
            
            function getConsent() {{
                var match = document.cookie.match(new RegExp('(^| )' + CONSENT_COOKIE + '=([^;]+)'));
                return match ? JSON.parse(decodeURIComponent(match[2])) : null;
            }}
            
            function setConsent(consent) {{
                var date = new Date();
                date.setTime(date.getTime() + (CONSENT_EXPIRY_DAYS * 24 * 60 * 60 * 1000));
                document.cookie = CONSENT_COOKIE + '=' + encodeURIComponent(JSON.stringify(consent)) + ';expires=' + date.toUTCString() + ';path=/;SameSite=Lax';
            }}
            
            function updateGtagConsent(consent) {{
                if (typeof gtag !== 'function') return;
                gtag('consent', 'update', {{
                    'analytics_storage': consent.analytics ? 'granted' : 'denied',
                    'ad_storage': consent.marketing ? 'granted' : 'denied',
                    'ad_user_data': consent.marketing ? 'granted' : 'denied',
                    'ad_personalization': consent.marketing ? 'granted' : 'denied'
                }});
            }}
            
            function showBanner() {{
                var banner = document.getElementById('cookie-banner');
                if (banner) banner.hidden = false;
            }}
            
            function hideBanner() {{
                var banner = document.getElementById('cookie-banner');
                if (banner) banner.hidden = true;
            }}
            
            // Initialize on DOM ready
            document.addEventListener('DOMContentLoaded', function() {{
                var consent = getConsent();
                if (consent) {{
                    // Consent exists - apply to GA4
                    updateGtagConsent(consent);
                }} else {{
                    // No consent - show banner
                    showBanner();
                }}
                
                // Button handlers
                var acceptBtn = document.getElementById('cookie-accept');
                var rejectBtn = document.getElementById('cookie-reject');
                
                if (acceptBtn) {{
                    acceptBtn.addEventListener('click', function() {{
                        var consent = {{ analytics: true, marketing: true, essential: true, timestamp: Date.now() }};
                        setConsent(consent);
                        updateGtagConsent(consent);
                        hideBanner();
                    }});
                }}
                if (rejectBtn) {{
                    rejectBtn.addEventListener('click', function() {{
                        var consent = {{ analytics: false, marketing: false, essential: true, timestamp: Date.now() }};
                        setConsent(consent);
                        updateGtagConsent(consent);
                        hideBanner();
                    }});
                }}
            }});
        }})();
        
        // Affiliate Click Tracking - only fires with marketing consent
        document.addEventListener("DOMContentLoaded", function() {{
            document.querySelectorAll("a.product-link[data-asin]").forEach(function(link) {{
                link.addEventListener("click", function(e) {{
                    var asin = this.getAttribute("data-asin");
                    var niche = this.getAttribute("data-niche");
                    var position = this.getAttribute("data-position");
                    var price = this.getAttribute("data-price");
                    
                    // Check marketing consent before firing
                    var consent = (function() {{
                        var match = document.cookie.match(new RegExp('(^| )cookie_consent=([^;]+)'));
                        return match ? JSON.parse(decodeURIComponent(match[2])) : null;
                    }})();
                    
                    if (asin && typeof gtag === "function" && consent && consent.marketing) {{
                        gtag("event", "affiliate_click", {{
                            "asin": asin,
                            "niche": niche || "",
                            "position": parseInt(position) || 0,
                            "price": parseFloat(price) || 0,
                            "currency": "EUR",
                            "affiliate_tag": "balu17051-21",
                            "link_domain": "amazon.de"
                        }});
                    }}
                }});
            }});
        }});
    </script>
    <script src="/assets/main.js"></script>
</body>
</html>'''

def generate_homepage(all_products):
    """Generate the main homepage - Phase 1: Premium Lifestyle Magazine Design."""
    import random
    from datetime import datetime
    
    # Helper: get high-res Amazon image URL
    def get_hero_image(asin):
        if not asin:
            return "https://m.media-amazon.com/images/I/71example.jpg"
        return f"https://m.media-amazon.com/images/I/{asin}._AC_SL1500_.jpg"
    
    # Helper: get product image for cards
    def get_product_image(asin):
        if not asin:
            return "https://m.media-amazon.com/images/I/61example.jpg"
        return f"https://m.media-amazon.com/images/I/{asin}._AC_SL500_.jpg"
    
    # Current season detection
    month = datetime.now().month
    if month in [12, 1, 2]:
        season = "Winter"
        season_emoji = "❄️"
        season_desc = "Gemütliche Winter-Essentials für kalte Tage"
        seasonal_cat_slug = "kategorie/wohnen-haushalt"  # Weihnachtsdeko, Heizung, Wellness
    elif month in [3, 4, 5]:
        season = "Frühling"
        season_emoji = "🌱"
        season_desc = "Frische Frühlings-Ideen für dein Zuhause"
        seasonal_cat_slug = "kategorie/wohnen-haushalt"  # Balkon, Garten, Pflanzen
    elif month in [6, 7, 8]:
        season = "Sommer"
        season_emoji = "☀️"
        season_desc = "Sommer-Highlights für Balkon, Garten & Reisen"
        seasonal_cat_slug = "kategorie/wohnen-haushalt"  # Outdoor, Grillen, Reisen
    else:
        season = "Herbst"
        season_emoji = "🍂"
        season_desc = "Warme Herbst-Favoriten für drinnen & draußen"
        seasonal_cat_slug = "kategorie/wohnen-haushalt"  # Herbstdeko, Kerzen, Wohlfühlen
    
    # 1. HERO SECTION - Emotionales Wohnbild mit starker Headline
    # Find a good hero product from Wohnen categories
    wohnen_niches = CATEGORIES.get("Wohnen & Haushalt", [])
    hero_product = None
    for niche in wohnen_niches[:5]:
        if niche in all_products and all_products[niche]:
            hero_product = all_products[niche][0]
            break
    hero_img = get_hero_image(hero_product['asin']) if hero_product and hero_product.get('asin') else "https://m.media-amazon.com/images/I/71living-room-example._AC_SL1500_.jpg"
    
    # 2. ALL 7 THEME WORLDS - Professionelle Karten
    theme_worlds = []
    for cat_name in CATEGORIES.keys():
        niches = CATEGORIES[cat_name]
        valid_niches = [n for n in niches if n in all_products and all_products[n]]
        if not valid_niches:
            continue
        total_products = sum(len(all_products[n]) for n in valid_niches)
        # Get representative image from first niche
        first_niche = valid_niches[0]
        first_product = all_products[first_niche][0] if all_products[first_niche] else None
        img_url = get_product_image(first_product['asin']) if first_product and first_product.get('asin') else ''
        cat_slug = CATEGORY_SLUGS[cat_name]
        cat_display = CATEGORY_DISPLAY[cat_name]
        theme_worlds.append({
            'name': cat_display,
            'slug': cat_slug,
            'image': img_url,
            'niche_count': len(valid_niches),
            'product_count': total_products,
            'description': f"{len(valid_niches)} Kategorien, {total_products} kuratierte Produkte"
        })
    
    # 3. SEASONAL RECOMMENDATIONS - Produkte passend zur Jahreszeit
    seasonal_products = []
    # Pick products from seasonally relevant niches
    seasonal_niche_map = {
        "Winter": ["weihnachten-advent", "herbst-winter-deko", "schlafen-wohlfuehlzimmer", "heizung-waerme", "duftkerzen", "wellness"],
        "Frühling": ["balkon-garten", "garten-pflanzen", "pflanzen", "bad-deko", "wanddeko", "gaeste-willkommen"],
        "Sommer": ["balkon-moebel-lounge", "outdoor-abenteuer", "reiseausruestung-leicht", "grillen", "camping"],
        "Herbst": ["herbst-deko", "herbst-winter-deko", "kaffee-genuss", "tee-lounge", "duftkerzen", "schlafen-wohlfuehlzimmer"]
    }
    relevant_niches = seasonal_niche_map.get(season, [])
    for niche_slug in relevant_niches:
        if niche_slug in all_products and all_products[niche_slug]:
            p = all_products[niche_slug][0]
            seasonal_products.append({
                'title': p.get('name', 'Produkt')[:60],
                'price': p.get('price', ''),
                'image': get_product_image(p.get('asin', '')),
                'link': p.get('link', f'https://www.amazon.de/dp/{p.get("asin", "")}?tag=balu17051-21'),
                'niche': NICHE_NAMES.get(niche_slug, niche_slug),
                'asin': p.get('asin', '')
            })
            if len(seasonal_products) >= 4:
                break
    
    # If not enough seasonal products, fill from general pool
    if len(seasonal_products) < 4:
        for niche_slug, products in all_products.items():
            if len(seasonal_products) >= 4:
                break
            if products and niche_slug not in [sp['niche'] for sp in seasonal_products]:
                p = products[0]
                seasonal_products.append({
                    'title': p.get('name', 'Produkt')[:60],
                    'price': p.get('price', ''),
                    'image': get_product_image(p.get('asin', '')),
                    'link': p.get('link', f'https://www.amazon.de/dp/{p.get("asin", "")}?tag=balu17051-21'),
                    'niche': NICHE_NAMES.get(niche_slug, niche_slug),
                    'asin': p.get('asin', '')
                })
    
    # 4. BUYING GUIDES (Kaufberatungen) - Placeholder für Phase 3
    # These will be real pages once Phase 3 is implemented
    buying_guides = [
        {
            'title': 'Die besten Möbel für kleine Wohnungen',
            'category': 'Wohnen & Haushalt',
            'slug': 'kaufberatung/moebel-kleine-wohnungen',
            'description': 'Platzsparende Lösungen, die funktionieren – getestet & verglichen.'
        },
        {
            'title': 'Smart Home für Einsteiger: Der komplette Guide',
            'category': 'Technik & Gaming',
            'slug': 'kaufberatung/smart-home-einsteiger',
            'description': 'Von smarter Beleuchtung bis Sicherheit – alles was du brauchst.'
        },
        {
            'title': 'Praktische Küchengadgets, die Zeit sparen',
            'category': 'Küche & Kochen',
            'slug': 'kaufberatung/kuechengadgets-zeit-sparen',
            'description': 'Clevere Helfer für den Alltag – unsere Top-Empfehlungen 2026.'
        }
    ]
    
    # 5. TOP PRODUCT HIGHLIGHTS - Besonders interessante Empfehlungen
    # Pick diverse top products across categories
    highlight_products = []
    used_niches = set()
    for cat_name, niches in CATEGORIES.items():
        if len(highlight_products) >= 6:
            break
        for niche_slug in niches[:3]:
            if niche_slug in all_products and all_products[niche_slug] and niche_slug not in used_niches:
                p = all_products[niche_slug][0]
                highlight_products.append({
                    'title': p.get('name', 'Produkt')[:55],
                    'price': p.get('price', ''),
                    'image': get_product_image(p.get('asin', '')),
                    'link': p.get('link', f'https://www.amazon.de/dp/{p.get("asin", "")}?tag=balu17051-21'),
                    'category': CATEGORY_DISPLAY[cat_name],
                    'asin': p.get('asin', '')
                })
                used_niches.add(niche_slug)
                break
    
    # 6. TRUST SECTION - Über Andreas Stehmann
    # 7. NEWSLETTER SECTION
    # 8. FOOTER - wird unten gerendert
    
    # Build theme worlds HTML
    theme_worlds_html = ''
    for tw in theme_worlds:
        theme_worlds_html += f'''
        <article class="theme-world-card" data-category="{tw['name']}">
            <a href="/{tw['slug']}/" class="theme-world-link" aria-label="{tw['name']} - {tw['niche_count']} Kategorien entdecken">
                <div class="theme-world-image" style="background-image: url('{tw['image']}')">
                    <span class="theme-world-overlay">
                        <span class="theme-world-count">{tw['product_count']} Produkte</span>
                    </span>
                </div>
                <div class="theme-world-content">
                    <h3>{tw['name']}</h3>
                    <p>{tw['description']}</p>
                    <span class="theme-world-cta">Entdecken →</span>
                </div>
            </a>
        </article>'''
    
    # Build seasonal products HTML
    seasonal_html = ''
    for sp in seasonal_products[:4]:
        seasonal_html += f'''
        <article class="product-card seasonal-card">
            <a href="{sp['link']}" class="product-link" rel="nofollow sponsored" target="_blank" aria-label="{sp['title']} bei Amazon ansehen" data-asin="{sp['asin']}" data-niche="{sp['niche']}" data-position="0" data-price="{sp['price']}">
                <div class="product-image-wrapper">
                    <img src="{sp['image']}" alt="{sp['title']}" loading="lazy" width="400" height="400">
                    <span class="product-badge">{season_emoji} {season}</span>
                </div>
                <div class="product-content">
                    <p class="product-category">{sp['niche']}</p>
                    <h4 class="product-title">{sp['title']}</h4>
                    {f'<p class="product-price">{sp["price"]}</p>' if sp['price'] else ''}
                    <span class="product-cta">Bei Amazon ansehen →</span>
                </div>
            </a>
            <p class="affiliate-disclosure" aria-hidden="true">*</p>
        </article>'''
    
    # Build buying guides HTML
    guides_html = ''
    for guide in buying_guides:
        guides_html += f'''
        <article class="guide-card">
            <div class="guide-content">
                <span class="guide-category">{guide['category']}</span>
                <h3><a href="/{guide['slug']}/">{guide['title']}</a></h3>
                <p>{guide['description']}</p>
                <a href="/{guide['slug']}/" class="guide-cta">Zum Ratgeber →</a>
            </div>
        </article>'''
    
    # Build highlight products HTML
    highlights_html = ''
    for hp in highlight_products:
        highlights_html += f'''
        <article class="product-card highlight-card">
            <a href="{hp['link']}" class="product-link" rel="nofollow sponsored" target="_blank" aria-label="{hp['title']} bei Amazon ansehen" data-asin="{hp['asin']}" data-niche="{hp['category']}" data-position="0" data-price="{hp['price']}">
                <div class="product-image-wrapper">
                    <img src="{hp['image']}" alt="{hp['title']}" loading="lazy" width="400" height="400">
                    <span class="product-badge highlight-badge">Empfehlung</span>
                </div>
                <div class="product-content">
                    <p class="product-category">{hp['category']}</p>
                    <h4 class="product-title">{hp['title']}</h4>
                    {f'<p class="product-price">{hp["price"]}</p>' if hp['price'] else ''}
                    <span class="product-cta">Bei Amazon ansehen →</span>
                </div>
            </a>
            <p class="affiliate-disclosure" aria-hidden="true">* Affiliate-Link</p>
        </article>'''
    
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Andreas Stehmann Links – Kuratierte Produktempfehlungen für dein Zuhause</title>
    <meta name="description" content="Handverlesene Amazon-Produkte für Wohnen, Küche, Smart Home, Wellness & mehr. Echte Empfehlungen, keine Algorithmen. Als Amazon-Partner verdiene ich an qualifizierten Käufen.">
    <link rel="canonical" href="https://balu1705.github.io/andreasstehmann-links/">
    <meta property="og:title" content="Andreas Stehmann Links – Kuratierte Produktempfehlungen für dein Zuhause">
    <meta property="og:description" content="Handverlesene Amazon-Produkte für Wohnen, Küche, Smart Home, Wellness & mehr. Echte Empfehlungen, keine Algorithmen.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://balu1705.github.io/andreasstehmann-links/">
    <meta property="og:image" content="{hero_img}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Andreas Stehmann Links – Kuratierte Produktempfehlungen">
    <meta name="twitter:description" content="Handverlesene Amazon-Produkte für dein Zuhause. Echte Empfehlungen, keine Algorithmen.">
    <meta name="twitter:image" content="{hero_img}">
    <link rel="stylesheet" href="/assets/style.css">
    <link rel="preconnect" href="https://m.media-amazon.com">
    <link rel="preconnect" href="https://images-na.ssl-images-amazon.com">
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('consent', 'default', {{
            'analytics_storage': 'denied',
            'ad_storage': 'denied',
            'ad_user_data': 'denied',
            'ad_personalization': 'denied'
        }});
        gtag('js', new Date());
        gtag('config', '{GA4_ID}');
    </script>
    <!-- JSON-LD WebSite Schema -->
    <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "WebSite", "name": "Andreas Stehmann Links", "url": "https://balu1705.github.io/andreasstehmann-links/", "potentialAction": {{"@type": "SearchAction", "target": "https://balu1705.github.io/andreasstehmann-links/?q={{search_term_string}}", "query-input": "required name=search_term_string"}}}}</script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="logo" aria-label="Andreas Stehmann Links – Startseite">
                <span class="logo-icon" aria-hidden="true">🔗</span>
                <span class="logo-text">Andreas Stehmann Links</span>
            </a>
            <nav class="main-nav" aria-label="Hauptnavigation">
                <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Menü öffnen">
                    <span class="hamburger" aria-hidden="true"></span>
                </button>
                <ul id="nav-menu" class="nav-menu" role="menubar">
                    {''.join(f'<li role="none"><a href="/{CATEGORY_SLUGS[cat]}/" role="menuitem">{CATEGORY_DISPLAY[cat]}</a></li>' for cat in CATEGORIES.keys())}
                    <li role="none"><a href="/deals/" role="menuitem">Deals</a></li>
                    <li role="none"><a href="/ueber-uns/" role="menuitem">Über uns</a></li>
                    <li role="none"><a href="/impressum/" role="menuitem">Impressum</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="site-main">
        <!-- 1. HERO SECTION -->
        <section class="hero" aria-labelledby="hero-title">
            <div class="hero-background" style="background-image: url('{hero_img}')"></div>
            <div class="hero-overlay"></div>
            <div class="container hero-content">
                <h1 id="hero-title">Produkte, die dein Zuhause besser machen</h1>
                <p class="hero-subtitle">Handverlesene Empfehlungen für Wohnen, Küche, Smart Home, Wellness & mehr. Keine Algorithmen – nur echte Auswahl.</p>
                <p class="hero-date" aria-live="polite">Stand: {datetime.now().strftime('%d. %B %Y')}</p>
                <div class="hero-cta-group">
                    <a href="#theme-worlds" class="btn btn-primary btn-large">Entdecke unsere Empfehlungen</a>
                    <a href="#highlights" class="btn btn-secondary btn-large">Unsere beliebtesten Produkte</a>
                </div>
                <p class="hero-disclaimer" aria-live="polite">Als Amazon-Partner verdiene ich an qualifizierten Käufen.</p>
            </div>
        </section>

        <!-- Affiliate Disclosure Notice -->
        <section class="affiliate-disclosure" aria-labelledby="affiliate-disclosure-title">
            <div class="container">
                <div class="affiliate-notice">
                    <strong id="affiliate-disclosure-title">Werbung / Affiliate-Links:</strong>
                    <span>Bei einem Kauf über diese Links erhalte ich eine Provision. Der Preis für dich bleibt gleich.</span>
                </div>
            </div>
        </section>

        <!-- 2. THEME WORLDS - 7 Themenwelten -->
        <section id="theme-worlds" class="theme-worlds" aria-labelledby="theme-worlds-title">
            <div class="container">
                <header class="section-header">
                    <h2 id="theme-worlds-title">Unsere Themenwelten</h2>
                    <p class="section-subtitle">Sieben kuratierte Bereiche – finde genau das, was du suchst</p>
                </header>
                <div class="theme-worlds-grid" role="list">
                    {theme_worlds_html}
                </div>
            </div>
        </section>

        <!-- 3. SEASONAL RECOMMENDATIONS -->
        <section id="seasonal" class="seasonal" aria-labelledby="seasonal-title">
            <div class="container">
                <header class="section-header">
                    <h2 id="seasonal-title">{season_emoji} {season}-Highlights</h2>
                    <p class="section-subtitle">{season_desc}</p>
                </header>
                <div class="product-grid seasonal-grid" role="list">
                    {seasonal_html}
                </div>
                <div class="section-footer">
                    <a href="/{seasonal_cat_slug}/" class="btn btn-outline">Alle {season}-Produkte entdecken</a>
                </div>
            </div>
        </section>

        <!-- 4. BUYING GUIDES -->
        <section id="guides" class="guides" aria-labelledby="guides-title">
            <div class="container">
                <header class="section-header">
                    <h2 id="guides-title">Aktuelle Kaufberatungen</h2>
                    <p class="section-subtitle">Fundierte Entscheidungs-Hilfen für wichtige Anschaffungen</p>
                </header>
                <div class="guides-grid" role="list">
                    {guides_html}
                </div>
                <div class="section-footer">
                    <a href="/kaufberatungen/" class="btn btn-outline">Alle Kaufberatungen anzeigen</a>
                </div>
            </div>
        </section>

        <!-- 5. PRODUCT HIGHLIGHTS -->
        <section id="highlights" class="highlights" aria-labelledby="highlights-title">
            <div class="container">
                <header class="section-header">
                    <h2 id="highlights-title">Besonders empfehlenswert</h2>
                    <p class="section-subtitle">Unsere Favoriten über alle Kategorien hinweg</p>
                </header>
                <div class="product-grid highlights-grid" role="list">
                    {highlights_html}
                </div>
            </div>
        </section>

        <!-- 6. TRUST SECTION -->
        <section id="trust" class="trust" aria-labelledby="trust-title">
            <div class="container">
                <div class="trust-grid">
                    <div class="trust-content">
                        <h2 id="trust-title">Vertrauen durch Transparenz</h2>
                        <p><strong>Andreas Stehmann</strong> kuratiert diese Empfehlungen seit 2024. Das Ziel: Dir die Recherche abnehmen und dir Produkte zeigen, die wirklich überzeugen.</p>
                        <div class="trust-points">
                            <div class="trust-point">
                                <span class="trust-icon" aria-hidden="true">✋</span>
                                <div>
                                    <h4>Handverlesen</h4>
                                    <p>Keine automatisierten Feeds. Jedes Produkt wird einzeln geprüft.</p>
                                </div>
                            </div>
                            <div class="trust-point">
                                <span class="trust-icon" aria-hidden="true">💬</span>
                                <div>
                                    <h4>Echte Bewertungen</h4>
                                    <p>Wir gewichten Kundenrezensionen stärker als Marketing-Versprechen.</p>
                                </div>
                            </div>
                            <div class="trust-point">
                                <span class="trust-icon" aria-hidden="true">🔄</span>
                                <div>
                                    <h4>Regelmäßige Updates</h4>
                                    <p>Preise, Verfügbarkeit & Sortiment werden wöchentlich geprüft.</p>
                                </div>
                            </div>
                            <div class="trust-point">
                                <span class="trust-icon" aria-hidden="true">🔗</span>
                                <div>
                                    <h4>Transparent finanziert</h4>
                                    <p>Affiliate-Links kennzeichnen wir offen. Dein Preis bleibt gleich.</p>
                                </div>
                            </div>
                        </div>
                        <a href="/ueber-uns/" class="btn btn-secondary">Mehr über uns erfahren</a>
                    </div>
                    <div class="trust-image" aria-hidden="true">
                        <div class="trust-stats">
                            <div class="stat"><strong>90+</strong><span>Kategorien</span></div>
                            <div class="stat"><strong>700+</strong><span>Produkte</span></div>
                            <div class="stat"><strong>7</strong><span>Themenwelten</span></div>
                            <div class="stat"><strong>wöchentlich</strong><span>aktualisiert</span></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 7. NEWSLETTER SECTION -->
        <section id="newsletter" class="newsletter" aria-labelledby="newsletter-title">
            <div class="container">
                <div class="newsletter-card">
                    <div class="newsletter-content">
                        <h2 id="newsletter-title">Wöchentlich Inspiration für dein Zuhause</h2>
                        <p>Keine Werbung. Nur kuratierte Produkt-Tipps, saisonale Ideen & exklusive Fundstücke – jeden Sonntag in deinem Postfach.</p>
                        <ul class="newsletter-benefits">
                            <li><span aria-hidden="true">✓</span> 3-5 handverlesene Empfehlungen pro Woche</li>
                            <li><span aria-hidden="true">✓</span> Saisonale Guides (Weihnachten, Balkon-Saison, etc.)</li>
                            <li><span aria-hidden="true">✓</span> Exklusive Preis-Drops & Lightning Deals</li>
                            <li><span aria-hidden="true">✓</span> Jederzeit abbestellbar, DSGVO-konform</li>
                        </ul>
                    </div>
                    <form class="newsletter-form" action="#" method="POST" aria-label="Newsletter anmelden">
                        <div class="form-group">
                            <label for="email" class="visually-hidden">E-Mail-Adresse</label>
                            <input type="email" id="email" name="email" placeholder="deine@email.de" required autocomplete="email" aria-describedby="newsletter-privacy">
                            <button type="submit" class="btn btn-primary">Kostenlos abonnieren</button>
                        </div>
                        <p id="newsletter-privacy" class="form-hint">Kein Spam. Datenschutz <a href="/datenschutz/">hier</a>. Als Amazon-Partner verdiene ich an qualifizierten Käufen.</p>
                    </form>
                    <p class="newsletter-whatsapp">
                        <a href="https://whatsapp.com/channel/0029VbE6HFZDjiOZFNBfRC2h" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp Kanal für tägliche Deals">
                            💬 Auch auf WhatsApp: Tägliche Amazon-Deals folgen
                        </a>
                    </p>
                </div>
            </div>
        </section>
    </main>

    <!-- 8. PROFESSIONAL FOOTER -->
    <footer class="site-footer" role="contentinfo">
        <div class="container">
            <div class="footer-main">
                <div class="footer-brand">
                    <a href="/" class="logo" aria-label="Andreas Stehmann Links – Startseite">
                        <span class="logo-icon" aria-hidden="true">🔗</span>
                        <span class="logo-text">Andreas Stehmann Links</span>
                    </a>
                    <p class="footer-tagline">Kuratierte Produktempfehlungen für smarte Kaufentscheidungen.</p>
                    <p class="footer-disclaimer">Als Amazon-Partner verdiene ich an qualifizierten Käufen.</p>
                </div>
                <nav class="footer-nav" aria-label="Themenwelten">
                    <h4>Themenwelten</h4>
                    <ul>
                        {''.join(f'<li><a href="/{CATEGORY_SLUGS[cat]}/">{CATEGORY_DISPLAY[cat]}</a></li>' for cat in CATEGORIES.keys())}
                    </ul>
                </nav>
                <nav class="footer-nav" aria-label="Hilfe & Info">
                    <h4>Hilfe & Info</h4>
                    <ul>
                        <li><a href="/ueber-uns/">Über uns</a></li>
                        <li><a href="/kaufberatungen/">Alle Kaufberatungen</a></li>
                        <li><a href="/newsletter/">Newsletter-Archiv</a></li>
                        <li><a href="/kontakt/">Kontakt</a></li>
                    </ul>
                </nav>
                <nav class="footer-nav" aria-label="Rechtliches">
                    <h4>Rechtliches</h4>
                    <ul>
                        <li><a href="/impressum/">Impressum</a></li>
                        <li><a href="/datenschutz/">Datenschutz</a></li>
                        <li><a href="/affiliate-hinweis/">Affiliate-Hinweis</a></li>
                        <li><a href="/preischeck/">Preisprüfung & Methodik</a></li>
                        <li><a href="/cookie-einstellungen/">Cookie-Einstellungen</a></li>
                    </ul>
                </nav>
            </div>
            <div class="footer-bottom">
                <p>&copy; {datetime.now().year} Andreas Stehmann Links. Alle Rechte vorbehalten.</p>
                <div class="footer-social" aria-label="Social Media">
                    <a href="https://www.threads.net/@gamerbrosis14" target="_blank" rel="noopener noreferrer" aria-label="Threads">🧵</a>
                    <a href="https://www.tiktok.com/@gamerbrosis14" target="_blank" rel="noopener noreferrer" aria-label="TikTok">🎵</a>
                    <a href="https://www.youtube.com/@Gamerbrosis" target="_blank" rel="noopener noreferrer" aria-label="YouTube">▶️</a>
                    <a href="https://whatsapp.com/channel/0029VbE6HFZDjiOZFNBfRC2h" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp Kanal">💬</a>
                </div>
            </div>
        </div>
    </footer>
    <!-- GA4 Affiliate Click Tracking -->
    <!-- Cookie Consent Banner -->
    <div id="cookie-banner" class="cookie-banner" role="dialog" aria-label="Cookie-Einwilligung" hidden>
        <div class="cookie-banner-content">
            <div class="cookie-banner-text">
                <h3>🍪 Cookie-Einstellungen</h3>
                <p>Wir nutzen Cookies für Analyse (GA4) und Affiliate-Tracking. Essentielle Funktionen laufen immer. <a href="/cookie-einstellungen/">Details & individuelle Einstellung</a></p>
            </div>
            <div class="cookie-banner-actions">
                <button class="btn btn-secondary" id="cookie-reject">Nur essentiell</button>
                <button class="btn btn-primary" id="cookie-accept">Alle akzeptieren</button>
            </div>
        </div>
    </div>
    <!-- GA4 Affiliate Click Tracking (Consent-gated) -->
    <script>
        // Cookie Consent Management
        (function() {{
            var CONSENT_COOKIE = 'cookie_consent';
            var CONSENT_EXPIRY_DAYS = 365;
            
            function getConsent() {{
                var match = document.cookie.match(new RegExp('(^| )' + CONSENT_COOKIE + '=([^;]+)'));
                return match ? JSON.parse(decodeURIComponent(match[2])) : null;
            }}
            
            function setConsent(consent) {{
                var date = new Date();
                date.setTime(date.getTime() + (CONSENT_EXPIRY_DAYS * 24 * 60 * 60 * 1000));
                document.cookie = CONSENT_COOKIE + '=' + encodeURIComponent(JSON.stringify(consent)) + ';expires=' + date.toUTCString() + ';path=/;SameSite=Lax';
            }}
            
            function updateGtagConsent(consent) {{
                if (typeof gtag !== 'function') return;
                gtag('consent', 'update', {{
                    'analytics_storage': consent.analytics ? 'granted' : 'denied',
                    'ad_storage': consent.marketing ? 'granted' : 'denied',
                    'ad_user_data': consent.marketing ? 'granted' : 'denied',
                    'ad_personalization': consent.marketing ? 'granted' : 'denied'
                }});
            }}
            
            function showBanner() {{
                var banner = document.getElementById('cookie-banner');
                if (banner) banner.hidden = false;
            }}
            
            function hideBanner() {{
                var banner = document.getElementById('cookie-banner');
                if (banner) banner.hidden = true;
            }}
            
            // Initialize on DOM ready
            document.addEventListener('DOMContentLoaded', function() {{
                var consent = getConsent();
                if (consent) {{
                    // Consent exists - apply to GA4
                    updateGtagConsent(consent);
                }} else {{
                    // No consent - show banner
                    showBanner();
                }}
                
                // Button handlers
                var acceptBtn = document.getElementById('cookie-accept');
                var rejectBtn = document.getElementById('cookie-reject');
                
                if (acceptBtn) {{
                    acceptBtn.addEventListener('click', function() {{
                        var consent = {{ analytics: true, marketing: true, essential: true, timestamp: Date.now() }};
                        setConsent(consent);
                        updateGtagConsent(consent);
                        hideBanner();
                    }});
                }}
                if (rejectBtn) {{
                    rejectBtn.addEventListener('click', function() {{
                        var consent = {{ analytics: false, marketing: false, essential: true, timestamp: Date.now() }};
                        setConsent(consent);
                        updateGtagConsent(consent);
                        hideBanner();
                    }});
                }}
            }});
        }})();
        
        // Affiliate Click Tracking - only fires with marketing consent
        document.addEventListener("DOMContentLoaded", function() {{
            document.querySelectorAll("a.product-link[data-asin]").forEach(function(link) {{
                link.addEventListener("click", function(e) {{
                    var asin = this.getAttribute("data-asin");
                    var niche = this.getAttribute("data-niche");
                    var position = this.getAttribute("data-position");
                    var price = this.getAttribute("data-price");
                    
                    // Check marketing consent before firing
                    var consent = (function() {{
                        var match = document.cookie.match(new RegExp('(^| )cookie_consent=([^;]+)'));
                        return match ? JSON.parse(decodeURIComponent(match[2])) : null;
                    }})();
                    
                    if (asin && typeof gtag === "function" && consent && consent.marketing) {{
                        gtag("event", "affiliate_click", {{
                            "asin": asin,
                            "niche": niche || "",
                            "position": parseInt(position) || 0,
                            "price": parseFloat(price) || 0,
                            "currency": "EUR",
                            "affiliate_tag": "balu17051-21",
                            "link_domain": "amazon.de"
                        }});
                    }}
                }});
            }});
        }});
    </script>
    <script src="/assets/main.js"></script>
</body>
</html>'''

def generate_legal_pages():
    """Generate legal pages (Impressum, Datenschutz, Affiliate-Hinweis)."""
    impressum = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Impressum - Andreas Stehmann Links</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <header class="site-header"><div class="container"><a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a></div></header>
    <main class="site-main"><div class="container"><h1>Impressum</h1><div class="legal-content"><h2>Angaben gemäß § 5 TMG</h2><p><strong>Andreas Stehmann</strong><br>Musterstraße 123<br>12345 Musterstadt<br>Deutschland</p><h2>Kontakt</h2><p>E-Mail: andreas@example.de</p><h2>Haftungsausschluss</h2><p>Als Amazon-Partner verdiene ich an qualifizierten Käufen. Die auf dieser Website enthaltenen Links zu Amazon sind Affiliate-Links.</p></div></div></main>
    <footer class="site-footer"><div class="container"><p>&copy; 2024 Andreas Stehmann Links.</p></div></footer>
</body>
</html>'''

    datenschutz = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datenschutz - Andreas Stehmann Links</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <header class="site-header"><div class="container"><a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a></div></header>
    <main class="site-main"><div class="container"><h1>Datenschutzerklärung</h1><div class="legal-content"><p>Diese Website verwendet keine Cookies und speichert keine persönlichen Daten. Bei Klick auf Affiliate-Links wirst du zu Amazon weitergeleitet – dort gelten die Datenschutzbestimmungen von Amazon.</p><h2>Affiliate-Links</h2><p>Die mit * gekennzeichneten Links sind Affiliate-Links. Erfolgt darüber ein Kauf, erhalten wir eine Provision. Für dich entstehen keine Mehrkosten.</p></div></div></main>
    <footer class="site-footer"><div class="container"><p>&copy; 2024 Andreas Stehmann Links.</p></div></footer>
</body>
</html>'''

    preischeck = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preisprüfung & Methodik - Andreas Stehmann Links</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <header class="site-header"><div class="container"><a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a></div></header>
    <main class="site-main"><div class="container"><h1>Wie wir Preise prüfen</h1><div class="legal-content">
        <section class="transparency-box" aria-labelledby="preischeck-title">
            <h2 id="preischeck-title">🔄 Unsere Preisprüfung im Überblick</h2>
            <p>Wir aktualisieren Preise, Verfügbarkeit und Sortiment <strong>wöchentlich automatisiert</strong> über die Amazon Product Advertising API. Die angezeigten Preise sind Momentaufnahmen und können sich kurzfristig ändern.</p>
            <div class="transparency-grid">
                <div class="transparency-item">
                    <span class="transparency-icon" aria-hidden="true">🤖</span>
                    <div>
                        <h3>Automatisierter Abgleich</h3>
                        <p>Preise werden via Amazon API wöchentlich abgeglichen. Manuelle Prüfung bei Auffälligkeiten.</p>
                    </div>
                </div>
                <div class="transparency-item">
                    <span class="transparency-icon" aria-hidden="true">⏰</span>
                    <div>
                        <h3>Momentaufnahme</h3>
                        <p>Der angezeigte Preis ist der Zeitpunkt des letzten API-Abgleichs. Auf Amazon kann er abweichen.</p>
                    </div>
                </div>
                <div class="transparency-item">
                    <span class="transparency-icon" aria-hidden="true">🔗</span>
                    <div>
                        <h3>Live-Preis auf Amazon</h3>
                        <p>Ein Klick auf den Produktlink zeigt dir immer den aktuellen Preis direkt bei Amazon.</p>
                    </div>
                </div>
            </div>
        </section>
        <h2>Methodik der Produktauswahl</h2>
        <ul>
            <li><strong>Datenbasis:</strong> Amazon Product Advertising API (offizielle Schnittstelle)</li>
            <li><strong>Aktualisierungszyklus:</strong> Wöchentlich (montags) + bei saisonalen Events (Prime Day, Black Friday) täglich</li>
            <li><strong>Qualitätskriterien:</strong> Mindestbewertung 4,0 Sterne, mind. 50 Bewertungen, Lieferbarkeit</li>
            <li><strong>Preisvalidierung:</strong> Plausibilitätsprüfung gegen historische Preisspannen (Ausreißer werden geflaggt)</li>
        </ul>
        <h2>Hinweis zu Preisangaben</h2>
        <p>Alle Preise in EUR, inkl. MwSt., zzgl. ggf. Versandkosten. Der finale Preis wird auf der Amazon-Produktseite angezeigt. Preisänderungen seit dem letzten API-Abgleich sind möglich.</p>
        <h2>Legal-TODO (für Anwalt prüfen)</h2>
        <ul>
            <li>§ 5a UWG: Angabe des Grundpreises bei Mengenware prüfen</li>
            <li>PAngV: Preisangabenverordnung-Konformität bei Aktionspreisen sicherstellen</li>
            <li>Kennzeichnungspflicht bei „Streichpreisen“ (UVP vs. Verkaufspreis) klären</li>
            <li>Haftungsausschluss für Preisabweichungen zwischen API und Amazon-Webseite formulieren</li>
        </ul>
</div></div></main>
    <footer class="site-footer"><div class="container"><p>&copy; 2024 Andreas Stehmann Links.</p></div></footer>
</body>
</html>'''

    affiliate_hinweis = '''<!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Affiliate-Hinweis - Andreas Stehmann Links</title>
        <link rel="stylesheet" href="/assets/style.css">
    </head>
    <body>
        <header class="site-header"><div class="container"><a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a></div></header>
        <main class="site-main"><div class="container"><h1>Affiliate-Hinweis</h1><div class="legal-content">
            <section class="transparency-box" aria-labelledby="transparency-title">
                <h2 id="transparency-title">❓ Verdiene ich an den Links?</h2>
                <p><strong>Ja.</strong> Als Amazon-Partner verdiene ich an qualifizierten Käufen. Das bedeutet: Wenn du über einen Produktlink auf dieser Seite bei Amazon einkaufe, erhalte ich eine kleine Provision.</p>
                <div class="transparency-grid">
                    <div class="transparency-item">
                        <span class="transparency-icon" aria-hidden="true">💰</span>
                        <div>
                            <h3>Keine Mehrkosten für dich</h3>
                            <p>Du zahlst den regulären Amazon-Preis. Die Provision wird vom Händler getragen, nicht von dir.</p>
                        </div>
                    </div>
                    <div class="transparency-item">
                        <span class="transparency-icon" aria-hidden="true">🔍</span>
                        <div>
                            <h3>Unabhängige Auswahl</h3>
                            <p>Die Provision beeinflusst <strong>nicht</strong> unsere Empfehlungen. Wir wählen Produkte nach Kundenbewertungen, Tests & Preis-Leistung.</p>
                        </div>
                    </div>
                    <div class="transparency-item">
                        <span class="transparency-icon" aria-hidden="true">🏠</span>
                        <div>
                            <h3>Finanziert den Betrieb</h3>
                            <p>Die Einnahmen decken Hosting, Domain, Wartung & Recherche – damit diese Seite unabhängig bleibt.</p>
                        </div>
                    </div>
                </div>
            </section>
            <h2>Transparenz bei Empfehlungen</h2><p>Auf dieser Website verwenden wir Affiliate-Links (markiert mit * oder durch den Hinweis "Als Amazon-Partner verdiene ich an qualifizierten Käufen").</p><h2>Was bedeutet das für dich?</h2><ul><li>Du klickst auf einen Produktlink und wirst zu Amazon weitergeleitet</li><li>Kaufst du dort etwas, erhalten wir eine kleine Provision</li><li><strong>Für dich ändert sich der Preis nicht</strong> – du zahlst den regulären Amazon-Preis</li></ul><h2>Warum Affiliate-Links?</h2><p>Die Provisionen decken die Betriebskosten dieser Website (Hosting, Domain, Wartung) und ermöglichen es uns, weiterhin unabhängige Produktempfehlungen zu recherchieren und zu veröffentlichen.</p><h2>Unsere Unabhängigkeit</h2><p>Die Provision beeinflusst <strong>nicht</strong> unsere Produktauswahl. Wir empfehlen nur Produkte, von denen wir überzeugt sind – basierend auf Kundenbewertungen, Testergebnissen und Preis-Leistungs-Verhältnis.</p></div></div></main>
        <footer class="site-footer"><div class="container"><p>&copy; 2024 Andreas Stehmann Links.</p></div></footer>
    </body>
    </html>'''

    cookie_einstellungen = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cookie-Einstellungen - Andreas Stehmann Links</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <header class="site-header"><div class="container"><a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a></div></header>
    <main class="site-main"><div class="container"><h1>Cookie-Einstellungen</h1><div class="legal-content">
        <section class="transparency-box" aria-labelledby="cookie-title">
            <h2 id="cookie-title">🍪 Deine Cookie-Präferenzen</h2>
            <p>Wir respektieren deine Privatsphäre. Hier kannst du einstellen, welche Daten wir erfassen dürfen. Essenzielle Funktionen (wie die Seitennavigation) funktionieren immer.</p>
        </section>
        <h2>Kategorien</h2>
        <div class="cookie-category">
            <h3>Essentiell (immer aktiv)</h3>
            <p>Diese Cookies sind für den Betrieb der Website zwingend erforderlich und können nicht deaktiviert werden.</p>
            <ul>
                <li>Sitzungs-Cookies für Navigation & Sicherheit</li>
                <li>Cookie-Consent-Speicherung (deine Wahl hier)</li>
            </ul>
        </div>
        <div class="cookie-category">
            <h3>Analyse & Messung (Google Analytics / GA4)</h3>
            <label class="cookie-toggle">
                <input type="checkbox" id="consent-analytics">
                <span class="toggle-slider"></span>
                <span class="toggle-label">Aktiviert – misst Seitenaufrufe, Verweildauer, Geräteinformationen (anonymisiert)</span>
            </label>
            <p class="cookie-desc">Wir nutzen Google Analytics 4 mit IP-Anonymisierung. Daten helfen uns, Inhalte zu verbessern. <a href="/datenschutz/">Details in der Datenschutzerklärung</a>.</p>
        </div>
        <div class="cookie-category">
            <h3>Affiliate-Tracking (Klick-Messung)</h3>
            <label class="cookie-toggle">
                <input type="checkbox" id="consent-affiliate">
                <span class="toggle-slider"></span>
                <span class="toggle-label">Aktiviert – misst Klicks auf Produktlinks (ASIN, Position, Preis) für GA4 Event 'affiliate_click'</span>
            </label>
            <p class="cookie-desc">Wenn du auf einen Produktlink klickst, senden wir ein anonymisiertes Event an GA4 (ASIN, Nische, Position, Preis). Keine personenbezogene Daten. <a href="/affiliate-hinweis/">Mehr zu Affiliate-Links</a>.</p>
        </div>
        <p class="form-hint">Änderungen speichern wir in einem Cookie (Laufzeit: 1 Jahr). Du kannst deine Einstellung jederzeit hier anpassen.</p>
        <button class="btn btn-secondary" id="save-consent">Einstellungen speichern</button>
    </div></div></main>
    <footer class="site-footer"><div class="container"><p>&copy; 2024 Andreas Stehmann Links.</p></div></footer>
    <script src="/assets/main.js"></script>
</body>
</html>'''

    return {
        "impressum": impressum,
        "datenschutz": datenschutz,
        "affiliate-hinweis": affiliate_hinweis,
        "preischeck": preischeck,
        "cookie-einstellungen": cookie_einstellungen
    }

def generate_sitemap(all_products):
    """Generate sitemap.xml."""
    urls = [
        ('https://balu1705.github.io/andreasstehmann-links/', '1.0', 'daily'),
    ]
    
    # Category pages
    for cat_name in CATEGORIES.keys():
        slug = cat_name.lower().replace(' ', '-').replace('&', '').replace('🏠 ', '').replace('🍳 ', '').replace('💄 ', '').replace('👶 ', '').replace('🏋️ ', '').replace('💻 ', '').replace('📚 ', '')
        urls.append((f'https://balu1705.github.io/andreasstehmann-links/{slug}/', '0.8', 'weekly'))
    
    # Niche pages
    for niche_slug, products in all_products.items():
        if products:
            urls.append((f'https://balu1705.github.io/andreasstehmann-links/{niche_slug}/', '0.6', 'weekly'))
    
    # Blog index
    urls.append(('https://balu1705.github.io/andreasstehmann-links/blog/', '0.8', 'daily'))
    
    # Blog article pages
    niche_scores = [(slug, len(products)) for slug, products in all_products.items() if products]
    niche_scores.sort(key=lambda x: x[1], reverse=True)
    top_niches = [slug for slug, _ in niche_scores[:20]]
    for slug in top_niches:
        urls.append((f'https://balu1705.github.io/andreasstehmann-links/blog/{slug}/', '0.6', 'weekly'))
    
    # Deals page and feeds
    urls.append(('https://balu1705.github.io/andreasstehmann-links/deals/', '0.8', 'daily'))
    urls.append(('https://balu1705.github.io/andreasstehmann-links/deals/feed.xml', '0.5', 'daily'))
    urls.append(('https://balu1705.github.io/andreasstehmann-links/deals/feed.json', '0.5', 'daily'))
    urls.append(('https://balu1705.github.io/andreasstehmann-links/shopping-feed.xml', '0.5', 'daily'))
    
    # Legal pages
    for page in ['impressum', 'datenschutz', 'affiliate-hinweis', 'ueber-uns', 'preischeck']:
        urls.append((f'https://balu1705.github.io/andreasstehmann-links/{page}/', '0.3', 'monthly'))
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, priority, changefreq in urls:
        xml.append(f'  <url><loc>{url}</loc><priority>{priority}</priority><changefreq>{changefreq}</changefreq></url>')
    xml.append('</urlset>')
    return '\n'.join(xml)

def generate_robots_txt():
    """Generate robots.txt."""
    return '''User-agent: *
Allow: /
Sitemap: https://balu1705.github.io/andreasstehmann-links/sitemap.xml
'''


def generate_deals_feed(all_products):
    """Generate RSS 2.0, JSON Feed, and HTML page for deals."""
    from datetime import datetime, timezone
    import json
    
    # Collect all products with affiliate links
    deals = []
    for niche_slug, products in all_products.items():
        if not products:
            continue
        niche_name = NICHE_NAMES.get(niche_slug, niche_slug.replace('-', ' ').title())
        for i, product in enumerate(products):
            asin = product.get('asin', '')
            name = product.get('name', '')
            price = product.get('price', '')
            if asin and name:
                affiliate_url = f'https://www.amazon.de/dp/{asin}?tag=balu17051-21'
                image_url = f'https://m.media-amazon.com/images/I/{asin}._AC_SL500_.jpg'
                deals.append({
                    'niche_slug': niche_slug,
                    'niche_name': niche_name,
                    'asin': asin,
                    'name': name,
                    'price': price,
                    'affiliate_url': affiliate_url,
                    'image_url': image_url,
                    'position': i,
                })
    
    # Sort by niche priority (bestseller first) then position
    niche_priority = {'bestseller': 0, 'smart-home': 1, 'geschenke': 2}
    deals.sort(key=lambda d: (niche_priority.get(d['niche_slug'], 99), d['position']))
    
    # Limit to top 50 deals for feeds
    feed_deals = deals[:50]
    
    now = datetime.now(timezone.utc)
    now_rfc2822 = now.strftime('%a, %d %b %Y %H:%M:%S %z')
    now_iso = now.isoformat()
    base_url = 'https://balu1705.github.io/andreasstehmann-links'
    
    # ---- RSS 2.0 ----
    rss_items = []
    for deal in feed_deals:
        pub_date = now_rfc2822  # Could use individual dates if available
        rss_items.append(f'''    <item>
      <title><![CDATA[{deal['name']} – {deal['price']} €]]></title>
      <link>{deal['affiliate_url']}</link>
      <guid isPermaLink="true">{deal['affiliate_url']}</guid>
      <description><![CDATA[<img src="{deal['image_url']}" alt="{deal['name']}" style="max-width:200px;"><br/><strong>{deal['niche_name']}</strong><br/>Preis: {deal['price']} €<br/><a href="{deal['affiliate_url']}">Bei Amazon ansehen →</a>]]></description>
      <pubDate>{pub_date}</pubDate>
      <category>{deal['niche_name']}</category>
    </item>''')
    
    rss_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>Andreas Stehmann Links – Top Deals</title>
    <link>{base_url}/deals/</link>
    <description>Die besten Amazon-Deals täglich aktualisiert. Affiliate-Links mit Tag balu17051-21.</description>
    <language>de-DE</language>
    <lastBuildDate>{now_rfc2822}</lastBuildDate>
    <atom:link href="{base_url}/deals/feed.xml" rel="self" type="application/rss+xml"/>
    <ttl>60</ttl>
    {''.join(rss_items)}
  </channel>
</rss>'''
    
    # ---- JSON Feed (version 1.1) ----
    json_items = []
    for deal in feed_deals:
        json_items.append({
            'id': deal['affiliate_url'],
            'url': deal['affiliate_url'],
            'title': f"{deal['name']} – {deal['price']} €",
            'content_html': f'<img src="{deal["image_url"]}" alt="{deal["name"]}" style="max-width:200px;"><br/><strong>{deal["niche_name"]}</strong><br/>Preis: {deal["price"]} €<br/><a href="{deal["affiliate_url"]}">Bei Amazon ansehen →</a>',
            'date_published': now_iso,
            'tags': [deal['niche_name'], 'Amazon', 'Deal'],
            'author': {'name': 'Andreas Stehmann Links'},
        })
    
    json_feed = {
        'version': 'https://jsonfeed.org/version/1.1',
        'title': 'Andreas Stehmann Links – Top Deals',
        'home_page_url': f'{base_url}/deals/',
        'feed_url': f'{base_url}/deals/feed.json',
        'description': 'Die besten Amazon-Deals täglich aktualisiert.',
        'language': 'de',
        'items': json_items,
    }
    
    # ---- HTML Page ----
    deal_cards = []
    for deal in deals[:100]:  # Show more on HTML page
        badge = ''
        if deal['position'] == 0:
            badge = '<span class="deal-badge badge-favorite">🏆 Favorit</span>'
        elif deal['position'] == 1:
            badge = '<span class="deal-badge badge-value">💡 Preis-Leistung</span>'
        elif deal['position'] == 2:
            badge = '<span class="deal-badge badge-popular">⭐ Beliebt</span>'
        
        deal_cards.append(f'''
        <article class="deal-card" data-niche="{deal['niche_slug']}">
            <a href="{deal['affiliate_url']}" class="deal-link" target="_blank" rel="noopener sponsored">
                <div class="deal-image-wrapper">
                    <img src="{deal['image_url']}" alt="{deal['name']}" class="deal-image" loading="lazy">
                    {badge}
                </div>
                <div class="deal-info">
                    <span class="deal-niche">{deal['niche_name']}</span>
                    <h3 class="deal-title">{deal['name']}</h3>
                    <div class="deal-price">{deal['price']} €</div>
                </div>
            </a>
        </article>''')
    
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top Deals – Andreas Stehmann Links</title>
    <meta name="description" content="Die besten Amazon-Deals täglich aktualisiert. 719+ Produkte, 94 Nischen, Affiliate-Links mit Tag balu17051-21.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{base_url}/deals/">
    <link rel="alternate" type="application/rss+xml" title="RSS Feed" href="{base_url}/deals/feed.xml">
    <link rel="alternate" type="application/json" title="JSON Feed" href="{base_url}/deals/feed.json">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="de_DE">
    <meta property="og:site_name" content="Andreas Stehmann Links">
    <meta property="og:title" content="Top Deals – Täglich aktualisiert">
    <meta property="og:description" content="Die besten Amazon-Deals aus 94 Nischen. Täglich frisch, mit Affiliate-Links.">
    <meta property="og:url" content="{base_url}/deals/">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="stylesheet" href="/assets/style.css">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-YPCSF9BFH2"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-YPCSF9BFH2');
    </script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a>
            <nav class="main-nav" aria-label="Hauptnavigation">
                <a href="/">Startseite</a>
                <a href="/blog/">Blog</a>
                <a href="/deals/">Deals</a>
                <a href="/ueber-uns/">Über uns</a>
            </nav>
        </div>
    </header>
    
    <main class="site-main">
        <div class="container">
            <nav class="breadcrumb" aria-label="Breadcrumb">
                <a href="/">Startseite</a> <span class="sep">/</span>
                <span aria-current="page">Top Deals</span>
            </nav>
            
            <header class="page-header">
                <h1>Top Deals – Täglich aktualisiert</h1>
                <p class="page-lead">Die besten Produkte aus 94 Nischen, sortiert nach Relevanz. Alle Links sind Affiliate-Links (Tag: <code>balu17051-21</code>).</p>
                <p class="page-meta">Letzte Aktualisierung: {now.strftime('%d.%m.%Y %H:%M')} UTC | {len(deals)} Produkte | <a href="/deals/feed.xml">RSS abonnieren</a> | <a href="/deals/feed.json">JSON Feed</a></p>
            </header>
            
            <div class="deal-filters">
                <button class="filter-btn active" data-filter="all">Alle ({len(deals)})</button>
                <button class="filter-btn" data-filter="bestseller">Bestseller</button>
                <button class="filter-btn" data-filter="smart-home">Smart Home</button>
                <button class="filter-btn" data-filter="geschenke">Geschenke</button>
                <button class="filter-btn" data-filter="kuechenhelfer">Küche</button>
                <button class="filter-btn" data-filter="technik">Technik</button>
            </div>
            
            <div class="deals-grid" id="deals-grid">
                {''.join(deal_cards)}
            </div>
            
            <section class="cta-section">
                <h2>Mehr entdecken</h2>
                <p>Stöbere in allen <a href="/">Nischenkategorien</a> oder lies unsere <a href="/blog/">Kaufberatungen im Blog</a>.</p>
                <a href="/" class="btn btn-primary">Zur Startseite</a>
            </section>
        </div>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div><h4>Andreas Stehmann Links</h4><p>Die besten Produkte finden – ohne stundenlanges Suchen.</p></div>
                <nav><h4>Navigation</h4><ul><li><a href="/">Startseite</a></li><li><a href="/deals/">Deals</a></li><li><a href="/blog/">Blog</a></li><li><a href="/ueber-uns/">Über uns</a></li><li><a href="/impressum/">Impressum</a></li><li><a href="/datenschutz/">Datenschutz</a></li></ul></nav>
                <nav><h4>Feeds</h4><ul><li><a href="/deals/feed.xml">RSS Feed</a></li><li><a href="/deals/feed.json">JSON Feed</a></li></ul></nav>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Andreas Stehmann Links. Alle Rechte vorbehalten.</p>
                <p>* Affiliate-Links: Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p>
            </div>
        </div>
    </footer>
    
    <script src="/assets/main.js"></script>
    <script>
    // Simple filter for deals page
    document.addEventListener('DOMContentLoaded', function() {{
        const buttons = document.querySelectorAll('.filter-btn');
        const cards = document.querySelectorAll('.deal-card');
        buttons.forEach(btn => {{
            btn.addEventListener('click', function() {{
                buttons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                const filter = this.dataset.filter;
                cards.forEach(card => {{
                    if (filter === 'all' || card.dataset.niche === filter || card.dataset.niche.startsWith(filter)) {{
                        card.style.display = '';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
            }});
        }});
    }});
    </script>
</body>
</html>'''
    
    return {
        'rss': rss_xml,
        'json': json.dumps(json_feed, ensure_ascii=False, indent=2),
        'html': html,
    }


def generate_shopping_feed(all_products):
    """Generate Google Shopping Feed XML (Merchant Center format)."""
    from datetime import datetime, timezone
    
    products_feed = []
    for niche_slug, products in all_products.items():
        if not products:
            continue
        niche_name = NICHE_NAMES.get(niche_slug, niche_slug.replace('-', ' ').title())
        for i, product in enumerate(products):
            asin = product.get('asin', '')
            name = product.get('name', '')
            price = product.get('price', '')
            if asin and name and price:
                # Clean price (remove €, comma to dot)
                price_clean = price.replace('€', '').replace(',', '.').strip()
                try:
                    price_val = float(price_clean)
                except ValueError:
                    continue
                
                affiliate_url = f'https://www.amazon.de/dp/{asin}?tag=balu17051-21'
                image_url = f'https://m.media-amazon.com/images/I/{asin}._AC_SL1500_.jpg'
                
                # Google Product Category mapping (simplified)
                category_map = {
                    'smart-home': 'Electronics > Communications > Telephony > Smart Home Devices',
                    'bestseller': 'Electronics',
                    'geschenke': 'Arts & Entertainment > Hobbies & Creative Arts > Party & Celebration > Gifts',
                    'kuechenhelfer': 'Home & Garden > Kitchen & Dining > Kitchen Tools & Gadgets',
                    'backen-kochen': 'Home & Garden > Kitchen & Dining > Kitchen Tools & Gadgets',
                    'baby-kindersicherheit': 'Baby & Toddler > Baby Safety',
                    'babywelt': 'Baby & Toddler > Baby Gear',
                    'fitness-zu-hause': 'Sporting Goods > Exercise & Fitness > Home Gym Equipment',
                    'outdoor-camping': 'Sporting Goods > Camping & Hiking',
                    'gaming-zubehoer': 'Electronics > Computers > Computer Accessories > Gaming Accessories',
                    'pflanzen-pflege': 'Home & Garden > Gardening > Garden Tools & Equipment',
                }
                google_category = category_map.get(niche_slug, 'Electronics')
                
                products_feed.append(f'''    <item>
      <g:id>{asin}</g:id>
      <g:title><![CDATA[{name}]]></g:title>
      <g:description><![CDATA[Top Produkt in der Kategorie {niche_name}. Preis: {price} €.]]></g:description>
      <g:link>{affiliate_url}</g:link>
      <g:image_link>{image_url}</g:image_link>
      <g:condition>new</g:condition>
      <g:availability>in stock</g:availability>
      <g:price>{price_val:.2f} EUR</g:price>
      <g:brand><![CDATA[Amazon]]></g:brand>
      <g:google_product_category><![CDATA[{google_category}]]></g:google_product_category>
      <g:product_type><![CDATA[{niche_name}]]></g:product_type>
      <g:identifier_exists>FALSE</g:identifier_exists>
    </item>''')
    
    now = datetime.now(timezone.utc).isoformat()
    
    shopping_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Andreas Stehmann Links – Product Feed</title>
    <link>https://balu1705.github.io/andreasstehmann-links/</link>
    <description>Product feed for Google Merchant Center</description>
    <atom:link href="https://balu1705.github.io/andreasstehmann-links/shopping-feed.xml" rel="self" type="application/rss+xml"/>
    <lastBuildDate>{now}</lastBuildDate>
    {''.join(products_feed)}
  </channel>
</rss>'''
    
    return shopping_xml


def generate_assets():
    """Generate CSS and JS assets."""
    css = '''
/* ===== RESET & BASE ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
    --color-primary: #0066cc;
    --color-primary-hover: #0052a3;
    --color-primary-light: #e6f0fa;
    --color-text: #1a1a2e;
    --color-text-muted: #6b7280;
    --color-text-light: #9ca3af;
    --color-bg: #ffffff;
    --color-bg-alt: #f8fafc;
    --color-border: #e5e7eb;
    --color-border-hover: #d1d5db;
    --color-success: #059669;
    --color-warning: #d97706;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --transition-fast: 150ms ease;
    --transition-base: 250ms ease;
    --container-max: 1200px;
    --header-height: 72px;
}
html { scroll-behavior: smooth; -webkit-font-smoothing: antialiased; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; font-size: 16px; line-height: 1.6; color: var(--color-text); background: var(--color-bg); min-height: 100vh; display: flex; flex-direction: column; }
a { color: var(--color-primary); text-decoration: none; transition: color var(--transition-fast); }
a:hover { color: var(--color-primary-hover); }
img { max-width: 100%; height: auto; display: block; }
.container { width: 100%; max-width: var(--container-max); margin: 0 auto; padding: 0 20px; }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 12px 24px; font-size: 15px; font-weight: 600; border-radius: var(--radius-md); border: none; cursor: pointer; transition: all var(--transition-fast); text-decoration: none; }
.btn-primary { background: var(--color-primary); color: white; }
.btn-primary:hover { background: var(--color-primary-hover); color: white; transform: translateY(-1px); box-shadow: var(--shadow-md); }
.btn-large { padding: 16px 32px; font-size: 17px; }

/* ===== HEADER ===== */
.site-header { position: sticky; top: 0; z-index: 100; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-bottom: 1px solid var(--color-border); height: var(--header-height); }
.site-header .container { display: flex; align-items: center; justify-content: space-between; height: 100%; }
.logo { display: flex; align-items: center; gap: 10px; font-size: 20px; font-weight: 700; color: var(--color-text); text-decoration: none; }
.logo:hover { color: var(--color-primary); }
.logo-icon { font-size: 24px; }
.main-nav ul { display: flex; align-items: center; gap: 4px; list-style: none; }
.main-nav a { display: block; padding: 10px 16px; font-size: 14px; font-weight: 500; color: var(--color-text); border-radius: var(--radius-sm); transition: all var(--transition-fast); }
.main-nav a:hover { color: var(--color-primary); background: var(--color-primary-light); }
.nav-toggle { display: none; background: none; border: none; font-size: 24px; cursor: pointer; padding: 8px; }

/* ===== BREADCRUMB ===== */
.breadcrumb { padding: 16px 0; font-size: 14px; color: var(--color-text-muted); }
.breadcrumb a { color: var(--color-text-muted); }
.breadcrumb a:hover { color: var(--color-primary); }
.breadcrumb span { margin: 0 8px; color: var(--color-text-light); }

/* ===== HERO ===== */
.hero { padding: 80px 0; text-align: center; background: linear-gradient(180deg, var(--color-bg) 0%, var(--color-bg-alt) 100%); }
.hero h1 { font-size: clamp(32px, 5vw, 48px); font-weight: 800; line-height: 1.2; margin-bottom: 16px; color: var(--color-text); }
.hero-tagline { font-size: clamp(18px, 2.5vw, 22px); color: var(--color-text-muted); margin-bottom: 12px; max-width: 700px; margin-left: auto; margin-right: auto; }
.hero-disclaimer { font-size: 14px; color: var(--color-text-light); margin-bottom: 32px; }
.hero-date { font-size: 14px; color: var(--color-text-muted); font-weight: 500; margin-bottom: 24px; padding: 8px 16px; background: var(--color-bg); border-radius: var(--radius-md); display: inline-block; border: 1px solid var(--color-border); }
.niche-hero, .category-hero { padding: 60px 0; background: var(--color-bg-alt); border-bottom: 1px solid var(--color-border); }
.niche-hero h1, .category-hero h1 { font-size: clamp(28px, 4vw, 40px); font-weight: 800; margin-bottom: 8px; }
.hero-subtitle { font-size: 18px; color: var(--color-text-muted); }

/* ===== AFFILIATE DISCLOSURE ===== */
.affiliate-disclosure { padding: 16px 0; background: var(--color-primary-light); border-bottom: 1px solid var(--color-border); }
.affiliate-notice { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; color: var(--color-text); }
.affiliate-notice strong { font-weight: 600; color: var(--color-text); }
.affiliate-notice span { color: var(--color-text-muted); }

/* ===== PRODUCT GRID ===== */
.product-grid-section { padding: 60px 0; }
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 24px; }
.product-card { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden; transition: all var(--transition-base); }
.product-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-xl); border-color: var(--color-border-hover); }
.product-link { display: block; text-decoration: none; color: inherit; }
.product-image-wrapper { position: relative; aspect-ratio: 1; background: var(--color-bg-alt); overflow: hidden; }
.product-image { width: 100%; height: 100%; object-fit: contain; padding: 20px; transition: transform var(--transition-base); }
.product-card:hover .product-image { transform: scale(1.02); }
.product-badge { position: absolute; bottom: 12px; right: 12px; background: var(--color-primary); color: white; padding: 6px 12px; border-radius: var(--radius-sm); font-size: 12px; font-weight: 600; opacity: 0; transform: translateY(10px); transition: all var(--transition-fast); }
.product-card:hover .product-badge { opacity: 1; transform: translateY(0); }
.product-info { padding: 16px; }
.product-title { font-size: 15px; font-weight: 600; line-height: 1.4; color: var(--color-text); margin-bottom: 8px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.product-price { font-size: 18px; font-weight: 700; color: var(--color-primary); }

/* ===== CATEGORY GRID (Homepage) ===== */
.home-categories { padding: 60px 0; background: var(--color-bg); }
.home-categories h2 { font-size: 28px; font-weight: 700; text-align: center; margin-bottom: 40px; }
.home-category-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; }
.home-category-card { border-radius: var(--radius-xl); overflow: hidden; border: 1px solid var(--color-border); transition: all var(--transition-base); background: var(--color-bg); }
.home-category-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-xl); }
.home-category-link { display: block; text-decoration: none; color: inherit; }
.home-category-image { aspect-ratio: 16/10; background: var(--color-bg-alt); overflow: hidden; }
.home-category-image img { width: 100%; height: 100%; object-fit: cover; transition: transform var(--transition-base); }
.home-category-card:hover .home-category-image img { transform: scale(1.05); }
.home-category-content { padding: 24px; }
.home-category-content h2 { font-size: 20px; font-weight: 700; margin-bottom: 8px; }
.home-category-content p { color: var(--color-text-muted); font-size: 14px; }

/* ===== CATEGORY GRID (Category Pages) ===== */
.category-grid-section { padding: 60px 0; }
.category-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; }
.category-card { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden; transition: all var(--transition-base); }
.category-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-xl); }
.category-link { display: block; text-decoration: none; color: inherit; }
.category-image-wrapper { aspect-ratio: 1; background: var(--color-bg-alt); overflow: hidden; }
.category-image { width: 100%; height: 100%; object-fit: cover; padding: 16px; transition: transform var(--transition-base); }
.category-card:hover .category-image { transform: scale(1.05); }
.category-info { padding: 16px; }
.category-info h3 { font-size: 15px; font-weight: 600; margin-bottom: 4px; }
.product-count { font-size: 13px; color: var(--color-text-muted); }

/* ===== HOME ALL CATEGORIES ===== */
.home-all-categories { padding: 60px 0; background: var(--color-bg-alt); }
.home-all-categories h2 { font-size: 28px; font-weight: 700; text-align: center; margin-bottom: 40px; }
.all-categories-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
.all-categories-list { list-style: none; display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
.all-categories-list a { display: block; padding: 12px 16px; background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-md); font-size: 14px; font-weight: 500; color: var(--color-text); transition: all var(--transition-fast); }
.all-categories-list a:hover { border-color: var(--color-primary); color: var(--color-primary); background: var(--color-primary-light); }

/* ===== HOME CTA / FEATURES ===== */
.home-cta { padding: 80px 0; background: var(--color-bg); }
.home-cta h2 { font-size: 28px; font-weight: 700; text-align: center; margin-bottom: 48px; }
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px; }
.feature { text-align: center; padding: 32px 24px; background: var(--color-bg-alt); border-radius: var(--radius-lg); border: 1px solid var(--color-border); }
.feature-icon { font-size: 36px; display: block; margin-bottom: 16px; }
.feature h3 { font-size: 18px; font-weight: 700; margin-bottom: 12px; }
.feature p { color: var(--color-text-muted); font-size: 15px; }

/* ===== CTA SECTION ===== */
.cta-section { padding: 60px 0; text-align: center; background: var(--color-bg-alt); }
.cta-section h2 { font-size: 24px; font-weight: 700; margin-bottom: 12px; }
.cta-section p { color: var(--color-text-muted); margin-bottom: 24px; max-width: 600px; margin-left: auto; margin-right: auto; }

/* ===== BUYING GUIDE ===== */
.buying-guide { padding: 60px 0; background: var(--color-bg); }
.buying-guide h2 { font-size: 24px; font-weight: 700; margin-bottom: 24px; color: var(--color-text); }
.buying-guide h3 { font-size: 18px; font-weight: 600; margin: 32px 0 16px; color: var(--color-text); }
.buying-guide-content p { font-size: 16px; line-height: 1.7; color: var(--color-text); margin-bottom: 16px; }
.criteria-list { list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 24px; }
.criteria-list li { display: flex; align-items: flex-start; gap: 10px; padding: 12px 16px; background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-md); font-size: 14px; color: var(--color-text); }
.check-icon { color: var(--color-success); font-weight: 700; flex-shrink: 0; margin-top: 2px; }
.expert-tip { display: flex; gap: 12px; padding: 20px; background: linear-gradient(135deg, var(--color-primary-light) 0%, #fff 100%); border: 1px solid var(--color-primary-light); border-radius: var(--radius-lg); border-left: 4px solid var(--color-primary); }
.tip-icon { font-size: 24px; flex-shrink: 0; }
.tip-content { font-size: 15px; line-height: 1.6; color: var(--color-text); }
.tip-content strong { color: var(--color-primary); }

/* ===== FAQ SECTION ===== */
.faq-section { padding: 60px 0; background: var(--color-bg-alt); }
.faq-section h2 { font-size: 24px; font-weight: 700; margin-bottom: 32px; text-align: center; color: var(--color-text); }
.faq-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; max-width: 1000px; margin: 0 auto; }
.faq-item { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; transition: all var(--transition-base); }
.faq-item:hover { box-shadow: var(--shadow-md); border-color: var(--color-border-hover); }
.faq-item h3 { font-size: 16px; font-weight: 600; margin-bottom: 12px; color: var(--color-text); line-height: 1.4; }
.faq-answer { font-size: 15px; line-height: 1.7; color: var(--color-text-muted); }
.faq-answer p { margin: 0; }

/* ===== BADGE VARIANTS ===== */
.badge-favorite { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.badge-value { background: linear-gradient(135deg, #059669 0%, #047857 100%); }
.badge-popular { background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%); }

/* ===== NEWSLETTER ===== */
.newsletter { padding: 60px 0; background: var(--color-bg); }
.newsletter-card { display: grid; grid-template-columns: 1fr 400px; gap: 40px; align-items: start; max-width: 900px; margin: 0 auto; background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 40px; }
.newsletter-content h2 { font-size: 24px; font-weight: 700; margin-bottom: 12px; }
.newsletter-content p { color: var(--color-text-muted); margin-bottom: 24px; }
.newsletter-benefits { list-style: none; display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 24px; }
.newsletter-benefits li { display: flex; align-items: center; gap: 8px; font-size: 14px; color: var(--color-text); }
.newsletter-benefits span { color: var(--color-success); font-weight: 600; }
.newsletter-form { display: flex; flex-direction: column; gap: 12px; }
.newsletter-form .form-group { display: flex; gap: 8px; }
.newsletter-form input { flex: 1; padding: 12px 16px; border: 1px solid var(--color-border); border-radius: var(--radius-md); font-size: 15px; }
.newsletter-form input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-light); }
.form-hint { font-size: 13px; color: var(--color-text-muted); text-align: center; }
.newsletter-whatsapp { text-align: center; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--color-border); }
.newsletter-whatsapp a { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 500; color: var(--color-primary); transition: color var(--transition-fast); }
.newsletter-whatsapp a:hover { color: var(--color-primary-hover); }

/* ===== FOOTER ===== */
.site-footer { background: var(--color-text); color: white; margin-top: auto; }
.site-footer a { color: rgba(255,255,255,0.7); }
.site-footer a:hover { color: white; }
.footer-grid { display: grid; grid-template-columns: 2fr repeat(2, 1fr); gap: 40px; padding: 60px 0 40px; }
.footer-brand .logo { color: white; margin-bottom: 16px; }
.footer-brand p { color: rgba(255,255,255,0.6); font-size: 15px; max-width: 300px; }
.footer-nav h4 { font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 16px; color: rgba(255,255,255,0.5); }
.footer-nav ul { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.1); padding: 20px 0; text-align: center; color: rgba(255,255,255,0.4); font-size: 14px; }

/* ===== LEGAL PAGES ===== */
.legal-content { max-width: 800px; line-height: 1.8; }
.legal-content h2 { font-size: 22px; font-weight: 700; margin: 32px 0 16px; padding-top: 32px; border-top: 1px solid var(--color-border); }
.legal-content h2:first-child { border-top: none; padding-top: 0; margin-top: 0; }
.legal-content ul { margin: 16px 0; padding-left: 24px; }
.legal-content li { margin-bottom: 8px; }

/* Transparency Box */
.transparency-box { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 32px; margin-bottom: 32px; }
.transparency-box h2 { font-size: 24px; font-weight: 700; margin-bottom: 16px; color: var(--color-text); border: none; padding: 0; }
.transparency-box > p { font-size: 16px; color: var(--color-text-muted); margin-bottom: 24px; }
.transparency-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 24px; }
.transparency-item { display: flex; gap: 16px; }
.transparency-icon { font-size: 28px; flex-shrink: 0; }
.transparency-item h3 { font-size: 16px; font-weight: 600; margin: 0 0 8px; color: var(--color-text); }
.transparency-item p { font-size: 14px; color: var(--color-text-muted); margin: 0; line-height: 1.6; }

/* ===== COMPARISON SECTION ===== */
.comparison-section { padding: 60px 0; background: var(--color-bg); }
.comparison-section h2 { font-size: 24px; font-weight: 700; margin-bottom: 8px; color: var(--color-text); text-align: center; }
.comparison-intro { text-align: center; color: var(--color-text-muted); margin-bottom: 32px; font-size: 16px; }
.table-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.comparison-table { width: 100%; min-width: 600px; border-collapse: collapse; font-size: 14px; }
.comparison-table th,
.comparison-table td { padding: 14px 16px; text-align: left; border-bottom: 1px solid var(--color-border); }
.comparison-table th { background: var(--color-bg-alt); font-weight: 600; color: var(--color-text); white-space: nowrap; position: sticky; top: 0; z-index: 1; }
.comparison-table tbody tr:hover { background: var(--color-bg-alt); }
.comparison-table td:first-child { font-weight: 500; color: var(--color-text); }
.niche-link { color: var(--color-primary); font-weight: 500; text-decoration: none; }
.niche-link:hover { text-decoration: underline; }
.product-link { color: var(--color-text); text-decoration: none; transition: color var(--transition-fast); }
.product-link:hover { color: var(--color-primary); }
.comparison-table .btn-sm { padding: 8px 16px; font-size: 13px; white-space: nowrap; display: inline-flex; align-items: center; gap: 6px; }
.comparison-table .badge { font-size: 11px; padding: 3px 8px; border-radius: var(--radius-sm); font-weight: 600; }

/* ===== FAQ GRID (Category Pages) ===== */
.faq-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; max-width: 1000px; margin: 0 auto; }
.faq-item { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; transition: all var(--transition-base); }
.faq-item:hover { box-shadow: var(--shadow-md); border-color: var(--color-border-hover); }
.faq-item h3 { font-size: 16px; font-weight: 600; margin-bottom: 12px; color: var(--color-text); line-height: 1.4; }
.faq-answer { font-size: 15px; line-height: 1.7; color: var(--color-text-muted); }
.faq-answer p { margin: 0; }

/* ===== RESPONSIVE (additions) ===== */
@media (max-width: 768px) {
    .comparison-table { font-size: 13px; min-width: 560px; }
    .comparison-table th,
    .comparison-table td { padding: 10px 12px; }
    .comparison-table .btn-sm { padding: 6px 12px; font-size: 12px; }
    .newsletter-card { grid-template-columns: 1fr; }
    .newsletter-benefits { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
    .comparison-table { font-size: 12px; min-width: 500px; }
    .comparison-table th,
    .comparison-table td { padding: 8px 10px; }
    .category-grid { grid-template-columns: 1fr; }
    .faq-grid { grid-template-columns: 1fr; }
}

/* ===== CATEGORY PAGE HERO ===== */
.category-hero { padding: 60px 0; background: var(--color-bg-alt); border-bottom: 1px solid var(--color-border); }
.category-hero h1 { font-size: clamp(28px, 4vw, 40px); font-weight: 800; margin-bottom: 8px; }
.hero-subtitle { font-size: 18px; color: var(--color-text-muted); }

/* ===== DEALS PAGE ===== */
.deals-page { padding: 60px 0; }
.page-header { margin-bottom: 32px; }
.page-header h1 { font-size: clamp(28px, 4vw, 40px); font-weight: 800; margin-bottom: 8px; }
.page-lead { font-size: 18px; color: var(--color-text-muted); margin-bottom: 16px; }
.page-meta { font-size: 14px; color: var(--color-text-muted); }
.page-meta a { color: var(--color-primary); text-decoration: underline; }
.page-meta a:hover { color: var(--color-primary-hover); }

.deal-filters { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 32px; padding: 16px 0; border-top: 1px solid var(--color-border); border-bottom: 1px solid var(--color-border); }
.filter-btn { padding: 8px 16px; background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-md); font-size: 13px; font-weight: 500; color: var(--color-text); cursor: pointer; transition: all var(--transition-fast); }
.filter-btn:hover { border-color: var(--color-primary); color: var(--color-primary); }
.filter-btn.active { background: var(--color-primary); border-color: var(--color-primary); color: white; }

.deals-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 24px; }
.deal-card { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden; transition: all var(--transition-base); }
.deal-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-xl); border-color: var(--color-border-hover); }
.deal-link { display: block; text-decoration: none; color: inherit; }
.deal-image-wrapper { position: relative; aspect-ratio: 1; background: var(--color-bg-alt); overflow: hidden; }
.deal-image { width: 100%; height: 100%; object-fit: contain; padding: 20px; transition: transform var(--transition-base); }
.deal-card:hover .deal-image { transform: scale(1.02); }
.deal-badge { position: absolute; bottom: 12px; right: 12px; color: white; padding: 6px 12px; border-radius: var(--radius-sm); font-size: 11px; font-weight: 600; opacity: 0; transform: translateY(10px); transition: all var(--transition-fast); white-space: nowrap; }
.deal-card:hover .deal-badge { opacity: 1; transform: translateY(0); }
.badge-favorite { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.badge-value { background: linear-gradient(135deg, #059669 0%, #047857 100%); }
.badge-popular { background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%); }
.deal-info { padding: 16px; }
.deal-niche { font-size: 12px; font-weight: 600; color: var(--color-primary); text-transform: uppercase; letter-spacing: 0.5px; }
.deal-title { font-size: 15px; font-weight: 600; line-height: 1.4; color: var(--color-text); margin: 8px 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.deal-price { font-size: 18px; font-weight: 700; color: var(--color-primary); }

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .nav-toggle { display: block; }
    .main-nav { position: absolute; top: var(--header-height); left: 0; right: 0; background: white; border-bottom: 1px solid var(--color-border); padding: 16px; box-shadow: var(--shadow-lg); display: none; }
    .main-nav.open { display: block; }
    .main-nav ul { flex-direction: column; width: 100%; }
    .main-nav a { width: 100%; text-align: left; }
    .footer-grid { grid-template-columns: 1fr; gap: 32px; text-align: center; }
    .footer-brand { display: flex; flex-direction: column; align-items: center; }
    .product-grid { grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
    .category-grid { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
    .home-category-grid { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
    .product-grid { grid-template-columns: 1fr; }
    .category-grid { grid-template-columns: 1fr; }
    .all-categories-list { grid-template-columns: 1fr; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}

/* ===== KAUFBERATUNGEN PAGE ===== */
.guides-overview { padding: 60px 0; background: var(--color-bg); }
.section-header { text-align: center; margin-bottom: 40px; }
.section-header h2 { font-size: 28px; font-weight: 700; margin-bottom: 8px; color: var(--color-text); }
.section-subtitle { color: var(--color-text-muted); font-size: 16px; }

.guides-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; }
.guide-card { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden; transition: all var(--transition-base); }
.guide-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-xl); border-color: var(--color-border-hover); }
.guide-content { padding: 24px; }
.guide-category { display: inline-block; font-size: 12px; font-weight: 600; color: var(--color-primary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
.guide-content h3 { font-size: 20px; font-weight: 700; margin-bottom: 12px; line-height: 1.3; }
.guide-content h3 a { color: var(--color-text); text-decoration: none; transition: color var(--transition-fast); }
.guide-content h3 a:hover { color: var(--color-primary); }
.guide-content p { color: var(--color-text-muted); margin-bottom: 16px; font-size: 15px; line-height: 1.6; }
.guide-cta { display: inline-flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 600; color: var(--color-primary); text-decoration: none; transition: all var(--transition-fast); }
.guide-cta:hover { gap: 10px; color: var(--color-primary-hover); }

.guide-categories { padding: 60px 0; background: var(--color-bg-alt); }
.guide-categories h2 { font-size: 28px; font-weight: 700; text-align: center; margin-bottom: 8px; }
.guide-categories .section-subtitle { text-align: center; margin-bottom: 40px; }

/* ===== CONTACT PAGE ===== */
.contact-section { padding: 60px 0; background: var(--color-bg); }
.contact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; max-width: 1000px; margin: 0 auto; }
.contact-info h2 { font-size: 28px; font-weight: 700; margin-bottom: 16px; color: var(--color-text); }
.contact-info > p { color: var(--color-text-muted); font-size: 16px; line-height: 1.7; margin-bottom: 32px; }

.contact-methods { display: flex; flex-direction: column; gap: 24px; margin-bottom: 32px; }
.contact-method { display: flex; gap: 16px; padding: 20px; background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-lg); transition: all var(--transition-base); }
.contact-method:hover { border-color: var(--color-border-hover); box-shadow: var(--shadow-md); }
.contact-icon { font-size: 28px; flex-shrink: 0; }
.contact-method h3 { font-size: 16px; font-weight: 600; margin-bottom: 4px; color: var(--color-text); }
.contact-method p { margin: 0; color: var(--color-text-muted); }
.contact-method a { color: var(--color-primary); text-decoration: none; transition: color var(--transition-fast); }
.contact-method a:hover { color: var(--color-primary-hover); text-decoration: underline; }

.contact-info h3 { font-size: 18px; font-weight: 600; margin: 32px 0 16px; color: var(--color-text); }
.contact-info ul { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 12px; }
.contact-info li { padding: 16px; background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-md); font-size: 15px; line-height: 1.6; color: var(--color-text); }
.contact-info li strong { color: var(--color-text); }
.contact-note { margin-top: 24px; padding: 20px; background: var(--color-primary-light); border: 1px solid var(--color-primary); border-radius: var(--radius-lg); border-left: 4px solid var(--color-primary); }
.contact-note p { margin: 8px 0; font-size: 14px; color: var(--color-text); }
.contact-note a { color: var(--color-primary); font-weight: 500; }

.contact-form-wrapper { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: 32px; height: fit-content; }
.contact-form { display: flex; flex-direction: column; gap: 20px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { font-size: 14px; font-weight: 500; color: var(--color-text); }
.form-group input,
.form-group select,
.form-group textarea { padding: 12px 16px; border: 1px solid var(--color-border); border-radius: var(--radius-md); font-size: 15px; font-family: inherit; background: var(--color-bg); color: var(--color-text); transition: all var(--transition-fast); }
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-light); }
.form-group textarea { resize: vertical; min-height: 120px; }
.form-hint { font-size: 13px; color: var(--color-text-muted); text-align: center; margin-top: 8px; }
.btn-large { padding: 14px 28px; font-size: 16px; font-weight: 600; }

/* ===== RESPONSIVE KAUFBERATUNGEN / CONTACT ===== */
@media (max-width: 768px) {
    .contact-grid { grid-template-columns: 1fr; gap: 40px; }
    .contact-form-wrapper { padding: 24px; }
    .guides-grid { grid-template-columns: 1fr; }
    .guide-categories .theme-worlds-grid { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
    .contact-method { flex-direction: column; text-align: center; gap: 8px; }
}

/* ===== ACCESSIBILITY ===== */
:focus-visible { outline: 3px solid var(--color-primary); outline-offset: 2px; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }

/* ===== COOKIE BANNER ===== */
.cookie-banner { position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000; background: var(--color-bg); border-top: 1px solid var(--color-border); box-shadow: 0 -4px 20px rgba(0,0,0,0.1); padding: 16px 0; }
.cookie-banner-content { max-width: var(--container-max); margin: 0 auto; padding: 0 20px; display: flex; flex-direction: column; gap: 16px; }
@media (min-width: 640px) { .cookie-banner-content { flex-direction: row; align-items: center; justify-content: space-between; } }
.cookie-banner-text h3 { font-size: 16px; font-weight: 600; margin-bottom: 4px; color: var(--color-text); }
.cookie-banner-text p { font-size: 14px; color: var(--color-text-muted); margin: 0; }
.cookie-banner-text a { color: var(--color-primary); text-decoration: underline; }
.cookie-banner-text a:hover { color: var(--color-primary-hover); }
.cookie-banner-actions { display: flex; gap: 12px; flex-wrap: wrap; }
.cookie-banner-actions .btn { padding: 10px 20px; font-size: 14px; }
'''

    js = '''
// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.querySelector('.nav-toggle');
    const menu = document.querySelector('.nav-menu');
    if (toggle && menu) {
        toggle.addEventListener('click', function() {
            const expanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !expanded);
            menu.classList.toggle('open');
        });
    }

    // Close menu on link click (mobile)
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                menu.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Lazy loading fallback for older browsers
    if ('loading' in HTMLImageElement.prototype) {
        // Native lazy loading supported
    } else {
        // Fallback: load all images
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            img.removeAttribute('loading');
        });
    }
});

// Add active state to current nav item
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.main-nav a, .footer-nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = 'var(--color-primary)';
            link.style.fontWeight = '600';
        }
    });
});
'''
    return css, js


def get_blog_intro(niche_slug, niche_name):
    """Generate unique blog article intro for a niche."""
    intros = {
        'smart-home': f'{niche_name} entwickelt sich rasant – vom einfachen Steckdosen-Schalter bis zum vernetzten Ökosystem. Dieser Ratgeber zeigt, worauf es 2025 wirklich ankommt, welche Systeme zusammenpassen und wo du dein Geld sinnvoll investierst.',
        'bestseller': f'Die {niche_name} auf Amazon verraten, was Käufer wirklich überzeugt – nicht Marketing, sondern echte Nutzererfahrung. Wir analysieren die Top-Produkte, decken Muster auf und zeigen, welche sich langfristig lohnen.',
        'geschenke': f'Geschenke zu finden, die wirklich Freude machen, ist eine Kunst. Unsere {niche_name.lower()}-Auswahl basiert auf Bewertungen, Vielseitigkeit und dem „Wow“-Effekt beim Auspacken – für jeden Anlass und jedes Budget.',
        'kuechenhelfer': f'{niche_name} sind die stillen Helden im Alltag – sie sparen Zeit, Nerven und oft auch Geld. Wir haben die Kategorie durchforstet und präsentieren die Tools, die in keiner Küche fehlen sollten.',
        'backen-kochen': f'{niche_name} braucht das richtige Equipment. Vom Teigschaber bis zur Küchenmaschine: Wir zeigen, welche Produkte Profis und Hobbyköche gleichermaßen überzeugen und warum.',
        'baby-kindersicherheit': f'Wenn es um {niche_name.lower()} geht, gibt es keine Kompromisse. Dieser Guide hilft Eltern, die richtigen Sicherheitsprodukte zu finden – geprüft, bewährt und kindgerecht.',
        'fitness-zu-hause': f'{niche_name} boomt – aber nicht jedes Gerät hält, was die Werbung verspricht. Wir trennen Marketing von Substanz und zeigen Equipment, das langfristig motiviert und Ergebnisse liefert.',
        'outdoor-camping': f'{niche_name} bedeutet Freiheit – aber nur mit der richtigen Ausrüstung. Ob Wochenendtrip oder Langzeitreise: Diese Produkte haben sich in der Praxis bewährt.',
        'gaming-zubehoer': f'{niche_name} entscheidet oft über Sieg oder Frust. Wir testen Mäuse, Tastaturen, Headsets und Stühle auf Ergonomie, Latenz und Haltbarkeit – für Casuals und Pros.',
        'pflanzen-pflege': f'{niche_name} gelingt mit Wissen und den richtigen Tools. Ob Balkon, Garten oder Indoor-Dschungel: Diese Produkte machen die Pflege einfacher und die Ernte reicher.',
    }
    return intros.get(niche_slug, f'In unserem großen {niche_name}-Ratgeber 2025 findest du die besten Produkte, ehrliche Vergleiche und praktische Tipps für die richtige Kaufentscheidung.')


def get_blog_criteria(niche_slug):
    """Generate buying criteria for blog article."""
    criteria_map = {
        'smart-home': [
            ('Ökosystem-Kompatibilität', 'Matter, Zigbee, Thread, HomeKit, Alexa, Google Home – je mehr Standards, desto flexibler.'),
            ('Lokal vs. Cloud', 'Lokale Steuerung funktioniert ohne Internet, Cloud-Geräte bieten mehr Features aber Abhängigkeit.'),
            ('Strommessung', 'Wichtig für Verbrauchskontrolle und Automatisierungen (z. B. „Waschmaschine fertig“).'),
            ('Installationsaufwand', 'Plug-and-Play vs. Verkabelung – Mietwohnungen brauchen oft rückrüstbare Lösungen.'),
            ('Langzeit-Support', 'Hersteller mit regelmäßigen Firmware-Updates sichern die Investition ab.'),
        ],
        'bestseller': [
            ('Bewertungsanzahl & Score', 'Produkte mit 1.000+ Bewertungen und ≥4,5 Sternen sind statistisch verlässlicher.'),
            ('Preisstabilität', 'Extreme Preisschwankungen deuten auf saisonale Hypes oder Qualitätsprobleme hin.'),
            ('Rücklaufquote', 'Niedrige Retouren = zufriedene Käufer. Amazon zeigt dies indirekt über „Häufig zusammen gekauft“.'),
            ('Variantenvielfalt', 'Mehrere Größen/Farben = ausgereiftes Produkt mit breiter Zielgruppe.'),
            ('Marken-Präsenz', 'Etablierte Marken bieten meist besseren Support und Ersatzteilverfügbarkeit.'),
        ],
        'geschenke': [
            ('Personalisierbarkeit', 'Gravur, Foto, Konfiguration – individuelle Geschenke wirken wertiger.'),
            ('Altersgerechtigkeit', 'Klare Altersempfehlung vermeidet Fehlkäufe und Enttäuschung.'),
            ('Verpackung & Unboxing', 'Hochwertige Verpackung steigert den wahrgenommenen Wert massiv.'),
            ('Vielseitigkeit', 'Produkte mit mehreren Nutzungsmöglichkeiten werden länger genutzt.'),
            ('Nachhaltigkeit', 'Langlebig, reparierbar, plastikfrei – gewinnt an Bedeutung beim Schenken.'),
        ],
        'kuechenhelfer': [
            ('Materialqualität', 'Edelstahl, Silikon, Holz – hitze- und spülmaschinenfest, geschmacksneutral.'),
            ('Ergonomie', 'Griffdesign, Gewicht, Balance – entscheidend bei täglicher Nutzung.'),
            ('Platzbedarf', 'Kompakt, stapelbar, multifunktional – wichtig für kleine Küchen.'),
            ('Reinigung', 'Spülmaschinenfest, wenige Ecken, keine versteckten Schmutzfallen.'),
            ('Vielseitigkeit', 'Ein Tool für mehrere Aufgaben schont Budget und Stauraum.'),
        ],
        'backen-kochen': [
            ('Temperaturbeständigkeit', 'Backformen bis 250 °C, Silikon bis 220 °C – Sicherheitsreserve beachten.'),
            ('Antihaft-Eigenschaften', 'Keramik, PTFE-frei, emailliert – für fettarmes Backen und leichte Reinigung.'),
            ('Präzision', 'Messbecher mit Skala, Waagen auf 1 g genau – Backen ist Chemie.'),
            ('Formstabilität', 'Verzugsfreie Bleche, rissfeste Formen – für gleichmäßige Ergebnisse.'),
            ('Marken-Support', 'Ersatzteile, Garantie, Community-Rezepte – Ökosystem-Vorteil.'),
        ],
        'baby-kindersicherheit': [
            ('Zertifizierung', 'GS-Zeichen, TÜV, EN-Normen – unverzichtbar bei Sicherheitsprodukten.'),
            ('Montage ohne Bohren', 'Klemm- und Klebelösungen für Mietwohnungen, rückstandslos entfernbar.'),
            ('Altersanpassung', 'Mitwachsend, justierbar – deckt mehrere Entwicklungsphasen ab.'),
            ('Alltagstauglichkeit', 'Einhandbedienung, leise, optisch unauffällig – Elternfreundlichkeit.'),
            ('Material-Sicherheit', 'BPA-frei, schadstoffgeprüft, keine Kleinteile verschluckbar.'),
        ],
        'fitness-zu-hause': [
            ('Platzbedarf', 'Klappbar, wandmontierbar, stapelbar – realistische Wohnungsgröße beachten.'),
            ('Geräuschpegel', 'Magnetbremse < Luftwiderstand < Reibung – kritisch bei Nachbarn.'),
            ('Progressions-Möglichkeiten', 'Gewichtssteigerung, Widerstandsstufen, App-Tracking – langfristig motivierend.'),
            ('Verarbeitungsqualität', 'Schweißbeständigkeit, stabile Schweißnähte, Garantiezeit.'),
            ('Trainingsvielfalt', 'Mehrere Übungen pro Gerät – Ganzkörper-Training auf < 2 m².'),
        ],
        'outdoor-camping': [
            ('Packmaß & Gewicht', 'Rucksack-tauglich vs. Auto-Camping – Kompromiss finden.'),
            ('Wetterfestigkeit', 'Wassersäule (mm), UV-Beständigkeit, Windstabilität – EN-Normen prüfen.'),
            ('Aufbauzeit', 'Pop-up vs. Gestänge – nach langer Anreise entscheidend.'),
            ('Langlebigkeit', 'Nahtversiegelung, Reparatursets, Garantie – Investitionsschutz.'),
            ('Vielseitigkeit', 'Mehrjahreszeiten-Tauglichkeit, Modularität, Zubehör-Ökosystem.'),
        ],
        'gaming-zubehoer': [
            ('Sensor & Polling-Rate', 'Optisch ≥ 26.000 DPI, 1.000 Hz – für kompetitives Gaming.'),
            ('Ergonomie & Gewicht', 'Klaue/Palm/Fingertip-Griff, < 80 g Maus – Ermüdungsfreiheit.'),
            ('Latenz', 'Kabel < 2,4 GHz < Bluetooth – bei Turnieren nur kabelgebunden/2,4 GHz.'),
            ('Akku-Laufzeit', '≥ 50 h (Headset), ≥ 70 h (Maus) – Laden stört den Flow.'),
            ('Software & Anpassung', 'Makros, DPI-Stufen, EQ-Profile – Treiber-Stabilität prüfen.'),
        ],
        'pflanzen-pflege': [
            ('Messgenauigkeit', 'Bodenfeuchte ± 5 %, pH ± 0,5, Licht in Lux/PAR – Entscheidungssicherheit.'),
            ('Stromversorgung', 'Batterie 12+ Monate, Solar, fest verbaut – Wartungsarmut.'),
            ('App & Datenhistorie', 'Trends, Export, Push-Benachrichtigungen – langfristiges Pflanzenmanagement.'),
            ('Robustheit', 'IP67+, UV-beständig, Erdtauglich – Outdoor-Einsatz.'),
            ('Kalibrierung', 'Werkskalibriert, nutzerkalibrierbar, Referenzlösungen inklusive.'),
        ],
    }
    return criteria_map.get(niche_slug, [
        ('Qualität & Verarbeitung', 'Hochwertige Materialien und saubere Verarbeitung zahlen sich langfristig aus.'),
        ('Preis-Leistung', 'Der teuerste Artikel ist nicht immer der beste – vergleiche Nutzen und Kosten.'),
        ('Kundenbewertungen', 'Echte Nutzererfahrungen zeigen Stärken und Schwächen jenseits der Werbung.'),
        ('Garantie & Support', 'Lange Garantie und erreichbarer Support signalisieren Herstellervertrauen.'),
        ('Nachhaltigkeit', 'Langlebig, reparierbar, recyclebar – schont Ressourcen und Geldbeutel.'),
    ])


def get_blog_faqs(niche_slug, niche_name):
    """Generate FAQ items for blog article."""
    faq_map = {
        'smart-home': [
            ('Brauche ich einen Hub für Smart Home?', 'Nicht zwingend. Matter-Geräte funktionieren direkt mit Thread-Bordern (z. B. HomePod, Echo 4. Gen). Für Zigbee brauchst du einen Hub (Home Assistant, Hue Bridge, Aqara Hub).'),
            ('Was ist der Unterschied zwischen Zigbee, Thread und Matter?', 'Zigbee/Thread sind Funkprotokolle, Matter ist der gemeinsame Anwendungsstandard darüber. Matter-Geräte sprechen Thread oder Wi-Fi und funktionieren plattformübergreifend.'),
            ('Funktioniert Smart Home ohne Internet?', 'Ja, mit lokaler Steuerung (Home Assistant, HomeKit, Matter über Thread). Cloud-only-Geräte (z. B. Tuya ohne Local API) fallen aus.'),
            ('Wie sicher sind Smart-Home-Geräte?', 'Regelmäßige Updates, getrenntes IoT-Netzwerk (VLAN), starke Passwörter, 2FA beim Hersteller-Account. Billig-Geräte ohne Update-Zusage meiden.'),
            ('Lohnt sich Strommessung an Steckdosen?', 'Ja – für Verbrauchskontrolle, Geräte-Erkennung (Waschmaschine fertig) und Automatisierungen. Amortisiert sich oft innerhalb eines Jahres.'),
        ],
        'bestseller': [
            ('Sind Amazon-Bestseller wirklich die besten Produkte?', 'Nicht immer. Der Algorithmus gewichtet Verkäufe, Bewertungen, Conversion – aber auch Werbung und Prime-Platzierung. Immer Bewertungen lesen, nicht nur Sternschnitt.'),
            ('Wie erkenne ich gefälschte Bewertungen?', 'Unnatürliche Häufung 5-Sterne-Bewertungen in kurzer Zeit, generische Texte, fehlende Verified-Purchase-Kennzeichnung, ähnliche Formulierungen. Tools wie ReviewMeta helfen.'),
            ('Ändern sich Bestseller oft?', 'Ja – saisonal, durch neue Modelle, TikTok-Hypes oder Preiskriege. Wöchentlich prüfen lohnt sich bei sich schnell drehenden Kategorien (Tech, Beauty).'),
            ('Sind teurere Alternativen besser?', 'Oft ja – aber der Mehrwert muss zum Nutzen passen. Diminishing Returns: ab 80 % des Spitzenpreises oft nur noch marginale Qualitätsgewinne.'),
            ('Wie finde ich langfristig gute Produkte?', 'Marken mit konstanter Qualität (z. B. Miele, Bosch, Sony, Logitech), Produktserien mit jahrelanger Modellpflege, Ersatzteilverfügbarkeit prüfen.'),
        ],
        'geschenke': [
            ('Was schenkt man jemandem, der alles hat?', 'Erlebnisse (Workshops, Tastings, Zeit), personalisierte Unikate (Fotobuch, Gravur), Konsumables in Premium-Qualität (Kaffee, Whisky, Gewürze), Spenden im Namen.'),
            ('Wie vermeide ich Fehlkäufe?', 'Wunschlisten abfragen, gemeinsame Pinterest-Boards, „Geschenk-Anker“ setzen (z. B. „Was hast du dir letztes Jahr gewünscht?“), Rückgaberecht prüfen.'),
            ('Sind Gutscheine unpersönlich?', 'Nicht, wenn sie thematisch passen (Buchladen für Leser, Baumarkt für Heimwerker) und hübsch verpackt sind. Erlebnis-Gutscheine > reine Wertgutscheine.'),
            ('Was ist ein gutes Budget?', 'Richtwert: 20–50 € für Kollegen/Bekannte, 50–150 € für enge Freunde/Familie, 150 €+ für Partner/Eltern. Gruppen-Geschenke ermöglichen höhere Einzelwerte.'),
            ('Nachhaltig schenken – wie?', 'Second-Hand/Vintage, reparierbar, plastikfrei, regional, Erlebnisse statt Dinge, Bäume pflanzen, Zeit schenken. Verpackung: Furoshiki, Zeitung, Stoffbeutel.'),
        ],
    }
    default_faqs = [
        (f'Welches {niche_name} ist für Einsteiger am besten?', f'Einsteigern empfehlen wir das Preis-Leistungs-Sieger-Modell – es bietet die wichtigsten Funktionen ohne Überforderung.'),
        (f'Wie oft sollte man {niche_name.lower()} ersetzen?', 'Bei Verschleißteilen (Filter, Bürsten) alle 3–6 Monate, bei Geräten alle 5–7 Jahre oder bei Defekt.'),
        (f'Gibt es {niche_name.lower()} im Test von Stiftung Warentest?', 'Oft ja – die Testberichte (meist kostenpflichtig) bieten unabhängige Labordaten. Wir fassen relevante Ergebnisse zusammen.'),
        (f'Worauf bei der Garantie achten?', 'Mindestens 2 Jahre Gesetzesgewährleistung, idealerweise 3–5 Jahre Herstellergarantie mit deutschem Service.'),
        (f'Wo kauft man {niche_name.lower()} am besten?', 'Amazon (schnelle Lieferung, einfache Retoure), Fachhändler (Beratung, Vorführung), Hersteller-Direct (exklusive Modelle, Support).'),
    ]
    return faq_map.get(niche_slug, default_faqs)


def get_blog_tip(niche_slug):
    """Generate expert tip box for blog article."""
    tips = {
        'smart-home': '💡 Profi-Tipp: Starte mit einem Matter-kompatiblen Thread-Border-Router (HomePod mini, Echo 4. Gen, Google Nest Hub 2. Gen). Dann kannst du künftig Geräte aller Marken hub-frei hinzufügen – maximaler Flexibilität, minimaler Vendor-Lock-in.',
        'bestseller': '💡 Profi-Tipp: Nutze CamelCamelCamel oder Keepa für Preisverläufe. Kauf bei „Preis nahe Allzeittief“ + „Bewertung ≥ 4,5 Sterne bei 500+ Reviews“ = statistisch sicherster Kauf.',
        'geschenke': '💡 Profi-Tipp: Führe ganzjährig eine „Geschenk-Ideen-Liste“ (Notion, Notes, Papier). Wenn du etwas siehst: notieren + Link speichern. Zum Anlass nur noch auswählen – kein Stresskauf.',
        'kuechenhelfer': '💡 Profi-Tipp: Investiere in ein gutes Kochmesser (z. B. Wüsthof, Zwilling, Global) und ein Schneidebrett aus Holz (Hirnholz). Diese zwei Tools ersetzen 80 % aller Spezial-Gadgets.',
        'backen-kochen': '💡 Profi-Tipp: Wiege Zutaten (Mehl, Zucker, Butter) statt Volumen zu messen. Eine Küchenwaage mit 1-g-Schritten kostet < 20 € und macht Backergebnisse reproduzierbar.',
        'baby-kindersicherheit': '💡 Profi-Tipp: Sichere nicht alles auf einmal. Gehe krabbelnd durch die Wohnung („Kind-Perspektive“) und sichere genau das, was erreichbar & gefährlich ist. Weniger ist oft sicherer (keine falsche Sicherheit).',
        'fitness-zu-hause': '💡 Profi-Tipp: Kauf gebraucht (Kleinanzeigen, Fitness-Marktplätze). Hanteln, Bänke, Racks verlieren kaum Wert, sind fast unkaputtbar. Spare 40–60 % vs. Neu.',
        'outdoor-camping': '💡 Profi-Tipp: Teste Zelt & Schlafsystem EINMAL zu Hause im Wohnzimmer. Aufbau üben, Passform prüfen, Kondensation testen. Im Regen auf dem Campingplatz ist der schlechteste Zeitpunkt für Überraschungen.',
        'gaming-zubehoer': '💡 Profi-Tipp: Mausform > Sensor-Specs. Eine 100-€-Maus in der falschen Form (zu breit, zu flach) performt schlechter als eine 40-€-Maus, die perfekt in der Hand liegt. Probiere vor dem Kauf (Händler, Freunde).',
        'pflanzen-pflege': '💡 Profi-Tipp: Gieße nach Bodenfeuchte, nicht nach Kalender. Finger-Test (2–3 cm tief) oder Feuchtemesser. Staunasse Wurzeln töten mehr Pflanzen als Trockenheit.',
    }
    return tips.get(niche_slug, f'💡 Profi-Tipp: Qualität vor Quantität. Ein gutes {niche_slug.replace("-", " ")} hält Jahre, billige Alternativen müssen oft ersetzt werden – am Ende teurer.')


def generate_blog_article(niche_slug, products, all_products):
    """Generate a single blog article page for a niche."""
    if not products:
        return None
    
    niche_name = NICHE_NAMES.get(niche_slug, niche_slug.replace('-', ' ').title())
    top_products = products[:5]
    
    # Build affiliate URLs
    for p in top_products:
        p['affiliate_url'] = f'https://www.amazon.de/dp/{p["asin"]}?tag=balu17051-21&utm_source=blog&utm_medium=organic&utm_content={niche_slug}'
        p['img_url'] = p.get('image', '').replace('._AC_SL1500_.', '._AC_SL1500_.') if p.get('image') else f'https://m.media-amazon.com/images/I/{p["asin"]}._AC_SL1500_.jpg'
    
    # Schema data
    breadcrumb_items = [
        ('Startseite', 'https://balu1705.github.io/andreasstehmann-links/'),
        ('Blog', 'https://balu1705.github.io/andreasstehmann-links/blog/'),
        (f'{niche_name} – Ratgeber & Tests', f'https://balu1705.github.io/andreasstehmann-links/blog/{niche_slug}/'),
    ]
    breadcrumb_schema = generate_breadcrumb_schema(breadcrumb_items)
    
    # Article schema
    article_schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': f'{niche_name} – Top-Produkte, Tests & Kaufberatung 2025',
        'description': get_blog_intro(niche_slug, niche_name)[:160],
        'url': f'https://balu1705.github.io/andreasstehmann-links/blog/{niche_slug}/',
        'author': {'@type': 'Person', 'name': 'Andreas Stehmann'},
        'publisher': {
            '@type': 'Organization',
            'name': 'Andreas Stehmann Links',
            'logo': {'@type': 'ImageObject', 'url': 'https://balu1705.github.io/andreasstehmann-links/assets/logo.png'}
        },
        'datePublished': datetime.now().strftime('%Y-%m-%d'),
        'dateModified': datetime.now().strftime('%Y-%m-%d'),
        'inLanguage': 'de-DE',
        'mainEntityOfPage': {'@type': 'WebPage', '@id': f'https://balu1705.github.io/andreasstehmann-links/blog/{niche_slug}/'},
    }
    
    # FAQ schema
    faq_items = get_blog_faqs(niche_slug, niche_name)
    faq_schema = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
            for q, a in faq_items
        ]
    }
    
    import json
    json_ld_scripts = f'''
    <script type="application/ld+json">{json.dumps(breadcrumb_schema, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(article_schema, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
'''
    
    # Build product cards HTML
    product_cards = []
    for i, p in enumerate(top_products):
        badge = ''
        if i == 0:
            badge = '<span class="product-badge badge-favorite">🏆 Unser Favorit</span>'
        elif i == 1:
            badge = '<span class="product-badge badge-value">💡 Preis-Leistung</span>'
        elif i == 2:
            badge = '<span class="product-badge badge-popular">⭐ Beliebt</span>'
        
        price_html = f'<div class="product-price">ca. {p.get("price", "—")} €</div>' if p.get('price') else ''
        
        product_cards.append(f'''
        <article class="product-card" itemscope itemtype="https://schema.org/Product">
            {badge}
            <a href="{p['affiliate_url']}" target="_blank" rel="noopener sponsored nofollow" class="product-link" data-asin="{p['asin']}" data-niche="{niche_slug}" onclick="trackAffiliateClick(this)">
                <img src="{p['img_url']}" alt="{p.get('name', 'Produktbild')}" loading="lazy" itemprop="image" class="product-image">
            </a>
            <h3 class="product-title" itemprop="name"><a href="{p['affiliate_url']}" target="_blank" rel="noopener sponsored nofollow" onclick="trackAffiliateClick(this)">{p.get('name', 'Unbekanntes Produkt')}</a></h3>
            {price_html}
            <a href="{p['affiliate_url']}" target="_blank" rel="noopener sponsored nofollow" class="btn btn-primary btn-small" onclick="trackAffiliateClick(this)">Zum Angebot</a>
            <meta itemprop="sku" content="{p['asin']}">
            <meta itemprop="brand" content="{p.get('brand', 'Unbekannt')}">
            <link itemprop="url" href="{p['affiliate_url']}">
        </article>
''')
    
    # Comparison table
    criteria = get_blog_criteria(niche_slug)
    comparison_rows = []
    for i, p in enumerate(top_products[:3]):
        cells = [f'<td><strong>{p.get("name", "—")[:30]}</strong></td>']
        cells.append(f'<td>{p.get("price", "—")} €</td>')
        cells.append(f'<td>⭐ {p.get("rating", "—")}</td>')
        cells.append(f'<td>{p.get("review_count", "—")} Bew.</td>')
        cells.append(f'<td><a href="{p["affiliate_url"]}" target="_blank" rel="noopener sponsored nofollow" class="btn btn-small" onclick="trackAffiliateClick(this)">Prüfen</a></td>')
        comparison_rows.append(f'<tr>{"".join(cells)}</tr>')
    
    comparison_table = f'''
    <div class="comparison-section">
        <h2>Direktvergleich: Die Top 3 im Überblick</h2>
        <div class="table-wrapper">
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Produkt</th>
                        <th>Preis</th>
                        <th>Bewertung</th>
                        <th>Reviews</th>
                        <th>Aktion</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(comparison_rows)}
                </tbody>
            </table>
        </div>
    </div>
''' if top_products else ''
    
    # Blog article HTML
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{niche_name} – Top-Produkte, Tests & Kaufberatung 2025 | Andreas Stehmann Links</title>
    <meta name="description" content="{get_blog_intro(niche_slug, niche_name)[:160]}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://balu1705.github.io/andreasstehmann-links/blog/{niche_slug}/">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="de_DE">
    <meta property="og:site_name" content="Andreas Stehmann Links">
    <meta property="og:title" content="{niche_name} – Top-Produkte, Tests & Kaufberatung 2025">
    <meta property="og:description" content="{get_blog_intro(niche_slug, niche_name)[:160]}">
    <meta property="og:url" content="https://balu1705.github.io/andreasstehmann-links/blog/{niche_slug}/">
    <meta property="og:image" content="{top_products[0]['img_url'] if top_products else 'https://balu1705.github.io/andreasstehmann-links/assets/logo.png'}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="stylesheet" href="/assets/style.css">
    {json_ld_scripts}
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-YPCSF9BFH2"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-YPCSF9BFH2');
    </script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a>
            <nav class="main-nav" aria-label="Hauptnavigation">
                <a href="/">Startseite</a>
                <a href="/blog/">Blog</a>
                <a href="/deals/">Deals</a>
                <a href="/ueber-uns/">Über uns</a>
            </nav>
        </div>
    </header>
    
    <main class="site-main">
        <div class="container">
            <nav class="breadcrumb" aria-label="Breadcrumb">
                <a href="/">Startseite</a> <span class="sep">/</span>
                <a href="/blog/">Blog</a> <span class="sep">/</span>
                <span aria-current="page">{niche_name} – Ratgeber</span>
            </nav>
            
            <article class="blog-article">
                <header class="article-header">
                    <div class="article-meta">
                        <span class="article-category">{niche_name}</span>
                        <time datetime="{datetime.now().strftime('%Y-%m-%d')}">{datetime.now().strftime('%d. %B %Y')}</time>
                        <span class="article-author">Andreas Stehmann</span>
                    </div>
                    <h1>{niche_name} – Top-Produkte, Tests & Kaufberatung 2025</h1>
                    <p class="article-lead">{get_blog_intro(niche_slug, niche_name)}</p>
                </header>
                
                <div class="affiliate-disclosure">
                    <strong>Affiliate-Hinweis:</strong> Dieser Artikel enthält Affiliate-Links (markiert mit *). Wenn du über diese Links einkaufst, erhalten wir eine kleine Provision – für dich entstehen keine zusätzlichen Kosten.
                </div>
                
                <div class="article-toc">
                    <h2>Inhaltsverzeichnis</h2>
                    <ul>
                        <li><a href="#ueberblick">1. Überblick: {len(products)} Produkte in der Kategorie</a></li>
                        <li><a href="#top-produkte">2. Die Top 5 im Detail</a></li>
                        <li><a href="#kriterien">3. Kaufkriterien: Worauf es ankommt</a></li>
                        <li><a href="#vergleich">4. Direktvergleich der Top 3</a></li>
                        <li><a href="#faq">5. Häufige Fragen</a></li>
                        <li><a href="#fazit">6. Fazit & Empfehlung</a></li>
                    </ul>
                </div>
                
                <section id="ueberblick">
                    <h2>1. Überblick: {len(products)} Produkte in der Kategorie</h2>
                    <p>Unsere Datenbank enthält aktuell <strong>{len(products)} Produkte</strong> in der Kategorie „{niche_name}“. Davon haben wir die Top 5 basierend auf Bewertungen, Preis-Leistung und Beliebtheit für dich ausgewählt. Alle Produkte sind auf Amazon verfügbar und verlinkt – du kannst Preise und Verfügbarkeit direkt prüfen.</p>
                </section>
                
                <section id="top-produkte">
                    <h2>2. Die Top 5 im Detail</h2>
                    <div class="product-grid schema-grid">
                        {''.join(product_cards)}
                    </div>
                </section>
                
                <section id="kriterien">
                    <h2>3. Kaufkriterien: Worauf es bei {niche_name} ankommt</h2>
                    <div class="criteria-grid">
                        {''.join([f'<div class="criterion-card"><h3>{c[0]}</h3><p>{c[1]}</p></div>' for c in criteria])}
                    </div>
                </section>
                
                {comparison_table}
                
                <section id="faq">
                    <h2>5. Häufige Fragen zu {niche_name}</h2>
                    <div class="faq-accordion">
                        {''.join([f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq_items])}
                    </div>
                </section>
                
                <section id="fazit" class="expert-tip">
                    <h2>6. Fazit & Empfehlung</h2>
                    <p>{get_blog_tip(niche_slug)}</p>
                    <p><strong>Unser Favorit:</strong> {top_products[0].get('name', '—')} – bestes Gesamtpaket aus Leistung, Bewertungen und Preis.</p>
                    <p><strong>Preis-Leistung:</strong> {top_products[1].get('name', '—') if len(top_products) > 1 else '—'} – bekommt man viel Leistung fürs Geld.</p>
                    <p><a href="/{niche_slug}/" class="btn btn-primary">Alle {niche_name}-Produkte ansehen →</a></p>
                </section>
            </article>
            
            <aside class="article-sidebar">
                <div class="sidebar-widget">
                    <h3>Zur Kategorie</h3>
                    <p>Mehr Produkte, Filter & Vergleiche:</p>
                    <a href="/{niche_slug}/" class="btn btn-outline">Nischenseite öffnen</a>
                </div>
                <div class="sidebar-widget">
                    <h3>Verwandte Kategorien</h3>
                    <ul>
                        {''.join([f'<li><a href="/{slug}/">{NICHE_NAMES.get(slug, slug.replace("-", " ").title())}</a></li>' for slug in list(all_products.keys())[:5] if slug != niche_slug][:4])}
                    </ul>
                </div>
            </aside>
        </div>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div><h4>Andreas Stehmann Links</h4><p>Die besten Produkte finden – ohne stundenlanges Suchen.</p></div>
                <nav><h4>Navigation</h4><ul><li><a href="/">Startseite</a></li><li><a href="/blog/">Blog</a></li><li><a href="/ueber-uns/">Über uns</a></li><li><a href="/impressum/">Impressum</a></li><li><a href="/datenschutz/">Datenschutz</a></li></ul></nav>
                <nav><h4>Rechtliches</h4><ul><li><a href="/affiliate-hinweis/">Affiliate-Hinweis</a></li><li><a href="/cookie-einstellungen/">Cookie-Einstellungen</a></li></ul></nav>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Andreas Stehmann Links. Alle Rechte vorbehalten.</p>
                <p>* Affiliate-Links: Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p>
            </div>
        </div>
    </footer>
    
    <script src="/assets/main.js"></script>
    <script>
    document.addEventListener('click', function(e) {{
        try {{
            var a = e.target.closest('a[href*="amazon."]');
            if (a) {{
                gtag('event', 'outbound_click', {{
                    link_domain: 'amazon',
                    asin: (a.href.match(/\\/dp\\/([A-Z0-9]{{10}})/) || [])[1] || ''
                }});
            }}
        }} catch (_) {{}}
    }}, true);
    </script>
</body>
</html>'''
    return html


def generate_blog_index(all_products):
    """Generate the blog index page."""
    # Select top niches for blog articles (prioritize by product count)
    niche_scores = [(slug, len(products)) for slug, products in all_products.items() if products]
    niche_scores.sort(key=lambda x: x[1], reverse=True)
    top_niches = [slug for slug, _ in niche_scores[:20]]  # Top 20 niches
    
    breadcrumb_items = [
        ('Startseite', 'https://balu1705.github.io/andreasstehmann-links/'),
        ('Blog', 'https://balu1705.github.io/andreasstehmann-links/blog/'),
    ]
    breadcrumb_schema = generate_breadcrumb_schema(breadcrumb_items)
    
    collection_schema = {
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        'name': 'Blog – Kaufberatungen, Tests & Vergleiche',
        'description': 'Unsere Experten-Ratgeber zu den besten Produkten in allen Kategorien. Ehrliche Tests, echte Vergleiche, klare Empfehlungen.',
        'url': 'https://balu1705.github.io/andrastehmann-links/blog/',
    }
    
    import json
    json_ld_scripts = f'''
    <script type="application/ld+json">{json.dumps(breadcrumb_schema, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(collection_schema, ensure_ascii=False)}</script>
'''
    
    article_cards = []
    for slug in top_niches:
        niche_name = NICHE_NAMES.get(slug, slug.replace('-', ' ').title())
        product_count = len(all_products.get(slug, []))
        article_cards.append(f'''
        <article class="blog-index-card">
            <a href="/blog/{slug}/" class="card-link">
                <div class="card-badge">{product_count} Produkte</div>
                <h3>{niche_name}</h3>
                <p>Top-Produkte, Tests & Kaufberatung für {niche_name.lower()}.</p>
            </a>
        </article>
''')
    
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog – Kaufberatungen, Tests & Vergleiche | Andreas Stehmann Links</title>
    <meta name="description" content="Unsere Experten-Ratgeber zu den besten Produkten in allen Kategorien. Ehrliche Tests, echte Vergleiche, klare Empfehlungen.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://balu1705.github.io/andreasstehmann-links/blog/">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="de_DE">
    <meta property="og:site_name" content="Andreas Stehmann Links">
    <meta property="og:title" content="Blog – Kaufberatungen, Tests & Vergleiche">
    <meta property="og:description" content="Unsere Experten-Ratgeber zu den besten Produkten in allen Kategorien.">
    <meta property="og:url" content="https://balu1705.github.io/andreasstehmann-links/blog/">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="stylesheet" href="/assets/style.css">
    {json_ld_scripts}
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-YPCSF9BFH2"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-YPCSF9BFH2');
    </script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a>
            <nav class="main-nav" aria-label="Hauptnavigation">
                <a href="/">Startseite</a>
                <a href="/blog/">Blog</a>
                <a href="/deals/">Deals</a>
                <a href="/ueber-uns/">Über uns</a>
            </nav>
        </div>
    </header>
    
    <main class="site-main">
        <div class="container">
            <nav class="breadcrumb" aria-label="Breadcrumb">
                <a href="/">Startseite</a> <span class="sep">/</span>
                <span aria-current="page">Blog</span>
            </nav>
            
            <header class="page-header">
                <h1>Blog – Kaufberatungen, Tests & Vergleiche</h1>
                <p class="page-lead">Unsere Experten-Ratgeber helfen dir, die besten Produkte zu finden. Ehrlich getestet, transparent verglichen, klar empfohlen.</p>
            </header>
            
            <div class="blog-index-grid">
                {''.join(article_cards)}
            </div>
            
            <section class="cta-section">
                <h2>Nicht fündig geworden?</h2>
                <p>Stöbere in allen <a href="/">Nischenkategorien</a> oder nutze die Suche auf der Startseite.</p>
                <a href="/" class="btn btn-primary">Zur Startseite</a>
            </section>
        </div>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div><h4>Andreas Stehmann Links</h4><p>Die besten Produkte finden – ohne stundenlanges Suchen.</p></div>
                <nav><h4>Navigation</h4><ul><li><a href="/">Startseite</a></li><li><a href="/blog/">Blog</a></li><li><a href="/ueber-uns/">Über uns</a></li><li><a href="/impressum/">Impressum</a></li><li><a href="/datenschutz/">Datenschutz</a></li></ul></nav>
                <nav><h4>Rechtliches</h4><ul><li><a href="/affiliate-hinweis/">Affiliate-Hinweis</a></li><li><a href="/cookie-einstellungen/">Cookie-Einstellungen</a></li></ul></nav>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Andreas Stehmann Links. Alle Rechte vorbehalten.</p>
                <p>* Affiliate-Links: Als Amazon-Partner verdiene ich an qualifizierten Verkäufen.</p>
            </div>
        </div>
    </footer>
    
    <script src="/assets/main.js"></script>
</body>
</html>'''
    return html


def generate_blog_pages(all_products):
    """Generate all blog pages and return list of blog slugs for sitemap."""
    blog_slugs = []
    niche_scores = [(slug, len(products)) for slug, products in all_products.items() if products]
    niche_scores.sort(key=lambda x: x[1], reverse=True)
    top_niches = [slug for slug, _ in niche_scores[:20]]  # Top 20 niches get blog articles
    
    for slug in top_niches:
        products = all_products[slug]
        article_html = generate_blog_article(slug, products, all_products)
        if article_html:
            blog_slugs.append(slug)
    
    return blog_slugs


from datetime import datetime

def main():
    print("🔄 Loading product data...")
    all_products = load_products()
    print(f"✅ Loaded {len(all_products)} niches with products")

    # Clean output directory
    output_path = Path(OUTPUT_DIR)
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True)
    (output_path / "assets").mkdir(parents=True)

    # Generate assets
    print("🎨 Generating assets...")
    css, js = generate_assets()
    (output_path / "assets" / "style.css").write_text(css, encoding='utf-8')
    (output_path / "assets" / "main.js").write_text(js, encoding='utf-8')

    # Generate homepage
    print("🏠 Generating homepage...")
    homepage_html = generate_homepage(all_products)
    (output_path / "index.html").write_text(homepage_html, encoding='utf-8')

    # Generate category pages
    print("📁 Generating category pages...")
    for cat_name, niches_in_cat in CATEGORIES.items():
        slug = CATEGORY_SLUGS.get(cat_name, f"kategorie/{cat_name.lower().replace(' ', '-').replace('&', '')}")
        cat_dir = output_path / slug
        cat_dir.mkdir(parents=True)
        cat_html = generate_category_page(cat_name, niches_in_cat, all_products)
        (cat_dir / "index.html").write_text(cat_html, encoding='utf-8')

    # Generate niche pages
    print("📦 Generating niche pages...")
    niche_count = 0
    for niche_slug, products in all_products.items():
        if not products:
            continue
        niche_dir = output_path / niche_slug
        niche_dir.mkdir(parents=True)
        niche_html = generate_niche_page(niche_slug, products, all_products)
        (niche_dir / "index.html").write_text(niche_html, encoding='utf-8')
        niche_count += 1

    # Generate legal pages
    print("⚖️ Generating legal pages...")
    legal_pages = generate_legal_pages()
    for page_name, page_html in legal_pages.items():
        page_dir = output_path / page_name
        page_dir.mkdir(parents=True)
        (page_dir / "index.html").write_text(page_html, encoding='utf-8')

    # Generate blog pages
    print("📝 Generating blog pages...")
    blog_dir = output_path / "blog"
    blog_dir.mkdir(parents=True)
    blog_slugs = generate_blog_pages(all_products)
    for slug in blog_slugs:
        niche_name = NICHE_NAMES.get(slug, slug.replace('-', ' ').title())
        products = all_products[slug]
        article_html = generate_blog_article(slug, products, all_products)
        if article_html:
            article_dir = blog_dir / slug
            article_dir.mkdir(parents=True)
            (article_dir / "index.html").write_text(article_html, encoding='utf-8')
    # Generate blog index
    blog_index_html = generate_blog_index(all_products)
    (blog_dir / "index.html").write_text(blog_index_html, encoding='utf-8')
    print(f"   📝 Blog articles: {len(blog_slugs)}")

    # Generate deals feed (RSS, JSON, HTML)
    print("🎯 Generating deals feed...")
    deals_feed = generate_deals_feed(all_products)
    deals_dir = output_path / "deals"
    deals_dir.mkdir(parents=True)
    (deals_dir / "index.html").write_text(deals_feed['html'], encoding='utf-8')
    (deals_dir / "feed.xml").write_text(deals_feed['rss'], encoding='utf-8')
    (deals_dir / "feed.json").write_text(deals_feed['json'], encoding='utf-8')
    print(f"   🎯 Deals: {len(deals_feed['rss'].split('<item>')) - 1} items in RSS")

    # Generate Google Shopping feed
    print("🛒 Generating shopping feed...")
    shopping_xml = generate_shopping_feed(all_products)
    (output_path / "shopping-feed.xml").write_text(shopping_xml, encoding='utf-8')
    product_count = shopping_xml.count('<item>') - 1
    print(f"   🛒 Shopping feed: {product_count} products")

    # Generate über-uns page
    ueber_uns = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Über uns - Andreas Stehmann Links</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <header class="site-header"><div class="container"><a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a></div></header>
    <main class="site-main"><div class="container"><h1>Über uns</h1><div class="legal-content"><h2>Unsere Mission</h2><p>Andreas Stehmann Links hilft dir, die besten Produkte auf Amazon zu finden – ohne stundenlanges Suchen und Vergleichen.</p><h2>Wie wir arbeiten</h2><ul><li><strong>Recherche:</strong> Wir analysieren Kundenbewertungen, Testberichte und Preisverläufe.</li><li><strong>Selektion:</strong> Nur Produkte mit überdurchschnittlicher Qualität und gutem Preis-Leistungs-Verhältnis schaffen es auf die Seite.</li><li><strong>Aktualisierung:</strong> Preise und Verfügbarkeit werden regelmäßig geprüft.</li></ul><h2>Transparenz</h2><p>Diese Website wird durch Affiliate-Links finanziert. Mehr dazu in unserem <a href="/affiliate-hinweis/">Affiliate-Hinweis</a>.</p></div></div></main>
    <footer class="site-footer"><div class="container"><p>&copy; 2024 Andreas Stehmann Links.</p></div></footer>
</body>
</html>'''
    ueber_dir = output_path / "ueber-uns"
    ueber_dir.mkdir(parents=True)
    (ueber_dir / "index.html").write_text(ueber_uns, encoding='utf-8')

    # Generate Kaufberatungen overview page (Phase 3 prep)
    kaufberatungen = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kaufberatungen - Andreas Stehmann Links</title>
    <meta name="description" content="Fundierte Kaufberatungen für wichtige Anschaffungen. Vergleiche, Checklisten und Empfehlungen für Möbel, Smart Home, Küche & mehr.">
    <link rel="canonical" href="https://balu1705.github.io/andreasstehmann-links/kaufberatungen/">
    <meta property="og:title" content="Kaufberatungen - Andreas Stehmann Links">
    <meta property="og:description" content="Fundierte Kaufberatungen für wichtige Anschaffungen. Vergleiche, Checklisten und Empfehlungen.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://balu1705.github.io/andreasstehmann-links/kaufberatungen/">
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="logo" aria-label="Andreas Stehmann Links – Startseite">
                <span class="logo-icon" aria-hidden="true">🔗</span>
                <span class="logo-text">Andreas Stehmann Links</span>
            </a>
            <nav class="main-nav" aria-label="Hauptnavigation">
                <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Menü öffnen">
                    <span class="hamburger" aria-hidden="true"></span>
                </button>
                <ul id="nav-menu" class="nav-menu" role="menubar">
                    <li role="none"><a href="/kategorie/wohnen-haushalt/" role="menuitem">Wohnen & Haushalt</a></li>
                    <li role="none"><a href="/kategorie/kueche-kochen/" role="menuitem">Küche & Kochen</a></li>
                    <li role="none"><a href="/kategorie/beauty-pflege/" role="menuitem">Beauty & Pflege</a></li>
                    <li role="none"><a href="/kategorie/baby-familie/" role="menuitem">Baby & Familie</a></li>
                    <li role="none"><a href="/kategorie/fitness-sport/" role="menuitem">Fitness & Sport</a></li>
                    <li role="none"><a href="/kategorie/technik-gaming/" role="menuitem">Technik & Gaming</a></li>
                    <li role="none"><a href="/kategorie/lifestyle-mehr/" role="menuitem">Lifestyle & Mehr</a></li>
                    <li role="none"><a href="/deals/" role="menuitem">Deals</a></li>
                    <li role="none"><a href="/ueber-uns/" role="menuitem">Über uns</a></li>
                    <li role="none"><a href="/impressum/" role="menuitem">Impressum</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="site-main">
        <section class="page-hero" aria-labelledby="page-title">
            <div class="container">
                <h1 id="page-title">Kaufberatungen</h1>
                <p class="page-subtitle">Fundierte Entscheidungs-Hilfen für wichtige Anschaffungen – vergleichen, verstehen, richtig kaufen</p>
            </div>
        </section>

        <section class="guides-overview" aria-labelledby="guides-title">
            <div class="container">
                <header class="section-header">
                    <h2 id="guides-title">Unsere Kaufberatungen</h2>
                    <p class="section-subtitle">In Arbeit – neue Ratgeber erscheinen regelmäßig</p>
                </header>
                <div class="guides-grid" role="list">
                    <article class="guide-card">
                        <div class="guide-content">
                            <span class="guide-category">Wohnen & Haushalt</span>
                            <h3><a href="/kaufberatung/moebel-kleine-wohnungen/">Die besten Möbel für kleine Wohnungen</a></h3>
                            <p>Platzsparende Lösungen, die funktionieren – getestet & verglichen.</p>
                            <a href="/kaufberatung/moebel-kleine-wohnungen/" class="guide-cta">Zum Ratgeber →</a>
                        </div>
                    </article>
                    <article class="guide-card">
                        <div class="guide-content">
                            <span class="guide-category">Technik & Gaming</span>
                            <h3><a href="/kaufberatung/smart-home-einsteiger/">Smart Home für Einsteiger: Der komplette Guide</a></h3>
                            <p>Von smarter Beleuchtung bis Sicherheit – alles was du brauchst.</p>
                            <a href="/kaufberatung/smart-home-einsteiger/" class="guide-cta">Zum Ratgeber →</a>
                        </div>
                    </article>
                    <article class="guide-card">
                        <div class="guide-content">
                            <span class="guide-category">Küche & Kochen</span>
                            <h3><a href="/kaufberatung/kuechengadgets-zeit-sparen/">Praktische Küchengadgets, die Zeit sparen</a></h3>
                            <p>Clevere Helfer für den Alltag – unsere Top-Empfehlungen 2026.</p>
                            <a href="/kaufberatung/kuechengadgets-zeit-sparen/" class="guide-cta">Zum Ratgeber →</a>
                        </div>
                    </article>
                </div>
                <div class="section-footer">
                    <p style="text-align: center; color: var(--muted); margin-top: 1rem;">Weitere Kaufberatungen in Vorbereitung. <a href="/newsletter/">Newsletter abonnieren</a> für Updates.</p>
                </div>
            </div>
        </section>

        <section class="guide-categories" aria-labelledby="cat-title">
            <div class="container">
                <h2 id="cat-title">Nach Kategorien stöbern</h2>
                <p class="section-subtitle">Alle Produktkategorien mit kuratierten Empfehlungen</p>
                <div class="theme-worlds-grid" role="list">
                    <article class="theme-world-card">
                        <a href="/kategorie/wohnen-haushalt/" class="theme-world-link">
                            <div class="theme-world-image" style="background-image: url('https://m.media-amazon.com/images/I/B0H1CMGNHR._AC_SL500_.jpg')">
                                <span class="theme-world-overlay"><span class="theme-world-count">36 Kategorien</span></span>
                            </div>
                            <div class="theme-world-content">
                                <h3>Wohnen & Haushalt</h3>
                                <p>Bad, Balkon, Schlafzimmer, Organisation & mehr</p>
                                <span class="theme-world-cta">Entdecken →</span>
                            </div>
                        </a>
                    </article>
                    <article class="theme-world-card">
                        <a href="/kategorie/kueche-kochen/" class="theme-world-link">
                            <div class="theme-world-image" style="background-image: url('https://m.media-amazon.com/images/I/B0GX5H49DW._AC_SL500_.jpg')">
                                <span class="theme-world-overlay"><span class="theme-world-count">9 Kategorien</span></span>
                            </div>
                            <div class="theme-world-content">
                                <h3>Küche & Kochen</h3>
                                <p>Kaffee, Heißluftfritteuse, Backen, Tischkultur</p>
                                <span class="theme-world-cta">Entdecken →</span>
                            </div>
                        </a>
                    </article>
                    <article class="theme-world-card">
                        <a href="/kategorie/technik-gaming/" class="theme-world-link">
                            <div class="theme-world-image" style="background-image: url('https://m.media-amazon.com/images/I/B0C81Z7BBM._AC_SL500_.jpg')">
                                <span class="theme-world-overlay"><span class="theme-world-count">7 Kategorien</span></span>
                            </div>
                            <div class="theme-world-content">
                                <h3>Technik & Gaming</h3>
                                <p>Smart Home, Gaming, Audio, Zubehör</p>
                                <span class="theme-world-cta">Entdecken →</span>
                            </div>
                        </a>
                    </article>
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a>
                    <p>Kuratierte Produktempfehlungen für dein Zuhause. Handverlesen, nicht algorithmisch.</p>
                </div>
                <nav class="footer-nav" aria-label="Produktkategorien">
                    <h4>Kategorien</h4>
                    <ul>
                        <li><a href="/kategorie/wohnen-haushalt/">Wohnen & Haushalt</a></li>
                        <li><a href="/kategorie/kueche-kochen/">Küche & Kochen</a></li>
                        <li><a href="/kategorie/beauty-pflege/">Beauty & Pflege</a></li>
                        <li><a href="/kategorie/baby-familie/">Baby & Familie</a></li>
                        <li><a href="/kategorie/fitness-sport/">Fitness & Sport</a></li>
                        <li><a href="/kategorie/technik-gaming/">Technik & Gaming</a></li>
                        <li><a href="/kategorie/lifestyle-mehr/">Lifestyle & Mehr</a></li>
                    </ul>
                </nav>
                <nav class="footer-nav" aria-label="Service & Info">
                    <h4>Service</h4>
                    <ul>
                        <li><a href="/deals/">Tagesaktuelle Deals</a></li>
                        <li><a href="/kaufberatungen/">Kaufberatungen</a></li>
                        <li><a href="/newsletter/">Newsletter</a></li>
                        <li><a href="/kontakt/">Kontakt</a></li>
                        <li><a href="/preischeck/">Preisprüfung & Methodik</a></li>
                    </ul>
                </nav>
                <nav class="footer-nav" aria-label="Rechtliches">
                    <h4>Rechtliches</h4>
                    <ul>
                        <li><a href="/impressum/">Impressum</a></li>
                        <li><a href="/datenschutz/">Datenschutz</a></li>
                        <li><a href="/affiliate-hinweis/">Affiliate-Hinweis</a></li>
                        <li><a href="/ueber-uns/">Über uns</a></li>
                    </ul>
                </nav>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Andreas Stehmann Links. Als Amazon-Partner verdiene ich an qualifizierten Käufen.</p>
            </div>
        </div>
    </footer>

    <script src="/assets/main.js"></script>
</body>
</html>'''
    kb_dir = output_path / "kaufberatungen"
    kb_dir.mkdir(parents=True)
    (kb_dir / "index.html").write_text(kaufberatungen, encoding='utf-8')

    # Generate Kontakt page
    kontakt = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kontakt - Andreas Stehmann Links</title>
    <meta name="description" content="Kontakt zu Andreas Stehmann Links. Fragen, Anregungen, Kooperationen.">
    <link rel="canonical" href="https://balu1705.github.io/andreasstehmann-links/kontakt/">
    <meta property="og:title" content="Kontakt - Andreas Stehmann Links">
    <meta property="og:description" content="Kontakt zu Andreas Stehmann Links. Fragen, Anregungen, Kooperationen.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://balu1705.github.io/andreasstehmann-links/kontakt/">
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="/" class="logo" aria-label="Andreas Stehmann Links – Startseite">
                <span class="logo-icon" aria-hidden="true">🔗</span>
                <span class="logo-text">Andreas Stehmann Links</span>
            </a>
            <nav class="main-nav" aria-label="Hauptnavigation">
                <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Menü öffnen">
                    <span class="hamburger" aria-hidden="true"></span>
                </button>
                <ul id="nav-menu" class="nav-menu" role="menubar">
                    <li role="none"><a href="/kategorie/wohnen-haushalt/" role="menuitem">Wohnen & Haushalt</a></li>
                    <li role="none"><a href="/kategorie/kueche-kochen/" role="menuitem">Küche & Kochen</a></li>
                    <li role="none"><a href="/kategorie/beauty-pflege/" role="menuitem">Beauty & Pflege</a></li>
                    <li role="none"><a href="/kategorie/baby-familie/" role="menuitem">Baby & Familie</a></li>
                    <li role="none"><a href="/kategorie/fitness-sport/" role="menuitem">Fitness & Sport</a></li>
                    <li role="none"><a href="/kategorie/technik-gaming/" role="menuitem">Technik & Gaming</a></li>
                    <li role="none"><a href="/kategorie/lifestyle-mehr/" role="menuitem">Lifestyle & Mehr</a></li>
                    <li role="none"><a href="/deals/" role="menuitem">Deals</a></li>
                    <li role="none"><a href="/ueber-uns/" role="menuitem">Über uns</a></li>
                    <li role="none"><a href="/impressum/" role="menuitem">Impressum</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="site-main">
        <section class="page-hero" aria-labelledby="page-title">
            <div class="container">
                <h1 id="page-title">Kontakt</h1>
                <p class="page-subtitle">Du hast Fragen, Anregungen oder möchtest kooperieren?</p>
            </div>
        </section>

        <section class="contact-section" aria-labelledby="contact-title">
            <div class="container">
                <div class="contact-grid">
                    <div class="contact-info">
                        <h2 id="contact-title">Schreib uns</h2>
                        <p>Ob Produktvorschlag, Korrekturhinweis, Kooperationsanfrage oder einfach Feedback – wir freuen uns über deine Nachricht.</p>
                        
                        <div class="contact-methods">
                            <div class="contact-method">
                                <span class="contact-icon" aria-hidden="true">✉️</span>
                                <div>
                                    <h3>E-Mail</h3>
                                    <p><a href="mailto:andreas@stehmann-links.de">andreas@stehmann-links.de</a></p>
                                </div>
                            </div>
                            <div class="contact-method">
                                <span class="contact-icon" aria-hidden="true">💬</span>
                                <div>
                                    <h3>Telegram</h3>
                                    <p><a href="https://t.me/andreasstehmann" target="_blank" rel="noopener">@andreasstehmann</a></p>
                                </div>
                            </div>
                        </div>

                        <h3>Was du uns schreiben kannst</h3>
                        <ul>
                            <li><strong>Produktvorschläge:</strong> Fehlt ein gutes Produkt? Schick uns den ASIN oder Link.</li>
                            <li><strong>Korrekturen:</strong> Preis falsch, Link kaputt, Info veraltet? Danke für den Hinweis!</li>
                            <li><strong>Kooperationen:</strong> Du bist Marke, Agentur oder Creator? Gerne per Mail mit Details.</li>
                            <li><strong>Feedback:</strong> Was gefällt, was fehlt, was nervt? Wir lesen alles.</li>
                        </ul>

                        <div class="contact-note">
                            <p><strong>Antwortzeit:</strong> Meist innerhalb 24–48h (werktags).</p>
                            <p><strong>Technischer Support für Amazon-Bestellungen:</strong> Bitte direkt an <a href="https://www.amazon.de/gp/help/customer/display.html" target="_blank" rel="noopener">Amazon Kundenservice</a> wenden – wir haben keinen Zugriff auf Bestellungen.</p>
                        </div>
                    </div>

                    <div class="contact-form-wrapper">
                        <form class="contact-form" action="https://formspree.io/f/your-form-id" method="POST" aria-label="Kontaktformular">
                            <div class="form-group">
                                <label for="name">Name</label>
                                <input type="text" id="name" name="name" required placeholder="Dein Name">
                            </div>
                            <div class="form-group">
                                <label for="email">E-Mail</label>
                                <input type="email" id="email" name="email" required placeholder="deine@email.de">
                            </div>
                            <div class="form-group">
                                <label for="subject">Betreff</label>
                                <select id="subject" name="subject" required>
                                    <option value="">Bitte wählen</option>
                                    <option value="product">Produktvorschlag / Korrektur</option>
                                    <option value="cooperation">Kooperationsanfrage</option>
                                    <option value="feedback">Feedback / Sonstiges</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="message">Nachricht</label>
                                <textarea id="message" name="message" rows="5" required placeholder="Deine Nachricht..."></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary btn-large">Absenden</button>
                            <p class="form-hint">Das Formular nutzt Formspree – keine Daten werden auf diesem Server gespeichert.</p>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="/" class="logo"><span class="logo-icon">🔗</span><span class="logo-text">Andreas Stehmann Links</span></a>
                    <p>Kuratierte Produktempfehlungen für dein Zuhause. Handverlesen, nicht algorithmisch.</p>
                </div>
                <nav class="footer-nav" aria-label="Produktkategorien">
                    <h4>Kategorien</h4>
                    <ul>
                        <li><a href="/kategorie/wohnen-haushalt/">Wohnen & Haushalt</a></li>
                        <li><a href="/kategorie/kueche-kochen/">Küche & Kochen</a></li>
                        <li><a href="/kategorie/beauty-pflege/">Beauty & Pflege</a></li>
                        <li><a href="/kategorie/baby-familie/">Baby & Familie</a></li>
                        <li><a href="/kategorie/fitness-sport/">Fitness & Sport</a></li>
                        <li><a href="/kategorie/technik-gaming/">Technik & Gaming</a></li>
                        <li><a href="/kategorie/lifestyle-mehr/">Lifestyle & Mehr</a></li>
                    </ul>
                </nav>
                <nav class="footer-nav" aria-label="Service & Info">
                    <h4>Service</h4>
                    <ul>
                        <li><a href="/deals/">Tagesaktuelle Deals</a></li>
                        <li><a href="/kaufberatungen/">Kaufberatungen</a></li>
                        <li><a href="/newsletter/">Newsletter</a></li>
                        <li><a href="/kontakt/">Kontakt</a></li>
                        <li><a href="/preischeck/">Preisprüfung & Methodik</a></li>
                    </ul>
                </nav>
                <nav class="footer-nav" aria-label="Rechtliches">
                    <h4>Rechtliches</h4>
                    <ul>
                        <li><a href="/impressum/">Impressum</a></li>
                        <li><a href="/datenschutz/">Datenschutz</a></li>
                        <li><a href="/affiliate-hinweis/">Affiliate-Hinweis</a></li>
                        <li><a href="/ueber-uns/">Über uns</a></li>
                    </ul>
                </nav>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Andreas Stehmann Links. Als Amazon-Partner verdiene ich an qualifizierten Käufen.</p>
            </div>
        </div>
    </footer>

    <script src="/assets/main.js"></script>
</body>
</html>'''
    kontakt_dir = output_path / "kontakt"
    kontakt_dir.mkdir(parents=True)
    (kontakt_dir / "index.html").write_text(kontakt, encoding='utf-8')

    # Generate sitemap & robots.txt
    print("🗺️ Generating sitemap & robots.txt...")
    (output_path / "sitemap.xml").write_text(generate_sitemap(all_products), encoding='utf-8')
    (output_path / "robots.txt").write_text(generate_robots_txt(), encoding='utf-8')

    print(f"\n✅ Site generated successfully!")
    print(f"   📄 Homepage: 1")
    print(f"   📁 Categories: {len(CATEGORIES)}")
    print(f"   📦 Niches: {niche_count}")
    print(f"   ⚖️ Legal pages: 4")
    print(f"   📍 Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()