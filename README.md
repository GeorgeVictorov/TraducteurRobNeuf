# Traducteur Rob Neuf

«Neuf» - from French language may mean «nine» or «new» - it's up to you to decide.

More than 200000 translations already made.

## Introduction

Welcome to our multi-language translator bot!

This is not your average translator bot.

To get a translation, simply type in your message.

We support translation between 9 languages and even have an auto-detect feature for convenience.

🇨🇳 Chinese
🇬🇧 English
🇮🇳 Hindi

🇪🇸 Spanish
🇫🇷 French
🇸🇦 Arabic

🇧🇩 Bengali
🇵🇹 Portuguese
🇷🇺 Russian

🌐 Auto Detect

The project employs [aiogram](https://github.com/aiogram/aiogram), [googletrans](https://github.com/ssut/py-googletrans)
and [psycopg](https://github.com/psycopg/psycopg) for its core functionalities.

Users configurations are stored in [PostgreSQL database](https://www.postgresql.org),
with user IDs hashed using SHA256 to ensure they cannot be retrieved again.

## Check out Traducteur Rob Neuf [here](https://t.me/TraducteurRobNeufBot).

## Overview

![overview 12 09 12](https://github.com/GeorgeVictorov/TraducteurRobNeuf/assets/120365126/0d9ed058-6a00-45a1-811d-588e9df0d550)

## Project structure

```bash
TraducteurRobNeuf
├── config_data
│   └── config.py
│   └── langs.py
├── database
│   └── db.py
│   └── select_data.py
│   └── users_postgres.py
│   └── users_stats.py
├── handlers
│   └── other_handlers.py
│   └── user_handlers.py
├── keyboards
│   └── keyboards.py
│   └── main_menu.py
├── lexicon
│   └── lexicon.py
├── logger
│   └── logger.py
├── services
│   └── services.py
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```
