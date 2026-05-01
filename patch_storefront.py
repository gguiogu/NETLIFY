import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Supabase CDN to HEAD if not present
if '@supabase' not in content:
    content = content.replace(
        '<!-- Babel for in-browser JSX parsing -->',
        '<!-- Supabase JS -->\n    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n\n    <!-- Babel for in-browser JSX parsing -->'
    )

# 2. Add Supabase init inside the script
if 'const SUPABASE_URL =' not in content:
    content = content.replace(
        'const { HashRouter, Routes, Route, Link, useLocation } = window.ReactRouterDOM;',
        """const { HashRouter, Routes, Route, Link, useLocation } = window.ReactRouterDOM;
        
        // --- SUPABASE CLIENT ---
        const SUPABASE_URL = 'https://axbrosibywcdxwlbjyqv.supabase.co';
        const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF4YnJvc2lieXdjZHh3bGJqeXF2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY4NzE1MDAsImV4cCI6MjA5MjQ0NzUwMH0.hXs9aFZ_GZzb1TGkk0lU1WpLL1fE_EohO1enS7H8Itc';
        const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);"""
    )

# 3. Create the Reviews component
reviews_component = """
        function CustomerReviews() {
            const [reviews, setReviews] = useState([]);
            const [loading, setLoading] = useState(true);
            const [form, setForm] = useState({ user_name: '', content: '' });
            const [submitState, setSubmitState] = useState('idle'); // idle, loading, success

            const fetchReviews = async () => {
                const { data } = await supabase.from('comments').select('*').eq('status', 'Approved').order('created_at', { ascending: false }).limit(6);
                if (data) setReviews(data);
                setLoading(false);
            };

            useEffect(() => { fetchReviews(); }, []);

            const handleSubmit = async (e) => {
                e.preventDefault();
                setSubmitState('loading');
                const { error } = await supabase.from('comments').insert([form]);
                if (error) {
                    alert("حدث خطأ أثناء إرسال التقييم");
                    setSubmitState('idle');
                } else {
                    setSubmitState('success');
                    setForm({ user_name: '', content: '' });
                    setTimeout(() => setSubmitState('idle'), 5000);
                }
            };

            return (
                <div className="my-20 max-w-6xl mx-auto">
                    <h2 className="text-3xl font-bold text-center mb-4">آراء <span className="text-gradient">العملاء</span> 💬</h2>
                    <p className="text-center text-white/70 mb-10">تجارب حقيقية من عملائنا الكرام بعد استخدام خدمات المتجر</p>
                    
                    <div className="grid md:grid-cols-3 gap-6 mb-12">
                        {loading ? (
                            Array(3).fill(0).map((_, i) => <Card key={i} className="h-32 bg-white/5 animate-pulse" />)
                        ) : reviews.length === 0 ? (
                            <div className="col-span-3 text-center text-white/50 py-8 border border-white/5 border-dashed rounded-xl">لا توجد تقييمات حتى الآن. كن أول من يقيّم خدماتنا!</div>
                        ) : (
                            reviews.map(r => (
                                <Card key={r.id} className="relative">
                                    <div className="flex items-center gap-3 mb-3">
                                        <div className="w-10 h-10 rounded-full bg-gradient-to-r from-primary to-accent flex items-center justify-center font-bold text-white shadow-glowCyan">
                                            {r.user_name.charAt(0)}
                                        </div>
                                        <div>
                                            <h4 className="font-bold">{r.user_name}</h4>
                                            <div className="flex text-yellow-400 text-xs"><i className="fa-solid fa-star"></i><i className="fa-solid fa-star"></i><i className="fa-solid fa-star"></i><i className="fa-solid fa-star"></i><i className="fa-solid fa-star"></i></div>
                                        </div>
                                    </div>
                                    <p className="text-white/80 text-sm leading-relaxed">{r.content}</p>
                                </Card>
                            ))
                        )}
                    </div>

                    <Card className="max-w-2xl mx-auto p-8 relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-full h-1 bg-gradient-to-r from-accent to-primary"></div>
                        <h3 className="text-xl font-bold mb-6 text-center">أضف تقييمك الخاص</h3>
                        
                        {submitState === 'success' ? (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-6">
                                <i className="fa-solid fa-circle-check text-5xl text-green-400 mb-4 shadow-glowCyan rounded-full"></i>
                                <h4 className="font-bold text-lg text-green-400 mb-2">شكراً لتقييمك!</h4>
                                <p className="text-white/60 text-sm">تم إرسال تقييمك بنجاح، سيظهر هنا بعد مراجعته من الإدارة.</p>
                            </motion.div>
                        ) : (
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div>
                                    <label className="block text-sm text-white/60 mb-1">الاسم الكامل</label>
                                    <input required value={form.user_name} onChange={e=>setForm({...form, user_name: e.target.value})} className="w-full bg-black/40 border border-white/10 rounded-xl p-3 focus:border-accent outline-none" placeholder="الاسم" />
                                </div>
                                <div>
                                    <label className="block text-sm text-white/60 mb-1">التقييم (التجربة)</label>
                                    <textarea required value={form.content} onChange={e=>setForm({...form, content: e.target.value})} className="w-full bg-black/40 border border-white/10 rounded-xl p-3 focus:border-accent outline-none h-24 resize-none" placeholder="اكتب تجربتك هنا..."></textarea>
                                </div>
                                <Button type="submit" className="w-full" disabled={submitState === 'loading'}>
                                    {submitState === 'loading' ? <i className="fa-solid fa-circle-notch fa-spin"></i> : "إرسال التقييم"}
                                </Button>
                            </form>
                        )}
                    </Card>
                </div>
            );
        }
"""

