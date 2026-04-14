import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from g4f.client import AsyncClient
import g4f

# --- SOZLAMALAR ---
# MUHIM: Agar Conflict xatosi ketavermasa, @BotFather orqali yangi token oling!
TOKEN = "8778676243:AAFhlhEcm91mnWntTO0etF0MF2-QNyHaAAc"

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = AsyncClient()

# Xatolarni terminalda ko'rish uchun sozlama
logging.basicConfig(level=logging.INFO)

# --- RENDER/SERVER PORT UCHUN (Health Check) ---
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
    logging.info(f"Veb-server {port}-portda ishga tushdi.")

# --- BOT HANDLERLARI ---
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}! 👋 Men tayyorman. Savolingizni bering!")

@dp.message(F.text)
async def ai_chat(message: types.Message):
    # Foydalanuvchi kutib turishi uchun xabar
    wait_msg = await message.answer("🤖 O'ylayapman...")
    
    try:
        # 'gpt-4o' hozirda g4f kutubxonasida eng barqaror modallardan biri
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message.text}],
        )
        
        answer = response.choices[0].message.content

        if answer and len(answer) > 0:
            await wait_msg.edit_text(answer)
        else:
            raise Exception("AI bo'sh javob qaytardi (Provayder xatosi).")

    except Exception as e:
        # Terminalda aniq xatolikni ko'rish (MUHIM!)
        logging.error(f"AI XATOLIK TAFSILOTI: {str(e)}")
        
        # Foydalanuvchiga tushunarli xato xabari
        await wait_msg.edit_text("❌ Hozirda bepul AI serverlari band. Iltimos, 1 daqiqadan so'ng qayta urinib ko'ring.")

# --- ASOSIY ISHGA TUSHIRISH ---
async def main():
    # 1. Web serverni yurgizish (Render.com uchun)
    await start_web_server()

    # 2. Conflict (to'qnashuv)ni oldini olish:
    # Eski ulanishlarni uzish va navbatda qolib ketgan xabarlarni o'chirib yuborish
    logging.info("Eski sessiyalar tozalanmoqda...")
    await bot.delete_webhook(drop_pending_updates=True)

    # 3. Botni ishga tushirish
    logging.info("Bot polling rejimida muvaffaqiyatli ishga tushdi.")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot qo'lda to'xtatildi.")
