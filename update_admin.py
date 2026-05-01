import os

html_content = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kouki Admin Pro</title>
    
    <!-- Fonts & Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
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
              sans: ['Inter', 'sans-serif'],
            }
          }
        }
      }
    </script>
    <style type="text/tailwindcss">
      body {
        font-family: 'Inter', sans-serif;
        background-color: #0B0F1A;
        color: rgba(255, 255, 255, 0.9);
      }
      .text-muted { color: rgba(255, 255, 255, 0.6); }
      ::-webkit-scrollbar { width: 8px; height: 8px; }
      ::-webkit-scrollbar-track { background: #0B0F1A; }
      ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }
      ::-webkit-scrollbar-thumb:hover { background: rgba(34,211,238,0.5); }
      
      .status-pending { color: #FBBF24; background: rgba(251, 191, 36, 0.1); }
      .status-done { color: #22C55E; background: rgba(34, 197, 94, 0.1); }
      .status-failed { color: #EF4444; background: rgba(239, 68, 68, 0.1); }
      
      .glass-panel {
        @apply bg-surface backdrop-blur-xl border border-white/10 rounded-2xl shadow-lg;
      }
      
      .shimmer {
        animation: shimmer 2s infinite linear;
        background: linear-gradient(to right, rgba(255,255,255,0.05) 4%, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.05) 36%);
        background-size: 1000px 100%;
      }
      @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
      }
    </style>

    <!-- React, Router, Framer Motion, Babel -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/@remix-run/router@1.16.1/dist/router.umd.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-router@6.23.1/dist/umd/react-router.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-router-dom@6.23.1/dist/umd/react-router-dom.production.min.js"></script>
    <script src="https://unpkg.com/framer-motion@10.16.4/dist/framer-motion.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    
    <!-- Supabase JS -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, createContext, useContext } = React;
        const { HashRouter, Routes, Route, Link, useLocation, Navigate, useNavigate } = window.ReactRouterDOM;
        const { motion, AnimatePresence } = window.Motion;

        // --- SUPABASE CLIENT ---
        const SUPABASE_URL = 'https://axbrosibywcdxwlbjyqv.supabase.co';
        const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF4YnJvc2lieXdjZHh3bGJqeXF2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY4NzE1MDAsImV4cCI6MjA5MjQ0NzUwMH0.hXs9aFZ_GZzb1TGkk0lU1WpLL1fE_EohO1enS7H8Itc';
        const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

        // --- UI COMPONENTS ---
        
        // Context for Toasts
        const ToastContext = createContext(null);
        function ToastProvider({ children }) {
            const [toasts, setToasts] = useState([]);
            const addToast = (message, type = 'success') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, message, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
            };
            return (
                <ToastContext.Provider value={addToast}>
                    {children}
                    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
                        <AnimatePresence>
                            {toasts.map(t => (
                                <motion.div
                                    key={t.id}
                                    initial={{ opacity: 0, y: 20, scale: 0.9 }}
                                    animate={{ opacity: 1, y: 0, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.9 }}
                                    className={`px-4 py-3 rounded-xl shadow-lg border backdrop-blur-xl flex items-center gap-3 ${
                                        t.type === 'error' ? 'bg-red-500/20 border-red-500/50 text-red-100' : 'bg-green-500/20 border-green-500/50 text-green-100'
                                    }`}
                                >
                                    <i className={`fa-solid ${t.type === 'error' ? 'fa-circle-xmark text-red-400' : 'fa-circle-check text-green-400'}`}></i>
                                    {t.message}
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>
                </ToastContext.Provider>
            );
        }

        const useToast = () => useContext(ToastContext);

        function Skeleton({ className = "" }) {
            return <div className={`shimmer rounded-xl ${className}`}></div>;
        }

        function EmptyState({ icon, title, message }) {
            return (
                <div className="flex flex-col items-center justify-center p-12 text-center border border-white/5 border-dashed rounded-2xl bg-black/20">
                    <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mb-4">
                        <i className={`fa-solid ${icon} fa-2x text-white/30`}></i>
                    </div>
                    <h3 className="text-xl font-bold mb-2">{title}</h3>
                    <p className="text-muted">{message}</p>
                </div>
            );
        }

        function Modal({ isOpen, onClose, title, children, onConfirm, confirmText = "Confirm", isDanger = false }) {
            if (!isOpen) return null;
            return (
                <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
                    <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose}></div>
                    <motion.div 
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="glass-panel p-6 w-full max-w-md relative z-10 border border-white/20"
                    >
                        <h3 className="text-xl font-bold mb-4">{title}</h3>
                        <div className="mb-6 text-muted">{children}</div>
                        <div className="flex justify-end gap-3">
                            <Button variant="outline" onClick={onClose}>Cancel</Button>
                            <Button variant={isDanger ? "danger" : "primary"} onClick={onConfirm}>{confirmText}</Button>
                        </div>
                    </motion.div>
                </div>
            );
        }

        // Shared UI elements
        function PageWrapper({ children, route }) {
            return (
                <motion.div
                    key={route}
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -15 }}
                    transition={{ duration: 0.3 }}
                >
                    {children}
                </motion.div>
            );
        }

        function Card({ children, className = "" }) {
            return (
                <motion.div whileHover={{ y: -4 }} className={`glass-panel p-5 hover:shadow-glow transition-all ${className}`}>
                    {children}
                </motion.div>
            );
        }

        function Button({ children, className = "", variant = "primary", onClick, disabled }) {
            const baseStyles = "px-4 py-2 rounded-xl font-semibold transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed";
            const variants = {
                primary: "bg-gradient-to-r from-primary to-accent text-white shadow-glow hover:scale-105",
                danger: "bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/40",
                success: "bg-green-500/20 text-green-400 border border-green-500/30 hover:bg-green-500/40",
                outline: "border border-white/20 text-white/80 hover:bg-white/10"
            };
            return (
                <motion.button whileTap={disabled ? {} : { scale: 0.95 }} onClick={onClick} disabled={disabled} className={`${baseStyles} ${variants[variant]} ${className}`}>
                    {children}
                </motion.button>
            );
        }

        function StatusBadge({ status }) {
            const s = (status || "").toLowerCase();
            let cClass = "bg-white/10 text-white/70";
            if (s === 'pending') cClass = "status-pending";
            if (s === 'completed' || s === 'verified' || s === 'done') cClass = "status-done";
            if (s === 'failed' || s === 'rejected') cClass = "status-failed";
            return <span className={`px-3 py-1 rounded-full text-xs font-bold ${cClass}`}>{status}</span>;
        }

        // --- AUTHENTICATION ---
        
        function Login({ setSession }) {
            const [email, setEmail] = useState('');
            const [password, setPassword] = useState('');
            const [loading, setLoading] = useState(false);
            const toast = useToast();

            const handleLogin = async (e) => {
                e.preventDefault();
                setLoading(true);
                const { data, error } = await supabase.auth.signInWithPassword({ email, password });
                if (error) {
                    toast(error.message, 'error');
                } else {
                    // Check if user is admin
                    const { data: profile } = await supabase.from('profiles').select('role').eq('id', data.user.id).single();
                    if (profile && profile.role === 'admin') {
                        setSession(data.session);
                        toast('Welcome back, Admin!');
                    } else {
                        toast('Access Denied: Not an admin', 'error');
                        await supabase.auth.signOut();
                    }
                }
                setLoading(false);
            };

            return (
                <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(79,70,229,0.15),transparent)] pointer-events-none" />
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_80%,rgba(34,211,238,0.15),transparent)] pointer-events-none" />
                    
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
                        <div className="text-center mb-8">
                            <div className="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-tr from-primary to-accent flex items-center justify-center mb-4 shadow-glow">
                                <i className="fa-solid fa-cube text-3xl text-white"></i>
                            </div>
                            <h1 className="text-3xl font-bold">Kouki <span className="text-accent">Admin</span></h1>
                            <p className="text-muted mt-2">Secure access to the SaaS control panel</p>
                        </div>

                        <Card className="p-8 border border-white/20">
                            <form onSubmit={handleLogin} className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium mb-1 text-white/80">Admin Email</label>
                                    <input 
                                        type="email" 
                                        value={email}
                                        onChange={e => setEmail(e.target.value)}
                                        className="w-full bg-black/40 border border-white/10 rounded-xl p-3 focus:border-accent outline-none" 
                                        required 
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium mb-1 text-white/80">Password</label>
                                    <input 
                                        type="password" 
                                        value={password}
                                        onChange={e => setPassword(e.target.value)}
                                        className="w-full bg-black/40 border border-white/10 rounded-xl p-3 focus:border-accent outline-none" 
                                        required 
                                    />
                                </div>
                                <Button className="w-full mt-4 py-3" disabled={loading}>
                                    {loading ? <i className="fa-solid fa-circle-notch fa-spin"></i> : "Sign In securely"}
                                </Button>
                            </form>
                        </Card>
                    </motion.div>
                </div>
            );
        }

        // --- LAYOUT ---
        function AdminLayout({ children, session }) {
            const location = useLocation();
            const navigate = useNavigate();
            const toast = useToast();
            
            const handleLogout = async () => {
                await supabase.auth.signOut();
                toast('Logged out successfully');
                window.location.reload();
            };

            const navLinks = [
                { path: "/overview", label: "Overview", icon: "fa-chart-pie" },
                { path: "/orders", label: "Orders", icon: "fa-shopping-cart" },
                { path: "/digital", label: "Digital Services", icon: "fa-bolt" },
                { path: "/gaming", label: "Game Top-ups", icon: "fa-gamepad" },
                { path: "/users", label: "Users", icon: "fa-users" },
                { path: "/payments", label: "Payments", icon: "fa-credit-card" },
                { path: "/analytics", label: "Analytics", icon: "fa-chart-line" },
                { path: "/settings", label: "Settings", icon: "fa-gear" }
            ];

            return (
                <div className="min-h-screen bg-bg text-white flex">
                    <aside className="w-64 bg-black/40 border-r border-white/5 p-6 flex flex-col fixed h-full z-20 backdrop-blur-xl">
                        <div className="flex items-center gap-3 mb-10">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary to-accent flex items-center justify-center">
                                <i className="fa-solid fa-cube text-white"></i>
                            </div>
                            <h1 className="text-xl font-bold tracking-wider">Kouki <span className="text-accent">Admin</span></h1>
                        </div>

                        <nav className="space-y-2 flex-1 overflow-y-auto">
                            {navLinks.map(link => {
                                const isActive = location.pathname === link.path || (link.path === '/overview' && location.pathname === '/');
                                return (
                                    <Link 
                                        key={link.path} 
                                        to={link.path}
                                        className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                                            isActive 
                                                ? "bg-primary/20 text-accent border border-primary/30 shadow-[0_0_15px_rgba(34,211,238,0.1)]" 
                                                : "text-white/60 hover:bg-white/5 hover:text-white"
                                        }`}
                                    >
                                        <i className={`fa-solid ${link.icon} w-5`}></i>
                                        <span className="font-medium">{link.label}</span>
                                    </Link>
                                );
                            })}
                        </nav>
                        
                        <div className="mt-auto pt-6 border-t border-white/5">
                            <div className="flex items-center justify-between px-2 py-2">
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
                                        <i className="fa-solid fa-user text-xs"></i>
                                    </div>
                                    <div className="overflow-hidden">
                                        <div className="text-sm font-bold truncate">{session.user.email}</div>
                                        <div className="text-xs text-accent">Super Admin</div>
                                    </div>
                                </div>
                                <button onClick={handleLogout} className="text-red-400 hover:text-red-300 p-2"><i className="fa-solid fa-arrow-right-from-bracket"></i></button>
                            </div>
                        </div>
                    </aside>

                    <main className="flex-1 ml-64 p-8 relative min-h-screen">
                        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(79,70,229,0.05),transparent)] pointer-events-none" />
                        <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_80%,rgba(34,211,238,0.05),transparent)] pointer-events-none" />
                        <div className="relative z-10 max-w-7xl mx-auto">
                            {children}
                        </div>
                    </main>
                </div>
            );
        }

        // --- VIEWS ---

        function Overview() {
            const [stats, setStats] = useState({ orders: 0, revenue: 0, pending: 0 });
            const [loading, setLoading] = useState(true);

            useEffect(() => {
                const fetchStats = async () => {
                    const { data: orders } = await supabase.from('orders').select('amount_dzd, status');
                    if (orders) {
                        const totalOrders = orders.length;
                        const pending = orders.filter(o => o.status === 'Pending').length;
                        const revenue = orders.filter(o => o.status === 'Completed').reduce((acc, curr) => acc + curr.amount_dzd, 0);
                        setStats({ orders: totalOrders, revenue, pending });
                    }
                    setLoading(false);
                };
                fetchStats();
            }, []);

            return (
                <PageWrapper route="/overview">
                    <div className="flex justify-between items-end mb-8">
                        <div>
                            <h2 className="text-3xl font-bold">Overview Dashboard</h2>
                            <p className="text-muted mt-1">Real-time business intelligence.</p>
                        </div>
                        <Button variant="outline"><i className="fa-solid fa-download"></i> Export Report</Button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                        {loading ? (
                            Array(3).fill(0).map((_, i) => <Skeleton key={i} className="h-32" />)
                        ) : (
                            <>
                                <Card className="relative overflow-hidden">
                                    <div className="absolute top-0 right-0 w-16 h-16 bg-white/5 rounded-bl-full -mr-8 -mt-8"></div>
                                    <div className="w-10 h-10 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center mb-4"><i className="fa-solid fa-shopping-bag"></i></div>
                                    <div className="text-muted text-sm">Total Orders</div>
                                    <div className="text-2xl font-bold mt-1">{stats.orders}</div>
                                </Card>
                                <Card className="relative overflow-hidden">
                                    <div className="absolute top-0 right-0 w-16 h-16 bg-white/5 rounded-bl-full -mr-8 -mt-8"></div>
                                    <div className="w-10 h-10 rounded-lg bg-green-500/20 text-green-400 flex items-center justify-center mb-4"><i className="fa-solid fa-wallet"></i></div>
                                    <div className="text-muted text-sm">Revenue (Completed)</div>
                                    <div className="text-2xl font-bold mt-1">{stats.revenue.toLocaleString()} DZD</div>
                                </Card>
                                <Card className="relative overflow-hidden">
                                    <div className="absolute top-0 right-0 w-16 h-16 bg-white/5 rounded-bl-full -mr-8 -mt-8"></div>
                                    <div className="w-10 h-10 rounded-lg bg-yellow-500/20 text-yellow-400 flex items-center justify-center mb-4"><i className="fa-solid fa-clock"></i></div>
                                    <div className="text-muted text-sm">Pending Orders</div>
                                    <div className="text-2xl font-bold mt-1">{stats.pending}</div>
                                </Card>
                            </>
                        )}
                    </div>
                </PageWrapper>
            );
        }

        function Orders() {
            const [orders, setOrders] = useState([]);
            const [loading, setLoading] = useState(true);
            const toast = useToast();

            useEffect(() => {
                fetchOrders();
            }, []);

            const fetchOrders = async () => {
                setLoading(true);
                const { data, error } = await supabase.from('orders').select('*').order('created_at', { ascending: false });
                if (!error) setOrders(data);
                setLoading(false);
            };

            const updateStatus = async (id, status) => {
                const { error } = await supabase.from('orders').update({ status }).eq('id', id);
                if (error) {
                    toast(error.message, 'error');
                } else {
                    toast(`Order marked as ${status}`);
                    setOrders(orders.map(o => o.id === id ? { ...o, status } : o));
                }
            };

            return (
                <PageWrapper route="/orders">
                    <h2 className="text-3xl font-bold mb-1">Orders System</h2>
                    <p className="text-muted mb-8">Manage global shopping and digital orders.</p>

                    <Card className="p-0 overflow-hidden">
                        {loading ? (
                            <div className="p-6 space-y-4">
                                {Array(5).fill(0).map((_, i) => <Skeleton key={i} className="h-10 w-full" />)}
                            </div>
                        ) : orders.length === 0 ? (
                            <EmptyState icon="fa-box-open" title="No Orders Found" message="You don't have any orders in the database yet." />
                        ) : (
                            <table className="w-full text-left border-collapse">
                                <thead>
                                    <tr className="bg-white/5 border-b border-white/10 text-sm">
                                        <th className="p-4 font-semibold text-muted">Customer</th>
                                        <th className="p-4 font-semibold text-muted">Type</th>
                                        <th className="p-4 font-semibold text-muted">Details</th>
                                        <th className="p-4 font-semibold text-muted">Status</th>
                                        <th className="p-4 font-semibold text-muted">Amount</th>
                                        <th className="p-4 font-semibold text-muted text-right">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {orders.map((o) => (
                                        <tr key={o.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                            <td className="p-4">
                                                <div className="font-bold">{o.customer_name}</div>
                                                <div className="text-xs text-muted">{o.customer_contact}</div>
                                            </td>
                                            <td className="p-4 text-sm font-semibold text-accent">{o.type}</td>
                                            <td className="p-4 text-sm max-w-xs truncate text-muted">
                                                {JSON.stringify(o.product_details)}
                                            </td>
                                            <td className="p-4"><StatusBadge status={o.status} /></td>
                                            <td className="p-4 font-bold">{o.amount_dzd} DZD</td>
                                            <td className="p-4 text-right flex gap-2 justify-end">
                                                {o.status === 'Pending' && (
                                                    <Button variant="success" className="py-1 text-xs" onClick={() => updateStatus(o.id, 'Completed')}>Complete</Button>
                                                )}
                                                <Button variant="danger" className="py-1 text-xs px-2" onClick={() => updateStatus(o.id, 'Failed')}><i className="fa-solid fa-x"></i></Button>
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

        // Placeholder functional wrappers for other routes
        function DigitalServices() { return <PageWrapper route="/digital"><h2 className="text-3xl font-bold mb-4">Digital Services</h2><EmptyState icon="fa-layer-group" title="Services Module" message="Fetch from Supabase 'services' table here."/></PageWrapper>; }
        function GameTopups() { return <PageWrapper route="/gaming"><h2 className="text-3xl font-bold mb-4">Game Top-ups</h2><EmptyState icon="fa-gamepad" title="Gaming Module" message="Filter orders by type = 'Game Top-up'."/></PageWrapper>; }
        function Users() { return <PageWrapper route="/users"><h2 className="text-3xl font-bold mb-4">Users</h2><EmptyState icon="fa-users" title="Users Module" message="Fetch from Supabase 'profiles' table here."/></PageWrapper>; }
        function Payments() { return <PageWrapper route="/payments"><h2 className="text-3xl font-bold mb-4">Payments</h2><EmptyState icon="fa-money-bill-transfer" title="Payments Module" message="Fetch from Supabase 'payments' table here."/></PageWrapper>; }
        function Analytics() { return <PageWrapper route="/analytics"><h2 className="text-3xl font-bold mb-4">Analytics</h2><EmptyState icon="fa-chart-line" title="Analytics Engine" message="Build revenue charts based on completed orders."/></PageWrapper>; }
        function Settings() { return <PageWrapper route="/settings"><h2 className="text-3xl font-bold mb-4">Settings</h2><EmptyState icon="fa-gear" title="Platform Settings" message="Configure API keys and delivery rules."/></PageWrapper>; }

        function AnimatedAdminRoutes() {
            const location = useLocation();
            return (
                <AnimatePresence mode="wait">
                    <Routes location={location} key={location.pathname}>
                        <Route path="/" element={<Navigate to="/overview" replace />} />
                        <Route path="/overview" element={<Overview />} />
                        <Route path="/orders" element={<Orders />} />
                        <Route path="/digital" element={<DigitalServices />} />
                        <Route path="/gaming" element={<GameTopups />} />
                        <Route path="/users" element={<Users />} />
                        <Route path="/payments" element={<Payments />} />
                        <Route path="/analytics" element={<Analytics />} />
                        <Route path="/settings" element={<Settings />} />
                    </Routes>
                </AnimatePresence>
            );
        }

        function App() {
            const [session, setSession] = useState(null);
            const [loading, setLoading] = useState(true);

            useEffect(() => {
                supabase.auth.getSession().then(({ data: { session } }) => {
                    setSession(session);
                    setLoading(false);
                });

                const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
                    setSession(session);
                });

                return () => subscription.unsubscribe();
            }, []);

            if (loading) return <div className="min-h-screen bg-bg flex items-center justify-center text-white"><i className="fa-solid fa-circle-notch fa-spin fa-2x"></i></div>;

            return (
                <ToastProvider>
                    <HashRouter>
                        {!session ? (
                            <Login setSession={setSession} />
                        ) : (
                            <AdminLayout session={session}>
                                <AnimatedAdminRoutes />
                            </AdminLayout>
                        )}
                    </HashRouter>
                </ToastProvider>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>"""

with open("admin.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("admin.html successfully rewritten with Supabase and UI Polish!")
