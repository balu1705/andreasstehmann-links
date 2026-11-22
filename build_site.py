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

def generate_product_card(product, index, niche_slug=None):
    """Generate HTML for a single product card."""
    asin = product.get('asin', '')
    name = product.get('name', 'Produkt')
    price = product.get('price', '')
    img_url = get_amazon_image_url(asin)
    affiliate_url = get_affiliate_link(asin)

    # Truncate long names
    display_name = name[:80] + "..." if len(name) > 80 else name
    
    # Data attributes for GA4 click tracking
    data_attrs = f'data-asin="{asin}" data-niche="{niche_slug or ""}" data-position="{index}" data-price="{price}"'

    return f'''
    <article class="product-card" data-index="{index}">
        <a href="{affiliate_url}" target="_blank" rel="noopener sponsored" class="product-link" {data_attrs}>
            <div class="product-image-wrapper">
                <img src="{img_url}" alt="{display_name}" loading="lazy" class="product-image">
                <span class="product-badge">Zum Angebot</span>
            </div>
            <div class="product-info">
                <h3 class="product-title">{display_name}</h3>
                <div class="product-price">{price} €</div>
            </div>
        </a>
    </article>'''

def generate_niche_page(niche_slug, products, all_niches):
    """Generate HTML for a single niche page."""
    niche_name = NICHE_NAMES.get(niche_slug, niche_slug.replace('-', ' ').title())
    product_cards = ''.join(generate_product_card(p, i, niche_slug) for i, p in enumerate(products[:12]))
    
    # Find category for breadcrumb
    category = None
    for cat, niches in CATEGORIES.items():
        if niche_slug in niches:
            category = cat
            break
    
    cat_display = CATEGORY_DISPLAY.get(category, category) if category else None
    cat_slug = CATEGORY_SLUGS.get(category, category.lower().replace(" ", "-").replace("&", "")) if category else None
    breadcrumb = f'<a href="/">Startseite</a> / <a href="/{cat_slug}/">{cat_display}</a> / {niche_name}' if category else f'<a href="/">Startseite</a> / {niche_name}'
    
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{niche_name} - Andreas Stehmann Links</title>
    <meta name="description" content="Die besten {niche_name.lower()} Produkte auf Amazon. Experten-Empfehlungen mit echten Kundenbewertungen und aktuellen Preisen.">
    <link rel="canonical" href="https://balu1705.github.io/andreasstehmann-links/{niche_slug}/">
    <meta property="og:title" content="{niche_name} - Andreas Stehmann Links">
    <meta property="og:description" content="Die besten {niche_name.lower()} Produkte auf Amazon.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://balu1705.github.io/andreasstehmann-links/{niche_slug}/">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="stylesheet" href="/assets/style.css">
    <link rel="preconnect" href="https://m.media-amazon.com">
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
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
                    <li><a href="/ueber-uns/">Über uns</a></li>
                    <li><a href="/impressum/">Impressum</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="site-main">
        <nav class="breadcrumb" aria-label="Brotkrumennavigation">
            <div class="container">{breadcrumb}</div>
        </nav>

        <section class="niche-hero">
            <div class="container">
                <h1>{niche_name}</h1>
                <p class="hero-subtitle">Handverlesene Empfehlungen • Aktuelle Preise • Echte Amazon-Bewertungen</p>
                <p class="hero-disclaimer">Als Amazon-Partner verdiene ich an qualifizierten Käufen.</p>
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

        <section class="product-grid-section">
            <div class="container">
                <div class="product-grid" role="list">
                    {product_cards}
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
    <!-- GA4 Affiliate Click Tracking -->
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            document.querySelectorAll("a.product-link[data-asin]").forEach(function(link) {{
                link.addEventListener("click", function(e) {{
                    var asin = this.getAttribute("data-asin");
                    var niche = this.getAttribute("data-niche");
                    var position = this.getAttribute("data-position");
                    var price = this.getAttribute("data-price");
                    if (asin && typeof gtag === "function") {{
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
    """Generate HTML for a category overview page."""
    niche_cards = ''
    for niche_slug in niches_in_cat:
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
    
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_display} - Andreas Stehmann Links</title>
    <meta name="description" content="Alle {cat_display.lower()} Kategorien auf einen Blick. Finde die besten Produkte in {len(niches_in_cat)} Unterkategorien.">
    <link rel="canonical" href="https://balu1705.github.io/andreasstehmann-links/{cat_slug}/">
    <meta property="og:title" content="{cat_display} - Andreas Stehmann Links">
    <meta property="og:description" content="Alle {cat_display.lower()} Kategorien auf einen Blick.">
    <meta property="og:type" content="website">
    <link rel="stylesheet" href="/assets/style.css">
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
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
                <p class="hero-subtitle">{len([n for n in niches_in_cat if n in all_products and all_products[n]])} Unterkategorien • Hunderte Produkte</p>
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

        <section class="category-grid-section">
            <div class="container">
                <div class="category-grid" role="list">
                    {niche_cards}
                </div>
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
    <!-- GA4 Affiliate Click Tracking -->
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            document.querySelectorAll("a.product-link[data-asin]").forEach(function(link) {{
                link.addEventListener("click", function(e) {{
                    var asin = this.getAttribute("data-asin");
                    var niche = this.getAttribute("data-niche");
                    var position = this.getAttribute("data-position");
                    var price = this.getAttribute("data-price");
                    if (asin && typeof gtag === "function") {{
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
    elif month in [3, 4, 5]:
        season = "Frühling"
        season_emoji = "🌱"
        season_desc = "Frische Frühlings-Ideen für dein Zuhause"
    elif month in [6, 7, 8]:
        season = "Sommer"
        season_emoji = "☀️"
        season_desc = "Sommer-Highlights für Balkon, Garten & Reisen"
    else:
        season = "Herbst"
        season_emoji = "🍂"
        season_desc = "Warme Herbst-Favoriten für drinnen & draußen"
    
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
                    <a href="/kategorie/{cat_slug}/" class="btn btn-outline">Alle {season}-Produkte entdecken</a>
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
                </div>
            </div>
        </div>
    </footer>
    <!-- GA4 Affiliate Click Tracking -->
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            document.querySelectorAll("a.product-link[data-asin]").forEach(function(link) {{
                link.addEventListener("click", function(e) {{
                    var asin = this.getAttribute("data-asin");
                    var niche = this.getAttribute("data-niche");
                    var position = this.getAttribute("data-position");
                    var price = this.getAttribute("data-price");
                    if (asin && typeof gtag === "function") {{
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
    <main class="site-main"><div class="container"><h1>Affiliate-Hinweis</h1><div class="legal-content"><h2>Transparenz bei Empfehlungen</h2><p>Auf dieser Website verwenden wir Affiliate-Links (markiert mit * oder durch den Hinweis "Als Amazon-Partner verdiene ich an qualifizierten Käufen").</p><h2>Was bedeutet das für dich?</h2><ul><li>Du klickst auf einen Produktlink und wirst zu Amazon weitergeleitet</li><li>Kaufst du dort etwas, erhalten wir eine kleine Provision</li><li><strong>Für dich ändert sich der Preis nicht</strong> – du zahlst den regulären Amazon-Preis</li></ul><h2>Warum Affiliate-Links?</h2><p>Die Provisionen decken die Betriebskosten dieser Website (Hosting, Domain, Wartung) und ermöglichen es uns, weiterhin unabhängige Produktempfehlungen zu recherchieren und zu veröffentlichen.</p><h2>Unsere Unabhängigkeit</h2><p>Die Provision beeinflusst <strong>nicht</strong> unsere Produktauswahl. Wir empfehlen nur Produkte, von denen wir überzeugt sind – basierend auf Kundenbewertungen, Testergebnissen und Preis-Leistungs-Verhältnis.</p></div></div></main>
    <footer class="site-footer"><div class="container"><p>&copy; 2024 Andreas Stehmann Links.</p></div></footer>
</body>
</html>'''
    
    return {
        'impressum': impressum,
        'datenschutz': datenschutz,
        'affiliate-hinweis': affiliate_hinweis
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
    
    # Legal pages
    for page in ['impressum', 'datenschutz', 'affiliate-hinweis', 'ueber-uns']:
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

/* ===== ACCESSIBILITY ===== */
:focus-visible { outline: 3px solid var(--color-primary); outline-offset: 2px; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
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