# dumpDB_bot
бэкап постгреса в телеграм каждый день через Cron
1. Создаем виртуальное окружение python3 -m venv venv     >   sourse venv/bin/activate
2. pip install aiogram==3.6.0
3. Создаем задачу в Cron'e sudo crontab -e
0 18 * * * source /root/dumpDB_bot/venv/bin/activate && /usr/bin/python /root/dumpDB_bot/script.py # Каждый день в 6 p.m
