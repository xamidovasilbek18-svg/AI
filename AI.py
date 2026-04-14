import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from g4f.client import AsyncClient
from g4f import Provider

# --- SOZLAMALAR ---
TOKEN = "8778676243:AAFhlhEcm91mnWntTO0etF0MF2-QNyHaAAc"

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = AsyncClient()

logging.basicConfig(level=logging.INFO)

# --- RENDER PORT XATOLIGINI TUZATISH ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render avtomatik beradigan PORT ni eshitadi
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server {port}-portda ishga tushdi.")

# --- BOT HANDLERLARI ---
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        f"Salom {message.from_user.full_name}! 👋\n"
        "Men aqlli AI botman. Menga xohlagan savolingizni bering, javob berishga harakat qilaman!"
    )

@dp.message(F.text)
async def ai_chat(message: types.Message):
    # Foydalanuvchi kutib qolmasligi uchun
    wait_msg = await message.answer("🤖 O'ylayapman...")
    
    try:
        # AI dan javob olish (Blackbox provayderi orqali)
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            provider=Provider.Blackbox, # Eng barqaror provayder
            messages=[{"role": "user", "content": message.text}],
        )
        
        answer = response.choices.message.content
        
        if not answer:
            raise Exception("Bo'sh javob keldi")

        await wait_msg.edit_text(answer)
        
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await wait_msg.edit_text("❌ Kechirasiz, hozirda javob bera olmayman. Birozdan so'ng qayta urinib ko'ring.")

# --- ASOSIY ISHGA TUSHIRISH ---
async def main():
    # 1. Web serverni ishga tushiramiz (Render uchun)
    await start_web_server()
    
    # 2. Botni ishga tushiramiz
    print("Bot pollingni boshladi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")
