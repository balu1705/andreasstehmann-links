with open('/opt/data/andreasstehmann-links/build_site.py', 'r') as f:
    content = f.read()

# The tracking script with proper 4-space base indentation for template
ts = (
    '    <!-- GA4 Affiliate Click Tracking -->\n'
    '    <script>\n'
    '        document.addEventListener("DOMContentLoaded", function() {\n'
    '            document.querySelectorAll("a.product-link[data-asin]").forEach(function(link) {\n'
    '                link.addEventListener("click", function(e) {\n'
    '                    var asin = this.getAttribute("data-asin");\n'
    '                    var niche = this.getAttribute("data-niche");\n'
    '                    var position = this.getAttribute("data-position");\n'
    '                    var price = this.getAttribute("data-price");\n'
    '                    if (asin && typeof gtag === "function") {\n'
    '                        gtag("event", "affiliate_click", {\n'
    '                            "asin": asin,\n'
    '                            "niche": niche || "",\n'
    '                            "position": parseInt(position) || 0,\n'
    '                            "price": parseFloat(price) || 0,\n'
    '                            "currency": "EUR",\n'
    '                            "affiliate_tag": "balu17051-21",\n'
    '                            "link_domain": "amazon.de"\n'
    '                        });\n'
    '                    }\n'
    '                });\n'
    '            });\n'
    '        });\n'
    '    </script>'
)

# Remove any existing broken tracking scripts first
import re
pattern = r'<!-- GA4 Affiliate Click Tracking -->\s*<script>.*?</script>\s*'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# The current pattern in all three templates:
#     </footer>
#         <script src="/assets/main.js"></script>
# </body>
# </html>'''

# Fix template 1: niche page (before generate_category_page)
old1 = (
    '    </footer>\n'
    '        <script src="/assets/main.js"></script>\n'
    '</body>\n'
    '</html>\'\'\'\n'
    '\n'
    'def generate_category_page'
)
new1 = (
    '    </footer>\n'
    + ts + '\n'
    '        <script src="/assets/main.js"></script>\n'
    '</body>\n'
    '</html>\'\'\'\n'
    '\n'
    'def generate_category_page'
)
content = content.replace(old1, new1, 1)

# Fix template 2: category page (before generate_homepage)
old2 = (
    '    </footer>\n'
    '        <script src="/assets/main.js"></script>\n'
    '</body>\n'
    '</html>\'\'\'\n'
    '\n'
    'def generate_homepage'
)
new2 = (
    '    </footer>\n'
    + ts + '\n'
    '        <script src="/assets/main.js"></script>\n'
    '</body>\n'
    '</html>\'\'\'\n'
    '\n'
    'def generate_homepage'
)
content = content.replace(old2, new2, 1)

# Fix template 3: homepage (before generate_legal_pages)
old3 = (
    '    </footer>\n'
    '        <script src="/assets/main.js"></script>\n'
    '</body>\n'
    '</html>\'\'\'\n'
    '\n'
    'def generate_legal_pages'
)
new3 = (
    '    </footer>\n'
    + ts + '\n'
    '        <script src="/assets/main.js"></script>\n'
    '</body>\n'
    '</html>\'\'\'\n'
    '\n'
    'def generate_legal_pages'
)
content = content.replace(old3, new3, 1)

with open('/opt/data/andreasstehmann-links/build_site.py', 'w') as f:
    f.write(content)

print("Done - fixed with proper indentation")