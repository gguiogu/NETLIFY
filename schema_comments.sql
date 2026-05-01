-- ==========================================
-- KOUKI SHOP SAAS - COMMENTS TABLE
-- Paste this into your Supabase SQL Editor
-- ==========================================

CREATE TABLE public.comments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_name TEXT NOT NULL,
    content TEXT NOT NULL,
    status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Secure Comments
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;

-- Anyone can read APPROVED comments
CREATE POLICY "Approved comments are public" ON public.comments FOR SELECT USING (status = 'Approved');

-- Admins can read ALL comments
CREATE POLICY "Admins can view all comments" ON public.comments FOR SELECT USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'staff'))
);

-- Anyone can insert a new comment (it goes to Pending automatically)
CREATE POLICY "Anyone can insert a comment" ON public.comments FOR INSERT WITH CHECK (true);

-- Only Admins can update/delete comments (to approve or reject)
CREATE POLICY "Admins can update comments" ON public.comments FOR UPDATE USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'staff'))
);
CREATE POLICY "Admins can delete comments" ON public.comments FOR DELETE USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role IN ('admin', 'staff'))
);

-- Insert a dummy approved comment to test
INSERT INTO public.comments (user_name, content, status) VALUES 
('Karim DZ', 'خدمة ممتازة وسريعة جداً! طلبت منتج من AliExpress ووصلني في 15 يوم فقط.', 'Approved'),
('Younes B.', 'شحن فوري وموثوق لبطاقات الألعاب، أنصح بالتعامل معهم.', 'Approved');
