with open("e:/KOUKI SHOP/style.css", "a", encoding="utf-8") as f:
    f.write("""
/* ---- Card Reveal Keyframe (used by JS stagger) ---- */
@keyframes cardReveal {
    from { opacity: 0; transform: translateY(20px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ---- Grid display fix when JS reveals it ---- */
#marketGrid[style*="display: grid"] {
    animation: gridFadeIn 0.5s ease forwards;
}
@keyframes gridFadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
""")
print("Keyframes added!")
