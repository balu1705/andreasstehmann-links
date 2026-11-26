#!/usr/bin/env python3
"""
Daily Maintenance Script for andreasstehmann-links
- Rebuilds site with fresh product data
- Checks product performance via Zernio/PartnerNet
- Rotates underperforming products
- Generates fresh blog content
- Triggers social media posts
"""

import json
import os
import sys
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/opt/data/andreasstehmann-links')

BASE_DIR = Path('/opt/data/andreasstehmann-links')
DATA_FILE = BASE_DIR / 'data' / 'niche_products.json'
OUTPUT_DIR = BASE_DIR / 'output'
BUILD_SCRIPT = BASE_DIR / 'build_site.py'
LOG_FILE = BASE_DIR / 'logs' / 'daily_maintenance.log'

# Zernio API config (from environment)
ZERNIO_API_KEY = os.getenv('ZERNIO_API_KEY')
ZERNIO_BASE_URL = 'https://api.zernio.com/v1'

# Amazon Affiliate Tag
AFFILIATE_TAG = 'balu17051-21'

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f'[{timestamp}] {msg}'
    print(log_msg)
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def run_build():
    """Rebuild the static site."""
    log('🔨 Starting site rebuild...')
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        log('✅ Site rebuild successful')
        log(result.stdout)
    else:
        log(f'❌ Site rebuild failed: {result.stderr}')
    return result.returncode == 0

def load_product_data():
    """Load current product data."""
    with open(DATA_FILE) as f:
        return json.load(f)

def save_product_data(data):
    """Save updated product data."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_zernio_clicks(asin, days=7):
    """Get click data for an ASIN from Zernio API."""
    if not ZERNIO_API_KEY:
        return None
    try:
        headers = {'Authorization': f'Bearer {ZERNIO_API_KEY}'}
        params = {'asin': asin, 'days': days}
        resp = requests.get(f'{ZERNIO_BASE_URL}/clicks', headers=headers, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        log(f'⚠️ Zernio API error for {asin}: {e}')
    return None

def analyze_product_performance(product_data):
    """Analyze which products perform well vs poorly."""
    log('📊 Analyzing product performance...')
    
    performance = {}
    for niche, products in product_data.items():
        for product in products:
            asin = product.get('asin')
            if not asin:
                continue
            
            clicks_data = get_zernio_clicks(asin, days=30)
            if clicks_data:
                clicks = clicks_data.get('clicks', 0)
                earnings = clicks_data.get('earnings', 0)
                conversion = clicks_data.get('conversion_rate', 0)
                
                performance[asin] = {
                    'niche': niche,
                    'title': product.get('title', '')[:50],
                    'clicks': clicks,
                    'earnings': earnings,
                    'conversion': conversion,
                    'score': clicks * 0.3 + earnings * 0.5 + conversion * 100 * 0.2
                }
                log(f'  {asin} ({product.get("title", "")[:40]}): {clicks} clicks, €{earnings:.2f}, {conversion:.2%} conv')
    
    return performance

def rotate_products(product_data, performance):
    """Replace bottom 20% performing products with alternatives."""
    log('🔄 Rotating underperforming products...')
    
    # Group by niche
    niche_performance = {}
    for asin, perf in performance.items():
        niche = perf['niche']
        if niche not in niche_performance:
            niche_performance[niche] = []
        niche_performance[niche].append(perf)
    
    rotated_count = 0
    for niche, products in niche_performance.items():
        if len(products) < 3:
            continue
        
        # Sort by score
        products.sort(key=lambda x: x['score'])
        bottom_count = max(1, len(products) // 5)  # Bottom 20%
        
        for perf in products[:bottom_count]:
            asin = perf['asin']
            # Find and replace in product_data
            for i, p in enumerate(product_data[niche]):
                if p.get('asin') == asin:
                    # Mark for replacement (in real implementation, fetch new product)
                    p['needs_replacement'] = True
                    p['performance_score'] = perf['score']
                    rotated_count += 1
                    log(f'  🔄 Marked for replacement: {asin} in {niche} (score: {perf["score"]:.1f})')
                    break
    
    log(f'✅ Marked {rotated_count} products for replacement')
    return rotated_count > 0

def generate_blog_content():
    """Generate fresh blog content for top niches."""
    log('✍️ Generating blog content...')
    
    # Use the existing generate_blog_content.py from site-build
    script = Path('/opt/data/site-build/generate_blog_content.py')
    if script.exists():
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd='/opt/data/site-build',
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            log('✅ Blog content generated')
        else:
            log(f'⚠️ Blog generation failed: {result.stderr[:200]}')
    else:
        log('⚠️ Blog generation script not found')

def trigger_social_posts():
    """Trigger social media posts via Zernio/BulkPublish."""
    log('📱 Triggering social media posts...')
    
    # Use existing social_daily.py for BulkPublish (TikTok/Threads/YouTube)
    script = Path('/opt/data/social_daily.py')
    if script.exists():
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd='/opt/data',
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            log('✅ Social posts triggered')
        else:
            log(f'⚠️ Social posts failed: {result.stderr[:200]}')
    
    # Zernio for Instagram/Pinterest (if configured)
    zernio_script = Path('/opt/data/zernio_post.py')
    if zernio_script.exists() and ZERNIO_API_KEY:
        result = subprocess.run(
            [sys.executable, str(zernio_script)],
            cwd='/opt/data',
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            log('✅ Zernio posts triggered')

def deploy_to_github_pages():
    """Deploy rebuilt site to GitHub Pages."""
    log('🚀 Deploying to GitHub Pages...')
    
    # Get token from existing remote
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        remote_url = result.stdout.strip()
        # Extract token from URL like https://token@github.com/user/repo.git
        if '@github.com' in remote_url:
            token_part = remote_url.split('https://')[1].split('@github.com')[0]
            
            # Push output directory
            subprocess.run(['git', 'add', '.'], cwd=OUTPUT_DIR, check=True)
            subprocess.run(['git', 'commit', '-m', f'Daily update {datetime.now().strftime("%Y-%m-%d")}'], 
                         cwd=OUTPUT_DIR, check=True)
            subprocess.run(['git', 'push'], cwd=OUTPUT_DIR, check=True)
            
            # Trigger GitHub Pages build via API
            headers = {'Authorization': f'token {token_part}', 'Accept': 'application/vnd.github.v3+json'}
            requests.post(
                'https://api.github.com/repos/balu1705/andreasstehmann-links/pages/builds',
                headers=headers,
                json={'source': {'branch': 'main', 'path': '/'}},
                timeout=30
            )
            log('✅ Deployed and GitHub Pages build triggered')
    except Exception as e:
        log(f'❌ Deploy failed: {e}')

def main():
    log('=' * 60)
    log('🌅 Starting daily maintenance for andreasstehmann-links')
    log('=' * 60)
    
    # 1. Load current data
    product_data = load_product_data()
    log(f'📦 Loaded {len(product_data)} niches with products')
    
    # 2. Analyze performance
    performance = analyze_product_performance(product_data)
    
    # 3. Rotate underperforming products
    if performance:
        rotated = rotate_products(product_data, performance)
        if rotated:
            save_product_data(product_data)
            log('💾 Updated product data saved')
    
    # 4. Generate fresh blog content
    generate_blog_content()
    
    # 5. Rebuild site
    if run_build():
        # 6. Deploy
        deploy_to_github_pages()
    
    # 7. Trigger social posts
    trigger_social_posts()
    
    log('=' * 60)
    log('🌙 Daily maintenance complete')
    log('=' * 60)

if __name__ == '__main__':
    main()