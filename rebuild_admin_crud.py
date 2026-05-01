import os

# We will read admin.html, look for the 'navLinks = [' block to insert Comments,
# look for 'function DigitalServices()' to replace it,
# look for '<Route path="/settings"' to insert '<Route path="/comments"'.

with open("admin.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Comments to Sidebar
if '{ path: "/analytics", label: "Analytics", icon: "fa-chart-line" },' in content and '{ path: "/comments"' not in content:
    content = content.replace(
        '{ path: "/analytics", label: "Analytics", icon: "fa-chart-line" },',
        '{ path: "/analytics", label: "Analytics", icon: "fa-chart-line" },\n                { path: "/comments", label: "Comments", icon: "fa-comments" },'
    )

# 2. Add the DigitalServices and Comments functions
new_components = """
        function DigitalServices() {
            const [services, setServices] = useState([]);
            const [loading, setLoading] = useState(true);
            const [isModalOpen, setModalOpen] = useState(false);
            const [editingService, setEditingService] = useState(null);
            
            const [formData, setFormData] = useState({ name: '', category: 'AI', price_dzd: '' });
            const toast = useToast();

            const fetchServices = async () => {
                setLoading(true);
                const { data, error } = await supabase.from('services').select('*').order('created_at', { ascending: false });
                if (!error) setServices(data);
                setLoading(false);
            };

            useEffect(() => { fetchServices(); }, []);

            const openAdd = () => {
                setEditingService(null);
                setFormData({ name: '', category: 'AI', price_dzd: '' });
                setModalOpen(true);
            };

            const openEdit = (s) => {
                setEditingService(s);
                setFormData({ name: s.name, category: s.category, price_dzd: s.price_dzd });
                setModalOpen(true);
            };

            const handleSave = async (e) => {
                e.preventDefault();
                if (editingService) {
                    const { error } = await supabase.from('services').update(formData).eq('id', editingService.id);
                    if (error) toast(error.message, 'error');
                    else { toast('Service updated!'); fetchServices(); setModalOpen(false); }
                } else {
                    const { error } = await supabase.from('services').insert([formData]);
                    if (error) toast(error.message, 'error');
                    else { toast('Service added!'); fetchServices(); setModalOpen(false); }
                }
            };

            const handleDelete = async (id) => {
                if(confirm("Are you sure you want to delete this product?")) {
                    const { error } = await supabase.from('services').delete().eq('id', id);
                    if (error) toast(error.message, 'error');
                    else { toast('Product deleted'); fetchServices(); }
                }
            };

            return (
                <PageWrapper route="/digital">
                    <div className="flex justify-between items-end mb-8">
                        <div>
                            <h2 className="text-3xl font-bold">Digital Services</h2>
                            <p className="text-muted mt-1">Manage catalog and pricing.</p>
                        </div>
                        <Button onClick={openAdd}><i className="fa-solid fa-plus"></i> Add Service</Button>
                    </div>

                    {loading ? (
                        <div className="grid md:grid-cols-3 gap-6">{Array(6).fill(0).map((_, i) => <Skeleton key={i} className="h-48" />)}</div>
                    ) : services.length === 0 ? (
                        <EmptyState icon="fa-layer-group" title="No Services" message="Add your first digital product!" />
                    ) : (
                        <div className="grid md:grid-cols-3 xl:grid-cols-4 gap-6">
                            {services.map((s) => (
                                <Card key={s.id} className="flex flex-col">
                                    <div className="flex justify-between items-start mb-4">
                                        <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center text-primary text-xl">
                                            <i className="fa-solid fa-layer-group"></i>
                                        </div>
                                        <span className={`w-2 h-2 rounded-full ${s.active ? 'bg-green-400 shadow-[0_0_8px_#22c55e]' : 'bg-red-400'}`}></span>
                                    </div>
                                    <h3 className="font-bold text-lg line-clamp-1">{s.name}</h3>
                                    <p className="text-muted text-sm mb-4">{s.category}</p>
                                    <div className="font-bold text-accent mb-6">{s.price_dzd} DZD</div>
                                    
                                    <div className="mt-auto flex gap-2 border-t border-white/10 pt-4">
                                        <Button variant="outline" className="flex-1 py-1 text-sm" onClick={() => openEdit(s)}>Edit</Button>
                                        <Button variant="danger" className="py-1 px-3" onClick={() => handleDelete(s.id)}><i className="fa-solid fa-trash"></i></Button>
                                    </div>
                                </Card>
                            ))}
                        </div>
                    )}

                    {isModalOpen && (
                        <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
                            <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setModalOpen(false)}></div>
                            <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="glass-panel p-6 w-full max-w-md relative z-10">
                                <h3 className="text-xl font-bold mb-4">{editingService ? 'Edit Product' : 'Add New Product'}</h3>
                                <form onSubmit={handleSave} className="space-y-4">
                                    <div><label className="text-sm text-muted">Name</label><input required value={formData.name} onChange={e=>setFormData({...formData, name: e.target.value})} className="w-full bg-black/40 border border-white/10 p-2 rounded mt-1 outline-none focus:border-primary" /></div>
                                    <div><label className="text-sm text-muted">Category</label><select value={formData.category} onChange={e=>setFormData({...formData, category: e.target.value})} className="w-full bg-black/40 border border-white/10 p-2 rounded mt-1 text-white"><option value="AI">AI</option><option value="Entertainment">Entertainment</option><option value="Design">Design</option><option value="Music">Music</option><option value="Gaming">Gaming</option></select></div>
                                    <div><label className="text-sm text-muted">Price (DZD)</label><input required type="number" value={formData.price_dzd} onChange={e=>setFormData({...formData, price_dzd: e.target.value})} className="w-full bg-black/40 border border-white/10 p-2 rounded mt-1 outline-none focus:border-primary" /></div>
                                    <div className="flex gap-2 justify-end mt-4"><Button type="button" variant="outline" onClick={()=>setModalOpen(false)}>Cancel</Button><Button type="submit">Save</Button></div>
                                </form>
                            </motion.div>
                        </div>
                    )}
                </PageWrapper>
            );
        }

        function CommentsManager() {
            const [comments, setComments] = useState([]);
            const [loading, setLoading] = useState(true);
            const toast = useToast();

            const fetchComments = async () => {
                setLoading(true);
                const { data, error } = await supabase.from('comments').select('*').order('created_at', { ascending: false });
                if (!error) setComments(data);
                setLoading(false);
            };

            useEffect(() => { fetchComments(); }, []);

            const updateStatus = async (id, status) => {
                const { error } = await supabase.from('comments').update({ status }).eq('id', id);
                if (error) toast(error.message, 'error');
                else { toast(`Comment ${status}!`); fetchComments(); }
            };
            
            const deleteComment = async (id) => {
                if(confirm("Delete this comment permanently?")) {
                    const { error } = await supabase.from('comments').delete().eq('id', id);
                    if (error) toast(error.message, 'error');
                    else { toast('Comment deleted'); fetchComments(); }
                }
            };

            return (
                <PageWrapper route="/comments">
                    <h2 className="text-3xl font-bold mb-1">Customer Reviews</h2>
                    <p className="text-muted mb-8">Approve or reject public comments.</p>
                    
                    <Card className="p-0 overflow-hidden">
                        {loading ? <div className="p-6"><Skeleton className="h-20 w-full" /></div> : comments.length === 0 ? <EmptyState icon="fa-comments" title="No Comments" message="No reviews submitted yet." /> : (
                            <table className="w-full text-left border-collapse">
                                <thead><tr className="bg-white/5 border-b border-white/10 text-sm"><th className="p-4 text-muted">User</th><th className="p-4 text-muted">Comment</th><th className="p-4 text-muted">Status</th><th className="p-4 text-muted text-right">Action</th></tr></thead>
                                <tbody>
                                    {comments.map(c => (
                                        <tr key={c.id} className="border-b border-white/5 hover:bg-white/5">
                                            <td className="p-4 font-bold">{c.user_name}</td>
                                            <td className="p-4 text-sm max-w-sm truncate text-muted">{c.content}</td>
                                            <td className="p-4"><StatusBadge status={c.status} /></td>
                                            <td className="p-4 text-right flex gap-2 justify-end">
                                                {c.status === 'Pending' && <Button variant="success" className="py-1 text-xs" onClick={() => updateStatus(c.id, 'Approved')}><i className="fa-solid fa-check"></i></Button>}
                                                <Button variant="danger" className="py-1 text-xs px-2" onClick={() => deleteComment(c.id)}><i className="fa-solid fa-trash"></i></Button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </Card>
                </PageWrapper>
            );
        }

        function GameTopups() { return <PageWrapper route="/gaming"><h2 className="text-3xl font-bold mb-4">Game Top-ups</h2><EmptyState icon="fa-gamepad" title="Gaming Module" message="Filter orders by type = 'Game Top-up'."/></PageWrapper>; }
"""

# Replace the old placeholder functions
import re
content = re.sub(
    r'function DigitalServices\(\) \{ return <PageWrapper.*?</PageWrapper>; \}.*?function GameTopups\(\) \{ return <PageWrapper route="/gaming">.*?</PageWrapper>; \}',
    new_components,
    content,
    flags=re.DOTALL
)

# 3. Add Comments Route
if '<Route path="/settings"' in content and '<Route path="/comments"' not in content:
    content = content.replace(
        '<Route path="/settings" element={<Settings />} />',
        '<Route path="/comments" element={<CommentsManager />} />\n                        <Route path="/settings" element={<Settings />} />'
    )

with open("admin.html", "w", encoding="utf-8") as f:
    f.write(content)

print("admin.html successfully updated with DigitalServices CRUD and CommentsManager!")
