import re

html_content = """
        <!-- Market Section Starts Here -->
        <section id="digital-market" class="digital-market fade-in-on-scroll" style="margin-top: 40px;">
            <div class="market-header" style="text-align: center; margin-bottom: 40px;">
                <h2 class="section-title gradient-text glow" style="font-size: 2.5rem; margin-bottom: 10px;">Marketplace الكتالوج الرقمي</h2>
                <p class="text-center text-muted" style="margin-bottom: 25px; font-size: 1.15rem;">ارتقِ بتجربتك الرقمية مع أفضل الاشتراكات والأدوات المدفوعة بالدينار!</p>
                
                <!-- Live Search -->
                <div class="digital-search-container box-glass flex-center" style="max-width: 600px; margin: 0 auto 30px auto; display: flex; align-items: center; padding: 15px 25px; border-radius: 50px;">
                    <i class="fa-solid fa-search" style="font-size: 1.2rem; color: var(--secondary); margin-left: 15px;"></i>
                    <input type="text" id="digitalSearch" placeholder="ابحث عن اشتراك (مثال: Netflix, Canva, ChatGPT)..." oninput="filterDigitalMarket()" style="width: 100%; border: none; background: transparent; color: var(--text); font-size: 1.1rem; outline: none;">
                </div>

                <!-- Sticky Categories -->
                <div class="category-tabs-wrapper" style="position: sticky; top: 70px; z-index: 100; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(15px); padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.05); overflow-x: auto; white-space: nowrap; margin-bottom: 40px; box-shadow: 0 10px 20px rgba(0,0,0,0.2);">
                    <div class="category-tabs" id="marketTabs" style="display: inline-flex; gap: 10px; padding: 0 20px;">
                        <button class="cat-tab active" onclick="selectCategory('all', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">الكل</button>
                        <button class="cat-tab" onclick="selectCategory('ai', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">🤖 ذكاء اصطناعي</button>
                        <button class="cat-tab" onclick="selectCategory('entertainment', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">🎬 ترفيه</button>
                        <button class="cat-tab" onclick="selectCategory('music', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">🎵 موسيقى</button>
                        <button class="cat-tab" onclick="selectCategory('design', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">🎨 تصميم وإبداع</button>
                        <button class="cat-tab" onclick="selectCategory('productivity', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">💼 إنتاجية أعمال</button>
                        <button class="cat-tab" onclick="selectCategory('learning', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">📚 تعليم</button>
                        <button class="cat-tab" onclick="selectCategory('gaming', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">🎮 ألعاب</button>
                        <button class="cat-tab" onclick="selectCategory('cloud', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">☁️ تخزين سحابي</button>
                        <button class="cat-tab" onclick="selectCategory('social', this)" style="padding: 10px 20px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); color: var(--text); cursor: pointer; transition: all 0.3s; font-weight: bold;">🌐 بطاقات ودعم</button>
                    </div>
                </div>
            </div>

            <!-- Standardizing Grid Display -->
            <div class="digital-services-grid" id="marketGrid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
                
                <!-- AI Tools -->
                <div class="digi-card" data-category="ai" data-title="ChatGPT Plus">
                    <div class="badge-popular" style="position: absolute; top: -10px; right: -10px; background: linear-gradient(135deg, #FF416C, #FF4B2B); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; font-weight: bold; box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); z-index: 2;">الأكثر طلباً 🔥</div>
                    <div class="digi-glow" style="background: rgba(16,163,127,0.3);"></div>
                    <div class="digi-icon"><img src="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg" alt="ChatGPT" style="width: 85px; height: 85px; object-fit: contain;"></div>
                    <h3>ChatGPT Plus</h3>
                    <p>النسخة المدفوعة، كتابة أكواد وبحوث وإجابات فورية بدون انتظار.</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                        <button onclick="orderService('ChatGPT Plus', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                        <button onclick="orderService('ChatGPT Plus', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                        <button onclick="orderService('ChatGPT Plus', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                    </div>
                </div>
                <div class="digi-card" data-category="ai" data-title="Gemini Advanced">
                    <div class="digi-glow" style="background: rgba(26,115,232,0.3);"></div>
                    <div class="digi-icon"><img src="https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg" alt="Gemini" style="width: 85px; height: 85px; object-fit: contain;"></div>
                    <h3>Gemini Advanced</h3>
                    <p>نموذج قوقل الذكي القادر على تحليل الصور والبيانات بدقة متناهية.</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                        <button onclick="orderService('Gemini Advanced', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                        <button onclick="orderService('Gemini Advanced', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                        <button onclick="orderService('Gemini Advanced', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                    </div>
                </div>
                <div class="digi-card" data-category="ai" data-title="Claude Pro">
                    <div class="digi-glow" style="background: rgba(217,119,87,0.3);"></div>
                    <div class="digi-icon"><img src="https://cdn.simpleicons.org/anthropic/d97757" alt="Claude" style="width: 85px; height: 85px; object-fit: contain;"></div>
                    <h3>Claude Pro</h3>
                    <p>ممتاز للتحليل الأدبي والملفات الطويلة بشكل خرافي وبلا أخطاء.</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                        <button onclick="orderService('Claude Pro', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                        <button onclick="orderService('Claude Pro', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                        <button onclick="orderService('Claude Pro', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                    </div>
                </div>
                <div class="digi-card" data-category="ai" data-title="Midjourney v6">
                    <div class="badge-discount" style="position: absolute; top: -10px; left: -10px; background: var(--secondary); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; font-weight: bold; box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4); z-index: 2;">-15% للجدد</div>
                    <div class="digi-glow" style="background: rgba(255,255,255,0.2);"></div>
                    <div class="digi-icon"><img src="https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.png" alt="Midjourney" onerror="this.src='https://cdn.simpleicons.org/midjourney/white'" style="width: 85px; height: 85px; object-fit: contain;"></div>
                    <h3>Midjourney V6</h3>
                    <p>مولد صور AI الأقوى عالمياً. عبر ديسكورد وبأعلى دقة V6.</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                        <button onclick="orderService('Midjourney', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                        <button onclick="orderService('Midjourney', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                        <button onclick="orderService('Midjourney', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                    </div>
                </div>

                <!-- Entertainment -->
                <div class="digi-card" data-category="entertainment" data-title="Netflix Premium">
                    <div class="badge-popular" style="position: absolute; top: -10px; right: -10px; background: linear-gradient(135deg, #FF416C, #FF4B2B); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; font-weight: bold; box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); z-index: 2;">الأكثر مبيعاً 🍿</div>
                    <div class="digi-glow" style="background: rgba(229,9,20,0.3);"></div>
                    <div class="digi-icon"><img src="https://cdn.simpleicons.org/netflix/E50914" alt="Netflix" style="width: 85px; height: 85px; object-fit: contain;"></div>
                    <h3>Netflix Premium</h3>
                    <p>حسابات رسمية للمسلسلات والأفلام بجودة 4K شاشة خاصة أو مشتركة.</p>
                    <div class="digi-price">حسب الباقة</div>
                    <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                        <button onclick="orderService('Netflix', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                        <button onclick="orderService('Netflix', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                        <button onclick="orderService('Netflix', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                    </div>
                </div>
                <div class="digi-card" data-category="entertainment" data-title="Disney+">
                     <div class="digi-glow" style="background: rgba(17,60,207,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/disneyplus/white" alt="Disney+" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Disney+</h3>
                     <p>جميع إصدارات مارفل وستار وورز وديزني الأصلية بأعلى جودة.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Disney+', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Disney+', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Disney+', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>
                <div class="digi-card" data-category="entertainment" data-title="Amazon Prime Video">
                     <div class="digi-glow" style="background: rgba(0,168,225,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/primevideo/00A8E1" alt="Prime Video" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Prime Video</h3>
                     <p>مكتبة أفلام أمازون الحصرية مع متعة التصفح وتعدد اللغات.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Prime Video', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Prime Video', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Prime Video', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>

                <!-- Music -->
                <div class="digi-card" data-category="music" data-title="Spotify Premium">
                     <div class="badge-discount" style="position: absolute; top: -10px; left: -10px; background: var(--secondary); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; font-weight: bold; box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4); z-index: 2;">🔥 عرض</div>
                     <div class="digi-glow" style="background: rgba(30,215,96,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/spotify/1ED760" alt="Spotify" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Spotify Premium</h3>
                     <p>موسيقى وبودكاست بلا إعلانات، تحميل للاستماع أوفلاين. حسابك الخاص.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Spotify', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Spotify', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Spotify', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>
                <div class="digi-card" data-category="music" data-title="Apple Music">
                     <div class="digi-glow" style="background: rgba(250,36,60,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/applemusic/FA243C" alt="Apple Music" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Apple Music</h3>
                     <p>جودة صوت نقية (Lossless) واستماع لجميع فنانيك بلا انقطاع.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Apple Music', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Apple Music', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Apple Music', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>

                <!-- Design & Creativity -->
                <div class="digi-card" data-category="design" data-title="Canva Pro">
                     <div class="badge-popular" style="position: absolute; top: -10px; right: -10px; background: linear-gradient(135deg, #FF416C, #FF4B2B); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; font-weight: bold; box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); z-index: 2;">أهم أداة 🎨</div>
                     <div class="digi-glow" style="background: rgba(0,196,204,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/canva/00C4CC" alt="Canva" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Canva Pro</h3>
                     <p>صمم منشوراتك الإحترافية و فيديوهاتك بكل سهولة وتفعيل على حسابك.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Canva Pro', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Canva Pro', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Canva Pro', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>
                <div class="digi-card" data-category="design" data-title="Adobe Creative Cloud">
                     <div class="digi-glow" style="background: rgba(255,0,0,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/adobecreativecloud/FF0000" alt="Adobe" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Adobe CC (كل التطبيقات)</h3>
                     <p>فوتوشوب، إليستريتور، بريمير، والمزيد باشتراك رسمي وآمن.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Adobe CC', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Adobe CC', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Adobe CC', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>

                <!-- Productivity -->
                <div class="digi-card" data-category="productivity" data-title="Microsoft 365">
                     <div class="digi-glow" style="background: rgba(216,59,1,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/microsoft365/D83B01" alt="Microsoft 365" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Microsoft 365</h3>
                     <p>وورد، إكسل، باوربوينت تفعيل أصلي لـ 5 أجهزة بلس 1TB ون درايف.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Microsoft 365', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Microsoft 365', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Microsoft 365', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>
                <div class="digi-card" data-category="productivity" data-title="Notion Pro">
                     <div class="digi-glow" style="background: rgba(255,255,255,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/notion/white" alt="Notion" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Notion Plus / AI</h3>
                     <p>نظم مهامك وملاحظاتك بأقوى أداة إنتاجية في العالم.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Notion', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Notion', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Notion', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>

                <!-- Gaming -->
                <div class="digi-card" data-category="gaming" data-title="Xbox Game Pass">
                     <div class="digi-glow" style="background: rgba(16,124,16,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/xbox/107C10" alt="Xbox" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Xbox Game Pass Ultimate</h3>
                     <p>مئات الألعاب للكمبيوتر والأكس بوكس باشتراك واحد يجدد باطمئنان.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Xbox Game Pass', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Xbox Game Pass', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Xbox Game Pass', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>
                <div class="digi-card" data-category="gaming" data-title="PlayStation Plus">
                     <div class="digi-glow" style="background: rgba(0,67,156,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/playstation/00439C" alt="PlayStation" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>PlayStation Plus</h3>
                     <p>العب أونلاين واستخدم مكتبة ألعاب إكسترا وبريميوم.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('PlayStation Plus', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('PlayStation Plus', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('PlayStation Plus', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>

                <!-- Cloud Storage -->
                <div class="digi-card" data-category="cloud" data-title="Google One Drive">
                     <div class="digi-glow" style="background: rgba(66,133,244,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/googledrive/4285F4" alt="Google Drive" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Google One / Drive</h3>
                     <p>مساحة تخزينية سحابية بدءا من 100GB إلى 2TB مضافة لحسابك الشخصي.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Google Drive', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Google Drive', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Google Drive', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>
                
                <!-- Learning -->
                <div class="digi-card" data-category="learning" data-title="Udemy Courses">
                     <div class="digi-glow" style="background: rgba(164,53,240,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/udemy/A435F0" alt="Udemy" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Udemy (شراء كورسات)</h3>
                     <p>نشتري لك أي دورة تفضلها على يوديمي وتدخل حسابك فوراً.</p>
                     <div class="digi-price">حسب دورة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Udemy Course', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Udemy Course', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Udemy Course', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>

                <!-- Social & Support -->
                <div class="digi-card" data-category="social" data-title="Meta Verified">
                     <div class="digi-glow" style="background: rgba(85,178,255,0.3);"></div>
                     <div class="digi-icon">
                         <svg viewBox="0 0 24 24" width="85" height="85">
                             <defs>
                                 <linearGradient id="metaVerifyv2" x1="0%" y1="0%" x2="0%" y2="100%">
                                     <stop offset="0%" stop-color="#55B2FF"/>
                                     <stop offset="100%" stop-color="#0064F2"/>
                                 </linearGradient>
                                 <filter id="badgeShadowv2" x="-20%" y="-20%" width="140%" height="140%">
                                     <feDropShadow dx="0" dy="1.5" stdDeviation="1" flood-color="#000000" flood-opacity="0.3"/>
                                 </filter>
                             </defs>
                             <path d="M12 1.488c-.687 0-1.32.413-1.631 1.056L9.6 4.394 7.6 4.606a1.82 1.82 0 0 0-1.631 1.813v2.013l-1.85 1.062a1.818 1.818 0 0 0 0 3.15l1.85 1.063v2.013c0 .925.706 1.706 1.631 1.813l2 .212.769 1.85c.312.644.944 1.056 1.631 1.056s1.32-.412 1.631-1.056l.769-1.85 2-.212c.925-.107 1.631-.888 1.631-1.813v-2.013l1.85-1.063a1.818 1.818 0 0 0 0-3.15l-1.85-1.062V6.419c0-.925-.706-1.706-1.631-1.813l-2-.212-.769-1.85A1.82 1.82 0 0 0 12 1.488zm-1.825 11.23-.002.002-3.12-3.12c-.294-.294-.294-.768 0-1.06.294-.293.768-.293 1.06 0l2.59 2.59 6.23-6.23c.294-.293.768-.293 1.06 0 .294.294.294.768 0 1.06l-6.76 6.76c-.292.294-.767.294-1.058 0z" fill="url(#metaVerifyv2)" filter="url(#badgeShadowv2)"/>
                         </svg>
                     </div>
                     <h3>توثيق حسابات Meta</h3>
                     <p>احصل على العلامة الزرقاء الرسمية لصفحاتك على فيسبوك وإنستغرام.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Meta Verified', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Meta Verified', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Meta Verified', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>
                <div class="digi-card" data-category="social" data-title="Snapchat Plus">
                     <div class="digi-glow" style="background: rgba(255,252,0,0.3);"></div>
                     <div class="digi-icon"><img src="https://cdn.simpleicons.org/snapchat/FFFC00" alt="Snapchat" style="width: 85px; height: 85px; object-fit: contain;"></div>
                     <h3>Snapchat Plus</h3>
                     <p>تفعيل كافة ميزات سناب شات بلس بوضع آمن ورسمي.</p>
                     <div class="digi-price">حسب الباقة</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Snapchat Plus', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Snapchat Plus', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Snapchat Plus', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>
                <div class="digi-card" data-category="social" data-title="Social Media Boost">
                     <div class="digi-glow" style="background: linear-gradient(135deg, #E1306C, #1877F2, #ff0050); filter: blur(40px);"></div>
                     <div class="digi-icon" style="background: transparent; border: none; box-shadow: none; display: flex; gap: 5px; height: 85px; width: 85px; align-items: center; justify-content: center;">
                         <img src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg" alt="Instagram" style="width: 30px; height: 30px;">
                         <img src="https://cdn.simpleicons.org/tiktok/white" alt="TikTok" style="width: 30px; height: 30px; filter: drop-shadow(0 0 2px rgba(255,255,255,0.8));">
                         <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" alt="Facebook" style="width: 30px; height: 30px;">
                     </div>
                     <h3>دعم وتكبير الحسابات</h3>
                     <p>متابعين، لايكات ومشاهدات عبر تيك توك، فيسبوك، انستغرام.</p>
                     <div class="digi-price">حسب العدد</div>
                     <div class="digi-actions" style="display: flex; gap: 10px; width: 100%;">
                         <button onclick="orderService('Social Media Support', 'whatsapp')" class="btn btn-digi" style="flex: 1; border-color: rgba(37, 211, 102, 0.5);"><i class="fa-brands fa-whatsapp" style="color: #25d366;"></i></button>
                         <button onclick="orderService('Social Media Support', 'messenger')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 132, 255, 0.5);"><i class="fa-brands fa-facebook-messenger" style="color: #0084ff;"></i></button>
                         <button onclick="orderService('Social Media Support', 'telegram')" class="btn btn-digi" style="flex: 1; border-color: rgba(0, 136, 204, 0.5);"><i class="fa-brands fa-telegram" style="color: #0088cc;"></i></button>
                     </div>
                </div>
            </div>
        </section>
        <!-- Market Section Ends Here -->
"""

with open("e:/KOUKI SHOP/index.html", "r", encoding="utf-8") as f:
    original = f.read()

start_marker = r'<p class="text-center text-muted fade-in-on-scroll" style="margin-bottom: 40px; font-size: 1.15rem;">ارتقِ بتجربتك الرقمية.*?</section>'
new_content = re.sub(start_marker, html_content, original, flags=re.DOTALL)

with open("e:/KOUKI SHOP/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Patch applied to index.html successfully!")