# Inject CustomerReviews definition before function Home()
if 'function CustomerReviews()' not in content:
    content = content.replace('function Home() {', reviews_component + '\n        function Home() {')

# Inject CustomerReviews component into Home page
if '<AdditionalServices />' in content and '<CustomerReviews />' not in content:
    content = content.replace('<AdditionalServices />', '<AdditionalServices />\n                    <CustomerReviews />')

# 4. Refactor Digital to use Supabase instead of ALL_SERVICES
import re
new_digital = """        function Digital() {
            const [services, setServices] = useState([]);
            const [filter, setFilter] = useState("all");
            const [loading, setLoading] = useState(true);

            useEffect(() => {
                const fetchServices = async () => {
                    const { data } = await supabase.from('services').select('*').eq('active', true).order('category');
                    if (data) setServices(data);
                    setLoading(false);
                };
                fetchServices();
            }, []);

            const filtered = filter === "all" ? services : services.filter(s => s.category === filter);

            return (
                <PageWrapper route="/digital">
                    <div className="py-10">
                        <h1 className="text-4xl font-bold mb-4 text-center">الكتالوج <span className="text-gradient">الرقمي</span></h1>
                        <p className="text-center text-white/70 mb-10">اشتراكات أصلية مضمونة • بالدينار الجزائري • تفعيل فوري</p>
                        
                        <div className="flex flex-wrap justify-center gap-3 mb-10">
                            {[
                                { id: "all", label: "الكل" },
                                { id: "AI", label: "ذكاء اصطناعي" },
                                { id: "Entertainment", label: "ترفيه" },
                                { id: "Music", label: "موسيقى" },
                                { id: "Design", label: "تصميم وإبداع" },
                                { id: "Gaming", label: "ألعاب" }
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

                        {loading ? (
                            <div className="grid md:grid-cols-3 gap-6">{Array(6).fill(0).map((_, i) => <Card key={i} className="h-48 bg-white/5 animate-pulse" />)}</div>
                        ) : filtered.length === 0 ? (
                            <div className="text-center py-20 text-white/50">لا توجد خدمات متاحة في هذا القسم حالياً.</div>
                        ) : (
                            <div className="grid md:grid-cols-3 gap-6">
                                {filtered.map((s) => (
                                    <Card key={s.id} className="flex flex-col h-full">
                                        <div className="flex items-center gap-4 mb-4">
                                            <div className="w-12 h-12 rounded-xl bg-primary/20 text-primary flex items-center justify-center text-xl shadow-glow">
                                                <i className={`fa-solid ${s.category === 'AI' ? 'fa-robot' : s.category === 'Entertainment' ? 'fa-film' : s.category === 'Gaming' ? 'fa-gamepad' : 'fa-layer-group'}`}></i>
                                            </div>
                                            <h3 className="text-xl font-bold line-clamp-1">{s.name}</h3>
                                        </div>
                                        <div className="text-sm text-white/70 mb-6 flex-grow">اشتراك آمن ومضمون 100%</div>
                                        <div className="mt-auto">
                                            <div className="text-center font-bold text-accent mb-4 text-xl">{s.price_dzd} د.ج</div>
                                            <a href={`https://wa.me/213562208794?text=${encodeURIComponent('مرحباً أريد طلب اشتراك: ' + s.name)}`} target="_blank">
                                                <Button className="w-full text-sm">اطلب الآن عبر واتساب</Button>
                                            </a>
                                        </div>
                                    </Card>
                                ))}
                            </div>
                        )}

                        <div className="mt-20 text-center bg-surface border border-white/5 p-8 rounded-2xl max-w-2xl mx-auto">
                            <h3 className="text-2xl font-bold mb-4">هل تبحث عن اشتراك محدد؟ 🎬💻</h3>
                            <p className="text-white/60 mb-6">نوفر تقريباً جميع الاشتراكات الرقمية! للاستفسار عن أي اشتراك اتصل بنا وسنقوم بتوفيره لك فوراً.</p>
                            <div className="flex justify-center gap-4">
                                <a href="https://t.me/BOOGEYMAN_DZ" target="_blank"><Button className="bg-gradient-to-r from-blue-500 to-cyan-400">تيليجرام</Button></a>
                                <a href="https://wa.me/213562208794" target="_blank"><Button className="bg-gradient-to-r from-green-500 to-emerald-400">واتساب</Button></a>
                            </div>
                        </div>
                    </div>
                </PageWrapper>
            );
        }
"""
content = re.sub(
    r'function Digital\(\) \{.*?return \(\s*<PageWrapper route="/digital">.*?</PageWrapper>\s*\);\s*\}',
    new_digital,
    content,
    flags=re.DOTALL
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("index.html successfully updated with dynamic products and comments section!")
