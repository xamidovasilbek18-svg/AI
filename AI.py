import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from openai import AsyncOpenAI

# 1. Sozlamalar
TOKEN = "TELEGRAM_BOT_TOKEN_SHU_YERGA"
BASE_URL = "https://vsegpt.ru" # Yoki boshqa bepul API provider manzili
API_KEY = "API_KEY_SHU_YERGA"

# 2. Obyektlarni yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)

logging.basicConfig(level=logging.INFO)

# /start komandasi
@dp.message(F.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer("Salom! Men AI botman. Savolingizni yuboring.")

# Asosiy AI chat funksiyasi
@dp.message(F.text)
async def ai_chat(message: types.Message):
    wait_msg = await message.answer("🤖 O'ylayapman...")
    
    # Sinab ko'rish uchun modellar ro'yxati (provayderingizda borlarini yozing)
    models = ["gpt-4o", "gpt-4-turbo", "claude-3-haiku", "llama-3-70b"]
    
    success = False
    for model_name in models:
        try:
            logging.info(f"Sinalmoqda: {model_name}")
            response = await client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": message.text}],
            )
            answer = response.choices[0].message.content
            
            if answer:
                await wait_msg.edit_text(answer)
                success = True
                break 
        except Exception as e:
            logging.error(f"{model_name} xatosi: {e}")
            continue

    if not success:
        await wait_msg.edit_text("❌ Hozirda barcha serverlar band. Keyinroq urinib ko'ring.")

# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")
