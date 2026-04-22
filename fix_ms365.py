import sys, io, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Microsoft Office 365 icon — inline SVG (official 4-colored grid)
MS365_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="5" y="5" width="42" height="42" rx="4" fill="#F25022"/>
  <rect x="53" y="5" width="42" height="42" rx="4" fill="#7FBA00"/>
  <rect x="5" y="53" width="42" height="42" rx="4" fill="#00A4EF"/>
  <rect x="53" y="53" width="42" height="42" rx="4" fill="#FFB900"/>
</svg>"""

def svg_to_data_uri(svg_str):
    encoded = base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{encoded}"

ms365_uri = svg_to_data_uri(MS365_SVG)

with open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8") as f:
    html = f.read()

broken_ms = [
    'https://cdn.simpleicons.org/microsoftoffice/D83B01',
    'https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg',
    'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg/240px-Microsoft_Office_logo_%282019%E2%80%93present%29.svg.png',
    'https://upload.wikimedia.org/wikipedia/commons/5/5b/Microsoft_Office_365_logo_and_wordmark_%282013-2019%29.png',
]
for old in broken_ms:
    if old in html:
        html = html.replace(f'src="{old}"', f'src="{ms365_uri}"')
        print(f"Replaced Microsoft: {old[:55]}...")

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
