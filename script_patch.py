with open("e:/KOUKI SHOP/script.js", "a", encoding="utf-8") as f:
    f.write("""
// ---------------------------------------------------
// Digital Marketplace SaaS Logic
// ---------------------------------------------------

function filterDigitalMarket() {
    const input = document.getElementById('digitalSearch').value.toLowerCase();
    const cards = document.querySelectorAll('#marketGrid .digi-card');
    
    // Auto-reset category to "All" when searching
    if (input.trim() !== '') {
        document.querySelectorAll('.cat-tab').forEach(tab => {
            tab.style.background = 'rgba(255,255,255,0.05)';
            tab.classList.remove('active');
        });
        const allTab = document.querySelector('.cat-tab[onclick*="all"]');
        if(allTab) {
            allTab.classList.add('active');
            allTab.style.background = 'var(--secondary)';
        }
    }
    
    cards.forEach(card => {
        const title = card.getAttribute('data-title').toLowerCase();
        const desc = card.querySelector('p').textContent.toLowerCase();
        
        if (title.includes(input) || desc.includes(input)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

function selectCategory(category, buttonElement) {
    // Clear search input
    const searchInput = document.getElementById('digitalSearch');
    if(searchInput) searchInput.value = '';
    
    // Update Active Tab Styling
    document.querySelectorAll('.cat-tab').forEach(tab => {
        tab.style.background = 'rgba(255,255,255,0.05)';
        tab.classList.remove('active');
    });
    buttonElement.style.background = 'var(--secondary)';
    buttonElement.classList.add('active');
    
    // Filter Cards
    const cards = document.querySelectorAll('#marketGrid .digi-card');
    cards.forEach(card => {
        if (category === 'all') {
            card.style.display = 'flex';
            card.style.animation = 'none';
            card.offsetHeight; /* trigger reflow */
            card.style.animation = 'scaleUp 0.4s ease-out forwards';
        } else {
            if (card.getAttribute('data-category') === category) {
                card.style.display = 'flex';
                card.style.animation = 'none';
                card.offsetHeight; /* trigger reflow */
                card.style.animation = 'scaleUp 0.4s ease-out forwards';
            } else {
                card.style.display = 'none';
            }
        }
    });
}
""")
print("Logic applied successfully")
