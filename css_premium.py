with open("e:/KOUKI SHOP/style.css", "a", encoding="utf-8") as f:
    f.write("""

/* ==============================================
   ULTRA-PREMIUM MARKETPLACE — SaaS UPGRADE
   ============================================== */

/* ---- Section Label Bar ---- */
.section-label-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
    margin-bottom: 10px;
}
.section-label-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--secondary);
    box-shadow: 0 0 10px var(--secondary);
    animation: dotPulse 2s infinite;
}
@keyframes dotPulse {
    0%,100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.6); opacity: 0.5; }
}

/* ---- Category Tabs Overhaul ---- */
.cat-tab {
    padding: 9px 20px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    color: var(--text-muted);
    cursor: pointer;
    font-weight: 600;
    font-size: 0.92rem;
    letter-spacing: 0.3px;
    transition: all 0.25s ease;
    white-space: nowrap;
}
.cat-tab:hover {
    background: rgba(6,182,212,0.12);
    border-color: rgba(6,182,212,0.3);
    color: var(--text);
}
.cat-tab.active {
    background: var(--secondary) !important;
    color: #fff !important;
    border-color: var(--secondary) !important;
    box-shadow: 0 0 20px rgba(6,182,212,0.4);
}

/* ---- Skeleton Loader ---- */
@keyframes shimmer {
    0% { background-position: -600px 0; }
    100% { background-position: 600px 0; }
}
.skeleton-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 28px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
}
.skeleton-icon {
    width: 72px; height: 72px;
    border-radius: 16px;
    background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.12) 50%, rgba(255,255,255,0.05) 75%);
    background-size: 600px 100%;
    animation: shimmer 1.5s infinite linear;
}
.skeleton-line {
    height: 12px;
    border-radius: 8px;
    background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.04) 75%);
    background-size: 600px 100%;
    animation: shimmer 1.5s infinite linear;
    align-self: stretch;
}
.skeleton-line.w70 { width: 70%; align-self: center; }
.skeleton-line.w50 { width: 50%; align-self: center; }
.skeleton-line.w60 { width: 60%; align-self: center; }

/* ---- Digi Card — Premium Remaster ---- */
.digi-card {
    position: relative;
    background: rgba(10, 15, 30, 0.6);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 28px 20px 22px;
    text-align: center;
    overflow: visible;
    backdrop-filter: blur(20px);
    transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275),
                box-shadow 0.35s ease,
                border-color 0.35s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    cursor: default;
}

/* Animated gradient border on hover */
.digi-card::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: 21px;
    padding: 1px;
    background: conic-gradient(from var(--angle, 0deg), transparent 70%, var(--brand-glow, rgba(6,182,212,0.8)) 80%, transparent 90%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.4s ease;
    animation: rotateBorder 3s linear infinite;
    pointer-events: none;
}
.digi-card:hover::before {
    opacity: 1;
}
@property --angle {
    syntax: '<angle>';
    initial-value: 0deg;
    inherits: false;
}
@keyframes rotateBorder {
    to { --angle: 360deg; }
}

.digi-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 25px 50px rgba(0,0,0,0.5), 0 0 35px var(--brand-glow, rgba(6,182,212,0.2));
    border-color: transparent;
    z-index: 2;
}

/* ---- Brand Icon ---- */
.brand-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 80px !important;
    height: 80px !important;
    border-radius: 18px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    margin-bottom: 6px;
}
.brand-icon img {
    width: 52px !important;
    height: 52px !important;
    object-fit: contain !important;
    transition: transform 0.4s ease, filter 0.4s ease;
    filter: drop-shadow(0 0 0px transparent);
}
.digi-card:hover .brand-icon {
    transform: translateY(-4px) scale(1.08);
    border-color: var(--brand-glow, rgba(6,182,212,0.3));
    background: rgba(255,255,255,0.07);
}
.digi-card:hover .brand-icon img {
    filter: drop-shadow(0 0 10px var(--brand-glow, rgba(6,182,212,0.6)));
}

/* ---- Card Badge ---- */
.card-badge {
    position: absolute;
    top: -10px;
    right: -10px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 800;
    z-index: 4;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    animation: badgePop 2.5s ease-in-out infinite;
}
.card-badge.hot {
    background: linear-gradient(135deg, #FF416C, #FF4B2B);
    color: #fff;
    box-shadow: 0 4px 15px rgba(255,65,108,0.4);
}
.card-badge.new {
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    color: #fff;
    box-shadow: 0 4px 15px rgba(6,182,212,0.4);
}
.card-badge.limited {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: #fff;
    box-shadow: 0 4px 15px rgba(245,158,11,0.4);
}
@keyframes badgePop {
    0%,100% { transform: scale(1) rotate(-1deg); }
    50% { transform: scale(1.1) rotate(1deg); }
}

/* ---- Digi Glow (Background effect) ---- */
.digi-glow {
    position: absolute;
    top: -30px; left: 50%;
    transform: translateX(-50%);
    width: 120px; height: 120px;
    border-radius: 50%;
    filter: blur(45px);
    z-index: 0;
    opacity: 0.2;
    transition: opacity 0.4s ease, transform 0.4s ease;
    pointer-events: none;
}
.digi-card:hover .digi-glow {
    opacity: 0.55;
    transform: translateX(-50%) scale(1.3);
}

/* ---- Card text ---- */
.digi-card h3 {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--text-main);
    margin: 0;
    z-index: 1;
}
.digi-card p {
    font-size: 0.88rem;
    color: var(--text-muted);
    margin: 0;
    line-height: 1.5;
    z-index: 1;
}
.digi-price {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--secondary);
    padding: 4px 14px;
    background: rgba(6,182,212,0.08);
    border-radius: 8px;
    border: 1px solid rgba(6,182,212,0.2);
    z-index: 1;
}

/* ---- Card Actions ---- */
.digi-actions {
    display: flex;
    gap: 8px;
    width: 100%;
    z-index: 1;
    margin-top: 4px;
}
.digi-actions .btn {
    flex: 1;
    padding: 10px 8px;
    border-radius: 10px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--text);
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}
.digi-actions .btn::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(255,255,255,0.3), transparent 70%);
    opacity: 0;
    transform: scale(0);
    transition: opacity 0.3s, transform 0.3s;
}
.digi-actions .btn:active::after {
    opacity: 1;
    transform: scale(2.5);
    transition: 0s;
}
.digi-actions .btn:hover {
    background: rgba(255,255,255,0.1);
    transform: translateY(-2px);
    border-color: rgba(255,255,255,0.2);
}

/* ---- Premium Tooltip ---- */
.digi-tooltip {
    position: absolute;
    bottom: calc(100% + 12px);
    left: 50%;
    transform: translateX(-50%) translateY(5px);
    background: rgba(10,15,30,0.97);
    border: 1px solid rgba(6,182,212,0.3);
    color: var(--text);
    font-size: 0.82rem;
    padding: 10px 14px;
    border-radius: 12px;
    white-space: nowrap;
    backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    z-index: 100;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.25s ease, transform 0.25s ease;
    direction: rtl;
    text-align: center;
    max-width: 280px;
    white-space: normal;
}
.digi-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: rgba(6,182,212,0.3);
}
.digi-card:hover .digi-tooltip {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

/* ---- Search Bar Neon Focus ---- */
.digital-search-container:focus-within {
    border-color: var(--secondary);
    box-shadow: 0 0 0 3px rgba(6,182,212,0.15), 0 0 25px rgba(6,182,212,0.1);
}

/* ---- Mobile ---- */
@media (max-width: 600px) {
    .digi-card { padding: 22px 14px 18px; }
    .brand-icon { width: 68px !important; height: 68px !important; }
    .brand-icon img { width: 44px !important; height: 44px !important; }
    .digi-tooltip { display: none; }
}
""")
print("CSS written successfully!")
