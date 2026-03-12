"""
AI自動スキル生成エージェント
30体のAIエージェントが毎日スキルを自動生成・出品する
"""
import anthropic
import json
import random
from datetime import datetime
import os

# .envファイルを自動ロード
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 30体のAIエージェント定義
AI_AGENTS = [
    {"id": "agent-001", "name": "WriterBot", "emoji": "✍️", "specialty": "文章生成・ライティング", "style": "プロフェッショナル"},
    {"id": "agent-002", "name": "CodeAssist", "emoji": "💻", "specialty": "Pythonコーディング・コードレビュー", "style": "技術的"},
    {"id": "agent-003", "name": "DataAnalyzer", "emoji": "📊", "specialty": "データ分析・可視化", "style": "分析的"},
    {"id": "agent-004", "name": "TranslateAI", "emoji": "🌐", "specialty": "翻訳・多言語対応", "style": "正確"},
    {"id": "agent-005", "name": "ImageGen", "emoji": "🎨", "specialty": "画像生成プロンプト・デザイン", "style": "クリエイティブ"},
    {"id": "agent-006", "name": "SEOBot", "emoji": "🔍", "specialty": "SEO最適化・キーワード", "style": "戦略的"},
    {"id": "agent-007", "name": "SummaryBot", "emoji": "📝", "specialty": "要約・抽出", "style": "簡潔"},
    {"id": "agent-008", "name": "ChatBot", "emoji": "💬", "specialty": "会話設計・チャットボット", "style": "フレンドリー"},
    {"id": "agent-009", "name": "MathSolver", "emoji": "🧮", "specialty": "数学・統計解析", "style": "論理的"},
    {"id": "agent-010", "name": "LegalBot", "emoji": "⚖️", "specialty": "法律文書・契約書", "style": "厳格"},
    {"id": "agent-011", "name": "FinanceAI", "emoji": "💰", "specialty": "財務分析・投資", "style": "慎重"},
    {"id": "agent-012", "name": "HealthBot", "emoji": "🏥", "specialty": "健康情報・医療翻訳", "style": "丁寧"},
    {"id": "agent-013", "name": "RecipeAI", "emoji": "🍳", "specialty": "レシピ・料理提案", "style": "楽しい"},
    {"id": "agent-014", "name": "TravelBot", "emoji": "✈️", "specialty": "旅行計画・観光情報", "style": "ワクワク"},
    {"id": "agent-015", "name": "NewsBot", "emoji": "📰", "specialty": "ニュース要約・トレンド", "style": "速報"},
    {"id": "agent-016", "name": "EduBot", "emoji": "📚", "specialty": "教育・学習支援", "style": "わかりやすい"},
    {"id": "agent-017", "name": "MarketBot", "emoji": "📈", "specialty": "市場調査・競合分析", "style": "客観的"},
    {"id": "agent-018", "name": "SocialBot", "emoji": "📱", "specialty": "SNS投稿・バズコンテンツ", "style": "バイラル"},
    {"id": "agent-019", "name": "EmailBot", "emoji": "📧", "specialty": "メール作成・返信", "style": "ビジネス"},
    {"id": "agent-020", "name": "PresentBot", "emoji": "🎯", "specialty": "プレゼン資料・スライド", "style": "説得力"},
    {"id": "agent-021", "name": "VideoBot", "emoji": "🎬", "specialty": "動画スクリプト・台本", "style": "エンタメ"},
    {"id": "agent-022", "name": "PodcastAI", "emoji": "🎙️", "specialty": "ポッドキャスト台本・構成", "style": "自然"},
    {"id": "agent-023", "name": "BrandBot", "emoji": "🏷️", "specialty": "ブランディング・ネーミング", "style": "クリエイティブ"},
    {"id": "agent-024", "name": "ResumeBot", "emoji": "📄", "specialty": "履歴書・職務経歴書", "style": "フォーマル"},
    {"id": "agent-025", "name": "SurveyBot", "emoji": "📋", "specialty": "アンケート設計・分析", "style": "客観的"},
    {"id": "agent-026", "name": "AdBot", "emoji": "📣", "specialty": "広告コピー・マーケティング", "style": "訴求力"},
    {"id": "agent-027", "name": "CodeReview", "emoji": "🔍", "specialty": "コードレビュー・品質改善", "style": "厳格"},
    {"id": "agent-028", "name": "TestBot", "emoji": "🧪", "specialty": "テストケース生成", "style": "網羅的"},
    {"id": "agent-029", "name": "DocBot", "emoji": "📖", "specialty": "ドキュメント作成・API仕様", "style": "明確"},
    {"id": "agent-030", "name": "IdeaBot", "emoji": "💡", "specialty": "アイデア発想・ブレスト", "style": "発散的"},
]

CATEGORIES = ["コーディング", "文章生成", "データ分析", "翻訳", "画像処理", "マーケティング", "教育", "ビジネス"]


def generate_skill_for_agent(agent: dict) -> dict:
    """Claudeを使ってエージェントのスキルを生成する"""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    prompt = f"""あなたは{agent['name']}（{agent['specialty']}専門のAIエージェント）です。
スタイル: {agent['style']}

以下のフォーマットでスキルをJSONで1つ生成してください：
{{
  "title": "スキルタイトル（簡潔で具体的）",
  "description": "スキルの説明（100文字以内、具体的な価値提案）",
  "category": "{random.choice(CATEGORIES)}",
  "price": 価格（500〜9800の整数、JPY）,
  "tags": ["タグ1", "タグ2", "タグ3"]
}}

実用的で市場性の高いスキルを生成してください。JSONのみ返してください。"""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        content = message.content[0].text.strip()
        # JSONを抽出
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        skill_data = json.loads(content)
        skill_data["agent_id"] = agent["id"]
        skill_data["agent_name"] = agent["name"]
        skill_data["agent_emoji"] = agent["emoji"]
        skill_data["generated_at"] = datetime.now().isoformat()
        return skill_data
    except Exception as e:
        print(f"エラー: {agent['name']}: {e}")
        return None


def generate_daily_skills(num_agents: int = 5) -> list:
    """毎日指定した数のエージェントがスキルを生成"""
    selected_agents = random.sample(AI_AGENTS, min(num_agents, len(AI_AGENTS)))
    skills = []
    for agent in selected_agents:
        skill = generate_skill_for_agent(agent)
        if skill:
            skills.append(skill)
            print(f"✅ {agent['name']}: {skill.get('title', 'N/A')}")
    return skills


if __name__ == "__main__":
    import sys
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print(f"🤖 {num}体のエージェントがスキル生成中...")
    skills = generate_daily_skills(num)
    print(f"\n✅ {len(skills)}件のスキル生成完了:")
    for s in skills:
        print(f"  - {s.get('agent_name')}: {s.get('title')} (¥{s.get('price')})")
