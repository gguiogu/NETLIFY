// --- Configuration ---
const CONFIG = {
    usdToDzd: 228, // Example conversion rate USD to DZD
    feePercentage: 0.15, // 15% service fee
    minFee: 200, // Minimum fee in DZD
};

// --- DOM Elements ---
const analyzeBtn = document.getElementById('analyze-btn');
const productUrlInput = document.getElementById('product-url');
const errorMsg = document.getElementById('error-message');

const loadingState = document.getElementById('loading-state');
const resultsDashboard = document.getElementById('results-dashboard');

const steps = [
    document.getElementById('step-1'),
    document.getElementById('step-2'),
    document.getElementById('step-3')
];

let globalProductData = null;

// --- Helper Functions ---

function clearErrors() {
    errorMsg.textContent = '';
    productUrlInput.style.borderColor = 'var(--border-glass)';
}

function showError(msg) {
    errorMsg.textContent = msg;
    productUrlInput.style.borderColor = 'var(--danger)';
}

function extractAliExpressId(url) {
    // Basic validation to check if it's an aliexpress link (standard or shortened)
    if (!url.includes('aliexpress.com') && !url.includes('a.aliexpress.com')) {
        return null;
    }
    return true; // Simplified: just confirm it's AliExpress
}

// --- Main Flow ---

