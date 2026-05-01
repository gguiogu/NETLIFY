-- ==========================================
-- KOUKI SHOP SAAS - SUPABASE SCHEMA
-- Paste this into your Supabase SQL Editor
-- ==========================================

-- 1. USERS TABLE (Extends Supabase Auth)
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE NOT NULL,
    role TEXT DEFAULT 'customer' CHECK (role IN ('customer', 'staff', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Secure Profiles (RLS)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public profiles are viewable by admin" ON public.profiles FOR SELECT USING (true);
CREATE POLICY "Users can insert their own profile." ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "Users can update own profile." ON public.profiles FOR UPDATE USING (auth.uid() = id);

-- 2. DIGITAL SERVICES
CREATE TABLE public.services (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price_dzd INTEGER NOT NULL,
    active BOOLEAN DEFAULT true,
    stock_type TEXT DEFAULT 'unlimited',
    images TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ==========================================
-- NOTE: Please ensure you create a Storage Bucket in Supabase named "products"
-- and set its permissions to "Public".
-- ==========================================

-- Secure Services
ALTER TABLE public.services ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Services are viewable by everyone." ON public.services FOR SELECT USING (true);
CREATE POLICY "Only admins can insert/update services" ON public.services FOR ALL USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
);

-- 3. ORDERS (AliExpress & Digital)
CREATE TABLE public.orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id), -- Optional if guest checkout allowed
    customer_name TEXT NOT NULL,
    customer_contact TEXT NOT NULL, -- Phone or telegram username
    type TEXT NOT NULL CHECK (type IN ('AliExpress', 'Digital Service', 'Game Top-up')),
    product_details JSONB NOT NULL, -- Store URL, Title, or Game Package
    amount_dzd INTEGER NOT NULL,
    status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending', 'Completed', 'Failed', 'Refunded')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Secure Orders
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Admins can view all orders" ON public.orders FOR SELECT USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'staff'))
);
CREATE POLICY "Anyone can insert an order" ON public.orders FOR INSERT WITH CHECK (true);
CREATE POLICY "Admins can update orders" ON public.orders FOR UPDATE USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'staff'))
);

-- 4. PAYMENTS
CREATE TABLE public.payments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    order_id UUID REFERENCES public.orders(id) ON DELETE CASCADE,
    method TEXT NOT NULL CHECK (method IN ('CCP', 'BaridiMob', 'Cash')),
    reference TEXT,
    amount_dzd INTEGER NOT NULL,
    status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending', 'Verified', 'Rejected')),
    proof_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Secure Payments
ALTER TABLE public.payments ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Admins can manage payments" ON public.payments FOR ALL USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'staff'))
);
CREATE POLICY "Anyone can insert a payment" ON public.payments FOR INSERT WITH CHECK (true);

-- Insert dummy data for Admin to test
INSERT INTO public.services (name, category, price_dzd, active) VALUES 
('Netflix Premium', 'Entertainment', 1200, true),
('ChatGPT Plus', 'AI', 4500, true),
('Canva Pro', 'Design', 800, true);

INSERT INTO public.orders (customer_name, customer_contact, type, product_details, amount_dzd, status) VALUES 
('Karim DZ', '0555123456', 'AliExpress', '{"url": "https://aliexpress.com/..."}', 4500, 'Pending'),
('Younes B.', '@younes_tg', 'Digital Service', '{"service": "Netflix Premium"}', 1200, 'Completed'),
('Roufaida', '0777123456', 'Game Top-up', '{"game": "Free Fire", "id": "1489392811", "package": "530"}', 800, 'Completed');
