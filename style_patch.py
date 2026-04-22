with open("e:/KOUKI SHOP/style.css", "a", encoding="utf-8") as f:
    f.write("""
/* =========================================
   SaaS MARKETPLACE ADDITIONS
   ========================================= */

/* Hide scrollbar for category tabs */
.category-tabs-wrapper::-webkit-scrollbar {
    display: none;
}
.category-tabs-wrapper {
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;  /* Firefox */
}

/* Tab Hover & Active Styling */
.cat-tab:hover {
    background: rgba(255,255,255,0.1) !important;
    transform: translateY(-2px);
}
.cat-tab.active {
    box-shadow: 0 5px 15px rgba(6, 182, 212, 0.4);
    border-color: var(--secondary) !important;
}

/* Search Bar Focus */
.digital-search-container:focus-within {
    border-color: var(--secondary);
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.2);
}

/* Cards Animation */
@keyframes scaleUp {
    0% { transform: scale(0.9); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

/* Enhanced Card Hover */
.digi-card:hover {
    transform: scale(1.04) translateY(-8px) !important;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(6, 182, 212, 0.15) !important;
    border-color: rgba(6, 182, 212, 0.3) !important;
}

/* Animated Badges */
.badge-popular, .badge-discount {
    animation: pulseBadge 2.5s infinite ease-in-out;
}

@keyframes pulseBadge {
    0% { transform: scale(1); }
    50% { transform: scale(1.08); }
    100% { transform: scale(1); }
}

/* Button Micro-interactions */
.digi-actions .btn-digi {
    transition: all 0.3s ease;
}
.digi-actions .btn-digi:hover {
    filter: brightness(1.25);
    transform: translateY(-3px);
    box-shadow: 0 5px 15px currentColor;
}
""")
print("CSS injected successfully")