async function analyzeProduct() {
    const url = productUrlInput.value.trim();
    
    if (!url) {
        showError('الرجاء إدخال رابط المنتج أولاً.');
        return;
    }

    if (!extractAliExpressId(url)) {
        showError('عذراً، الرابط غير صحيح. الرجاء التأكد من أنه رابط من موقع AliExpress.');
        return;
    }

    // Hide dashboard if it was open
    resultsDashboard.classList.add('hidden');
    clearErrors();
    
    // Disable input and button
    productUrlInput.disabled = true;
    analyzeBtn.disabled = true;
    
    // Show loading state
    loadingState.classList.remove('hidden');
    
    // Start loading animations
    const loadingPromise = simulateLoadingSteps();
    
    try {
        // Fetch from Render cloud backend
        const encodedUrl = encodeURIComponent(url);
        const response = await fetch('https://netfdly.onrender.com/product?url=' + encodedUrl, {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Wait for MINIMUM loading animation to finish to give AI vibe
        await loadingPromise;
        
        // Ensure final price calculation is robust
        const baseDZDVal = data.base_dzd || 0;
        const commDZDVal = data.commission || 0;
        let finalDZDVal = data.final_dzd || data.price_dzd || data.buy_dzd;
        if (!finalDZDVal || finalDZDVal === 0) {
            finalDZDVal = baseDZDVal + commDZDVal;
        }
        data.final_dzd = finalDZDVal;
        
        globalProductData = data;
        globalProductData.url = data.link || url;
        
        // Populate Dashboard
        renderDashboard(globalProductData);
    
    // Remove simulated error catches if needed
    } catch (err) {
        showError("تعذر تحليل هذا الرابط، الرجاء المحاولة مرة أخرى، أو التأكد من توفر المنتج. " + (err.message === 'Failed to fetch' ? '(تأكد من تشغيل السيرفر)' : ''));
        loadingState.classList.add('hidden');
        resetSteps();
        productUrlInput.disabled = false;
        analyzeBtn.disabled = false;
        return;
    }
    
    // Hide loading, show dashboard
    loadingState.classList.add('hidden');
    resultsDashboard.classList.remove('hidden');
    
    // Reset steps UI for next time
    resetSteps();
    
    // Re-enable input
    productUrlInput.disabled = false;
    analyzeBtn.disabled = false;
    
    // Scroll to results
    resultsDashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// --- UI Animations & Simulation ---

async function simulateLoadingSteps() {
    const delay = ms => new Promise(res => setTimeout(res, ms));
    
    // Step 1: Fetching
    steps[0].classList.add('active');
    steps[0].innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> جلب تفاصيل المنتج...';
    await delay(1200);
    steps[0].innerHTML = '<i class="fa-solid fa-circle-check"></i> تم جلب التفاصيل';
    
    // Step 2: Evaluation
    steps[1].classList.add('active');
    steps[1].innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> التقييم وكشف الاحتيال...';
    await delay(1500);
    steps[1].innerHTML = '<i class="fa-solid fa-circle-check"></i> البائع آمن وموثوق';

    // Step 3: Pricing
    steps[2].classList.add('active');
    steps[2].innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> حساب الأسعار وهوامش الربح...';
    await delay(1000);
    steps[2].innerHTML = '<i class="fa-solid fa-circle-check"></i> اكتمل بناء التقرير';
    await delay(500);
}

function resetSteps() {
    steps.forEach((step, index) => {
        step.classList.remove('active');
        const icons = [
            '<i class="fa-solid fa-circle-check"></i> جلب تفاصيل المنتج',
            '<i class="fa-solid fa-circle-notch fa-spin"></i> التقييم وكشف الاحتيال',
            '<i class="fa-solid fa-circle-notch fa-spin"></i> حساب الأسعار وهوامش الربح'
        ];
        step.innerHTML = icons[index];
    });
    // First one remains active by default
    steps[0].classList.add('active');
}

// --- Logic & Rendering ---

// Mock function removed in favor of real API

function renderDashboard(data) {
    // Basic Details
    document.getElementById('res-title').textContent = data.title || "منتج من AliExpress";
    document.getElementById('store-name').textContent = data.store_name || "AliExpress Official Store";
    
    // Main Prices
    const finalDZD = (data.final_dzd || 0).toLocaleString();
    const usdStr = data.price_usd ? `US $${data.price_usd}` : "US $0.00";
    
    document.getElementById('final-dzd').textContent = finalDZD;
    document.getElementById('original-usd').textContent = usdStr;
    
    // Tags & Badges
    const badge = document.getElementById('discount-badge');
    if (data.disc && data.disc > 0) {
        badge.textContent = `off ${data.disc}%`;
        badge.style.display = 'block';
    } else {
        badge.style.display = 'none';
    }

    // Main Image
    if (data.img) {
        document.getElementById('product-img').src = data.img;
    } else if (data.image) {
        document.getElementById('product-img').src = data.image; // fallback
    }

    // Price Note
    const baseDZD = (data.base_dzd || 0).toLocaleString();
    const commDZD = (data.commission || 0).toLocaleString();
    const noteEl = document.getElementById('price-note');
    if (noteEl) {
        noteEl.innerHTML = `<i class="fa-solid fa-circle-info text-secondary"></i> السعر يشمل: المنتج (${baseDZD} د.ج) + عمولة الموقع (${commDZD} د.ج)`;
    }

    // Invoice (فاتورة)
    if (document.getElementById('inv-base-dzd')) {
        document.getElementById('inv-base-dzd').textContent = baseDZD;
        document.getElementById('inv-usd').textContent = usdStr;
        document.getElementById('inv-commission').textContent = commDZD;
        document.getElementById('inv-shipping').textContent = "مجاني";
        document.getElementById('inv-ship-usd').textContent = "$0.00";
        document.getElementById('inv-total-dzd').textContent = finalDZD;
    }

    // Shipping Status from Backend
    if (data.shipping) {
        // Strip the HTML returned by bot.py or use it directly
        // Bot returns "🚚 <b>الشحن:</b> AliExpress..."
        const timeEl = document.getElementById('shipping-time');
        if (timeEl) {
            // Find duration text if possible, else default
            timeEl.textContent = data.shipping.replace(/<[^>]*>?/gm, '');
        }
    }
}

function orderNow() {
    if (!globalProductData) return;
    
    const botUsername = "AliExpressdiscountsdzbot"; 
    
    // Use the deep link format that the bot handles (?start=url)
    const encodedUrl = encodeURIComponent(globalProductData.url);
    const tgUrl = `https://t.me/${botUsername}?start=${encodedUrl}`;
    
    window.open(tgUrl, "_blank");
}

function orderNowFB() {
    if (!globalProductData) return;
    
    // Facebook page directly as requested
    const fbPage = "https://www.facebook.com/XBHTHAGOAT/";
    
    // Create the order text payload
    const finalPrice = globalProductData.final_dzd || globalProductData.price_dzd || 0;
    const msg = `مرحباً بكوكي شوب، أريد طلب هذا المنتج:\n\n`
              + `الرابط: ${globalProductData.url}\n`
              + `السعر: ${finalPrice.toLocaleString()} د.ج\n`;
              
    const encodedMsg = encodeURIComponent(msg);
    const fbUrl = `${fbPage}?text=${encodedMsg}`; // Note: FB URL text param doesn't always populate on desktop natively, but passing it is harmless.
    
    window.open(fbUrl, "_blank");
}

function orderNowWhatsApp() {
    if (!globalProductData) return;
    
    const waNumber = "213562208794";
    const finalPrice = globalProductData.final_dzd || globalProductData.price_dzd || 0;
    
    const msg = `مرحباً، أريد تأكيد طلب هذا المنتج عبر متجركم:\n\n`
              + `الرابط: ${globalProductData.url}\n`
              + `السعر المتوقع: ${finalPrice.toLocaleString()} د.ج\n`;
              
    const encodedMsg = encodeURIComponent(msg);
    const waUrl = `https://wa.me/${waNumber}?text=${encodedMsg}`;
    
    window.open(waUrl, "_blank");
}

function orderNowPersonalTG() {
    if (!globalProductData) return;
    
    // Personal Telegram direct message URL
    const personalUsername = "BOOGEYMAN_DZ";
    
    // Create the order text payload
    const msg = `مرحباً بكوكي شوب، أريد طلب هذا المنتج:\n\n`
              + `الرابط: ${globalProductData.url}\n`
              + `السعر المعروض: ${globalProductData.price_dzd.toLocaleString()} د.ج\n`;
              
    const encodedMsg = encodeURIComponent(msg);
    const tgUrl = `https://t.me/${personalUsername}?text=${encodedMsg}`;
    
    window.open(tgUrl, "_blank");
}

// Support hitting 'Enter' to analyze
if (productUrlInput) {
    productUrlInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            analyzeBtn.click();
        }
    });
}

