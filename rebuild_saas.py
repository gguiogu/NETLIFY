import re

def rebuild():
    # 1. READ EXISTING HTML to extract complex sections
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(f"Error reading index.html: {e}")
        return

    # Extract Results Dashboard
    dash_match = re.search(r'(<section id="results-dashboard".*?</section>)', html, re.DOTALL)
    results_dashboard = dash_match.group(1) if dash_match else '<!-- RESULTS DASHBOARD MISSING -->'
    
    # Update some classes in results dashboard for new saas look
    results_dashboard = results_dashboard.replace('background: rgba(13, 110, 253, 0.05);', 'background: var(--bg-surface);')
    results_dashboard = results_dashboard.replace('border: 2px solid rgba(13, 110, 253, 0.3);', 'border: 1px solid var(--border-glass);')

    # Extract Digital Market Grid (just the cards)
    market_grid_match = re.search(r'(<div class="digital-services-grid" id="marketGrid".*?>\s*(.*?)\s*</div>\s*<!-- ===== GAMING ===== -->)', html, re.DOTALL)
    digital_cards = market_grid_match.group(2) if market_grid_match else '<!-- DIGITAL CARDS MISSING -->'

    # 2. BUILD NEW HTML
    new_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kouki Shop - Everything You Want. Paid in DZD.</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link rel="icon" href="logo.png" type="image/png">
