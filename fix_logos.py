import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LOGO_MAP = {
    # AI
    'https://cdn.simpleicons.org/openai/10a37f':
        'https://cdn.simpleicons.org/openai/10A37F',
    'https://cdn.simpleicons.org/perplexity/20BFFF':
        'https://cdn.simpleicons.org/perplexity/1FB8CD',
    'https://cdn.simpleicons.org/anthropic/d97757':
        'https://cdn.simpleicons.org/anthropic/D97757',
    # Entertainment
    'https://cdn.simpleicons.org/disneyplus/ffffff':
        'https://cdn.simpleicons.org/disneyplus/113CCF',
    'https://cdn.simpleicons.org/primevideo/00A8E1':
        'https://cdn.simpleicons.org/amazonprimevideo/00A8E1',
    # Music
    'https://cdn.simpleicons.org/applemusic/FA243C':
        'https://cdn.simpleicons.org/applemusic/FC3C44',
    # Design
    'https://cdn.simpleicons.org/capcut/ffffff':
        'https://cdn.simpleicons.org/capcut/000000',
    'https://cdn.simpleicons.org/envato/52C41A':
        'https://cdn.simpleicons.org/envato/81B441',
    # Productivity
    'https://cdn.simpleicons.org/microsoft365/D83B01':
        'https://cdn.simpleicons.org/microsoftoffice/D83B01',
    # Gaming
    'https://cdn.simpleicons.org/playstation/00439C':
        'https://cdn.simpleicons.org/playstation/003791',
    'https://cdn.simpleicons.org/steam/1a9fff':
        'https://cdn.simpleicons.org/steam/ffffff',
    # Social
    'https://cdn.simpleicons.org/meta/0064F2':
        'https://cdn.simpleicons.org/meta/0082FB',
    'https://cdn.simpleicons.org/tiktok/ffffff':
        'https://cdn.simpleicons.org/tiktok/010101',
}

with open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = 0
for old, new in LOGO_MAP.items():
    if old in html and old != new:
        html = html.replace(old, new)
        changes += 1
        print(f"Fixed: {old.split('/')[-2]}")

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nDone! {changes} logo URLs corrected.")
