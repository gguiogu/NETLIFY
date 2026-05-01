import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_shopping = """        function Shopping() {
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
                        </Card>"""

new_shopping = """        function Shopping() {
            const [url, setUrl] = useState("");
            const [loading, setLoading] = useState(false);
            const [result, setResult] = useState(null);

            const analyze = async () => {
                if (!url) return alert("يرجى إدخال رابط المنتج");
                setLoading(true);
                setResult(null);
                try {
                    const response = await fetch("https://netlify-6ukv.onrender.com/analyze", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ url })
                    });
                    const data = await response.json();
                    if (data.error) throw new Error(data.error);
                    setResult(data);
                } catch (err) {
                    alert("حدث خطأ أثناء التحليل، قد يكون الرابط غير صالح أو المتجر لا يدعم هذه الميزة. " + err.message);
                } finally {
                    setLoading(false);
                }
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
                                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-8 p-6 bg-surface border border-white/10 rounded-xl relative overflow-hidden">
                                    <div className="absolute top-0 right-0 w-full h-1 bg-gradient-to-r from-primary to-accent"></div>
                                    <h3 className="text-2xl font-bold mb-6 text-accent text-center"><i className="fa-solid fa-file-invoice-dollar mr-2"></i> فاتورة مفصلة</h3>
                                    
                                    {result.image && <img src={result.image} alt="Product" className="w-32 h-32 object-cover rounded-xl mb-6 mx-auto border border-white/10 shadow-lg" />}

                                    <div className="space-y-3 bg-black/30 p-5 rounded-xl border border-white/5 mb-6">
                                        <div className="flex justify-between border-b border-white/5 pb-3">
                                            <span className="text-white/60">سعر المنتج:</span>
                                            <span className="font-bold">{result.base_dzd} د.ج <span className="text-sm font-normal text-white/50 dir-ltr">(US ${result.price_usd})</span></span>
                                        </div>
                                        <div className="flex justify-between border-b border-white/5 pb-3">
                                            <span className="text-white/60">عمولة الموقع:</span>
                                            <span className="font-bold text-accent">+ {result.commission} د.ج</span>
                                        </div>
                                        <div className="flex justify-between border-b border-white/5 pb-3">
                                            <span className="text-white/60">مصاريف الشحن:</span>
                                            <span className="font-bold">مجاني د.ج <span className="text-sm font-normal text-white/50">($0.00)</span></span>
                                        </div>
                                        <div className="flex justify-between pb-2 text-xl pt-2">
                                            <span className="font-bold text-white">المجموع الكلي:</span>
                                            <span className="font-bold text-primary">{result.price_dzd} د.ج</span>
                                        </div>
                                    </div>

                                    <div className="mb-6 bg-white/5 p-4 rounded-xl border border-white/5">
                                        <p className="text-sm text-accent mb-1"><i className="fa-brands fa-aliexpress mr-1"></i> AliExpress Official Store</p>
                                        <p className="font-bold text-sm leading-relaxed">{result.title}</p>
                                    </div>

                                    <div className="bg-primary/10 border border-primary/20 p-5 rounded-xl mb-8">
                                        <h4 className="font-bold mb-3 text-primary"><i className="fa-solid fa-truck-fast mr-2"></i> خيارات الشحن</h4>
                                        <p className="text-sm text-white/80 mb-2">مشمول أو يحدد لاحقاً</p>
                                        <p className="text-sm text-white/80 mb-2"><i className="fa-solid fa-check text-green-400 mr-2"></i> تتبع متاح شحن AliExpress القياسي</p>
                                        <p className="text-sm font-bold mt-2 text-green-400">يصل في: غضون 15 - 30 يوم</p>
                                    </div>

                                    <div className="text-center mb-6">
                                        <h4 className="font-bold text-xl mb-2 text-white">لتأكيد عملية الشراء</h4>
                                        <p className="text-sm text-white/70">التقط صورة (Capture) للشاشة وارسلها مع الرابط عبر واتساب لتأكيد طلبك</p>
                                    </div>

                                    <a href={`https://wa.me/213562208794?text=${encodeURIComponent("مرحباً، أريد طلب هذا المنتج:\\n" + url + "\\nالمجموع: " + result.price_dzd + " د.ج")}`} target="_blank" className="block w-full">
                                        <Button className="w-full bg-[#25D366] text-white shadow-none hover:shadow-[0_0_20px_rgba(37,211,102,0.4)] text-lg h-14">
                                            <i className="fa-brands fa-whatsapp fa-xl ml-2"></i> للطلب عبر واتساب 
                                        </Button>
                                    </a>
                                    <p className="text-center text-xs text-white/50 mt-6 px-4 leading-relaxed">ملاحظة: الدفع مسبق اثناء الشراء من الخارج، نشتري نيابة عنكم، ونضع عناوينكم الشخصية ثم نزودكم برقم التتبع.</p>
                                </motion.div>
                            )}
                        </Card>"""

if old_shopping in content:
    content = content.replace(old_shopping, new_shopping)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced Shopping logic successfully")
else:
    print("Could not find old_shopping block. Might be slightly different formatting.")
