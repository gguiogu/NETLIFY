import re

def apply_saas_polish():
    # --- 1. UPDATE CSS ---
    with open('style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Apply background gradients
    bg_pattern = r'body\s*\{[^}]*background-color:\s*var\(--bg-dark\);'
    new_bg = '''body {
    background: radial-gradient(circle at 20% 20%, rgba(79,70,229,0.15), transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(34,211,238,0.12), transparent 40%),
                var(--bg-dark);'''
    css = re.sub(bg_pattern, new_bg, css, count=1)

    # Apply glass card styling to .box-glass
    box_glass_pattern = r'\.box-glass\s*\{[^}]*\}'
    new_box_glass = '''.box-glass {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    transition: all 0.3s ease;
}'''
    css = re.sub(box_glass_pattern, new_box_glass, css)

    box_glass_hover_pattern = r'\.box-glass:hover\s*\{[^}]*\}'
    new_box_glass_hover = '''.box-glass:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4), 0 0 20px rgba(79,70,229,0.15);
}'''
    css = re.sub(box_glass_hover_pattern, new_box_glass_hover, css)

    # Apply neon button styling to .btn-primary
    btn_primary_pattern = r'\.btn-primary\s*\{[^}]*\}'
    new_btn_primary = '''.btn-primary {
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border: none;
    color: white;
    box-shadow: 0 0 10px rgba(79,70,229,0.4), 0 0 20px rgba(34,211,238,0.2);
    transition: all 0.25s ease;
}'''
    css = re.sub(btn_primary_pattern, new_btn_primary, css)

    btn_primary_hover_pattern = r'\.btn-primary:hover\s*\{[^}]*\}'
    new_btn_primary_hover = '''.btn-primary:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(79,70,229,0.6), 0 0 40px rgba(34,211,238,0.4);
}
.btn-primary:active {
    transform: scale(0.96);
}'''
    css = re.sub(btn_primary_hover_pattern, new_btn_primary_hover, css)

    # Replace digi-card hover and properties to match Vercel glow
    digi_card_hover_pattern = r'\.digi-card:hover\s*\{[^}]*\}'
    css = re.sub(digi_card_hover_pattern, '.digi-card:hover { transform: translateY(-6px); box-shadow: 0 10px 40px rgba(0,0,0,0.4), 0 0 20px rgba(79,70,229,0.15); }', css)

    # Game card neon boost
    game_card_pattern = r'\.game-card\s*\{'
    new_game_card = '''.game-card {
    border: 1px solid rgba(34,211,238,0.3);
    box-shadow: 0 0 15px rgba(34,211,238,0.2);
'''
    css = css.replace('.game-card {', new_game_card)
    
    # Add extra classes from user spec
    extra_css = """
/* Glow Border */
.glow-border {
    position: relative;
}
.glow-border::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    background: linear-gradient(135deg, #4F46E5, #22D3EE);
    opacity: 0;
    transition: opacity 0.3s;
    z-index: -1;
}
.glow-border:hover::before {
    opacity: 0.6;
    filter: blur(8px);
}

/* Loading Skeleton */
.skeleton {
    background: linear-gradient(
        90deg,
        rgba(255,255,255,0.05) 25%,
        rgba(255,255,255,0.1) 37%,
        rgba(255,255,255,0.05) 63%
    );
    background-size: 400% 100%;
    animation: shimmer 1.4s infinite;
}
@keyframes shimmer {
    0% { background-position: 100% 0 }
    100% { background-position: -100% 0 }
}

/* Floating / Depth Effect */
.float {
    animation: float 6s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

/* Success Animation */
.success {
    animation: pop 0.4s ease;
}
@keyframes pop {
    0% { transform: scale(0.8); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}
"""
    css += extra_css

    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css)

    # --- 2. UPDATE JS ---
    with open('script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # Rewrite showView function for SPA transition
    old_showView = r'function showView\(viewId\) \{.*?\n\}'
    # Actually the function might span multiple lines, let's use a robust regex or replacement
    js_router_pattern = re.compile(r'function showView\(viewId\)\s*\{[\s\S]*?(?=\n\}|//)\n\}')
    
    new_showView = """function showView(viewId) {
    const app = document.querySelector('.views-wrapper');
    if (!app) return;
    
    // Fade out
    app.style.transition = "all 0.15s ease-in-out";
    app.style.opacity = 0;
    app.style.transform = "translateY(10px)";
    
    setTimeout(() => {
        // Hide all views
        document.querySelectorAll('.view').forEach(view => {
            view.classList.remove('active');
            view.classList.add('hidden');
        });
        
        // Show target view
        const target = document.getElementById('view-' + viewId);
        if (target) {
            target.classList.remove('hidden');
            target.classList.add('active');
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
        
        // Fade in
        app.style.opacity = 1;
        app.style.transform = "translateY(0)";
    }, 180);
}"""
    
    # We'll just replace the router section
    if "function showView(viewId)" in js:
        # manual replace
        start = js.find("function showView(viewId)")
        end = js.find("}", start)
        if "document.getElementById('view-' + viewId)" in js[start:end+200]:
            end2 = js.find("}", js.find("}", start) + 1)
            # just replacing the whole block is tricky, we'll append and redefine or simple replace
            # Let's replace the first occurence.
            pass
    
    # Simpler regex replacement for the router we wrote earlier
    js = re.sub(r'function showView\(viewId\)\s*\{.*?\}\s*\}', new_showView, js, flags=re.DOTALL)

    # Add Cursor Glow and logic
    extra_js = """
// ==========================================
// Cursor Glow (Premium Feel)
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    const glow = document.createElement("div");
    glow.style.position = "fixed";
    glow.style.width = "200px";
    glow.style.height = "200px";
    glow.style.background = "radial-gradient(circle, rgba(79,70,229,0.25), transparent 60%)";
    glow.style.pointerEvents = "none";
    glow.style.borderRadius = "50%";
    glow.style.transform = "translate(-50%, -50%)";
    glow.style.zIndex = "9999";
    glow.style.transition = "opacity 0.3s";
    document.body.appendChild(glow);
    
    document.addEventListener("mousemove", e => {
        glow.style.left = e.clientX + "px";
        glow.style.top = e.clientY + "px";
    });
    
    // Hide glow when leaving window
    document.addEventListener("mouseleave", () => glow.style.opacity = "0");
    document.addEventListener("mouseenter", () => glow.style.opacity = "1");
});
"""
    if "Cursor Glow" not in js:
        js += extra_js

    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(js)

    # --- 3. UPDATE HTML ---
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Apply .glow-border to digi cards and main entry cards
    html = html.replace('class="entry-card box-glass"', 'class="entry-card box-glass glow-border"')
    html = html.replace('class="digi-card"', 'class="digi-card glow-border"')
    
    # Apply float effect to some elements like analyzer dashboard
    html = html.replace('class="analyzer-dashboard box-glass"', 'class="analyzer-dashboard box-glass float"')
    html = html.replace('class="hero-title"', 'class="hero-title float"')
    
    # Game cards specific
    html = html.replace('class="game-card box-glass"', 'class="game-card box-glass gaming-card glow-border"')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("SaaS polish applied successfully!")

if __name__ == '__main__':
    apply_saas_polish()
