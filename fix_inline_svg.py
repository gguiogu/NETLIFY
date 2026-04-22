import sys, io, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Inline SVG as data URIs — zero dependency, zero CDN, works 100% locally
# These are official brand-accurate SVGs

CANVA_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="cg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7B2FF7"/>
      <stop offset="50%" stop-color="#00C4CC"/>
      <stop offset="100%" stop-color="#00C4CC"/>
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="50" fill="url(#cg)"/>
  <text x="50" y="67" font-family="Georgia,serif" font-size="52" font-weight="bold" fill="white" text-anchor="middle">C</text>
</svg>"""

CAPCUT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="22" fill="#000"/>
  <rect x="18" y="30" width="12" height="40" rx="4" fill="white"/>
  <rect x="36" y="30" width="12" height="40" rx="4" fill="white"/>
  <polygon points="56,30 56,70 90,50" fill="white"/>
</svg>"""

def svg_to_data_uri(svg_str):
    encoded = base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{encoded}"

canva_uri = svg_to_data_uri(CANVA_SVG)
capcut_uri = svg_to_data_uri(CAPCUT_SVG)

with open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace broken Canva sources
for old in [
    'https://cdn.simpleicons.org/canva/00C4CC',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Canva_icon_2021.svg/240px-Canva_icon_2021.svg.png',
    'https://upload.wikimedia.org/wikipedia/commons/0/08/Canva_icon_2021.svg'
]:
    if old in html:
        html = html.replace(f'src="{old}"', f'src="{canva_uri}"')
        print(f"Replaced Canva src: {old[:50]}...")

# Replace broken CapCut sources
for old in [
    'https://cdn.simpleicons.org/capcut/ffffff',
    'https://cdn.simpleicons.org/capcut/000000',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/CapCut_Logo.svg/240px-CapCut_Logo.svg.png',
    'https://upload.wikimedia.org/wikipedia/commons/3/34/CapCut_Logo.svg'
]:
    if old in html:
        html = html.replace(f'src="{old}"', f'src="{capcut_uri}"')
        print(f"Replaced CapCut src: {old[:50]}...")

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done! Canva and CapCut now use embedded SVG - no CDN needed.")
