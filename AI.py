import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from g4f.client import AsyncClient

# --- SOZLAMALAR ---
TOKEN = "8778676243:AAFhlhEcm91mnWntTO0etF0MF2-QNyHaAAc"

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = AsyncClient()

logging.basicConfig(level=logging.INFO)

# --- RENDER PORT UCHUN ---
async def handle(request):
    return web.Response(text="AI Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# --- BOT HANDLERLARI ---
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}! 👋 Men tayyorman. Savolingizni bering!")

@dp.message(F.text)
async def ai_chat(message: types.Message):
    wait_msg = await message.answer("🤖 O'ylayapman...")
    try:
        # Provayderni olib tashladik, g4f o'zi eng yaxshisini (ishlaydiganini) tanlaydi
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
        )
        answer = response.choices[0].message.content
        await wait_msg.edit_text(answer)
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await wait_msg.edit_text("❌ Hozirda serverlar biroz band. Birozdan so'ng qayta urinib ko'ring.")

async def main():
    await start_web_server()
    # Konfliktni oldini olish uchun avvalgi seanslarni tozalaymiz
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
