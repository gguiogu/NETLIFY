import re

html_addition = """
        <!-- Commission Table Section -->
        <div class="commission-wrapper fade-in-on-scroll" style="margin: 60px auto 100px auto; max-width: 900px;" id="commission">
            <div class="box-glass p-0" style="border-radius: 20px; overflow: hidden; position: relative; padding: 0;">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(15, 23, 42, 0.8)); padding: 25px 20px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <h2 style="font-size: 1.8rem; margin-bottom: 5px; color: var(--text-main); font-weight: 900;"><i class="fa-solid fa-scale-balanced" style="color: var(--secondary); margin-left: 10px;"></i>جدول العمولات</h2>
                    <p style="color: var(--text-muted); font-size: 1rem; margin: 0;">أسعار شفافة • هيكل تسعير بسيط وعادل</p>
                </div>

                <!-- Grid Data -->
                <div class="com-grid" style="padding: 25px;">
                    <div class="com-item"><div class="com-price">تحت 3$</div><div class="com-fee">100 د.ج</div></div>
                    <div class="com-item"><div class="com-price">3$ - 5$</div><div class="com-fee">150 د.ج</div></div>
                    <div class="com-item"><div class="com-price">5$ - 11$</div><div class="com-fee">300 د.ج</div></div>
                    <div class="com-item"><div class="com-price">11$ - 15$</div><div class="com-fee">400 د.ج</div></div>
                    <div class="com-item"><div class="com-price">15$ - 18$</div><div class="com-fee">500 د.ج</div></div>
                    <div class="com-item"><div class="com-price">18$ - 22$</div><div class="com-fee">600 د.ج</div></div>
                    <div class="com-item"><div class="com-price">22$ - 25$</div><div class="com-fee">700 د.ج</div></div>
                    <div class="com-item"><div class="com-price">25$ - 32$</div><div class="com-fee">800 د.ج</div></div>
                    <div class="com-item"><div class="com-price">32$ - 38$</div><div class="com-fee">900 د.ج</div></div>
                    <div class="com-item"><div class="com-price">38$ - 44$</div><div class="com-fee">1000 د.ج</div></div>
                    <div class="com-item"><div class="com-price">44$ - 62$</div><div class="com-fee">1200 د.ج</div></div>
                    <div class="com-item"><div class="com-price">62$ - 70$</div><div class="com-fee">1300 د.ج</div></div>
                    <div class="com-item"><div class="com-price">70$ - 80$</div><div class="com-fee">1500 د.ج</div></div>
                    <div class="com-item"><div class="com-price">80$ - 90$</div><div class="com-fee">1700 د.ج</div></div>
                    <div class="com-item"><div class="com-price">90$ - 100$</div><div class="com-fee">1900 د.ج</div></div>
                    <div class="com-item"><div class="com-price">100$ - 120$</div><div class="com-fee">2100 د.ج</div></div>
                    <div class="com-item"><div class="com-price">120$ - 160$</div><div class="com-fee">2300 د.ج</div></div>
                    <div class="com-item"><div class="com-price">160$ - 200$</div><div class="com-fee">2500 د.ج</div></div>
                    <div class="com-item highlight"><div class="com-price">فوق 200$</div><div class="com-fee">قابلة للتفاوض</div></div>
                </div>
            </div>
        </div>
"""

css_addition = """

/* =========================================
   COMMISSION GRID ADDITIONS
   ========================================= */

.com-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 12px;
}

.com-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 12px 8px;
    text-align: center;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.com-item:hover {
    background: rgba(6, 182, 212, 0.08);
    border-color: rgba(6, 182, 212, 0.4);
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 5px 15px rgba(6, 182, 212, 0.15);
}

.com-price {
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-bottom: 6px;
    font-weight: 600;
}

.com-fee {
    font-size: 1.15rem;
    font-weight: 900;
    color: var(--secondary);
}

.com-item.highlight {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.02));
    border-color: rgba(16, 185, 129, 0.3);
}

.com-item.highlight .com-fee {
    color: #10b981;
}

.com-item.highlight:hover {
    box-shadow: 0 5px 15px rgba(16, 185, 129, 0.2);
    border-color: #10b981;
}

@media (min-width: 500px) {
    .com-grid {
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    }
}
"""

with open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8") as f:
    original = f.read()

# I will insert the commissioning table right after the Features section ends
# Find </section> that corresponds to the features section
# Best anchor: <!-- Final CTA -->
import sys
if "<!-- Final CTA -->" in original:
    new_content = original.replace("<!-- Final CTA -->", html_addition + "\n        <!-- Final CTA -->")
else:
    print("Could not find anchor to inject HTML")
    sys.exit(1)

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

with open("e:/KOUKI SHOP/style.css", "a", encoding="utf-8") as f:
    f.write(css_addition)

print("Commission table applied successfully!")
