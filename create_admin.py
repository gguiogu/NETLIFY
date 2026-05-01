import os

html_content = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kouki Admin Dashboard</title>
    
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
        const { HashRouter, Routes, Route, Link, useLocation, Navigate } = window.ReactRouterDOM;
        const { motion, AnimatePresence } = window.Motion;

        // --- SHARED COMPONENTS ---
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
                <motion.div
                    whileHover={{ y: -4 }}
                    transition={{ duration: 0.2 }}
                    className={`glass-panel p-5 hover:shadow-glow transition-all ${className}`}
                >
                    {children}
                </motion.div>
            );
        }

        function Button({ children, className = "", variant = "primary" }) {
            const baseStyles = "px-4 py-2 rounded-xl font-semibold transition-all flex items-center justify-center gap-2";
            const variants = {
                primary: "bg-gradient-to-r from-primary to-accent text-white shadow-glow hover:scale-105",
                danger: "bg-red-500/20 text-red-400 hover:bg-red-500/30",
                success: "bg-green-500/20 text-green-400 hover:bg-green-500/30",
                outline: "border border-white/20 text-white/80 hover:bg-white/10"
            };
            
            return (
                <motion.button
                    whileTap={{ scale: 0.95 }}
                    className={`${baseStyles} ${variants[variant]} ${className}`}
                >
                    {children}
                </motion.button>
            );
        }

        function StatusBadge({ status }) {
            const s = status.toLowerCase();
            let cClass = "";
            let text = status;
            
            if (s === 'pending') cClass = "status-pending";
            if (s === 'completed' || s === 'verified' || s === 'done') cClass = "status-done";
            if (s === 'failed' || s === 'rejected') cClass = "status-failed";

            return (
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${cClass}`}>
                    {text}
                </span>
            );
        }

        // --- LAYOUT ---
        function AdminLayout({ children }) {
            const location = useLocation();
            
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
                    {/* SIDEBAR */}
                    <aside className="w-64 bg-black/40 border-r border-white/5 p-6 flex flex-col fixed h-full z-20 backdrop-blur-xl">
                        <div className="flex items-center gap-3 mb-10">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary to-accent flex items-center justify-center">
                                <i className="fa-solid fa-cube text-white"></i>
                            </div>
                            <h1 className="text-xl font-bold tracking-wider">Kouki <span className="text-accent">Admin</span></h1>
                        </div>

                        <nav className="space-y-2 flex-1">
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
                            <div className="flex items-center gap-3 px-4 py-2">
                                <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
                                    <i className="fa-solid fa-user text-xs"></i>
                                </div>
                                <div>
                                    <div className="text-sm font-bold">Admin User</div>
                                    <div className="text-xs text-white/50">admin@koukishop.dz</div>
                                </div>
                            </div>
                        </div>
                    </aside>

                    {/* MAIN CONTENT */}
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
            const stats = [
                { label: "Total Orders", value: "1,284", icon: "fa-shopping-bag", color: "text-blue-400", trend: "+12%" },
                { label: "Revenue", value: "320,000 DZD", icon: "fa-wallet", color: "text-green-400", trend: "+8.5%" },
                { label: "Active Users", value: "2,450", icon: "fa-users", color: "text-purple-400", trend: "+24%" },
                { label: "Pending Orders", value: "32", icon: "fa-clock", color: "text-yellow-400", trend: "-5%" },
            ];

            return (
                <PageWrapper route="/overview">
                    <div className="flex justify-between items-end mb-8">
                        <div>
                            <h2 className="text-3xl font-bold">Overview Dashboard</h2>
                            <p className="text-muted mt-1">Welcome back, here's what's happening today.</p>
                        </div>
                        <Button variant="outline"><i className="fa-solid fa-download"></i> Export Report</Button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                        {stats.map((s, idx) => (
                            <Card key={idx} className="relative overflow-hidden">
                                <div className={`absolute top-0 right-0 w-16 h-16 bg-white/5 rounded-bl-full -mr-8 -mt-8`}></div>
                                <div className="flex justify-between items-start mb-4">
                                    <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center">
                                        <i className={`fa-solid ${s.icon} ${s.color}`}></i>
                                    </div>
                                    <span className={`text-xs font-bold ${s.trend.startsWith('+') ? 'text-green-400' : 'text-red-400'}`}>
                                        {s.trend}
                                    </span>
                                </div>
                                <div className="text-muted text-sm">{s.label}</div>
                                <div className="text-2xl font-bold mt-1">{s.value}</div>
                            </Card>
                        ))}
                    </div>

                    <div className="grid lg:grid-cols-3 gap-6">
                        <Card className="lg:col-span-2 min-h-[300px] flex flex-col">
                            <h3 className="font-bold mb-4">Revenue Overview</h3>
                            <div className="flex-1 border border-white/5 border-dashed rounded-xl flex items-center justify-center text-white/30 bg-black/20">
                                <i className="fa-solid fa-chart-line fa-3x mb-2 block w-full text-center"></i>
                                <span className="absolute mt-12 text-sm">Chart Visualization Area</span>
                            </div>
                        </Card>
                        <Card className="min-h-[300px] flex flex-col">
                            <h3 className="font-bold mb-4">Recent Activity</h3>
                            <div className="space-y-4 flex-1">
                                {[1,2,3,4].map(i => (
                                    <div key={i} className="flex items-center gap-3">
                                        <div className="w-2 h-2 rounded-full bg-accent"></div>
                                        <div>
                                            <p className="text-sm">New order <span className="text-accent font-bold">#102{i}</span> placed</p>
                                            <p className="text-xs text-muted">2 mins ago</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </Card>
                    </div>
                </PageWrapper>
            );
        }

        function Orders() {
            const orders = [
                { id: "#1024", type: "AliExpress", customer: "Karim", status: "Pending", amount: "4,500 DZD", date: "2026-04-30" },
                { id: "#1023", type: "Digital Service", customer: "Younes", status: "Completed", amount: "1,200 DZD", date: "2026-04-29" },
                { id: "#1022", type: "Game Top-up", customer: "Roufaida", status: "Completed", amount: "800 DZD", date: "2026-04-29" },
                { id: "#1021", type: "AliExpress", customer: "Ahmed", status: "Failed", amount: "12,000 DZD", date: "2026-04-28" },
                { id: "#1020", type: "Digital Service", customer: "Sara", status: "Pending", amount: "2,400 DZD", date: "2026-04-28" },
            ];

            return (
                <PageWrapper route="/orders">
                    <div className="flex justify-between items-end mb-8">
                        <div>
                            <h2 className="text-3xl font-bold">Orders System</h2>
                            <p className="text-muted mt-1">Manage global shopping and digital orders.</p>
                        </div>
                        <div className="flex gap-2">
                            <input type="text" placeholder="Search orders..." className="px-4 py-2 bg-black/30 border border-white/10 rounded-xl outline-none focus:border-accent" />
                            <Button variant="outline"><i className="fa-solid fa-filter"></i> Filter</Button>
                        </div>
                    </div>

                    <Card className="p-0 overflow-hidden">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-white/5 border-b border-white/10 text-sm">
                                    <th className="p-4 font-semibold text-muted">Order ID</th>
                                    <th className="p-4 font-semibold text-muted">Customer</th>
                                    <th className="p-4 font-semibold text-muted">Type</th>
                                    <th className="p-4 font-semibold text-muted">Status</th>
                                    <th className="p-4 font-semibold text-muted">Amount</th>
                                    <th className="p-4 font-semibold text-muted">Date</th>
                                    <th className="p-4 font-semibold text-muted text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {orders.map((o, idx) => (
                                    <tr key={idx} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                        <td className="p-4 font-bold">{o.id}</td>
                                        <td className="p-4">{o.customer}</td>
                                        <td className="p-4 text-sm"><i className={`fa-solid ${o.type.includes('Game')?'fa-gamepad':o.type.includes('Ali')?'fa-box':'fa-bolt'} mr-2 text-white/50`}></i>{o.type}</td>
                                        <td className="p-4"><StatusBadge status={o.status} /></td>
                                        <td className="p-4 font-semibold">{o.amount}</td>
                                        <td className="p-4 text-sm text-muted">{o.date}</td>
                                        <td className="p-4 text-right">
                                            <button className="text-accent hover:text-white transition-colors mr-3"><i className="fa-solid fa-eye"></i></button>
                                            <button className="text-muted hover:text-white transition-colors"><i className="fa-solid fa-ellipsis-vertical"></i></button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </Card>
                </PageWrapper>
            );
        }

        function DigitalServices() {
            const services = [
                { name: "ChatGPT Plus", category: "AI Subscription", price: "4,500 DZD", active: true },
                { name: "Netflix Premium", category: "Entertainment", price: "1,200 DZD", active: true },
                { name: "Canva Pro", category: "Design", price: "800 DZD", active: true },
                { name: "Midjourney", category: "AI Subscription", price: "5,000 DZD", active: false },
            ];

            return (
                <PageWrapper route="/digital">
                    <div className="flex justify-between items-end mb-8">
                        <div>
                            <h2 className="text-3xl font-bold">Digital Services Management</h2>
                            <p className="text-muted mt-1">Manage catalog, pricing, and activation methods.</p>
                        </div>
                        <Button><i className="fa-solid fa-plus"></i> Add Service</Button>
                    </div>

                    <div className="grid md:grid-cols-3 xl:grid-cols-4 gap-6">
                        {services.map((s, idx) => (
                            <Card key={idx} className="flex flex-col">
                                <div className="flex justify-between items-start mb-4">
                                    <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center text-primary text-xl">
                                        <i className="fa-solid fa-layer-group"></i>
                                    </div>
                                    <span className={`w-2 h-2 rounded-full ${s.active ? 'bg-green-400 shadow-[0_0_8px_#22c55e]' : 'bg-red-400'}`}></span>
                                </div>
                                <h3 className="font-bold text-lg">{s.name}</h3>
                                <p className="text-muted text-sm mb-4">{s.category}</p>
                                <div className="font-bold text-accent mb-6">{s.price}</div>
                                
                                <div className="mt-auto flex gap-2 border-t border-white/10 pt-4">
                                    <Button variant="outline" className="flex-1 py-1 text-sm">Edit</Button>
                                    <Button variant="danger" className="py-1 px-3"><i className="fa-solid fa-trash"></i></Button>
                                </div>
                            </Card>
                        ))}
                    </div>
                </PageWrapper>
            );
        }

        function GameTopups() {
            return (
                <PageWrapper route="/gaming">
                    <div className="flex justify-between items-end mb-8">
                        <div>
                            <h2 className="text-3xl font-bold">Game Top-up Panel</h2>
                            <p className="text-muted mt-1">Process pending top-up requests.</p>
                        </div>
                    </div>

                    <div className="grid lg:grid-cols-3 gap-6">
                        <div className="lg:col-span-2 space-y-4">
                            {[1, 2, 3].map((i) => (
                                <Card key={i} className="flex flex-col md:flex-row justify-between items-center gap-4">
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center text-xl border border-purple-500/30">
                                            <i className="fa-solid fa-gamepad"></i>
                                        </div>
                                        <div>
                                            <h4 className="font-bold">Free Fire - 530 💎</h4>
                                            <p className="text-sm text-muted">ID: 1489392811 • Paid: 1,200 DZD</p>
                                        </div>
                                    </div>
                                    <div className="flex gap-2 w-full md:w-auto">
                                        <Button variant="success" className="text-sm py-1.5 flex-1"><i className="fa-solid fa-check"></i> Deliver</Button>
                                        <Button variant="outline" className="text-sm py-1.5 flex-1"><i className="fa-solid fa-rotate-right"></i> Retry</Button>
                                        <Button variant="danger" className="text-sm py-1.5"><i className="fa-solid fa-rotate-left"></i></Button>
                                    </div>
                                </Card>
                            ))}
                        </div>
                        
                        <div>
                            <Card>
                                <h3 className="font-bold mb-4">Top-up Stats</h3>
                                <div className="space-y-4">
                                    <div className="flex justify-between items-center">
                                        <span className="text-muted">Pending Requests</span>
                                        <span className="font-bold text-yellow-400 bg-yellow-400/10 px-2 py-0.5 rounded">12</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                        <span className="text-muted">Completed Today</span>
                                        <span className="font-bold text-green-400">45</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                        <span className="text-muted">Success Rate</span>
                                        <span className="font-bold">98.5%</span>
                                    </div>
                                </div>
                            </Card>
                        </div>
                    </div>
                </PageWrapper>
            );
        }

        function Users() {
            return (
                <PageWrapper route="/users">
                    <h2 className="text-3xl font-bold mb-1">Users Management</h2>
                    <p className="text-muted mb-8">Customer database and order history.</p>

                    <Card className="p-0 overflow-hidden">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-white/5 border-b border-white/10 text-sm">
                                    <th className="p-4 font-semibold text-muted">Name</th>
                                    <th className="p-4 font-semibold text-muted">Email</th>
                                    <th className="p-4 font-semibold text-muted">Orders</th>
                                    <th className="p-4 font-semibold text-muted">Total Spent</th>
                                    <th className="p-4 font-semibold text-muted">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {[
                                    { name: "Karim DZ", email: "karim@example.com", orders: 12, spent: "45,000 DZD", status: "Active" },
                                    { name: "Younes B.", email: "younes@example.com", orders: 3, spent: "4,200 DZD", status: "Active" },
                                    { name: "Roufaida", email: "roufaida@example.com", orders: 1, spent: "800 DZD", status: "Active" },
                                ].map((u, idx) => (
                                    <tr key={idx} className="border-b border-white/5 hover:bg-white/5">
                                        <td className="p-4 font-bold flex items-center gap-3">
                                            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 flex items-center justify-center text-xs">
                                                {u.name.charAt(0)}
                                            </div>
                                            {u.name}
                                        </td>
                                        <td className="p-4 text-muted">{u.email}</td>
                                        <td className="p-4">{u.orders}</td>
                                        <td className="p-4 font-semibold">{u.spent}</td>
                                        <td className="p-4"><span className="text-green-400 text-sm"><i className="fa-solid fa-circle text-[8px] mr-1 align-middle"></i> {u.status}</span></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </Card>
                </PageWrapper>
            );
        }

        function Payments() {
            return (
                <PageWrapper route="/payments">
                    <h2 className="text-3xl font-bold mb-1">Payments System</h2>
                    <p className="text-muted mb-8">Track CCP, BaridiMob, and verify receipts.</p>

                    <div className="grid lg:grid-cols-2 gap-6">
                        <Card>
                            <h3 className="font-bold mb-4 flex items-center gap-2"><i className="fa-solid fa-money-bill-transfer text-accent"></i> Pending Verifications</h3>
                            <div className="space-y-4">
                                {[1, 2].map(i => (
                                    <div key={i} className="border border-white/10 p-4 rounded-xl flex justify-between items-center bg-black/20">
                                        <div>
                                            <div className="font-bold mb-1">BaridiMob Transfer</div>
                                            <div className="text-sm text-muted">Amount: 4,500 DZD • Ref: TX1029{i}</div>
                                        </div>
                                        <div className="flex gap-2">
                                            <button className="w-8 h-8 rounded bg-green-500/20 text-green-400 hover:bg-green-500/40"><i className="fa-solid fa-check"></i></button>
                                            <button className="w-8 h-8 rounded bg-red-500/20 text-red-400 hover:bg-red-500/40"><i className="fa-solid fa-xmark"></i></button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </Card>
                        
                        <Card>
                            <h3 className="font-bold mb-4">Payment Methods Config</h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center p-3 border border-white/10 rounded-xl bg-white/5">
                                    <div className="flex items-center gap-3">
                                        <i className="fa-solid fa-building-columns text-2xl text-yellow-500"></i>
                                        <div>
                                            <div className="font-bold">Algérie Poste (CCP)</div>
                                            <div className="text-xs text-muted">Active • 12345678 99</div>
                                        </div>
                                    </div>
                                    <span className="w-10 h-5 bg-accent rounded-full relative"><span className="absolute right-1 top-1 w-3 h-3 bg-white rounded-full"></span></span>
                                </div>
                                <div className="flex justify-between items-center p-3 border border-white/10 rounded-xl bg-white/5">
                                    <div className="flex items-center gap-3">
                                        <i className="fa-solid fa-mobile-screen text-2xl text-blue-400"></i>
                                        <div>
                                            <div className="font-bold">BaridiMob (RIP)</div>
                                            <div className="text-xs text-muted">Active • 00799999000012345678</div>
                                        </div>
                                    </div>
                                    <span className="w-10 h-5 bg-accent rounded-full relative"><span className="absolute right-1 top-1 w-3 h-3 bg-white rounded-full"></span></span>
                                </div>
                            </div>
                        </Card>
                    </div>
                </PageWrapper>
            );
        }

        function Analytics() {
            return (
                <PageWrapper route="/analytics">
                    <h2 className="text-3xl font-bold mb-1">Analytics Dashboard</h2>
                    <p className="text-muted mb-8">Deep insights into revenue and user behavior.</p>

                    <div className="grid md:grid-cols-3 gap-6 mb-8">
                        <Card className="text-center">
                            <i className="fa-solid fa-fire text-3xl text-orange-400 mb-3"></i>
                            <div className="text-muted text-sm">Best-Selling Service</div>
                            <div className="font-bold text-lg mt-1">Netflix Premium 4K</div>
                        </Card>
                        <Card className="text-center">
                            <i className="fa-solid fa-clock text-3xl text-blue-400 mb-3"></i>
                            <div className="text-muted text-sm">Peak Traffic Time</div>
                            <div className="font-bold text-lg mt-1">8:00 PM - 11:00 PM</div>
                        </Card>
                        <Card className="text-center">
                            <i className="fa-solid fa-percent text-3xl text-green-400 mb-3"></i>
                            <div className="text-muted text-sm">Conversion Rate</div>
                            <div className="font-bold text-lg mt-1">4.2%</div>
                        </Card>
                    </div>

                    <Card className="h-64 flex items-center justify-center border-dashed border border-white/20 bg-black/10">
                        <div className="text-center text-white/40">
                            <i className="fa-solid fa-chart-area fa-3x mb-3"></i>
                            <p>Advanced Charts Visualization Module</p>
                        </div>
                    </Card>
                </PageWrapper>
            );
        }

        function Settings() {
            return (
                <PageWrapper route="/settings">
                    <h2 className="text-3xl font-bold mb-1">System Settings</h2>
                    <p className="text-muted mb-8">Configure platform rules and security.</p>

                    <div className="max-w-3xl space-y-6">
                        <Card>
                            <h3 className="font-bold mb-4 text-lg border-b border-white/10 pb-2">Admin Accounts</h3>
                            <div className="flex justify-between items-center mb-3">
                                <div>
                                    <p className="font-bold">admin@koukishop.dz</p>
                                    <p className="text-sm text-muted">Super Admin</p>
                                </div>
                                <Button variant="outline" className="text-sm py-1">Change Password</Button>
                            </div>
                        </Card>
                        
                        <Card>
                            <h3 className="font-bold mb-4 text-lg border-b border-white/10 pb-2">API Keys & Integrations</h3>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm text-muted mb-1">AliExpress API Token</label>
                                    <div className="flex gap-2">
                                        <input type="password" value="************************" readOnly className="flex-1 bg-black/30 border border-white/10 rounded-lg px-3 py-2 text-muted" />
                                        <Button variant="outline"><i className="fa-solid fa-eye"></i></Button>
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm text-muted mb-1">Telegram Bot Token</label>
                                    <div className="flex gap-2">
                                        <input type="password" value="************************" readOnly className="flex-1 bg-black/30 border border-white/10 rounded-lg px-3 py-2 text-muted" />
                                        <Button variant="outline"><i className="fa-solid fa-eye"></i></Button>
                                    </div>
                                </div>
                            </div>
                        </Card>

                        <Card>
                            <h3 className="font-bold mb-4 text-lg border-b border-white/10 pb-2">Delivery Rules</h3>
                            <div className="flex justify-between items-center py-2">
                                <div>
                                    <p className="font-bold">Automated Order Forwarding</p>
                                    <p className="text-sm text-muted">Send orders to Telegram automatically</p>
                                </div>
                                <span className="w-12 h-6 bg-green-500 rounded-full relative"><span className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></span></span>
                            </div>
                        </Card>
                    </div>
                </PageWrapper>
            );
        }

        // --- APP ROUTER ---

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
            return (
                <HashRouter>
                    <AdminLayout>
                        <AnimatedAdminRoutes />
                    </AdminLayout>
                </HashRouter>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>"""

with open("admin.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("admin.html successfully generated.")
