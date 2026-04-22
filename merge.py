import re

with open('index_new_theme_full.html', 'r', encoding='utf-8') as f:
    new_html = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    old_html = f.read()

# 1. Get CSS from new
new_css_match = re.search(r'<style>(.*?)</style>', new_html, re.DOTALL)
new_css = new_css_match.group(0) if new_css_match else ""

# 2. Get Nav from new
new_nav_match = re.search(r'<nav id="nav">.*?</nav>', new_html, re.DOTALL)
new_nav = new_nav_match.group(0) if new_nav_match else ""

# 3. Get Hero from new
new_hero_match = re.search(r'<section class="hero" id="analyzer">.*?</section>', new_html, re.DOTALL)
new_hero = new_hero_match.group(0) if new_hero_match else ""

# 4. Get Reviews from new
new_reviews_match = re.search(r'<section class="sec" id="reviews">.*?</section>', new_html, re.DOTALL)
new_reviews = new_reviews_match.group(0) if new_reviews_match else ""

# 5. Get JS from new
new_js_match = re.search(r'<script>(.*?)</script>', new_html, re.DOTALL)
new_js = new_js_match.group(0) if new_js_match else ""

# Get animated background elements from new
new_bg_match = re.search(r'<div id="cur"></div>.*?<div class="grid"></div>', new_html, re.DOTALL)
new_bg = new_bg_match.group(0) if new_bg_match else ""

# Now modification inside old_html

# A: Inject CSS just before </head>
old_html = old_html.replace('</head>', f'{new_css}\n</head>')

# B: Replace old <header> and <section class="hero">
old_header_pat = r'<header class="navbar container">.*?</header>'
old_hero_pat = r'<main class="container">\s*<!-- Hero Section -->\s*<section class="hero">.*?</section>'

# Actually, finding these old sections by string matching or regex is better done manually if regex fails.
# The user's old header:
old_html = re.sub(r'<header class="navbar container">.*?</header>', new_nav, old_html, flags=re.DOTALL)

# The user's old hero section:
# Note: old html has <main class="container"> right before Hero Section
old_hero_regex = r'<!-- Hero Section -->\s*<section class="hero">.*?</section>'
# We also want to replace the stores section if it was part of the old hero, but we see it ends at </section>
# Let's replace the Hero
hero_replacement = '<!-- Hero Section -->\n' + new_bg + '\n' + new_hero
old_html = re.sub(old_hero_regex, hero_replacement, old_html, flags=re.DOTALL)

# C: Inject Reviews section before <section class="about-us-section ... (or before Footer)
# If we just insert it before <footer
old_html = old_html.replace('<footer', f'{new_reviews}\n<footer')

# D: Inject JS
old_html = old_html.replace('</body>', f'{new_js}\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(old_html)
print("Done merging!")
