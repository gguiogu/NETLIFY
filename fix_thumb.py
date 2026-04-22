import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Canva - use a direct SVG that definitely works
html = html.replace(
    'src="https://upload.wikimedia.org/wikipedia/commons/0/08/Canva_icon_2021.svg"',
    'src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Canva_icon_2021.svg/240px-Canva_icon_2021.svg.png"'
)

# CapCut — use a working direct URL
html = html.replace(
    'src="https://upload.wikimedia.org/wikipedia/commons/3/34/CapCut_Logo.svg"',
    'src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/CapCut_Logo.svg/240px-CapCut_Logo.svg.png"'
)

# Microsoft 365 — PNG thumb version is more reliable
html = html.replace(
    'src="https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg"',
    'src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg/240px-Microsoft_Office_logo_%282019%E2%80%93present%29.svg.png"'
)

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done! Switched to Wikipedia thumbnail PNG versions for faster loading.")