</head>
<body>
    <div class="bg-elements">
        <div class="blob purple"></div>
        <div class="blob cyan"></div>
    </div>

    <!-- Header -->
    <header class="navbar container">
        <a href="#" class="logo" onclick="showView('home')">
            <img src="logo.png" alt="Kouki Shop Logo" class="brand-logo">
        </a>
        <nav class="nav-links">
            <a href="#" onclick="showView('shopping')">تسوق عالمي</a>
            <a href="#" onclick="showView('digital')">خدمات رقمية</a>
            <a href="#" onclick="showView('gaming')">شحن ألعاب</a>
        </nav>
    </header>

    <!-- VIEWS CONTAINER -->
    <main class="container views-wrapper">
    
        <!-- ============================== -->
        <!-- VIEW: HOME (Main Entry)        -->
        <!-- ============================== -->
        <div id="view-home" class="view active">
            <!-- Hero Section -->
            <section class="hero-saas">
                <h1 class="hero-title">كل ما تحتاجه.<br><span class="gradient-text">بالدينار الجزائري.</span></h1>
                <p class="hero-subtitle">منتجات عالمية، اشتراكات رقمية، ورصيد ألعاب — في منصة واحدة موثوقة.</p>
                <div class="hero-ctas">
                    <button class="btn btn-primary large" onclick="document.getElementById('services-entry').scrollIntoView({{behavior:'smooth'}})">ابدأ الآن</button>
                    <button class="btn btn-outline large" onclick="document.getElementById('services-entry').scrollIntoView({{behavior:'smooth'}})">تصفح الخدمات</button>
                </div>
            </section>

            <!-- Trust Bar -->
            <div class="trust-bar box-glass">
                <div class="trust-item"><i class="fa-solid fa-flag text-green"></i> صمم للجزائر 🇩🇿</div>
                <div class="trust-item"><i class="fa-solid fa-clock-rotate-left text-blue"></i> +3 سنوات خبرة</div>
                <div class="trust-item"><i class="fa-solid fa-box-open text-orange"></i> آلاف الطلبات الناجحة</div>
                <div class="trust-item"><i class="fa-solid fa-shield-halved"></i> دفع آمن CCP/BaridiMob</div>
            </div>

            <!-- Main Entry Cards -->
            <section id="services-entry" class="main-entry-grid">
                <!-- Shopping -->
                <div class="entry-card box-glass">
                    <div class="entry-icon" style="color: var(--primary);"><i class="fa-solid fa-earth-americas"></i></div>
                    <h3>التسوق العالمي</h3>
                    <p>تسوق من AliExpress والمتاجر العالمية بدون بطاقة بنكية. ضع الرابط ونحن نتكفل بالباقي.</p>
                    <button class="btn btn-outline" onclick="showView('shopping')">اطلب الآن <i class="fa-solid fa-arrow-left"></i></button>
                </div>
                <!-- Digital -->
                <div class="entry-card box-glass">
                    <div class="entry-icon" style="color: var(--secondary);"><i class="fa-solid fa-laptop-code"></i></div>
                    <h3>الخدمات الرقمية</h3>
                    <p>اشتراكات ChatGPT، Netflix، Canva، Adobe والمزيد. تفعيل فوري وآمن لحسابك.</p>
                    <button class="btn btn-outline" onclick="showView('digital')">تصفح الخدمات <i class="fa-solid fa-arrow-left"></i></button>
                </div>
                <!-- Gaming -->
                <div class="entry-card box-glass">
                    <div class="entry-icon" style="color: var(--accent);"><i class="fa-solid fa-gamepad"></i></div>
                    <h3>شحن الألعاب</h3>
                    <p>شحن فوري لألعاب Free Fire، PUBG، eFootball مباشرة عبر الـ ID الخاص بك.</p>
                    <button class="btn btn-outline" onclick="showView('gaming')">اشحن الآن <i class="fa-solid fa-arrow-left"></i></button>
                </div>
            </section>
        </div>

        <!-- ============================== -->
        <!-- VIEW: GLOBAL SHOPPING          -->
        <!-- ============================== -->
        <div id="view-shopping" class="view hidden fade-in">
            <div class="service-header">
                <h2>تسوق من العالم <span class="gradient-text">بدون بطاقة</span></h2>
                <p>ضع رابط المنتج من AliExpress، احصل على السعر بالدينار، وسنقوم بطلبه إلى باب منزلك.</p>
            </div>

            <div class="shopping-steps box-glass">
                <div class="step-item">
                    <div class="step-num">1</div>
                    <h4>انسخ الرابط</h4>
                    <p>من تطبيق AliExpress</p>
                </div>
                <div class="step-item">
                    <div class="step-num">2</div>
                    <h4>احصل على السعر</h4>
                    <p>بالدينار الجزائري فوراً</p>
                </div>
                <div class="step-item">
                    <div class="step-num">3</div>
                    <h4>ادفع واستلم</h4>
                    <p>توصيل في 15-35 يوم</p>
                </div>
            </div>

            <!-- Dashboard Mockup (Analyzer) -->
            <div class="analyzer-dashboard box-glass">
                <div class="search-box">
                    <div class="search-input-wrapper">
                        <i class="fa-solid fa-link input-icon"></i>
                        <input type="text" id="product-url" placeholder="ضع رابط المنتج الذي تريد شرائه من موقع AliExpress..." oninput="clearErrors()">
                    </div>
                    <button class="btn btn-primary" onclick="analyzeProduct()" id="analyze-btn">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> حلّل المنتج
                    </button>
                </div>
                <div id="error-message" class="error-text"></div>

                <!-- Loading State -->
                <section id="loading-state" class="loading-container hidden">
                    <div class="loader"></div>
                    <h3 class="loading-title">جاري تحليل المنتج بالذكاء الاصطناعي...</h3>
                    <ul class="loading-steps">
                        <li class="step active" id="step-1"><i class="fa-solid fa-circle-check"></i> جلب تفاصيل المنتج</li>
                        <li class="step" id="step-2"><i class="fa-solid fa-circle-notch fa-spin"></i> التقييم وكشف الاحتيال</li>
                        <li class="step" id="step-3"><i class="fa-solid fa-circle-notch fa-spin"></i> حساب الأسعار وهوامش الربح</li>
                    </ul>
                </section>

                {results_dashboard}
            </div>

            <div class="guarantees-bar box-glass">
                <div><i class="fa-solid fa-truck-fast"></i> توصيل La Poste (15-35 يوم)</div>
                <div><i class="fa-solid fa-shield-check"></i> ضمان استرجاع الأموال</div>
                <div><i class="fa-solid fa-headset"></i> دعم فني متواصل</div>
            </div>
        </div>

        <!-- ============================== -->
        <!-- VIEW: DIGITAL SERVICES         -->
        <!-- ============================== -->
        <div id="view-digital" class="view hidden fade-in">
            <div class="service-header">
                <h2>خدمات رقمية <span class="gradient-text">بريميوم</span></h2>
                <p>اشتراكات أصلية ومضمونة، تفعيل فوري بالدينار الجزائري.</p>
            </div>

            <div class="digital-search-container box-glass">
                <i class="fa-solid fa-magnifying-glass"></i>
                <input type="text" id="digitalSearch" placeholder="ابحث (Netflix, ChatGPT...)" oninput="filterDigitalMarket()">
            </div>

            <div class="category-tabs-wrapper box-glass">
                <div class="category-tabs" id="marketTabs">
                    <button class="cat-tab active" onclick="selectCategory('all', this)">الكل</button>
                    <button class="cat-tab" onclick="selectCategory('ai', this)">ذكاء اصطناعي</button>
                    <button class="cat-tab" onclick="selectCategory('entertainment', this)">ترفيه</button>
                    <button class="cat-tab" onclick="selectCategory('music', this)">موسيقى</button>
                    <button class="cat-tab" onclick="selectCategory('design', this)">تصميم</button>
                    <button class="cat-tab" onclick="selectCategory('productivity', this)">إنتاجية</button>
                </div>
            </div>

            <div class="digital-services-grid" id="marketGrid">
                {digital_cards}
            </div>
        </div>

        <!-- ============================== -->
        <!-- VIEW: GAME TOP-UP              -->
        <!-- ============================== -->
        <div id="view-gaming" class="view hidden fade-in">
            <div class="service-header gaming-header">
                <h2>شحن ألعاب <span style="color: var(--accent);">سريع وآمن</span></h2>
                <p>اشحن رصيدك فوراً عبر الـ ID بأفضل الأسعار في الجزائر.</p>
            </div>

            <div class="games-grid">
                <!-- Free Fire -->
                <div class="game-card box-glass">
                    <img src="https://play-lh.googleusercontent.com/1OjsYhJpWiqH-0z-RXYzI0H2xJ7tY62P1Vf9-LhVb6T1u2r72o5q_pS0R8P2Q4G1-aM" alt="Free Fire" class="game-banner">
                    <div class="game-content">
                        <h3>Garena Free Fire</h3>
                        <div class="game-form">
                            <input type="text" id="ff-id" placeholder="أدخل Player ID" oninput="verifyGamePlayerId('ff')">
                            <div id="ff-player-name" class="player-name hidden"></div>
                            <select id="ff-package">
                                <option value="100">100 جوهرة (+10 مجاناً)</option>
                                <option value="210">210 جوهرة (+21 مجاناً)</option>
                                <option value="530">530 جوهرة (+53 مجاناً)</option>
                                <option value="weekly">عضوية أسبوعية</option>
                                <option value="monthly">عضوية شهرية</option>
                            </select>
                            <button class="btn btn-primary" onclick="buyGameTopup('Free Fire')">اشحن الآن</button>
                        </div>
                    </div>
                </div>

                <!-- PUBG Mobile -->
                <div class="game-card box-glass">
                    <img src="https://play-lh.googleusercontent.com/JRd05pyBH41qjgsJuWduRJpDeZG0Hnb0yq2GUqX28S8M1F1jH9-Yv9jA9L9h4Z5Q9Lw" alt="PUBG Mobile" class="game-banner">
                    <div class="game-content">
                        <h3>PUBG Mobile</h3>
                        <div class="game-form">
                            <input type="text" id="pubg-id" placeholder="أدخل Player ID" oninput="verifyGamePlayerId('pubg')">
                            <div id="pubg-player-name" class="player-name hidden"></div>
                            <select id="pubg-package">
                                <option value="60">60 UC</option>
                                <option value="325">325 UC</option>
                                <option value="660">660 UC</option>
                                <option value="1800">1800 UC</option>
                                <option value="prime">Prime Plus</option>
                            </select>
                            <button class="btn btn-primary" onclick="buyGameTopup('PUBG Mobile')">اشحن الآن</button>
                        </div>
                    </div>
                </div>

                <!-- eFootball -->
                <div class="game-card box-glass">
                    <img src="efootball.png" alt="eFootball 2024" class="game-banner" onerror="this.src='https://play-lh.googleusercontent.com/aC9N-Qv2Q2O4vYjH2o3X6X8Z6Z-Z9Z0Z1Z2Z3Z4Z5Z6Z7Z8Z9Z0Z1Z2Z3Z4Z5Z6'">
                    <div class="game-content">
                        <h3>eFootball 2024</h3>
                        <div class="game-form">
                            <input type="text" id="efootball-id" placeholder="أدخل Konami ID">
                            <select id="efootball-package">
                                <option value="130">130 Coins</option>
                                <option value="300">300 Coins</option>
                                <option value="1050">1050 Coins</option>
                                <option value="2150">2150 Coins</option>
                                <option value="3300">3300 Coins</option>
                            </select>
                            <button class="btn btn-primary" onclick="buyGameTopup('eFootball')">اشحن الآن</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================== -->
        <!-- TRUST & FOOTER (ALWAYS VISIBLE)-->
        <!-- ============================== -->
        
        <section class="global-trust-section">
            <div class="section-header text-center">
                <h2>لماذا يثق بنا <span class="gradient-text">الآلاف؟</span></h2>
            </div>
            <div class="social-proof-grid">
                <div class="review-card box-glass">
                    <div class="stars">★★★★★</div>
                    <p>"أفضل موقع صراحة، طلبت ساعة ذكية ووصلتني لباب الدار في ظرف 18 يوم فقط. أنصح به بشدة."</p>
                    <div class="reviewer">- كريم (سطيف)</div>
                </div>
                <div class="review-card box-glass">
                    <div class="stars">★★★★★</div>
                    <p>"اشتريت حساب نتفلكس وكان التسليم فوري بدون أي مشاكل. خدمة ممتازة وسريعة."</p>
                    <div class="reviewer">- سارة (الجزائر العاصمة)</div>
                </div>
                <div class="review-card box-glass">
                    <div class="stars">★★★★★</div>
                    <p>"شحن جواهر فري فاير وصلني في دقيقة واحدة بعد الدفع. موثوق جداً."</p>
                    <div class="reviewer">- أيمن (وهران)</div>
                </div>
            </div>
            <div class="guarantees-banner box-glass">
                <div class="guarantee"><i class="fa-solid fa-shield-check text-green"></i> ضمان تفعيل أو استرداد أموالك</div>
                <div class="guarantee"><i class="fa-solid fa-headset text-blue"></i> دعم فني سريع عبر واتساب</div>
                <div class="guarantee"><i class="fa-solid fa-lock text-orange"></i> تعامل سري وآمن تماماً</div>
            </div>
        </section>

        <section class="extra-services">
            <div class="section-header text-center">
                <h2>خدمات <span class="gradient-text">إضافية</span></h2>
            </div>
            <div class="extra-services-grid">
                <div class="extra-card box-glass">
                    <i class="fa-solid fa-code"></i>
                    <h3>إنشاء مواقع ويب</h3>
                    <p>مواقع احترافية للشركات والمتاجر الإلكترونية بأسعار تنافسية.</p>
                </div>
                <div class="extra-card box-glass">
                    <i class="fa-solid fa-bullhorn"></i>
                    <h3>إدارة الحملات الإعلانية</h3>
                    <p>إعلانات ممولة على فيسبوك وانستغرام لزيادة مبيعاتك.</p>
                </div>
                <div class="extra-card box-glass">
                    <i class="fa-solid fa-pen-nib"></i>
                    <h3>خدمات تصميم</h3>
                    <p>هويات بصرية، شعارات، وتصاميم سوشيال ميديا احترافية.</p>
                </div>
            </div>
        </section>
        
    </main>

    <footer class="main-footer box-glass">
        <div class="footer-content container">
            <div class="footer-col">
                <img src="logo.png" alt="Logo" class="footer-logo">
                <p>منصتك الأولى في الجزائر للتسوق العالمي والخدمات الرقمية.</p>
            </div>
            <div class="footer-col">
                <h4>روابط سريعة</h4>
                <ul>
                    <li><a href="#" onclick="showView('home')">الرئيسية</a></li>
                    <li><a href="#" onclick="showView('shopping')">التسوق العالمي</a></li>
                    <li><a href="#" onclick="showView('digital')">الخدمات الرقمية</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>تواصل معنا</h4>
                <div class="social-links">
                    <a href="https://wa.me/213562208794" class="social-icon wa"><i class="fa-brands fa-whatsapp"></i></a>
                    <a href="https://t.me/BOOGEYMAN_DZ" class="social-icon tg"><i class="fa-brands fa-telegram"></i></a>
                    <a href="https://www.facebook.com/XBHTHAGOAT/" class="social-icon fb"><i class="fa-brands fa-facebook"></i></a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Kouki Shop. جميع الحقوق محفوظة.</p>
        </div>
    </footer>

    <!-- Floating Contact -->
    <a href="https://wa.me/213562208794" class="floating-contact" target="_blank">
        <i class="fa-brands fa-whatsapp"></i>
    </a>

    <script src="script.js"></script>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    # 3. BUILD NEW CSS
    new_css = """/* Premium SaaS Design System - Kouki Shop */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Inter:wght@400;600;800&display=swap');

:root {
    --bg-dark: #0B0F1A;
    --bg-surface: #111827;
    --border-glass: rgba(255, 255, 255, 0.08);
    
    --primary: #4F46E5; /* Indigo */
    --primary-hover: #4338CA;
    --primary-glow: rgba(79, 70, 229, 0.4);
    
    --secondary: #06b6d4; /* Cyan */
    --accent: #22D3EE; /* Cyan glow */
    
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    
    --text-main: #F9FAFB;
    --text-muted: #9CA3AF;
    
    --font-heading: 'Inter', sans-serif;
    --font-body: 'Cairo', sans-serif;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--bg-dark);
    color: var(--text-main);
    font-family: var(--font-body);
    line-height: 1.6;
    overflow-x: hidden;
    min-height: 100vh;
    font-size: 16px;
    scroll-behavior: smooth;
}

h1, h2, h3, h4, .logo-text, .hero-title, .hero-subtitle {
    font-family: var(--font-heading);
}

/* Fallback for Arabic headings */
body[dir="rtl"] h1, body[dir="rtl"] h2, body[dir="rtl"] h3, body[dir="rtl"] h4 {
    font-family: var(--font-body); /* Use Cairo for Arabic */
}

a {
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease;
}

ul { list-style: none; }

/* Backgrounds */
.bg-elements {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: -1; overflow: hidden; pointer-events: none;
}

.blob {
    position: absolute;
    filter: blur(120px);
    border-radius: 50%;
    opacity: 0.3;
    animation: float 20s infinite ease-in-out alternate;
}

.blob.purple {
    top: -10%; right: -10%;
    width: 600px; height: 600px;
    background: radial-gradient(circle, var(--primary), transparent 70%);
}

.blob.cyan {
    bottom: -10%; left: -10%;
    width: 500px; height: 500px;
    background: radial-gradient(circle, var(--secondary), transparent 70%);
    animation-delay: -10s;
}

@keyframes float {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(-50px, 50px) scale(1.1); }
}

/* Utils */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.hidden { display: none !important; }
.text-green { color: var(--success); }
.text-blue { color: var(--secondary); }
.text-orange { color: var(--warning); }
.text-center { text-align: center; }

.box-glass {
    background: var(--bg-surface);
    border: 1px solid var(--border-glass);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.box-glass:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    border-color: rgba(255, 255, 255, 0.15);
}

.gradient-text {
    background: linear-gradient(90deg, var(--accent), var(--primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Header */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    position: relative;
    z-index: 100;
}

.brand-logo {
    height: 60px;
    object-fit: contain;
    border-radius: 8px;
}

.nav-links {
    display: flex;
    gap: 24px;
    font-weight: 600;
}

.nav-links a:hover {
    color: var(--accent);
}

/* Views Wrapper */
.views-wrapper {
    min-height: 60vh;
    padding-bottom: 60px;
}
.view {
    display: none;
    animation: fadeIn 0.4s ease forwards;
}
.view.active { display: block; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    outline: none;
    font-size: 1rem;
}

.btn.large {
    padding: 16px 32px;
    font-size: 1.1rem;
}

.btn-primary {
    background: var(--primary);
    color: white;
    box-shadow: 0 4px 15px var(--primary-glow);
}

.btn-primary:hover {
    background: var(--primary-hover);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--primary-glow);
}

.btn-outline {
    background: transparent;
    border: 1px solid var(--border-glass);
    color: var(--text-main);
}

.btn-outline:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: var(--text-muted);
}

/* Hero SaaS */
.hero-saas {
    text-align: center;
    padding: 80px 0 60px;
    max-width: 900px;
    margin: 0 auto;
}

.hero-title {
    font-size: 4rem;
    line-height: 1.1;
    margin-bottom: 24px;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: var(--text-muted);
    margin-bottom: 40px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.hero-ctas {
    display: flex;
    justify-content: center;
    gap: 16px;
}

/* Trust Bar */
.trust-bar {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
    padding: 20px;
    margin: 0 auto 60px;
    max-width: 1000px;
    border-radius: 50px;
    background: rgba(17, 24, 39, 0.8);
}

.trust-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    font-size: 1rem;
    color: var(--text-muted);
}

/* Main Entry Cards */
.main-entry-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    margin-bottom: 80px;
}

.entry-card {
    padding: 40px 30px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.entry-icon {
    font-size: 3.5rem;
    margin-bottom: 10px;
}

.entry-card h3 {
    font-size: 1.8rem;
}

.entry-card p {
    color: var(--text-muted);
    flex-grow: 1;
    font-size: 1.05rem;
}

.entry-card .btn {
    width: 100%;
    margin-top: 10px;
}

/* Service Headers */
.service-header {
    text-align: center;
    margin: 40px 0 60px;
}
.service-header h2 {
    font-size: 3rem;
    margin-bottom: 16px;
}
.service-header p {
    font-size: 1.2rem;
    color: var(--text-muted);
}

/* Shopping Flow */
.shopping-steps {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 20px;
    padding: 30px;
    margin-bottom: 40px;
    text-align: center;
}

.step-item {
    flex: 1;
    min-width: 200px;
}

.step-num {
    width: 40px; height: 40px;
    background: var(--primary);
    color: white;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: bold; font-size: 1.2rem;
    margin: 0 auto 16px;
}

.analyzer-dashboard {
    padding: 40px;
    margin-bottom: 40px;
}

.search-box {
    display: flex;
    flex-direction: column;
    gap: 16px;
    background: rgba(0,0,0,0.2);
    padding: 8px;
    border-radius: 12px;
    border: 1px solid var(--border-glass);
}

@media (min-width: 768px) {
    .search-box { flex-direction: row; border-radius: 50px; }
}

.search-input-wrapper {
    display: flex; align-items: center; flex: 1; padding: 0 20px; gap: 12px;
}
.search-input-wrapper input {
    width: 100%; background: transparent; border: none; color: var(--text-main); font-size: 1.1rem; outline: none; padding: 12px 0;
}

.guarantees-bar {
    display: flex; justify-content: space-around; padding: 20px; flex-wrap: wrap; gap: 20px; color: var(--text-muted); font-weight: 600;
}

/* Digital Market Grid from previous style.css + tweaks */
.digital-search-container {
    display: flex; align-items: center; gap: 12px; padding: 16px 24px; border-radius: 50px; max-width: 600px; margin: 0 auto 30px;
}
.digital-search-container input {
    width: 100%; border: none; background: transparent; color: white; font-size: 1.1rem; outline: none;
}
.category-tabs-wrapper {
    padding: 12px; border-radius: 12px; margin-bottom: 30px; overflow-x: auto; white-space: nowrap;
}
.category-tabs {
    display: inline-flex; gap: 10px;
}
.cat-tab {
    background: transparent; border: 1px solid var(--border-glass); color: var(--text-muted); padding: 8px 16px; border-radius: 50px; cursor: pointer; transition: all 0.3s;
}
.cat-tab.active, .cat-tab:hover {
    background: var(--primary); color: white; border-color: var(--primary);
}

.digital-services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
}

.digi-card {
    position: relative;
    padding: 24px;
    background: var(--bg-surface);
    border: 1px solid var(--border-glass);
    border-radius: 16px;
    display: flex; flex-direction: column; gap: 12px;
    overflow: hidden;
    transition: transform 0.3s, box-shadow 0.3s;
}
.digi-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.5); }

.card-badge { position: absolute; top: 12px; left: 12px; font-size: 0.8rem; padding: 4px 8px; border-radius: 6px; font-weight: bold; }
.card-badge.hot { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.card-badge.new { background: rgba(16, 185, 129, 0.2); color: #10b981; }

.digi-icon { width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.05); border-radius: 12px; margin-bottom: 8px; }
.digi-icon img, .digi-icon svg { max-width: 32px; max-height: 32px; }
.digi-card h3 { font-size: 1.4rem; margin: 0; }
.digi-card p { color: var(--text-muted); font-size: 0.95rem; margin: 0; }
.digi-price { font-weight: bold; color: var(--accent); margin-top: auto; }
.digi-actions { display: flex; gap: 8px; margin-top: 16px; }
.btn-digi { flex: 1; padding: 10px; background: rgba(255,255,255,0.05); border: none; border-radius: 8px; cursor: pointer; transition: 0.3s; }
.btn-digi:hover { background: rgba(255,255,255,0.1); }

/* Gaming Section */
.games-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; }
.game-card { overflow: hidden; display: flex; flex-direction: column; }
.game-banner { width: 100%; height: 180px; object-fit: cover; border-bottom: 1px solid var(--border-glass); }
.game-content { padding: 24px; flex-grow: 1; display: flex; flex-direction: column; gap: 16px; }
.game-content h3 { font-size: 1.6rem; text-align: center; }
.game-form { display: flex; flex-direction: column; gap: 16px; }
.game-form input, .game-form select { padding: 14px; background: rgba(0,0,0,0.3); border: 1px solid var(--border-glass); border-radius: 8px; color: white; font-size: 1rem; outline: none; }
.player-name { font-size: 0.9rem; color: var(--success); text-align: center; }
.player-name.error { color: var(--danger); }

/* Trust & Extra Services */
.section-header { margin: 60px 0 40px; }
.social-proof-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-bottom: 40px; }
.review-card { padding: 30px; }
.stars { color: #FBBF24; font-size: 1.2rem; margin-bottom: 12px; letter-spacing: 2px; }
.reviewer { color: var(--text-muted); font-size: 0.9rem; margin-top: 16px; font-weight: bold; }

.guarantees-banner { display: flex; justify-content: space-around; flex-wrap: wrap; padding: 24px; gap: 20px; font-weight: bold; }

.extra-services-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-bottom: 60px; }
.extra-card { padding: 30px; text-align: center; }
.extra-card i { font-size: 2.5rem; color: var(--primary); margin-bottom: 16px; }

/* Footer */
.main-footer { margin-top: 60px; border-radius: 24px 24px 0 0; padding-top: 40px; }
.footer-content { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; padding-bottom: 40px; border-bottom: 1px solid var(--border-glass); }
.footer-logo { height: 50px; margin-bottom: 16px; border-radius: 8px; }
.footer-col h4 { margin-bottom: 20px; font-size: 1.2rem; }
.footer-col ul { display: flex; flex-direction: column; gap: 12px; }
.footer-col a:hover { color: var(--accent); }
.social-links { display: flex; gap: 16px; }
.social-icon { width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; transition: 0.3s; }
.social-icon:hover { background: var(--primary); transform: translateY(-3px); }
.footer-bottom { text-align: center; padding: 20px; color: var(--text-muted); font-size: 0.9rem; }

/* Floating Contact */
.floating-contact { position: fixed; bottom: 30px; left: 30px; width: 60px; height: 60px; background: #25D366; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4); z-index: 1000; transition: 0.3s; }
.floating-contact:hover { transform: scale(1.1); }

/* Loading State (AliExpress Analyzer) */
.loading-container { text-align: center; padding: 40px 0; }
.loader { width: 50px; height: 50px; border: 4px solid var(--border-glass); border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px; }
@keyframes spin { to { transform: rotate(360deg); } }
.loading-steps { max-width: 300px; margin: 0 auto; text-align: right; display: flex; flex-direction: column; gap: 12px; }
.step { color: var(--text-muted); display: flex; gap: 10px; align-items: center; }
.step.active { color: var(--success); }

/* Responsive Dashboard inner layout (borrowed and adjusted from previous) */
.pro-product-layout { display: flex; flex-wrap: wrap; gap: 30px; }
.pro-image-col { flex: 1; min-width: 300px; }
.pro-details-col { flex: 1.5; min-width: 300px; }
"""
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(new_css)

    # 4. PATCH SCRIPT.JS to add the view routing
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            js = f.read()
            
        if "function showView(" not in js:
            router_js = """
// ==========================================
// View Routing System
// ==========================================
function showView(viewId) {
    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
        // A short timeout before adding hidden so the fade out could happen, 
        // but for instant snappy SaaS feel we just toggle classes:
        view.classList.add('hidden');
    });
    
    // Show target view
    const target = document.getElementById('view-' + viewId);
    if (target) {
        target.classList.remove('hidden');
        target.classList.add('active');
        window.scrollTo({top: 0, behavior: 'smooth'});
    }
}
"""
            with open('script.js', 'a', encoding='utf-8') as f:
                f.write(router_js)
    except Exception as e:
        print(f"Error reading/writing script.js: {e}")

    print("Rebuild complete!")

if __name__ == '__main__':
    rebuild()
