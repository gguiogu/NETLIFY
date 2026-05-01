import os

html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kouki Shop SaaS</title>
    
    <!-- Fonts & Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">

    <!-- Tailwind CSS (CDN for Development) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              bg: "#0B0F1A",
              surface: "rgba(17,24,39,0.6)",
              primary: "#4F46E5",
              accent: "#22D3EE",
            },
            boxShadow: {
              glow: "0 0 30px rgba(79,70,229,0.25)",
              glowCyan: "0 0 30px rgba(34,211,238,0.25)",
            },
            fontFamily: {
              arabic: ['Cairo', 'sans-serif'],
            }
          }
        }
      }
    </script>
    <style type="text/tailwindcss">
      @layer utilities {
        .text-gradient {
          @apply bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent;
        }
      }
      body {
        font-family: 'Cairo', sans-serif;
        background-color: #0B0F1A;
        color: white;
      }
      ::-webkit-scrollbar { width: 8px; }
      ::-webkit-scrollbar-track { background: #0B0F1A; }
      ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }
      ::-webkit-scrollbar-thumb:hover { background: rgba(34,211,238,0.5); }
    </style>

    <!-- React & ReactDOM -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>

    <!-- React Router -->
    <script crossorigin src="https://unpkg.com/@remix-run/router@1.16.1/dist/router.umd.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-router@6.23.1/dist/umd/react-router.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-router-dom@6.23.1/dist/umd/react-router-dom.production.min.js"></script>

    <!-- Framer Motion -->
    <script src="https://unpkg.com/framer-motion@10.16.4/dist/framer-motion.js"></script>

    <!-- Babel for in-browser JSX parsing -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;
        const { HashRouter, Routes, Route, Link, useLocation } = window.ReactRouterDOM;
        const { motion, AnimatePresence } = window.Motion;

        // ==========================================
        // SHARED COMPONENTS
        // ==========================================
        
        function Button({ children, onClick, className = "", type = "button" }) {
            return (
                <motion.button
                    type={type}
                    onClick={onClick}
                    whileTap={{ scale: 0.97 }}
                    whileHover={{ scale: 1.03 }}
                    className={`px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-accent shadow-glow font-bold text-white transition-all flex items-center justify-center gap-2 ${className}`}
                >
                    {children}
                </motion.button>
            );
        }

        function Card({ children, className = "" }) {
            return (
                <motion.div
                    whileHover={{ y: -8, scale: 1.01 }}
                    transition={{ duration: 0.3 }}
                    className={`bg-surface backdrop-blur-xl border border-white/5 rounded-2xl p-6 shadow-lg hover:shadow-glowCyan transition-all overflow-hidden relative ${className}`}
                >
                    {children}
                </motion.div>
            );
        }

        function PageWrapper({ children, route }) {
            return (
                <motion.div
                    key={route}
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -12 }}
                    transition={{ duration: 0.35, ease: "easeOut" }}
                >
                    {children}
                </motion.div>
            );
        }

        function Layout({ children }) {
            return (
                <div className="min-h-screen relative overflow-hidden flex flex-col">
                    <div className="fixed inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(79,70,229,0.15),transparent)] pointer-events-none" />
                    <div className="fixed inset-0 bg-[radial-gradient(circle_at_80%_80%,rgba(34,211,238,0.12),transparent)] pointer-events-none" />
                    
                    <header className="relative z-20 container mx-auto px-4 py-6 flex justify-between items-center border-b border-white/5 backdrop-blur-md bg-bg/50 sticky top-0">
                        <Link to="/" className="flex items-center gap-3 group">
                            <img src="logo.png" alt="Kouki Shop Logo" className="w-12 h-12 object-contain group-hover:scale-110 transition-transform" />
                            <span className="text-xl font-bold tracking-wide">Kouki <span className="text-gradient">Shop</span></span>
                        </Link>
                        <nav className="hidden md:flex gap-8 font-semibold">
                            <Link to="/shopping" className="hover:text-accent transition-colors">تسوق عالمي</Link>
                            <Link to="/digital" className="hover:text-accent transition-colors">خدمات رقمية</Link>
                            <Link to="/gaming" className="hover:text-accent transition-colors">شحن ألعاب</Link>
                        </nav>
                    </header>

                    <main className="relative z-10 container mx-auto px-4 py-10 flex-grow">
                        {children}
                    </main>

                    <footer className="relative z-10 border-t border-white/5 bg-surface/50 mt-auto backdrop-blur-md">
                        <div className="container mx-auto px-4 py-12">
                            <div className="grid md:grid-cols-3 gap-8 text-center md:text-right text-white/70 mb-8 border-b border-white/5 pb-8">
                                <div>
                                    <h4 className="text-lg font-bold text-white mb-4">من نحن</h4>
                                    <p className="mb-2">متجر كوكي بوابتكم الرقمية للتسوق من المتاجر العالمية.</p>
                                    <p className="text-sm">ولاية خنشلة، بلدية قايس، حي الأنوار، شقة 104</p>
                                </div>
                                <div>
                                    <h4 className="text-lg font-bold text-white mb-4">روابط سريعة</h4>
                                    <ul className="space-y-2">
                                        <li><Link to="/shopping" className="hover:text-accent">التسوق العالمي</Link></li>
                                        <li><Link to="/digital" className="hover:text-accent">الخدمات الرقمية</Link></li>
                                        <li><Link to="/gaming" className="hover:text-accent">شحن ألعاب</Link></li>
                                    </ul>
                                </div>
                                <div>
                                    <h4 className="text-lg font-bold text-white mb-4">تواصل معنا</h4>
                                    <p className="mb-2">واتساب: 0562208794</p>
                                    <p className="mb-2">إنستغرام: @abdelkarim_rem</p>
                                    <p>تيليجرام: @BOOGEYMAN_DZ</p>
                                </div>
                            </div>
                            <div className="text-center text-white/60 flex flex-col md:flex-row justify-between items-center">
                                <p>Kouki Shop © 2026 - منصتك الأولى في الجزائر</p>
                                <div className="flex gap-6 mt-4 md:mt-0">
                                    <a href="#" className="hover:text-accent transition-colors"><i className="fa-brands fa-facebook fa-xl"></i></a>
                                    <a href="#" className="hover:text-accent transition-colors"><i className="fa-brands fa-instagram fa-xl"></i></a>
                                    <a href="#" className="hover:text-accent transition-colors"><i className="fa-brands fa-tiktok fa-xl"></i></a>
                                    <a href="#" className="hover:text-accent transition-colors"><i className="fa-brands fa-telegram fa-xl"></i></a>
                                </div>
                            </div>
                        </div>
                    </footer>
                </div>
            );
        }

        // ==========================================
        // NEW SECTIONS
        // ==========================================

        function AdditionalServices() {
            return (
                <div className="my-20">
                    <h2 className="text-3xl font-bold text-center mb-4">خدمات <span className="text-gradient">إضافية</span></h2>
                    <p className="text-center text-white/70 mb-10">بالإضافة لخدمة الوساطة التجارية يقدم لكم متجر Kouki Shop:</p>
                    <div className="grid md:grid-cols-3 gap-6">
                        <Card className="text-center group">
                            <div className="w-16 h-16 mx-auto rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
                                <i className="fa-solid fa-code"></i>
                            </div>
                            <h3 className="text-xl font-bold mb-2">إنشاء المواقع</h3>
                            <p className="text-white/60">إنشاء المواقع وتصميم المتاجر الالكترونية الاحترافية.</p>
                        </Card>
                        <Card className="text-center group">
                            <div className="w-16 h-16 mx-auto rounded-full bg-pink-500/20 text-pink-400 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
                                <i className="fa-solid fa-bullhorn"></i>
                            </div>
                            <h3 className="text-xl font-bold mb-2">عمل إعلانات</h3>
                            <p className="text-white/60">إعلانات فيسبوك وإنستغرام ممولة (Sponsoring) لزيادة مبيعاتك.</p>
                        </Card>
                        <Card className="text-center group">
                            <div className="w-16 h-16 mx-auto rounded-full bg-green-500/20 text-green-400 flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
                                <i className="fa-solid fa-briefcase"></i>
                            </div>
                            <h3 className="text-xl font-bold mb-2">خدمات Freelance</h3>
                            <p className="text-white/60">خدمات Freelance متنوعة واحترافية تلبي جميع احتياجاتك.</p>
                        </Card>
                    </div>
                </div>
            );
        }

        function CommissionTable() {
            const tiers = [
                { range: "تحت 3$", fee: "100 د.ج" },
                { range: "3$ - 5$", fee: "150 د.ج" },
                { range: "5$ - 11$", fee: "300 د.ج" },
                { range: "11$ - 15$", fee: "400 د.ج" },
                { range: "15$ - 18$", fee: "500 د.ج" },
                { range: "18$ - 22$", fee: "600 د.ج" },
                { range: "22$ - 25$", fee: "700 د.ج" },
                { range: "25$ - 32$", fee: "800 د.ج" },
                { range: "32$ - 38$", fee: "900 د.ج" },
                { range: "38$ - 44$", fee: "1000 د.ج" },
                { range: "44$ - 62$", fee: "1200 د.ج" },
                { range: "62$ - 70$", fee: "1300 د.ج" },
                { range: "70$ - 80$", fee: "1500 د.ج" },
                { range: "80$ - 90$", fee: "1700 د.ج" },
                { range: "90$ - 100$", fee: "1900 د.ج" },
                { range: "100$ - 120$", fee: "2100 د.ج" },
                { range: "120$ - 160$", fee: "2300 د.ج" },
                { range: "160$ - 200$", fee: "2500 د.ج" },
                { range: "فوق 200$", fee: "قابلة للتفاوض" }
            ];

            return (
                <div className="my-20 max-w-4xl mx-auto">
                    <h2 className="text-3xl font-bold text-center mb-4">جدول <span className="text-gradient">العمولات</span></h2>
                    <p className="text-center text-white/70 mb-10">أسعار شفافة • هيكل تسعير بسيط وعادل</p>
                    <Card className="p-0 overflow-hidden">
                        <div className="grid grid-cols-2 bg-primary/20 p-4 font-bold text-lg text-center border-b border-white/10">
                            <div>سعر المنتج ($)</div>
                            <div>عمولة المتجر (د.ج)</div>
                        </div>
                        <div className="max-h-96 overflow-y-auto">
                            {tiers.map((tier, idx) => (
                                <div key={idx} className={`grid grid-cols-2 p-3 text-center ${idx % 2 === 0 ? 'bg-white/5' : ''} hover:bg-white/10 transition-colors`}>
                                    <div className="font-semibold">{tier.range}</div>
                                    <div className="text-accent">{tier.fee}</div>
                                </div>
                            ))}
                        </div>
                    </Card>
                </div>
            );
        }

        function HowToBuy() {
            return (
                <div className="my-20">
                    <h2 className="text-3xl font-bold text-center mb-4">خطوات <span className="text-gradient">الشراء</span></h2>
                    <p className="text-center text-white/70 mb-10">ماعليك غير ترسلنا الرابط وخلي الباقي علينا 😊👌</p>
                    <div className="grid md:grid-cols-4 gap-6 relative">
                        <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-gradient-to-r from-primary to-accent -z-10 -translate-y-1/2 opacity-30"></div>
                        {[
                            { num: "1", title: "اختر المنتج", desc: "ادخل لموقع Aliexpress او اي موقع يدعم الشحن للجزائر", icon: "fa-magnifying-glass" },
                            { num: "2", title: "ارسل الرابط", desc: "ارسل لنا الرابط عبر بوت التيليجرام او فيسبوك", icon: "fa-mobile-screen" },
                            { num: "3", title: "ادفع CCP", desc: "قم بالدفع والتأكيد عبر CCP او BARIDIMOB", icon: "fa-credit-card" },
                            { num: "4", title: "استلم طلبك", desc: "يجيبهالك ساعي البريد للدار او تستلمها من البريد", icon: "fa-box-open" }
                        ].map((step, idx) => (
                            <div key={idx} className="relative text-center">
                                <div className="w-16 h-16 mx-auto rounded-2xl bg-surface border border-primary/30 flex items-center justify-center text-2xl text-accent shadow-glowCyan mb-4 relative z-10">
                                    <i className={`fa-solid ${step.icon}`}></i>
                                </div>
                                <h3 className="text-xl font-bold mb-2">{step.title}</h3>
                                <p className="text-white/60 text-sm">{step.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            );
        }

        function RecentDeliveries() {
            const deliveries = [
                { title: "سماعات لينوفو بلوتوث", status: "تم التوصيل", client: "كريم (سطيف)", time: "وصلت في 18 يوم", icon: "fa-headphones", color: "text-green-400" },
                { title: "ساعة ذكية LIGE 2024", status: "تم التوصيل", client: "يونس (وهران)", time: "وصلت في 22 يوم", icon: "fa-clock", color: "text-green-400" },
                { title: "شاحن Baseus سريع", status: "في طريقها للزبون", client: "رفيدة (خنشلة)", time: "متوقع في غضون 5 أيام", icon: "fa-plug", color: "text-yellow-400" }
            ];

            return (
                <div className="my-20">
                    <h2 className="text-3xl font-bold text-center mb-4">طلبات عملائنا <span className="text-gradient">(وصلت بنجاح) 📦✨</span></h2>
                    <p className="text-center text-white/70 mb-10">شاهد كيف تصل منتجات من AliExpress ومتاجر أخرى إلى منازل عملائنا في الجزائر بكل أمان!</p>
                    <div className="grid md:grid-cols-3 gap-6">
                        {deliveries.map((item, idx) => (
                            <Card key={idx} className="flex flex-col gap-3">
                                <div className="flex justify-between items-start mb-2">
                                    <div className={`w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-xl ${item.color}`}>
                                        <i className={`fa-solid ${item.icon}`}></i>
                                    </div>
                                    <span className={`text-xs font-bold px-2 py-1 rounded-md bg-white/10 ${item.color}`}>{item.status}</span>
                                </div>
                                <h3 className="font-bold text-lg">{item.title}</h3>
                                <p className="text-white/60 text-sm"><i className="fa-solid fa-user mr-1"></i> العميل: {item.client}</p>
                                <p className="text-white/60 text-sm"><i className="fa-solid fa-truck mr-1"></i> {item.time}</p>
                            </Card>
                        ))}
                    </div>
                </div>
            );
        }

        // ==========================================
        // PAGES
        // ==========================================

        function Home() {
            return (
                <PageWrapper route="/">
                    <div className="text-center py-20 max-w-4xl mx-auto">
                        <motion.h1 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5 }}
                            className="text-5xl md:text-7xl font-extrabold mb-6 leading-tight"
                        >
                            KOUKI SHOP نافذتكم للتسوق <span className="text-gradient">العالمي</span>
                        </motion.h1>
                        <motion.p 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.1 }}
                            className="text-xl text-white/70 mb-10 leading-relaxed"
                        >
                            حنا نشرولك ونقومو بعملية دفع جميع مشترياتك سواء بالأورو أو الدولار.<br/> تسوق من أي مكان، وادفع بالدينار 🇩🇿
                        </motion.p>
                    </div>

                    <div className="grid md:grid-cols-4 gap-4 text-sm text-white/70 bg-surface/30 backdrop-blur-md rounded-2xl p-6 border border-white/5 my-10 max-w-4xl mx-auto">
                        <div className="flex items-center justify-center gap-2"><i className="fa-solid fa-shield-halved text-accent"></i> دفع آمن بالدينار</div>
                        <div className="flex items-center justify-center gap-2"><i className="fa-solid fa-users text-accent"></i> +10,000 عميل في الجزائر</div>
                        <div className="flex items-center justify-center gap-2"><i className="fa-solid fa-bolt text-accent"></i> تنفيذ سريع للطلبات</div>
                        <div className="flex items-center justify-center gap-2"><i className="fa-solid fa-globe text-accent"></i> أشهر المتاجر العالمية</div>
                    </div>

                    <div className="grid md:grid-cols-3 gap-6 my-20">
                        <Link to="/shopping" className="block">
                            <Card className="h-full group text-center hover:bg-surface/80">
                                <div className="w-16 h-16 mx-auto rounded-full bg-primary/20 text-primary flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
                                    <i className="fa-solid fa-earth-americas"></i>
                                </div>
                                <h3 className="text-2xl font-bold mb-3">التسوق العالمي</h3>
                                <p className="text-white/60 mb-6">اشتري أي منتج من AliExpress وادفع بالدينار بكل سهولة.</p>
                                <span className="text-accent font-semibold inline-flex items-center gap-2">ابدأ التسوق <i className="fa-solid fa-arrow-left"></i></span>
                            </Card>
                        </Link>
                        <Link to="/digital" className="block">
                            <Card className="h-full group text-center hover:bg-surface/80">
                                <div className="w-16 h-16 mx-auto rounded-full bg-accent/20 text-accent flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
                                    <i className="fa-solid fa-bolt"></i>
                                </div>
                                <h3 className="text-2xl font-bold mb-3">الخدمات الرقمية</h3>
                                <p className="text-white/60 mb-6">اشتراكات Netflix، Spotify، برامج التصميم والذكاء الاصطناعي.</p>
                                <span className="text-accent font-semibold inline-flex items-center gap-2">تصفح الخدمات <i className="fa-solid fa-arrow-left"></i></span>
                            </Card>
                        </Link>
                        <Link to="/gaming" className="block">
                            <Card className="h-full group text-center hover:bg-surface/80 relative overflow-hidden">
                                <div className="absolute inset-0 bg-gradient-to-tr from-primary/10 to-accent/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                <div className="w-16 h-16 mx-auto rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform relative z-10">
                                    <i className="fa-solid fa-gamepad"></i>
                                </div>
                                <h3 className="text-2xl font-bold mb-3 relative z-10">شحن الألعاب</h3>
                                <p className="text-white/60 mb-6 relative z-10">شحن فوري لألعاب Free Fire، PUBG، eFootball عبر الـ ID.</p>
                                <span className="text-accent font-semibold inline-flex items-center gap-2 relative z-10">اشحن الآن <i className="fa-solid fa-arrow-left"></i></span>
                            </Card>
                        </Link>
                    </div>

                    <AdditionalServices />
                </PageWrapper>
            );
        }

        function Shopping() {
            const [url, setUrl] = useState("");
            const [loading, setLoading] = useState(false);
            const [result, setResult] = useState(null);

            const analyze = () => {
                if (!url) return alert("يرجى إدخال رابط المنتج");
                setLoading(true);
                setTimeout(() => {
                    setLoading(false);
                    setResult({ price: "يتم تحديده", shipping: "حسب المنتج", delivery: "15-35 يوم عبر La Poste" });
                }, 1500);
            };

            return (
                <PageWrapper route="/shopping">
                    <div className="max-w-4xl mx-auto py-10">
                        <h1 className="text-4xl font-bold mb-4 text-center">التسوق <span className="text-gradient">العالمي</span></h1>
                        <p className="text-center text-white/70 mb-10">ضع رابط المنتج الذي تريد شرائه من موقع AliExpress أو المواقع الأخرى المدعومة.</p>
                        
                        <Card className="p-8 max-w-2xl mx-auto">
                            <div className="flex flex-col gap-4">
                                <input 
                                    value={url}
                                    onChange={(e) => setUrl(e.target.value)}
                                    placeholder="https://aliexpress.com/item/..." 
                                    className="w-full p-4 rounded-xl bg-black/40 border border-white/10 focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all text-left dir-ltr"
                                    dir="ltr"
                                />
                                <Button onClick={analyze} className="w-full">
                                    {loading ? <i className="fa-solid fa-circle-notch fa-spin"></i> : "حلّل المنتج"}
                                </Button>
                            </div>
                            
                            {result && (
                                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-8 p-6 bg-surface border border-white/10 rounded-xl">
                                    <h3 className="text-xl font-bold mb-4 text-accent"><i className="fa-solid fa-check-circle mr-2"></i> جاهز للطلب</h3>
                                    <p className="text-white/80 mb-4">الرابط جاهز. يمكنك الآن التواصل معنا عبر التيليجرام لإتمام عملية الدفع والتأكيد.</p>
                                    <a href="https://t.me/BOOGEYMAN_DZ" target="_blank" className="block w-full">
                                        <Button className="w-full bg-gradient-to-r from-blue-500 to-cyan-400 shadow-none hover:shadow-glow">
                                            الطلب عبر تيليجرام <i className="fa-brands fa-telegram fa-lg"></i>
                                        </Button>
                                    </a>
                                </motion.div>
                            )}
                        </Card>

                        <div className="text-center mt-8 text-white/60 flex flex-wrap justify-center gap-4 text-sm">
                            <span><i className="fa-solid fa-check text-accent"></i> AliExpress</span>
                            <span><i className="fa-solid fa-check text-accent"></i> Amazon</span>
                            <span><i className="fa-solid fa-check text-accent"></i> TEMU</span>
                            <span><i className="fa-solid fa-check text-accent"></i> Banggood</span>
                            <span><i className="fa-solid fa-check text-accent"></i> eBay</span>
                        </div>

                        <HowToBuy />
                        <CommissionTable />
                        <RecentDeliveries />
                        
                        <div className="text-center mt-10">
                            <p className="text-white/60 mb-4 text-sm">ملاحظة : كل المتاجر العالمية تفرض الدفع المسبق، متجر Kouki Shop وسيط خدماتي بينكم وبين البائعين الاجانب 🌎</p>
                            <p className="text-white/60 text-sm">الضمانات: 99% من الطرود تصل بشكل سليم لاصحابها ونسبة 1% تكون غالبا في منتجات ثانوية. وحتى اذا لم تصل، تقوم Kouki Shop بمعالجة الامر قصد تعويضكم 😍</p>
                        </div>
                    </div>
                </PageWrapper>
            );
        }

        const ALL_SERVICES = [
            { name: "ChatGPT Plus", category: "ai", iconUrl: "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg", desc: "GPT-4o • توليد صور • بلا حدود" },
            { name: "Grok AI (X)", category: "ai", icon: "fa-brands fa-x-twitter", desc: "أقوى AI من منصة X • تحليل ذكي فائق" },
            { name: "Gemini Advanced", category: "ai", iconUrl: "https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg", desc: "Ultra 1.5 • ملفات • صور • Vision" },
            { name: "Claude Pro", category: "ai", icon: "fa-solid fa-robot", desc: "Sonnet • ملفات طويلة • كود احترافي" },
            { name: "Perplexity Pro", category: "ai", icon: "fa-solid fa-magnifying-glass-chart", desc: "بحث ذكي • مصادر حية • تقارير" },
            { name: "Midjourney V6", category: "ai", icon: "fa-brands fa-discord text-indigo-400", desc: "توليد صور احترافي • عبر Discord" },
            { name: "Netflix Premium", category: "entertainment", icon: "fa-brands fa-youtube text-red-500", desc: "4K UHD • شاشة خاصة • 190 دولة" },
            { name: "Disney+", category: "entertainment", icon: "fa-solid fa-film text-blue-400", desc: "Marvel • Star Wars • Pixar • 4K" },
            { name: "Prime Video", category: "entertainment", icon: "fa-brands fa-amazon text-yellow-400", desc: "أفلام حصرية • أمازون ستوديو" },
            { name: "Spotify Premium", category: "music", icon: "fa-brands fa-spotify text-green-500", desc: "بلا إعلانات • تحميل • جودة عالية" },
            { name: "Apple Music", category: "music", icon: "fa-brands fa-apple text-white", desc: "Lossless • Spatial Audio • 100M أغنية" },
            { name: "Canva Pro", category: "design", iconUrl: "https://upload.wikimedia.org/wikipedia/commons/0/08/Canva_icon_2021.svg", desc: "قوالب Pro • Brand Kit • خلفيات AI" },
            { name: "Adobe CC", category: "design", iconUrl: "https://upload.wikimedia.org/wikipedia/commons/4/4c/Adobe_Creative_Cloud_rainbow_icon.svg", desc: "Photoshop • Premiere • Illustrator" },
            { name: "CapCut Pro", category: "design", icon: "fa-solid fa-scissors text-white", desc: "مونتاج AI • إزالة خلفية • ريلز" },
            { name: "Envato Elements", category: "design", icon: "fa-solid fa-leaf text-green-400", desc: "ملايين الأصول • قوالب • فيديو • صور" },
            { name: "Microsoft 365", category: "productivity", icon: "fa-brands fa-microsoft text-blue-400", desc: "5 أجهزة • 1TB OneDrive • Copilot AI" },
            { name: "Notion Plus + AI", category: "productivity", icon: "fa-solid fa-n text-white", desc: "مساحة لامحدودة • AI مدمج • Team" },
            { name: "Google One Drive", category: "cloud", icon: "fa-brands fa-google text-blue-400", desc: "100GB → 2TB • مشاركة عائلية" },
            { name: "Udemy Courses", category: "education", icon: "fa-solid fa-graduation-cap text-purple-400", desc: "شراء أي كورس • وصول مدى الحياة" },
            { name: "Meta Verified", category: "social", icon: "fa-solid fa-certificate text-blue-400", desc: "العلامة الزرقاء • Facebook & Instagram" },
            { name: "Snapchat+", category: "social", icon: "fa-brands fa-snapchat text-yellow-400", desc: "ميزات حصرية • Badge • Story Rewatch" },
            { name: "دعم السوشيال ميديا", category: "social", icon: "fa-solid fa-thumbs-up text-pink-400", desc: "متابعين • لايكات • مشاهدات" },
            { name: "Xbox Game Pass", category: "gaming", icon: "fa-brands fa-xbox text-green-500", desc: "400+ لعبة • PC & Console • EA Play" },
            { name: "PlayStation Plus", category: "gaming", icon: "fa-brands fa-playstation text-blue-500", desc: "Extra • Premium • ألعاب مجانية شهرية" },
            { name: "Steam Games", category: "gaming", icon: "fa-brands fa-steam text-white", desc: "شراء أي لعبة • تحويل للحساب" }
        ];

        function Digital() {
            const [filter, setFilter] = useState("all");
            const filtered = filter === "all" ? ALL_SERVICES : ALL_SERVICES.filter(s => s.category === filter);

            return (
                <PageWrapper route="/digital">
                    <div className="py-10">
                        <h1 className="text-4xl font-bold mb-4 text-center">الكتالوج <span className="text-gradient">الرقمي</span></h1>
                        <p className="text-center text-white/70 mb-10">اشتراكات أصلية مضمونة • بالدينار الجزائري • تفعيل فوري</p>
                        
                        <div className="flex flex-wrap justify-center gap-3 mb-10">
                            {[
                                { id: "all", label: "الكل" },
                                { id: "ai", label: "ذكاء اصطناعي" },
                                { id: "entertainment", label: "ترفيه" },
                                { id: "music", label: "موسيقى" },
                                { id: "design", label: "تصميم وإبداع" },
                                { id: "productivity", label: "إنتاجية" },
                                { id: "cloud", label: "تخزين سحابي" },
                                { id: "education", label: "تعليم" },
                                { id: "social", label: "سوشيال" },
                                { id: "gaming", label: "ألعاب" }
                            ].map(cat => (
                                <button
                                    key={cat.id}
                                    onClick={() => setFilter(cat.id)}
                                    className={`px-5 py-2 rounded-full transition-all font-semibold ${
                                        filter === cat.id 
                                        ? "bg-primary text-white shadow-glow" 
                                        : "bg-white/5 text-white/60 hover:bg-white/10"
                                    }`}
                                >
                                    {cat.label}
                                </button>
                            ))}
                        </div>

                        <div className="grid md:grid-cols-3 gap-6">
                            {filtered.map((s) => (
                                <Card key={s.name} className="flex flex-col h-full">
                                    <div className="flex items-center gap-4 mb-4">
                                        {s.iconUrl ? (
                                            <img src={s.iconUrl} alt={s.name} className="w-12 h-12 object-contain bg-white/5 p-1 rounded-xl" />
                                        ) : (
                                            <div className="w-12 h-12 rounded-xl bg-primary/20 text-primary flex items-center justify-center text-xl">
                                                <i className={s.icon}></i>
                                            </div>
                                        )}
                                        <h3 className="text-xl font-bold">{s.name}</h3>
                                    </div>
                                    <div className="text-sm text-white/70 mb-6 flex-grow">{s.desc}</div>
                                    <div className="mt-auto">
                                        <Button className="w-full text-sm">حسب الباقة - اطلب الآن</Button>
                                    </div>
                                </Card>
                            ))}
                        </div>

                        <div className="mt-20 text-center bg-surface border border-white/5 p-8 rounded-2xl max-w-2xl mx-auto">
                            <h3 className="text-2xl font-bold mb-4">هل تبحث عن اشتراك محدد؟ 🎬💻</h3>
                            <p className="text-white/60 mb-6">نوفر تقريباً جميع الاشتراكات الرقمية! للاستفسار عن أي اشتراك اتصل بنا وسنقوم بتوفيره لك فوراً.</p>
                            <div className="flex justify-center gap-4">
                                <Button className="bg-gradient-to-r from-blue-500 to-cyan-400">تيليجرام</Button>
                                <Button className="bg-gradient-to-r from-green-500 to-emerald-400">واتساب</Button>
                            </div>
                        </div>
                    </div>
                </PageWrapper>
            );
        }

        function Topup({ gameName, gameIcon, options }) {
            const [selected, setSelected] = useState(options[0].value);
            return (
                <Card className="p-0">
                    <div className="p-6">
                        <h3 className="text-xl font-bold text-center mb-6">{gameIcon} {gameName}</h3>
                        <input
                            placeholder="أدخل الـ ID"
                            className="w-full p-4 rounded-xl bg-black/40 border border-white/10 text-center focus:border-accent focus:ring-1 focus:ring-accent outline-none transition-all mb-4 text-lg"
                        />
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-6">
                            {options.map((opt) => (
                                <button
                                    key={opt.value}
                                    onClick={() => setSelected(opt.value)}
                                    className={`p-3 rounded-xl transition-all ${
                                        selected === opt.value
                                        ? "bg-primary/30 border border-primary text-white"
                                        : "bg-white/5 border border-white/5 text-white/70 hover:bg-white/10"
                                    }`}
                                >
                                    {opt.label}
                                </button>
                            ))}
                        </div>
                        <Button className="w-full text-lg py-4">اشحن {gameName}</Button>
                    </div>
                </Card>
            );
        }

        function Gaming() {
            return (
                <PageWrapper route="/gaming">
                    <div className="py-10">
                        <h1 className="text-4xl font-bold mb-4 text-center">شحن <span className="text-gradient">الألعاب 🎮</span></h1>
                        <p className="text-center text-white/70 mb-10">احصل على شحن فوري وآمن لحسابك</p>
                        
                        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
                            <Topup 
                                gameName="Free Fire"
                                gameIcon="🔥"
                                options={[
                                    { value: "100", label: "100 💎" },
                                    { value: "210", label: "210 💎" },
                                    { value: "530", label: "530 💎" },
                                    { value: "1080", label: "1080 💎" },
                                    { value: "weekly", label: "عضوية أسبوعية" },
                                    { value: "monthly", label: "عضوية شهرية" }
                                ]}
                            />
                            <Topup 
                                gameName="PUBG Mobile"
                                gameIcon="🔫"
                                options={[
                                    { value: "60", label: "60 UC" },
                                    { value: "325", label: "325 UC" },
                                    { value: "660", label: "660 UC" },
                                    { value: "1800", label: "1800 UC" },
                                    { value: "prime", label: "Prime Plus" }
                                ]}
                            />
                            <Topup 
                                gameName="eFootball 2026"
                                gameIcon="⚽"
                                options={[
                                    { value: "130", label: "130 Coins" },
                                    { value: "300", label: "300 Coins" },
                                    { value: "1050", label: "1050 Coins" },
                                    { value: "2150", label: "2150 Coins" },
                                    { value: "3300", label: "3300 Coins" }
                                ]}
                            />
                        </div>
                        <div className="mt-10 text-center text-white/60 max-w-2xl mx-auto">
                            <p className="mb-2"><strong className="text-accent">الدفع:</strong> بالدينار الجزائري | <strong className="text-accent">التفعيل:</strong> فوري بعد الدفع</p>
                            <p className="text-sm">ملاحظة: تأكد من إدخال ID صحيح، نحن غير مسؤولين عن الأخطاء.</p>
                        </div>
                    </div>
                </PageWrapper>
            );
        }

        function AnimatedRoutes() {
            const location = useLocation();
            return (
                <AnimatePresence mode="wait">
                    <Routes location={location} key={location.pathname}>
                        <Route path="/" element={<Home />} />
                        <Route path="/shopping" element={<Shopping />} />
                        <Route path="/digital" element={<Digital />} />
                        <Route path="/gaming" element={<Gaming />} />
                    </Routes>
                </AnimatePresence>
            );
        }

        function App() {
            return (
                <HashRouter>
                    <Layout>
                        <AnimatedRoutes />
                    </Layout>
                </HashRouter>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html completely rewritten.")
