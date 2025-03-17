import os
import subprocess
from aiogram import Bot
from aiogram.types import FSInputFile
from datetime import datetime
import gzip

# Замените на ваш токен
API_TOKEN = ''

# Замените на ваш chat_id
CHAT_ID = ''

# Настройки PostgreSQL
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = '5432'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DUMP_FILE = os.path.join(SCRIPT_DIR, 'name.dump')

bot = Bot(token=API_TOKEN)

# Сжатие файла дампа
def compress_dump():
    current_date = datetime.now().strftime('%d.%m.%Y')
    compressed_file = os.path.join(SCRIPT_DIR, f'db_dump_{current_date}.gz')
    with open(DUMP_FILE, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            f_out.writelines(f_in)
    return compressed_file

# Функция для создания дампа базы данных
def create_db_dump():
    try:
        command = [
            'pg_dump',
            '-U', DB_USER,
            '-h', DB_HOST,
            '-p', DB_PORT,
            '-d', DB_NAME,
            '-f', DUMP_FILE
        ]
        
        # Устанавливаем переменную окружения для пароля
        env = os.environ.copy()
        env['PGPASSWORD'] = DB_PASSWORD
        subprocess.run(command, check=True, env=env)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании дампа: {e}")
        return False

async def main():
    if create_db_dump():
        # Сжимаем дамп
        compressed_file = compress_dump()
        
        # Отправляем сжатый файл в Telegram
        await bot.send_document(chat_id=CHAT_ID, document=FSInputFile(compressed_file))
        
        # Удаляем временные файлы
        os.remove(DUMP_FILE)  # Удаляем оригинальный файл дампа
        os.remove(compressed_file)  # Удаляем сжатый файл
    else:
        await bot.send_message(chat_id=CHAT_ID, text="Ошибка при создании дампа базы данных.")

# Запуск скрипта
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
