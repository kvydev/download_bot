from aiogram import Bot, Dispatcher, executor, types, md
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from filters import IsFile
from middlewares import AddUser
from db import db
import keyboards

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

db = db()

@dp.message_handler(IsFile(), commands='start')
async def start(message: types.Message):
	link = message.get_args()
	n = '\n'
	await message.delete()
	await message.answer(f'Чтобы получить файл, вам нужно быть подписаным на каналы\n\n{md.hspoiler(f"Список каналов можно редактировать в админ панели{n}Если бот добавлен в админы канала, то пользователь не сможет получить файл без подписки")}', reply_markup=keyboards.download(link), parse_mode=types.ParseMode.HTML)
	db.add_view(link, message.chat.id)

@dp.message_handler(commands='start')
async def start(message: types.Message):
	await message.answer(f'🤖 Тестовый бот для скачивания файлов с правами администратора\n\n💾 Вы можете загрузить файл в бота, для этого отправьте его в чат и получите ссылку на установку\n\nДля заказа бота обращаться к: @kvydev')

@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def get_file(message: types.Message):
	link = db.add_fid(message.document.file_id, message.chat.id)
	await message.reply(f'Ссылка на установку - {BOT_URL}?start={link}')

@dp.callback_query_handler(lambda query: query.data.startswith('like'))
async def like(query: types.CallbackQuery):
	link = query.data.split('_')[1]
	try:
		db.like(link, query.message.chat.id)
		likes, dislikes = db.get_rating_file(link, query.message.chat.id)
		await query.message.edit_reply_markup(keyboards.rating(link, likes, dislikes))
		await query.answer('Спасибо за оценку!')
	except:
		await query.answer('Вы уже поставили оценку')

@dp.callback_query_handler(lambda query: query.data.startswith('dislike'))
async def like(query: types.CallbackQuery):
	link = query.data.split('_')[1]
	try:
		db.dislike(link, query.message.chat.id)
		likes, dislikes = db.get_rating_file(link, query.message.chat.id)
		await query.message.edit_reply_markup(keyboards.rating(link, likes, dislikes))
		await query.answer('Спасибо за оценку!')
	except:
		await query.answer('Вы уже поставили оценку')

@dp.callback_query_handler()
async def download(query: types.CallbackQuery):
	try:
		likes, dislikes = db.get_rating_file(query.data, query.message.chat.id)
		await query.message.answer_document(db.get_fid(query.data, query.message.chat.id), reply_markup=keyboards.rating(query.data, likes, dislikes))
		db.add_download(query.data, query.message.chat.id)
	except:
		await query.answer('Файл не найден', show_alert=True)
	finally:
		await query.message.delete()

if __name__ == '__main__':
	db.create_db()
	dp.setup_middleware(AddUser())
	executor.start_polling(dp)