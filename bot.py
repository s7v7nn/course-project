import os
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

logging.basicConfig(level=logging.INFO)


DATABASE_PATH = os.path.join(os.getcwd(), 'c:\\Users\\grits\\Desktop\\bot\\gallery.db')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'c:\\Users\\grits\\Desktop\\bot\\images')


os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

def initialize_database():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS paintings (
            id INTEGER PRIMARY KEY,
            artist_name TEXT NOT NULL,
            painting_title TEXT NOT NULL,
            image_path TEXT NOT NULL,
            genre TEXT NOT NULL,
            UNIQUE(artist_name, painting_title)  
        )
        ''')
        conn.commit()  

initialize_database()

TOKEN = '...'  

bot = Bot(token=TOKEN)
dp = Dispatcher()

def file_exists(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path)

@dp.message(Command(commands=['start']))
async def start(message: types.Message):
    start_text = (
        "Добро пожаловать! Я ваш виртуальный помощник. Вот доступные команды:\n"
        "/button - Показать меню с кнопками\n"
        "/reset - Сбросить чат\n"
        "/help - Показать это сообщение"
    )
    await message.answer(start_text)

@dp.message(Command(commands=['button']))
async def button(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Поиск по художникам', callback_data='search_paintings')
    builder.button(text='Поиск по жанрам', callback_data='search_genre')
    builder.adjust(2, 2, 2)  

    await message.answer(
        'Здравствуйте! Я ваш виртуальный помощник по поиску картин, выберите удобный для Вас вариант поиска.', 
        reply_markup=builder.as_markup()
    )

@dp.message(Command(commands=['reset']))
async def reset(message: types.Message):
    await message.answer('Чат был сброшен. Начните сначала, используя команды.')

@dp.message(Command(commands=['help']))
async def help_command(message: types.Message):
    help_text = (
        "Доступные команды:\n"
        "/button - Показать меню с кнопками\n"
        "/reset - Сбросить чат\n"
        "/help - Показать это сообщение"
    )
    await message.answer(help_text)


@dp.callback_query()
async def callback_handler(call: types.CallbackQuery):
    if call.data == 'search_paintings':
        await call.message.answer("Введите полностью ФИО художника:")
        await call.answer()

    elif call.data == 'search_genre':
        builder = InlineKeyboardBuilder()
        builder.button(text='Пейзаж', callback_data='Пейзаж')
        builder.button(text='Портрет', callback_data='Портрет')
        builder.button(text='Абстракция', callback_data='Абстракция')
        builder.button(text='Натюрморт', callback_data='Натюрморт')
        builder.button(text='Жанровая живопись', callback_data='Жанровая живопись')
        builder.button(text='Бытовой', callback_data='Бытовой')
        builder.button(text='Автопортрет', callback_data='Автопортрет')
        builder.button(text='Композиция', callback_data='Композиция')
        builder.button(text='Экспрессионизм', callback_data='Экспрессионизм')
        builder.button(text='Фовизм', callback_data='Фовизм')
        builder.button(text='Батальная сцена', callback_data='Батальная сцена')
        builder.button(text='Жанровая сцена', callback_data='Жанровая сцена')
        builder.button(text='Импрессионизм', callback_data='Импрессионизм')
        builder.button(text='Композиция', callback_data='Композиция')
        builder.button(text='Манифест', callback_data='Манифест')
        builder.button(text='Мифологический', callback_data='Мифологический')
        builder.button(text='Метафизический', callback_data='Метафизический')
        builder.button(text='Комбинированный', callback_data='Комбинированный')
        builder.button(text='Реализм', callback_data='Реализм')
        builder.button(text='Религиозный', callback_data='Религиозный')
        builder.button(text='Супрематизм', callback_data='Супрематизм')
        builder.button(text='Сюрреализм', callback_data='Сюрреализм')
        builder.button(text='Современный', callback_data='Современный')
        builder.button(text='Символизм', callback_data='Символизм')
        builder.button(text='Стрит-арт', callback_data='Стрит-арт')
        builder.button(text='Трони', callback_data='Трони')
        builder.button(text='Фовизм', callback_data='Фовизм')
        builder.button(text='Фигуратив', callback_data='Фигуратив')
        builder.button(text='Экспрессионизм', callback_data='Экспрессионизм')
        builder.button(text='Neo-Pop Art', callback_data='Neo-Pop Art')
        builder.adjust(1)

        await call.message.answer("Выберите жанр:", reply_markup=builder.as_markup())

    
    elif call.data in ['Пейзаж', 'Портрет', 'Абстракция', 'Натюрморт', 'Жанровая живопись', 'Бытовой', 'Автопортрет', 'Композиция', 'Экспрессионизм', 'Фовизм', 'Батальная сцена', 'Жанровая сцена', 'Импрессионизм', 'Композиция', 'Манифест', 'Мифологический', 'Метафизический', 'Комбинированный', 'Реализм', 'Религиозный', 'Супрематизм', 'Сюрреализм', 'Современный', 'Символизм', 'Стрит-арт', 'Трони', 'Фовизм', 'Фигуратив', 'Экспрессионизм', 'Neo-Pop Art']:
        genre = call.data
        
        await call.message.answer(f"Вы выбрали жанр: {genre}")
        
        paintings = get_paintings_by_genre(genre)
        if paintings:
            for painting in paintings:
                await call.message.answer(painting['title'])  
                image_path = painting['image_url']
                
                if os.path.exists(image_path):
                    try:
                        file = types.FSInputFile(image_path)
                        
                        await bot.send_document(call.message.chat.id, document=file)
                        logging.info(f"Изображение {painting['title']} отправлено успешно.")
                    except Exception as e:
                        logging.error(f"Ошибка при отправке изображения: {e}")
                        await call.message.answer(f"Ошибка при отправке изображения: {e}")
                else:
                    logging.error(f"Файл изображения для {painting['title']} не найден.")
                    await call.message.answer(f"Файл изображения для {painting['title']} не найден.")
        else:
            await call.message.answer("К сожалению, картины не найдены.")



@dp.message()
async def get_artist_name(message: types.Message):
    artist_name = message.text.strip()
    paintings = search_paintings_by_artist(artist_name)

    if paintings:
        for painting in paintings:
            await message.answer(painting['title'])  
            image_path = painting['image_url']

            if os.path.exists(image_path):
                try:
                    file = types.FSInputFile(image_path)
                    await bot.send_document(message.chat.id, document=file)
                except Exception as e:
                    await message.answer(f"Ошибка при отправке изображения: {e}")
            else:
                await message.answer(f"Файл не найден: {image_path}")
    else:
        await message.answer(f"К сожалению, картины художника {artist_name} не найдены.")

def search_paintings_by_artist(artist_name):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT a.name, p.title, p.image_path
            FROM artists AS a
            JOIN paintings AS p ON a.id = p.artist_id
            WHERE a.name LIKE ?
        ''', (f'%{artist_name}%',))
        results = cur.fetchall()
    return [{'artist_name': row[0], 'title': row[1], 'image_url': row[2]} for row in results]

def get_paintings_by_genre(genre):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT title, image_path FROM paintings WHERE genre = ?", (genre,))
        rows = cur.fetchall()

    return [{'title': row[0], 'image_url': row[1]} for row in rows]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))


