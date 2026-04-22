import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FIXES = {
    # Canva — Wikipedia official SVG
    'https://upload.wikimedia.org/wikipedia/commons/0/08/Canva_icon_2021.svg':
        'https://cdn.simpleicons.org/canva/00C4CC',

    # Adobe Creative Cloud — Wikipedia official SVG
    'https://cdn.simpleicons.org/adobecreativecloud/FF0000':
        'https://cdn.simpleicons.org/adobecreativecloud/FF0000',

    # CapCut — slug might be 'capcut' but with black color it blends in dark bg
    # Use white version
    'https://cdn.simpleicons.org/capcut/000000':
        'https://cdn.simpleicons.org/capcut/ffffff',

    # Xbox — slug 'xbox' 
    'https://cdn.simpleicons.org/xbox/107C10':
        'https://cdn.simpleicons.org/xbox/107C10',

    # Microsoft 365 — use Wikipedia
    'https://upload.wikimedia.org/wikipedia/commons/5/5b/Microsoft_Office_365_logo_and_wordmark_%282013-2019%29.png':
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg/800px-Microsoft_Office_logo_%282019%E2%80%93present%29.svg.png',
}

with open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = 0
for old, new in FIXES.items():
    if old in html and old != new:
        html = html.replace(old, new)
        changes += 1
        print(f"Fixed: {old[:60]}...")

# Also ensure all brand-icon imgs have proper sizes 52x52 set
# and add onerror fallbacks for any remaining icons
additional = [
    # Adobe CC fallback
    ('alt="Adobe CC" loading="lazy">',
     'alt="Adobe CC" loading="lazy" onerror="this.src=\'https://upload.wikimedia.org/wikipedia/commons/4/4c/Adobe_Creative_Cloud_rainbow_icon.svg\'">'),
    # Xbox fallback
    ('alt="Xbox" loading="lazy">',
     'alt="Xbox" loading="lazy" onerror="this.src=\'https://upload.wikimedia.org/wikipedia/commons/f/f9/Xbox_one_logo.svg\'">'),
    # Canva fallback
    ('alt="Canva" loading="lazy">',
     'alt="Canva" loading="lazy" onerror="this.src=\'https://cdn.simpleicons.org/canva/00C4CC\'">'),
    # CapCut fallback
    ('alt="CapCut" loading="lazy">',
     'alt="CapCut" loading="lazy" onerror="this.src=\'https://upload.wikimedia.org/wikipedia/commons/3/34/CapCut_Logo.svg\'">'),
]

for old, new in additional:
    if old in html and old != new:
        html = html.replace(old, new)
        changes += 1
        print(f"Added fallback for: {old[:40]}...")

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nDone! {changes} total fixes applied.")
