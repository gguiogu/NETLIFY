import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

text = open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8").read()

start_marker = "        <!-- Digital Services Section -->"
end_marker = "        <!-- Market Section Ends Here -->"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker) + len(end_marker)

NEW_SECTION = """        <!-- Digital Services Section -->
        <div class="section-label-bar fade-in-on-scroll">
            <span class="section-label-dot"></span>
            <h2 class="section-title gradient-text glow" style="margin:0; font-size:2rem;">الكتالوج الرقمي</h2>
            <span class="section-label-dot"></span>
        </div>
        <p class="text-center text-muted fade-in-on-scroll" style="margin-bottom: 30px; font-size: 1.1rem;">
            اشتراكات أصلية مضمونة • بالدينار الجزائري • تفعيل فوري
        </p>

        <!-- Market Section Starts Here -->
        <section id="digital-market" class="digital-market fade-in-on-scroll" style="margin-top: 20px;">
            <div class="market-header" style="text-align: center; margin-bottom: 30px;">
                <!-- Live Search -->
                <div class="digital-search-container box-glass" style="max-width:580px; margin:0 auto 24px auto; display:flex; align-items:center; padding:14px 22px; border-radius:50px; gap:12px;">
                    <i class="fa-solid fa-magnifying-glass" style="font-size:1.1rem; color:var(--secondary);"></i>
                    <input type="text" id="digitalSearch" placeholder="ابحث (Netflix, Canva, ChatGPT...)" oninput="filterDigitalMarket()" style="width:100%; border:none; background:transparent; color:var(--text); font-size:1.05rem; outline:none; direction:rtl;">
                </div>
                <!-- Category Tabs -->
                <div class="category-tabs-wrapper" style="position:sticky; top:70px; z-index:100; background:rgba(10,15,30,0.92); backdrop-filter:blur(16px); padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.05); overflow-x:auto; white-space:nowrap; box-shadow:0 8px 25px rgba(0,0,0,0.3);">
                    <div class="category-tabs" id="marketTabs" style="display:inline-flex; gap:8px; padding:0 20px;">
                        <button class="cat-tab active" onclick="selectCategory('all', this)">كل الخدمات</button>
                        <button class="cat-tab" onclick="selectCategory('ai', this)">ذكاء اصطناعي</button>
                        <button class="cat-tab" onclick="selectCategory('entertainment', this)">ترفيه</button>
                        <button class="cat-tab" onclick="selectCategory('music', this)">موسيقى</button>
                        <button class="cat-tab" onclick="selectCategory('design', this)">تصميم وإبداع</button>
                        <button class="cat-tab" onclick="selectCategory('productivity', this)">إنتاجية</button>
                        <button class="cat-tab" onclick="selectCategory('gaming', this)">ألعاب</button>
                        <button class="cat-tab" onclick="selectCategory('cloud', this)">تخزين سحابي</button>
                        <button class="cat-tab" onclick="selectCategory('learning', this)">تعليم</button>
                        <button class="cat-tab" onclick="selectCategory('social', this)">سوشيال</button>
                    </div>
                </div>
            </div>

            <!-- Skeleton Loader Row (hidden after load) -->
            <div id="skeletonGrid" class="digital-services-grid skeleton-visible" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:20px; margin-bottom:10px;">
                <div class="skeleton-card"><div class="skeleton-icon"></div><div class="skeleton-line w70"></div><div class="skeleton-line w50"></div><div class="skeleton-line w60"></div></div>
                <div class="skeleton-card"><div class="skeleton-icon"></div><div class="skeleton-line w70"></div><div class="skeleton-line w50"></div><div class="skeleton-line w60"></div></div>
                <div class="skeleton-card"><div class="skeleton-icon"></div><div class="skeleton-line w70"></div><div class="skeleton-line w50"></div><div class="skeleton-line w60"></div></div>
                <div class="skeleton-card"><div class="skeleton-icon"></div><div class="skeleton-line w70"></div><div class="skeleton-line w50"></div><div class="skeleton-line w60"></div></div>
                <div class="skeleton-card"><div class="skeleton-icon"></div><div class="skeleton-line w70"></div><div class="skeleton-line w50"></div><div class="skeleton-line w60"></div></div>
                <div class="skeleton-card"><div class="skeleton-icon"></div><div class="skeleton-line w70"></div><div class="skeleton-line w50"></div><div class="skeleton-line w60"></div></div>
            </div>

            <!-- Real Products Grid -->
            <div class="digital-services-grid" id="marketGrid" style="display:none; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:20px;">

                <!-- ===== AI TOOLS ===== -->
                <div class="digi-card" data-category="ai" data-title="ChatGPT Plus" style="--brand-glow: rgba(16,163,127,0.5);">
                    <span class="card-badge hot">الأكثر طلباً</span>
                    <div class="digi-glow" style="background: rgba(16,163,127,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/openai/10a37f" alt="ChatGPT" loading="lazy">
                    </div>
                    <h3>ChatGPT Plus</h3>
                    <p>GPT-4o • توليد صور • بلا حدود</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">GPT-4o مع توليد الصور وتحليل الملفات بلا قيود</div>
                    <div class="digi-actions">
                        <button onclick="orderService('ChatGPT Plus', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('ChatGPT Plus', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('ChatGPT Plus', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="ai" data-title="Grok AI" style="--brand-glow: rgba(130,80,255,0.5);">
                    <span class="card-badge new">جديد</span>
                    <div class="digi-glow" style="background: rgba(130,80,255,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/x/ffffff" alt="Grok AI" loading="lazy">
                    </div>
                    <h3>Grok AI (X)</h3>
                    <p>أقوى AI من منصة X • تحليل ذكي فائق</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">Grok 2 من إيلون ماسك مع وصول لبيانات X مباشرة</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Grok AI', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Grok AI', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Grok AI', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="ai" data-title="Gemini Advanced" style="--brand-glow: rgba(66,133,244,0.5);">
                    <div class="digi-glow" style="background: rgba(66,133,244,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg" alt="Gemini" loading="lazy">
                    </div>
                    <h3>Gemini Advanced</h3>
                    <p>Ultra 1.5 • ملفات • صور • Vision</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">نموذج Google الأقوى مع 1TB تخزين وتحليل الصور</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Gemini Advanced', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Gemini Advanced', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Gemini Advanced', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="ai" data-title="Claude Pro" style="--brand-glow: rgba(217,119,87,0.5);">
                    <div class="digi-glow" style="background: rgba(217,119,87,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/anthropic/d97757" alt="Claude" loading="lazy">
                    </div>
                    <h3>Claude Pro</h3>
                    <p>Sonnet • ملفات طويلة • كود احترافي</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">Claude 3.5 Sonnet الأفضل للتحليل والكتابة الأدبية</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Claude Pro', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Claude Pro', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Claude Pro', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="ai" data-title="Perplexity AI" style="--brand-glow: rgba(32,191,255,0.5);">
                    <span class="card-badge new">جديد</span>
                    <div class="digi-glow" style="background: rgba(32,191,255,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/perplexity/20BFFF" alt="Perplexity" loading="lazy">
                    </div>
                    <h3>Perplexity Pro</h3>
                    <p>بحث ذكي • مصادر حية • تقارير</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">محرك بحث AI يجمع كل المصادر ويلخصها فوراً</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Perplexity Pro', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Perplexity Pro', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Perplexity Pro', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="ai" data-title="Midjourney" style="--brand-glow: rgba(255,255,255,0.3);">
                    <span class="card-badge limited">محدود</span>
                    <div class="digi-glow" style="background: rgba(255,255,255,0.2);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.png" alt="Midjourney" loading="lazy" onerror="this.src='https://cdn.simpleicons.org/midjourney/ffffff'">
                    </div>
                    <h3>Midjourney V6</h3>
                    <p>توليد صور احترافي • عبر Discord</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">أقوى مولد صور بالذكاء الاصطناعي في العالم V6</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Midjourney', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Midjourney', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Midjourney', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <!-- ===== ENTERTAINMENT ===== -->
                <div class="digi-card" data-category="entertainment" data-title="Netflix" style="--brand-glow: rgba(229,9,20,0.5);">
                    <span class="card-badge hot">الأكثر مبيعاً</span>
                    <div class="digi-glow" style="background: rgba(229,9,20,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/netflix/E50914" alt="Netflix" loading="lazy">
                    </div>
                    <h3>Netflix Premium</h3>
                    <p>4K UHD • شاشة خاصة • 190 دولة</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">نتفليكس بريميوم 4K شاشة خاصة بدون مشاركة</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Netflix', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Netflix', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Netflix', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="entertainment" data-title="Disney+" style="--brand-glow: rgba(17,60,207,0.5);">
                    <div class="digi-glow" style="background: rgba(17,60,207,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/disneyplus/ffffff" alt="Disney+" loading="lazy">
                    </div>
                    <h3>Disney+</h3>
                    <p>Marvel • Star Wars • Pixar • 4K</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">كل أفلام ومسلسلات مارفل وسترواورز وديزني الأصلية</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Disney+', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Disney+', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Disney+', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="entertainment" data-title="Prime Video" style="--brand-glow: rgba(0,168,225,0.5);">
                    <div class="digi-glow" style="background: rgba(0,168,225,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/primevideo/00A8E1" alt="Prime Video" loading="lazy">
                    </div>
                    <h3>Prime Video</h3>
                    <p>أفلام حصرية • أمازون ستوديو</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">مكتبة أمازون الضخمة مع إنتاجات حصرية بجودة 4K</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Prime Video', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Prime Video', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Prime Video', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <!-- ===== MUSIC ===== -->
                <div class="digi-card" data-category="music" data-title="Spotify" style="--brand-glow: rgba(30,215,96,0.5);">
                    <span class="card-badge hot">عرض خاص</span>
                    <div class="digi-glow" style="background: rgba(30,215,96,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/spotify/1DB954" alt="Spotify" loading="lazy">
                    </div>
                    <h3>Spotify Premium</h3>
                    <p>بلا إعلانات • تحميل • جودة عالية</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">سبوتيفاي بريميوم حساب خاص بجودة 320kbps</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Spotify', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Spotify', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Spotify', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="music" data-title="Apple Music" style="--brand-glow: rgba(250,36,60,0.5);">
                    <div class="digi-glow" style="background: rgba(250,36,60,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/applemusic/FA243C" alt="Apple Music" loading="lazy">
                    </div>
                    <h3>Apple Music</h3>
                    <p>Lossless • Spatial Audio • 100M أغنية</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">جودة صوت Lossless مع صوت فضائي Spatial Audio</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Apple Music', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Apple Music', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Apple Music', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <!-- ===== DESIGN ===== -->
                <div class="digi-card" data-category="design" data-title="Canva Pro" style="--brand-glow: rgba(0,196,204,0.5);">
                    <span class="card-badge hot">الأهم</span>
                    <div class="digi-glow" style="background: rgba(0,196,204,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/canva/00C4CC" alt="Canva" loading="lazy">
                    </div>
                    <h3>Canva Pro</h3>
                    <p>قوالب Pro • Brand Kit • خلفيات AI</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">كانفا برو مع Brand Kit وإزالة خلفيات AI ومكتبة ضخمة</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Canva Pro', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Canva Pro', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Canva Pro', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="design" data-title="Adobe Creative Cloud" style="--brand-glow: rgba(255,0,0,0.5);">
                    <div class="digi-glow" style="background: rgba(255,0,0,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/adobecreativecloud/FF0000" alt="Adobe CC" loading="lazy">
                    </div>
                    <h3>Adobe CC (كل التطبيقات)</h3>
                    <p>Photoshop • Premiere • Illustrator</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">كل تطبيقات أدوبي بما فيها Premiere و After Effects</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Adobe CC', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Adobe CC', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Adobe CC', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="design" data-title="CapCut Pro" style="--brand-glow: rgba(255,255,255,0.25);">
                    <span class="card-badge new">جديد</span>
                    <div class="digi-glow" style="background: rgba(255,255,255,0.2);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/capcut/ffffff" alt="CapCut" loading="lazy">
                    </div>
                    <h3>CapCut Pro</h3>
                    <p>مونتاج AI • إزالة خلفية • ريلز</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">كاب كات برو مع أدوات AI للمونتاج الاحترافي للريلز</div>
                    <div class="digi-actions">
                        <button onclick="orderService('CapCut Pro', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('CapCut Pro', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('CapCut Pro', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="design" data-title="Envato Elements" style="--brand-glow: rgba(82,196,26,0.5);">
                    <span class="card-badge new">جديد</span>
                    <div class="digi-glow" style="background: rgba(82,196,26,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/envato/52C41A" alt="Envato" loading="lazy">
                    </div>
                    <h3>Envato Elements</h3>
                    <p>ملايين الأصول • قوالب • فيديو • صور</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">Envato Elements: ملايين ملفات الديزاين بترخيص تجاري</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Envato Elements', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Envato Elements', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Envato Elements', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <!-- ===== PRODUCTIVITY ===== -->
                <div class="digi-card" data-category="productivity" data-title="Microsoft 365" style="--brand-glow: rgba(216,59,1,0.5);">
                    <div class="digi-glow" style="background: rgba(216,59,1,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/microsoft365/D83B01" alt="Microsoft 365" loading="lazy">
                    </div>
                    <h3>Microsoft 365</h3>
                    <p>5 أجهزة • 1TB OneDrive • Copilot AI</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">Word, Excel, PowerPoint مع Copilot AI وOneDrive 1TB</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Microsoft 365', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Microsoft 365', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Microsoft 365', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="productivity" data-title="Notion AI" style="--brand-glow: rgba(255,255,255,0.25);">
                    <div class="digi-glow" style="background: rgba(255,255,255,0.2);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/notion/ffffff" alt="Notion" loading="lazy">
                    </div>
                    <h3>Notion Plus + AI</h3>
                    <p>مساحة لامحدودة • AI مدمج • Team</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">Notion Plus مع AI مدمج لكتابة الملاحظات والمشاريع</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Notion AI', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Notion AI', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Notion AI', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <!-- ===== GAMING ===== -->
                <div class="digi-card" data-category="gaming" data-title="Xbox Game Pass" style="--brand-glow: rgba(16,124,16,0.5);">
                    <div class="digi-glow" style="background: rgba(16,124,16,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/xbox/107C10" alt="Xbox" loading="lazy">
                    </div>
                    <h3>Xbox Game Pass Ultimate</h3>
                    <p>400+ لعبة • PC & Console • EA Play</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">مئات الألعاب للكمبيوتر والكونسول مع EA Play مجاناً</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Xbox Game Pass', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Xbox Game Pass', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Xbox Game Pass', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="gaming" data-title="PlayStation Plus" style="--brand-glow: rgba(0,67,156,0.5);">
                    <div class="digi-glow" style="background: rgba(0,67,156,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/playstation/00439C" alt="PlayStation" loading="lazy">
                    </div>
                    <h3>PlayStation Plus</h3>
                    <p>Extra • Premium • ألعاب مجانية شهرية</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">PS Plus Extra مع مكتبة ألعاب ضخمة وLive العب أونلاين</div>
                    <div class="digi-actions">
                        <button onclick="orderService('PlayStation Plus', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('PlayStation Plus', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('PlayStation Plus', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="gaming" data-title="Steam" style="--brand-glow: rgba(26,159,255,0.5);">
                    <span class="card-badge new">جديد</span>
                    <div class="digi-glow" style="background: rgba(26,159,255,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/steam/1a9fff" alt="Steam" loading="lazy">
                    </div>
                    <h3>شراء ألعاب Steam</h3>
                    <p>أي لعبة تختارها • تحويل للحساب</p>
                    <div class="digi-price">حسب اللعبة</div>
                    <div class="digi-tooltip">نشتري لك أي لعبة من متجر Steam ونرسلها لحسابك</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Steam Games', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Steam Games', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Steam Games', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <!-- ===== CLOUD ===== -->
                <div class="digi-card" data-category="cloud" data-title="Google One" style="--brand-glow: rgba(66,133,244,0.5);">
                    <div class="digi-glow" style="background: rgba(66,133,244,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/googledrive/4285F4" alt="Google Drive" loading="lazy">
                    </div>
                    <h3>Google One Drive</h3>
                    <p>100GB → 2TB • مشاركة عائلية</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">Google One من 100GB إلى 2TB مضافة لحسابك</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Google One', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Google One', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Google One', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <!-- ===== LEARNING ===== -->
                <div class="digi-card" data-category="learning" data-title="Udemy" style="--brand-glow: rgba(164,53,240,0.5);">
                    <div class="digi-glow" style="background: rgba(164,53,240,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/udemy/A435F0" alt="Udemy" loading="lazy">
                    </div>
                    <h3>شراء كورسات Udemy</h3>
                    <p>أي كورس تختاره • وصول مدى الحياة</p>
                    <div class="digi-price">حسب الكورس</div>
                    <div class="digi-tooltip">نشتري لك أي كورس على Udemy بأسعار حقيقية</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Udemy Course', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Udemy Course', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Udemy Course', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <!-- ===== SOCIAL ===== -->
                <div class="digi-card" data-category="social" data-title="Meta Verified توثيق" style="--brand-glow: rgba(85,178,255,0.5);">
                    <div class="digi-glow" style="background: rgba(85,178,255,0.4);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/meta/0064F2" alt="Meta" loading="lazy">
                    </div>
                    <h3>توثيق Meta Verified</h3>
                    <p>العلامة الزرقاء • Facebook & Instagram</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">توثيق Meta الرسمي للحصول على العلامة الزرقاء</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Meta Verified', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Meta Verified', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Meta Verified', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="social" data-title="Snapchat Plus" style="--brand-glow: rgba(255,252,0,0.5);">
                    <div class="digi-glow" style="background: rgba(255,252,0,0.35);"></div>
                    <div class="digi-icon brand-icon">
                        <img src="https://cdn.simpleicons.org/snapchat/FFFC00" alt="Snapchat" loading="lazy">
                    </div>
                    <h3>Snapchat+</h3>
                    <p>ميزات حصرية • Badge • Story Rewatch</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-tooltip">سناب بلس مع كل الميزات الحصرية والشارة المميزة</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Snapchat Plus', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Snapchat Plus', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Snapchat Plus', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

                <div class="digi-card" data-category="social" data-title="Social Media Boost متابعين" style="--brand-glow: rgba(225,48,108,0.5);">
                    <div class="digi-glow" style="background: rgba(225,48,108,0.4);"></div>
                    <div class="digi-icon brand-icon" style="gap:4px; flex-wrap:wrap; width:72px; height:72px; padding:8px; border-radius:16px; background:rgba(255,255,255,0.05);">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg" alt="Instagram" loading="lazy" style="width:28px;height:28px;">
                        <img src="https://cdn.simpleicons.org/tiktok/ffffff" alt="TikTok" loading="lazy" style="width:28px;height:28px;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" alt="Facebook" loading="lazy" style="width:28px;height:28px;">
                    </div>
                    <h3>دعم السوشيال ميديا</h3>
                    <p>متابعين • لايكات • مشاهدات</p>
                    <div class="digi-price">حسب العدد</div>
                    <div class="digi-tooltip">نموّ حقيقي لتيك توك، إنستغرام، فيسبوك - متابعين ولايكات</div>
                    <div class="digi-actions">
                        <button onclick="orderService('Social Media Support', 'whatsapp')" class="btn btn-digi"><i class="fa-brands fa-whatsapp" style="color:#25d366;"></i></button>
                        <button onclick="orderService('Social Media Support', 'messenger')" class="btn btn-digi"><i class="fa-brands fa-facebook-messenger" style="color:#0084ff;"></i></button>
                        <button onclick="orderService('Social Media Support', 'telegram')" class="btn btn-digi"><i class="fa-brands fa-telegram" style="color:#0088cc;"></i></button>
                    </div>
                </div>

            </div>
        </section>
        <!-- Market Section Ends Here -->"""

new_text = text[:start_idx] + NEW_SECTION + text[end_idx:]

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print("HTML marketplace section replaced successfully!")
print(f"Old length: {len(text)}, New length: {len(new_text)}")
