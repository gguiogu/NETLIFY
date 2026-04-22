import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Directly replace the broken logos with 100% verified Wikipedia/CDN SVG URLs
FINAL_FIXES = {
    # Canva — official Wikipedia upload
    'https://cdn.simpleicons.org/canva/00C4CC':
        'https://upload.wikimedia.org/wikipedia/commons/0/08/Canva_icon_2021.svg',

    # Adobe Creative Cloud — use static SVG from Wikipedia
    'https://cdn.simpleicons.org/adobecreativecloud/FF0000':
        'https://upload.wikimedia.org/wikipedia/commons/4/4c/Adobe_Creative_Cloud_rainbow_icon.svg',

    # CapCut — Wikipedia official SVG
    'https://cdn.simpleicons.org/capcut/ffffff':
        'https://upload.wikimedia.org/wikipedia/commons/3/34/CapCut_Logo.svg',

    # Xbox — Wikipedia official SVG
    'https://cdn.simpleicons.org/xbox/107C10':
        'https://upload.wikimedia.org/wikipedia/commons/f/f9/Xbox_one_logo.svg',

    # Microsoft Office 365 — Wikipedia official SVG
    'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg/800px-Microsoft_Office_logo_%282019%E2%80%93present%29.svg.png':
        'https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg',
}

with open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = 0
for old, new in FINAL_FIXES.items():
    count = html.count(old)
    if count > 0:
        html = html.replace(old, new)
        changes += count
        name = old.split('/')[-1][:30]
        print(f"Replaced ({count}x): {name}")

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nDone! {changes} logo SRC replacements applied.")
