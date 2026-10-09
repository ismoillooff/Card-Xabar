import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "+998994048747")

client = TelegramClient("userbot_session", API_ID, API_HASH)


async def login():
    print("=" * 50)
    print("🔐 Telegram Login")
    print("=" * 50)
    print(f"📱 Telefon: {PHONE_NUMBER}")
    print()
    
    await client.connect()
    
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"✅ Allaqachon login qilingan!")
        print(f"👤 Account: {me.first_name} (@{me.username})")
        print(f"🆔 User ID: {me.id}")
    else:
        print("📤 Kod yuborilmoqda...")
        await client.send_code_request(PHONE_NUMBER)
        
        print()
        code = input("📥 Telegram'dan kelgan kodni kiriting: ")
        
        try:
            await client.sign_in(PHONE_NUMBER, code)
            print()
            print("✅ Muvaffaqiyatli login qilindi!")
        except SessionPasswordNeededError:
            print()
            password = input("🔑 2FA parolni kiriting: ")
            await client.sign_in(password=password)
            print()
            print("✅ Muvaffaqiyatli login qilindi!")
        
        me = await client.get_me()
        print(f"👤 Account: {me.first_name} (@{me.username})")
        print(f"🆔 User ID: {me.id}")
    
    print()
    print("=" * 50)
    print("✅ Session fayli saqlandi: userbot_session.session")
    print("📌 Endi 'python userbot.py' ni ishga tushiring!")
    print("=" * 50)
    
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(login())
