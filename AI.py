import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from g4f.client import AsyncClient # Tekin AI provayderi

# Bot tokeningizni bura yozing
TOKEN = "8428517451:AAH1A11KYoi50VcZLyYhmrAhBNbhSpxdHWQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = AsyncClient()

logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}! Men aqlli AI botman. Savollaringizga javob bera olaman. Marhamat, biror nima deb yozing!")

@dp.message(F.text)
async def chat_ai(message: types.Message):
    # Foydalanuvchiga kutish xabarini yuboramiz
    wait_msg = await message.answer("🤖 O'ylayapman...")
    
    try:
        # AI dan javob olish
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
        )
        
        answer = response.choices[0].message.content
        
        # Kutish xabarini AI javobiga almashtiramiz
        await wait_msg.edit_text(answer)
        
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await wait_msg.edit_text("❌ Kechirasiz, javob topishda xatolik yuz berdi.")

async def main():
    print("AI Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
