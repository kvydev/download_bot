from aiogram import types

def download(fid):
	mk = types.InlineKeyboardMarkup()
	mk.add(types.InlineKeyboardButton(text='Канал #1', url='t.me/telegram'))
	mk.add(types.InlineKeyboardButton(text='Я подписался', callback_data=fid))
	return mk

def rating(fid, likes, dislikes):
	mk = types.InlineKeyboardMarkup()
	mk.add(types.InlineKeyboardButton(text=f'👍 {likes}', callback_data=f'like_{fid}'))
	mk.insert(types.InlineKeyboardButton(text=f'{dislikes} 👎', callback_data=f'dislike_{fid}'))
	return mk