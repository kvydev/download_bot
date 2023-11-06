from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from db import db

db = db()

class AddUser(BaseMiddleware):
	def __init__(self) -> None:
		super(AddUser, self).__init__()

	async def on_pre_process_message(self, message: types.Message, data):
		if not db.get_user(message.chat.id):
			db.add_user(message.chat.id)