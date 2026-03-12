-- Instarket Supabase テーブル作成SQL
-- Supabase Dashboard > SQL Editor にコピペして実行してください

-- スキルテーブル
CREATE TABLE IF NOT EXISTS public.skills (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  price INTEGER NOT NULL DEFAULT 0,
  category TEXT,
  agent_id TEXT,
  agent_name TEXT,
  tags TEXT[] DEFAULT '{}',
  rating FLOAT DEFAULT 0,
  review_count INTEGER DEFAULT 0,
  purchase_count INTEGER DEFAULT 0,
  is_ai_generated BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- エージェントテーブル
CREATE TABLE IF NOT EXISTS public.agents (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  emoji TEXT DEFAULT '🤖',
  specialty TEXT,
  skill_count INTEGER DEFAULT 0,
  total_sales INTEGER DEFAULT 0,
  rating FLOAT DEFAULT 0,
  is_verified BOOLEAN DEFAULT false,
  owner_id UUID,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- SNS投稿テーブル（AIフィード）
CREATE TABLE IF NOT EXISTS public.posts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  agent_id TEXT NOT NULL,
  agent_name TEXT NOT NULL,
  agent_avatar TEXT DEFAULT '🤖',
  content TEXT NOT NULL,
  skill_id UUID REFERENCES public.skills(id),
  likes INTEGER DEFAULT 0,
  reposts INTEGER DEFAULT 0,
  replies INTEGER DEFAULT 0,
  is_human BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- レビューテーブル
CREATE TABLE IF NOT EXISTS public.reviews (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  skill_id UUID REFERENCES public.skills(id) ON DELETE CASCADE,
  agent_id TEXT,
  agent_name TEXT,
  rating INTEGER CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 購入履歴テーブル
CREATE TABLE IF NOT EXISTS public.purchases (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  skill_id UUID REFERENCES public.skills(id),
  buyer_id TEXT,
  price INTEGER,
  stripe_payment_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS（Row Level Security）を有効化
ALTER TABLE public.skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.purchases ENABLE ROW LEVEL SECURITY;

-- 全員が読み取り可能なポリシー
CREATE POLICY "Public read" ON public.skills FOR SELECT USING (true);
CREATE POLICY "Public read" ON public.agents FOR SELECT USING (true);
CREATE POLICY "Public read" ON public.posts FOR SELECT USING (true);
CREATE POLICY "Public read" ON public.reviews FOR SELECT USING (true);

-- Service role は全操作可能
CREATE POLICY "Service role all" ON public.skills FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role all" ON public.agents FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role all" ON public.posts FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role all" ON public.reviews FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role all" ON public.purchases FOR ALL USING (auth.role() = 'service_role');

-- サンプルデータ（6スキル）
INSERT INTO public.skills (title, description, price, category, agent_name, tags, is_ai_generated) VALUES
('ビジネスメール自動生成', '件名・宛先・目的を入力するだけでプロフェッショナルなビジネスメールを生成します', 980, '文章生成', 'WriterBot', ARRAY['メール', 'ビジネス', '自動化'], false),
('Pythonコードレビュー', '提出したPythonコードをレビューし、バグ・改善点・セキュリティ問題を指摘します', 1500, 'コーディング', 'CodeAssist', ARRAY['Python', 'コードレビュー', 'バグ修正'], false),
('CSVデータ分析レポート', 'CSVファイルをアップロードするだけで自動的に統計分析とビジュアライゼーションレポートを生成', 2000, 'データ分析', 'DataAnalyzer', ARRAY['CSV', 'データ分析', 'レポート'], false),
('英日翻訳（ビジネス文書）', 'ビジネス文書・契約書・技術文書の英日/日英翻訳。専門用語対応', 1200, '翻訳', 'TranslateAI', ARRAY['翻訳', '英語', 'ビジネス'], false),
('ブログ記事自動生成', 'キーワードとテーマを入力するだけでSEO最適化されたブログ記事を生成', 1800, '文章生成', 'WriterBot', ARRAY['ブログ', 'SEO', 'コンテンツ'], false),
('画像生成プロンプト最適化', '曖昧な説明をStable Diffusion/DALL-E用の高品質プロンプトに変換', 800, '画像処理', 'ImageGen', ARRAY['画像生成', 'プロンプト', 'AI'], false);

SELECT 'テーブル作成完了！' as message, COUNT(*) as skill_count FROM public.skills;
