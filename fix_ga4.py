with open('build_site.py', 'r') as f:
    content = f.read()

# Remove the misplaced tracking scripts (3 occurrences outside templates)
import re
pattern = r'\s*<!-- GA4 Affiliate Click Tracking -->\s*<script>\s*document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{.*?\}\s*\);\s*\}\s*\);\s*</script>\s*'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# The tracking script to insert inside templates
ts = "    <!-- GA4 Affiliate Click Tracking -->\n    <script>\n        document.addEventListener('DOMContentLoaded', function() {\n            document.querySelectorAll('a.product-link[data-asin]').forEach(function(link) {\n                link.addEventListener('click', function(e) {\n                    var asin = this.getAttribute('data-asin');\n                    var niche = this.getAttribute('data-niche');\n                    var position = this.getAttribute('data-position');\n                    var price = this.getAttribute('data-price');\n                    if (asin && typeof gtag === 'function') {\n                        gtag('event', 'affiliate_click', {\n                            'asin': asin,\n                            'niche': niche || '',\n                            'position': parseInt(position) || 0,\n                            'price': parseFloat(price) || 0,\n                            'currency': 'EUR',\n                            'affiliate_tag': 'balu17051-21',\n                            'link_domain': 'amazon.de'\n                        });\n                    }\n                });\n            });\n        });\n    </script>"

# Fix template 1: niche page
old1 = '    <script src="/assets/main.js"></script>\n</body>\n</html>\'\'\'\n\ndef generate_category_page'
new1 = '    ' + ts + '\n    <script src="/assets/main.js"></script>\n</body>\n</html>\'\'\'\n\ndef generate_category_page'
content = content.replace(old1, new1, 1)

# Fix template 2: category page
old2 = '    <script src="/assets/main.js"></script>\n</body>\n</html>\'\'\'\n\ndef generate_homepage'
new2 = '    ' + ts + '\n    <script src="/assets/main.js"></script>\n</body>\n</html>\'\'\'\n\ndef generate_homepage'
content = content.replace(old2, new2, 1)

# Fix template 3: homepage
old3 = '    <script src="/assets/main.js"></script>\n</body>\n</html>\'\'\'\n\ndef generate_legal_pages'
new3 = '    ' + ts + '\n    <script src="/assets/main.js"></script>\n</body>\n</html>\'\'\'\n\ndef generate_legal_pages'
content = content.replace(old3, new3, 1)

with open('build_site.py', 'w') as f:
    f.write(content)

print('Done')