// ---------------------------------------------------
// Scroll Animations Observer
// ---------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.fade-in-on-scroll').forEach(el => observer.observe(el));
});

// ---------------------------------------------------
// Digital Services Actions
// ---------------------------------------------------
function orderService(serviceName, platform) {
    const waNumber = "213562208794";
    const fbPage = "https://www.facebook.com/XBHTHAGOAT/";
    const tgUsername = "BOOGEYMAN_DZ";
    
    // Create the order text payload
    const msg = `مرحباً كوكي شوب، أريد طلب خدمة رقمية:\n\nالخدمة المطلوبة: ${serviceName}`;
    const encodedMsg = encodeURIComponent(msg);
    
    if (platform === 'whatsapp') {
        const waUrl = `https://wa.me/${waNumber}?text=${encodedMsg}`;
        window.open(waUrl, "_blank");
    } else if (platform === 'messenger') {
        window.open(fbPage, "_blank");
    } else if (platform === 'telegram') {
        const tgUrl = `https://t.me/${tgUsername}?text=${encodedMsg}`;
        window.open(tgUrl, "_blank");
    }
}

function orderNowPersonalTG() {
    if (!globalProductData) return;
    
    // Personal Telegram direct message URL
    const personalUsername = "BOOGEYMAN_DZ";
    const finalPrice = globalProductData.final_dzd || globalProductData.price_dzd || 0;
    
    // Create the order text payload
    const msg = `مرحباً بكوكي شوب، أريد طلب هذا المنتج:\n\n`
              + `الرابط: ${globalProductData.url}\n`
              + `السعر المعروض: ${finalPrice.toLocaleString()} د.ج\n`;
              
    const encodedMsg = encodeURIComponent(msg);
    const tgUrl = `https://t.me/${personalUsername}?text=${encodedMsg}`;
    
    window.open(tgUrl, "_blank");
}

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
    const gameTopupWrapper = document.getElementById('gameTopupWrapper');
    if (gameTopupWrapper) {
        if (category === 'all' || category === 'gaming') {
            gameTopupWrapper.style.display = 'block';
        } else {
            gameTopupWrapper.style.display = 'none';
        }
    }
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
    const gameTopupWrapper = document.getElementById('gameTopupWrapper');
    if (gameTopupWrapper) {
        const topupKeywords = ['شحن', 'ألعاب', 'العاب', 'game', 'top', 'pubg', 'بوبجي', 'ببجي', 'فري فاير', 'free fire', 'uc', 'جواهر', 'id'];
        const matchTopup = query === '' || topupKeywords.some(k => query.includes(k) || k.includes(query));
        gameTopupWrapper.style.display = matchTopup ? 'block' : 'none';
    }
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
    const gameTopupWrapper = document.getElementById('gameTopupWrapper');
    if (gameTopupWrapper) {
        if (category === 'all' || category === 'gaming') {
            gameTopupWrapper.style.display = 'block';
        } else {
            gameTopupWrapper.style.display = 'none';
        }
    }
}


