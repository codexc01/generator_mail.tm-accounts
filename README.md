# 📨 Telegram Temporary Mail Bot

An asynchronous Telegram bot built with **aiogram 3** that instantly provisions temporary email addresses for users (via the `mail.tm` API) and automatically forwards incoming emails directly to the Telegram chat in real-time.

## ✨ Features

* **One-Click Generation:** Sending the `/start` command automatically registers a random mailbox and delivers the credentials.
* **Fully Asynchronous:** Powered by `aiogram` and `httpx`, ensuring non-blocking network requests to the mail API.
* **Background Live-Polling:** Checks for new emails every 5 seconds for each active user in the background, offering instant delivery.
* **Deployment Ready:** Minimalistic codebase with no complex database requirements (uses in-memory runtime storage).

## 🛠 Tech Stack

* **Python 3.8+**
* **aiogram 3.x** (Telegram Bot API framework)
* **httpx** (Asynchronous HTTP client)
* **mail.tm API** (Temporary email service)


 ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

 
 # 📨 Telegram Бот Временной Почты (Temporary Mail Bot)

Асинхронный Telegram-бот на фреймворке **aiogram 3**, который мгновенно создает для пользователя временный почтовый ящик (используя API сервиса `mail.tm`) и автоматически пересылает все входящие письма прямо в чат Telegram в режиме реального времени.

## ✨ Особенности

* **Генерация в один клик:** При отправке команды `/start` бот автоматически регистрирует случайный ящик и выдает его реквизиты.
* **Полная асинхронность:** Написан с использованием `aiogram` и `httpx`, что обеспечивает быструю работу без блокировки потоков при запросах к API почты.
* **Фоновая проверка (Live-Polling):** Бот проверяет новые письма каждые 5 секунд для каждого активного пользователя в фоновом режиме и мгновенно доставляет их.
* **Простая архитектура:** Минималистичный код без необходимости настройки сложных баз данных (данные активных сессий хранятся в оперативной памяти).

## 🛠 Стек технологий

* **Python 3.8+**
* **aiogram 3.x** (Один из лучших фреймворков для Telegram Bot API)
* **httpx** (Современный асинхронный HTTP-клиент)
* **mail.tm API** (Сервис создания временных почтовых ящиков)
