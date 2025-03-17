# dumpDB_bot
бэкап постгреса в телеграм каждый день через Cron
1. pip install aiogram==3.6.0
2. Создаем задачу в Cron'e:
sudo crontab -e
0 18 * * * source /root/dumpDB_bot/venv/bin/activate && /usr/bin/python /root/dumpDB_bot/script.py # Каждый день в 6 p.m
