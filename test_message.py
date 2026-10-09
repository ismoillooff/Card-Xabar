import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

client = TelegramClient("test_session", API_ID, API_HASH)


KIRIM_XABAR = """🟢 Perevod na kartu
➕ 50 000.00 UZS
💳 ***6909
📍 P2P ANOR HUMO NA DR UZKART, UZ
🕓 09.01.26 16:45
💵 1 386 711.20 UZS"""

CHIQIM_XABAR = """🔴 Spisanie c karty
➖ 50 000.00 UZS
💳 ***6909
📍 PAYME P2P, UZ
🕓 09.01.26 16:44
💵 1 336 711.20 UZS"""


async def main():
    await client.start()
    me = await client.get_me()
    
    print("Test xabarlarni tanlang:")
    print("1 - Pul kirimi (🟢 ➕) - guruhga yuboriladi")
    print("2 - Pul chiqimi (🔴 ➖) - yuborilmaydi")
    print("3 - Ikkalasini ham yuborish")
    
    choice = input("\nTanlang (1/2/3): ")
    
    if choice == "1":
        await client.send_message("me", KIRIM_XABAR)
        print("✅ Pul kirimi xabari yuborildi (o'zingizga)")
    elif choice == "2":
        await client.send_message("me", CHIQIM_XABAR)
        print("✅ Pul chiqimi xabari yuborildi (o'zingizga)")
    elif choice == "3":
        await client.send_message("me", CHIQIM_XABAR)
        await asyncio.sleep(1)
        await client.send_message("me", KIRIM_XABAR)
        print("✅ Ikkala xabar ham yuborildi (o'zingizga)")
    else:
        print("❌ Noto'g'ri tanlov")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
