# PanelimAze botu – yalnız AI ilə cavab verir (OpenRouter), sabit hazır cavab yoxdur
# pip install python-telegram-bot --upgrade
# pip install openai

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
from openai import OpenAI, OpenAIError

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "8410980542:AAFq59KidGoyobAr17diIXIGlDj0EAcYx9M"
OPENROUTER_API_KEY = "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"

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Aktual pulsuz model (yanvar 2026)
MODEL = "xiaomi/mimo-v2-flash:free"  # 262K context, güclü, agentik

# Alternativlər (işləməzsə bunları sına):
# MODEL = "mistralai/devstral-2512:free"
# MODEL = "allenai/molmo-2-8b:free"
# MODEL = "liquid/lfm-2.5-1.2b-instruct:free"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Salam {user.first_name}! 👋\n\n"
        "Mən PanelimAze botuyam – PanelimAze.com-un rəsmi köməkçisiyəm.\n"
        "Sifariş, balans, xidmət, qiymət... hər şeyi soruş, dərhal cavab verim!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text.strip()

    if not user_text:
        return  # boş mesajı keç

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sən PanelimAze.com-un rəsmi Telegram botusan. Adın PanelimAze botudur. "
                        "Heç vaxt 'AI', 'yapay zeka', 'model', 'OpenRouter', 'API', 'limit' və ya texniki detallar demə. "
                        "Cavablarını həmişə Azərbaycan dilində ver. "
                        "Dostcanlı, enerjili, qısa və SMM paneli tərzində ol: like, abunə, izlənmə, sifariş, balans, qiymət mövzularında kömək et. "
                        "Adını soruşanda 'PanelimAze botuyam' de. "
                        "Hər suala uyğun cavab ver, susma və ya 'gecikmə var' demə – həmişə faydalı ol. "
                        "Əgər sual SMM ilə bağlıdırsa, realistik qiymət/sifariş təklifləri ver. "
                        "Digər suallara da normal, maraqlı cavab ver, amma PanelimAze tərzini qoru."
                    )
                },
                {"role": "user", "content": user_text}
            ],
            max_tokens=400,
            temperature=0.85
        )
        ai_answer = response.choices[0].message.content.strip()
        await update.message.reply_text(ai_answer)

    except OpenAIError as api_err:
        logger.error(f"API xətası: {api_err}")
        await update.message.reply_text(
            "Hazırda sistemdə yüngül gecikmə var... 😅 Amma narahat olma, yenə yaz – dərhal həll edərik!"
        )
    except Exception as e:
        logger.error(f"Xəta: {e}")
        await update.message.reply_text(
            "Bir anlıq problem çıxdı... Yenə sualını yaz görüm, kömək edəcəm!"
        )

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Bütün mesajlar → yalnız AI
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("PanelimAze botu başladı (yalnız AI cavabları ilə)... 🚀")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