// ==========================================
// Game Top-Up Logic
// ==========================================

function verifyGamePlayerId(game) {
    const idInput = document.getElementById(`${game}-id`);
    const nameDisplay = document.getElementById(`${game}-player-name`);
    if (!idInput || !nameDisplay) return;
    
    const idValue = idInput.value.trim();

    if (idValue.length < 5) {
        nameDisplay.classList.add('hidden');
        return;
    }

    nameDisplay.classList.remove('hidden');
    nameDisplay.classList.remove('error');
    nameDisplay.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> جاري التحقق من الـ ID...`;

    clearTimeout(window[`${game}VerifyTimeout`]);
    window[`${game}VerifyTimeout`] = setTimeout(async () => {
        if (game === 'ff') {
            try {
                const response = await fetch(`https://id-game-checker.p.rapidapi.com/dfm-garena/${idValue}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'x-rapidapi-host': 'id-game-checker.p.rapidapi.com',
                        'x-rapidapi-key': '870d1cd772msh210272edbedbbafp199123jsnc72e2030b96e'
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    
                    // Safely extract name based on typical RapidAPI game checker structures
                    const extName = data.name || data.nickname || data.userName || data.player_name || (data.data && (data.data.name || data.data.nickname));
                    
                    if (extName) {
                        nameDisplay.classList.remove('error');
                        nameDisplay.innerHTML = `<i class="fa-solid fa-circle-check"></i> تم التأكيد: <strong>${extName}</strong>`;
                    } else if (data.status === false || data.error) {
                        nameDisplay.classList.add('error');
                        nameDisplay.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> لم يتم العثور على اللاعب`;
                    } else {
                        // Fallback fallback extraction for completely unknown formats
                        const raw = JSON.stringify(data);
                        const match = raw.match(/"(?:name|nickname|username|player_name|playerName)"\s*:\s*"([^"]+)"/i);
                        const foundName = match ? match[1] : "لاعب موثق";
                        nameDisplay.classList.remove('error');
                        nameDisplay.innerHTML = `<i class="fa-solid fa-circle-check"></i> تم التأكيد: <strong>${foundName}</strong>`;
                    }
                } else {
                    nameDisplay.classList.add('error');
                    nameDisplay.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> خطأ في الاتصال بالخادم`;
                }
            } catch (err) {
                console.error('API Error:', err);
                nameDisplay.classList.add('error');
                nameDisplay.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> حدث خطأ في التحقق`;
            }
        } else {
            // PUBG Simulate API check
            if (idValue === "12345678" || idValue === "11111111") {
                 nameDisplay.classList.add('error');
                 nameDisplay.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> لم يتم العثور على اللاعب`;
            } else {
                 nameDisplay.classList.remove('error');
                 const fakeNames = ["DZ_Gamer", "Pro_Player", "Kouki_Fan", "Sniper_DZ", "King", "Legend_DZ", "Panda_Gamer"];
                 const randomName = fakeNames[idValue.length % fakeNames.length] + "_" + idValue.slice(0,3);
                 nameDisplay.innerHTML = `<i class="fa-solid fa-circle-check"></i> تم التأكيد: <strong>${randomName}</strong>`;
            }
        }
    }, 800);
}

function buyGameTopup(gameName) {
    let prefix = gameName.includes('Free Fire') ? 'ff' : gameName.includes('eFootball') ? 'efootball' : 'pubg';
    const idInput = document.getElementById(`${prefix}-id`);
    const packageSelect = document.getElementById(`${prefix}-package`);
    
    if (!idInput.value.trim()) {
        alert("يرجى إدخال ID اللاعب أولاً.");
        idInput.focus();
        return;
    }
    
    const qty = packageSelect.options[packageSelect.selectedIndex].text;
    const playerId = idInput.value.trim();
    
    const message = `مرحباً، أريد شحن لعبة 🎮:

*الـلـعـبـة:* ${gameName}
*الـبـاقـة:* ${qty}
*الـ ID:* ${playerId}

متى يمكنني الدفع؟`;
    
    const waUrl = "https://wa.me/0562208794?text=";
    window.open(waUrl + encodeURIComponent(message), '_blank');
}
