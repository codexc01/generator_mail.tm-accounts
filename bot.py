import asyncio
import logging
import uuid
import random
import string
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import httpx

logging.basicConfig(level=logging.INFO)

TOKEN = "ваш токен от @BotFather"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список случайных слов для почты
RANDOM_WORDS = ["amazing", "brilliant", "creative", "dynamic", "elegant", "fantastic", "genuine", "happy", "incredible", "joyful", "keen", "lively", "mighty", "noble", "optimal", "peaceful", "quantum", "radiant", "stellar", "trusted", "ultimate", "vibrant", "wisdom", "xenial", "youthful", "zealous", "alpha", "bright", "cosmic", "dreamy", "epic", "flowing", "golden", "harmony", "infinite", "journey"]

# Хранилище активных ящиков: {user_id: {"email": ..., "token": ...}}
user_boxes = {}

async def check_mail_loop(user_id, token):
    """Фоновая проверка почты каждые 5 секунд"""
    async with httpx.AsyncClient() as client:
        seen_ids = set()
        while user_id in user_boxes:
            try:
                headers = {"Authorization": f"Bearer {token}"}
                # Получаем список писем
                res = await client.get("https://api.mail.tm/messages", headers=headers)
                if res.status_code == 200:
                    messages = res.json().get("hydra:member", [])
                    for msg in messages:
                        msg_id = msg["id"]
                        if msg_id not in seen_ids:
                            seen_ids.add(msg_id)
                            # Пересылаем текст письма (или тему) пользователю
                            text = f"📩 новое письмо!\nОт: {msg['from']['address']}\nТема: {msg['subject']}\n\nТекст:\n{msg['intro']}"
                            await bot.send_message(user_id, text)
            except Exception:
                pass
            await asyncio.sleep(5)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id

    async with httpx.AsyncClient() as client:
        # 1. Получаем доступный домен
        domain_res = await client.get("https://api.mail.tm/domains")
        domain_res.raise_for_status()
        domain = domain_res.json()["hydra:member"][0]["domain"]

        # 2. Создаем случайный ящик
        random_word = random.choice(RANDOM_WORDS)
        random_digits = str(random.randint(100000000, 999999999))
        username = f"{random_word}_{random_digits}"
        email = f"{username}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        account_res = await client.post("https://api.mail.tm/accounts", json={"address": email, "password": password})
        if account_res.status_code not in (200, 201):
            logging.warning("mail.tm account create failed: %s %s", account_res.status_code, account_res.text)

        # 3. Авторизуемся для получения токена
        token_res = await client.post("https://api.mail.tm/token", json={"address": email, "password": password})
        if token_res.status_code != 200:
            logging.error("mail.tm token error: %s %s", token_res.status_code, token_res.text)
            await message.answer("❌ не удалось создать почту. попробуй снова через пару минут.")
            return

        token = token_res.json().get("token")
        if not token:
            logging.error("mail.tm token missing in response: %s", token_res.text)
            await message.answer("❌ не удалось создать почту. попробуй снова через пару минут.")
            return

        # Сохраняем и запускаем фоновую проверку
        user_boxes[user_id] = {"email": email, "token": token}

        await message.answer(
            f"📋 `{email}`",
            parse_mode="Markdown"
        )
        
        await message.answer(
            f"🔑 `{password}`",
            parse_mode="Markdown"
        )

        # Запуск фоновой задачи для этого пользователя
        asyncio.create_task(check_mail_loop(user_id, token))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())