import os
import re
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

PHONE_NUMBER = os.getenv("PHONE_NUMBER", "+998994048747")

GROUP_ID = int(os.getenv("GROUP_ID"))

SOURCE_BOT_ID = 915326936

client = TelegramClient("userbot_session", API_ID, API_HASH)

TEST_KIRIM = """🟢 Perevod na kartu
➕ 50 000.00 UZS
💳 ***6909
📍 P2P ANOR HUMO NA DR UZKART, UZ
🕓 09.01.26 16:45
💵 1 386 711.20 UZS"""

TEST_CHIQIM = """🔴 Spisanie c karty
➖ 50 000.00 UZS
💳 ***6909
📍 PAYME P2P, UZ
🕓 09.01.26 16:44
💵 1 336 711.20 UZS"""


def format_message(text: str) -> str:
    amount_match = re.search(r'[➕➖]\s*([\d\s]+\.?\d*)\s*UZS', text)
    card_match = re.search(r'💳\s*(\*{3}\d+)', text)
    location_match = re.search(r'📍\s*(.+?)(?:\n|$)', text)
    time_match = re.search(r'🕓\s*(.+?)(?:\n|$)', text)
    balance_match = re.search(r'💵\s*([\d\s]+\.?\d*)\s*UZS', text)

    amount = amount_match.group(1).strip() if amount_match else "N/A"
    card = card_match.group(1).strip() if card_match else "N/A"
    location = location_match.group(1).strip() if location_match else "N/A"
    time = time_match.group(1).strip() if time_match else "N/A"
    balance = balance_match.group(1).strip() if balance_match else "N/A"

    formatted = f"""
╔══════════════╗
║   💰 PUL KIRIMI ANIQLANDI 💰 
╠══════════════╣
║                               
║  💵 Summa:  +{amount} UZS
║                               
║  💳 Karta:  {card}
║                               
║  📍 Manba:  {location}
║                               
╠══════════════╣
║       🕐 Vaqt:   {time}
╚══════════════╝
""".strip()

    return formatted


@client.on(events.NewMessage(pattern=r"^/test$", outgoing=True))
async def test_command(event):
    try:
        formatted_test = format_message(TEST_KIRIM)
        await client.send_message(GROUP_ID, formatted_test)
        await event.edit("✅ Test xabar (pul kirimi) guruhga yuborildi!")
        print("✅ /test buyrug'i bajarildi")
    except Exception as e:
        await event.edit(f"❌ Xatolik: {e}")


@client.on(events.NewMessage(pattern=r"^/line$", outgoing=True))
async def line_command(event):
    try:
        await client.send_message(GROUP_ID, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        await event.edit("✅ Ajratuvchi chiziq yuborildi!")
        print("✅ /line buyrug'i bajarildi")
    except Exception as e:
        await event.edit(f"❌ Xatolik: {e}")


@client.on(events.NewMessage(from_users=SOURCE_BOT_ID))
async def handler(event):
    try:
        message = event.message
        text = message.text or ""

        if "➕" not in text and "🟢" not in text:
            print(f"⏭️ Chiqim xabari - o'tkazib yuborildi")
            return

        if "➖" in text or "🔴" in text:
            print(f"⏭️ Chiqim xabari - o'tkazib yuborildi")
            return

        print(f"📥 Pul kirimi aniqlandi!")

        formatted_text = format_message(text)

        if message.media:
            await client.send_file(
                GROUP_ID,
                message.media,
                caption=formatted_text
            )
            print(f"✅ Media xabar guruhga yuborildi")
        else:
            await client.send_message(GROUP_ID, formatted_text)
            print(f"✅ Matn xabari guruhga yuborildi")

    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")


async def main():
    print("🚀 Userbot ishga tushmoqda...")
    print(f"📱 Telefon: {PHONE_NUMBER}")

    await client.start(phone=PHONE_NUMBER)

    me = await client.get_me()
    print(f"✅ Userbot muvaffaqiyatli ishga tushdi!")
    print(f"👤 Account: {me.first_name} (@{me.username})")
    print(f"🆔 Bot ID: {SOURCE_BOT_ID} dan xabarlar kuzatilmoqda")
    print(f"📤 Xabarlar guruhga yuboriladi: {GROUP_ID}")
    print("=" * 50)
    print("📋 Buyruqlar:")
    print("   /test - Test xabar yuborish")
    print("   /line - Ajratuvchi chiziq yuborish")
    print("=" * 50)
    print("Userbot ishlayapti... Xabarlar kuzatilmoqda...")

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
