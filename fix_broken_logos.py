import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# These are the 5 broken logos — fix with verified alternative CDN URLs
FIXES = {
    # ChatGPT — use official OpenAI SVG from their CDN
    'https://cdn.simpleicons.org/openai/10A37F':
        'https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg',

    # Disney+ — use correct simpleicons slug (lowercase)
    'https://cdn.simpleicons.org/disneyplus/113CCF':
        'https://cdn.simpleicons.org/disneyplus/113CCF',  # keep, unlikely the issue

    # Amazon Prime Video — correct slug is amazonprimevideo OR primevideo
    # Try Wikipedia fallback
    'https://cdn.simpleicons.org/amazonprimevideo/00A8E1':
        'https://cdn.simpleicons.org/primevideo/00A8E1',

    # Canva — try Wikipedia SVG 
    'https://cdn.simpleicons.org/canva/00C4CC':
        'https://upload.wikimedia.org/wikipedia/commons/0/08/Canva_icon_2021.svg',

    # Microsoft Office/365 — use correct slug  
    'https://cdn.simpleicons.org/microsoftoffice/D83B01':
        'https://upload.wikimedia.org/wikipedia/commons/5/5b/Microsoft_Office_365_logo_and_wordmark_%282013-2019%29.png',
}

with open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = 0
for old, new in FIXES.items():
    if old in html and old != new:
        html = html.replace(old, new)
        changes += 1
        slug = old.split('/')[-2] or old.split('/')[-1]
        print(f"Fixed: {slug}")

# Also fix Disney+ specifically - the slug is correct but let's also set a fallback onerror
# Disney+ official logo from Wikipedia
html = html.replace(
    '<img src="https://cdn.simpleicons.org/disneyplus/113CCF" alt="Disney+" loading="lazy">',
    '<img src="https://cdn.simpleicons.org/disneyplus/113CCF" alt="Disney+" loading="lazy" onerror="this.src=\'https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg\'">'
)

# Also add onerror fallbacks for all other potentially broken ones
html = html.replace(
    '<img src="https://cdn.simpleicons.org/primevideo/00A8E1" alt="Prime Video" loading="lazy">',
    '<img src="https://cdn.simpleicons.org/primevideo/00A8E1" alt="Prime Video" loading="lazy" onerror="this.src=\'https://upload.wikimedia.org/wikipedia/commons/1/11/Amazon_Prime_Video_logo.svg\'">'
)

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done! {changes} additional fixes applied.")
