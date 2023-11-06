from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import BoundFilter

class IsFile(BoundFilter):
	def __init__(self) -> None:
		super(IsFile, self).__init__()

	async def check(self, message: types.Message) -> bool:
		return message.get_args() != ''