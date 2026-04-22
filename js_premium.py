js_code = """
// ==============================================
// PREMIUM MARKETPLACE — SaaS Skeleton + Logic
// ==============================================

function initMarketplace() {
    const skeletonGrid = document.getElementById('skeletonGrid');
    const marketGrid = document.getElementById('marketGrid');
    if (!skeletonGrid || !marketGrid) return;

    // Show skeleton for 900ms, then reveal real cards with stagger animation
    setTimeout(() => {
        skeletonGrid.style.transition = 'opacity 0.4s ease';
        skeletonGrid.style.opacity = '0';
        setTimeout(() => {
            skeletonGrid.style.display = 'none';
            marketGrid.style.display = 'grid';
            // Stagger each card entrance
            const cards = marketGrid.querySelectorAll('.digi-card');
            cards.forEach((card, i) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(24px) scale(0.97)';
                card.style.transition = `opacity 0.4s ease ${i * 0.05}s, transform 0.4s ease ${i * 0.05}s`;
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0) scale(1)';
                }, 50);
            });
        }, 400);
    }, 900);
}

// Run on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMarketplace);
} else {
    initMarketplace();
}

function filterDigitalMarket() {
    const input = document.getElementById('digitalSearch');
    if (!input) return;
    const query = input.value.toLowerCase().trim();
    const cards = document.querySelectorAll('#marketGrid .digi-card');

    if (query !== '') {
        // Reset tabs
        document.querySelectorAll('.cat-tab').forEach(t => {
            t.classList.remove('active');
            t.style.background = '';
        });
        const allTab = document.querySelector('.cat-tab:first-child');
        if (allTab) allTab.classList.add('active');
    }

    let visible = 0;
    cards.forEach(card => {
        const title = (card.getAttribute('data-title') || '').toLowerCase();
        const desc = card.querySelector('p') ? card.querySelector('p').textContent.toLowerCase() : '';
        const headings = card.querySelectorAll('h3');
        const h3text = headings.length ? headings[0].textContent.toLowerCase() : '';
        const match = query === '' || title.includes(query) || desc.includes(query) || h3text.includes(query);
        card.style.display = match ? 'flex' : 'none';
        if (match) visible++;
    });
}

function selectCategory(category, buttonElement) {
    const searchInput = document.getElementById('digitalSearch');
    if (searchInput) searchInput.value = '';

    document.querySelectorAll('.cat-tab').forEach(tab => {
        tab.classList.remove('active');
        tab.style.background = '';
    });
    buttonElement.classList.add('active');

    const cards = document.querySelectorAll('#marketGrid .digi-card');
    let delay = 0;
    cards.forEach(card => {
        const matches = category === 'all' || card.getAttribute('data-category') === category;
        if (matches) {
            card.style.display = 'flex';
            card.style.animation = 'none';
            void card.offsetHeight;
            card.style.animation = `cardReveal 0.4s ease ${delay}s forwards`;
            card.style.opacity = '0';
            delay += 0.04;
        } else {
            card.style.display = 'none';
        }
    });
}
"""

with open("e:/KOUKI SHOP/script.js", "r", encoding="utf-8") as f:
    current = f.read()

# Remove old selectCategory and filterDigitalMarket if present (append replaces)
# We'll just append our new version (the old ones will be shadowed)
with open("e:/KOUKI SHOP/script.js", "a", encoding="utf-8") as f:
    f.write("\n" + js_code)

print("JS written successfully!")
