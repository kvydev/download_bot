import sqlite3

class db:
	def __init__(self) -> None:
		pass

	def create_db(self):
		with sqlite3.connect('db.db') as db:
			db.execute('''CREATE TABLE IF NOT EXISTS files (
				fid TXT,
				link TXT,
				uid INT,
				views INT DEFAULT 0,
				downloads INT DEFAULT 0,
				liked TXT DEFAULT "[]",
				disliked TXT DEFAULT "[]"
			)''')

			db.execute('''CREATE TABLE IF NOT EXISTS users (
				uid INT
			)''')

			db.execute('''CREATE TABLE IF NOT EXISTS sponsor (
				link TXT,
				name TXT,
				chat_id TXT
			)''')
			db.commit()

	def add_user(self, uid):
		with sqlite3.connect('db.db') as db:
			db.execute('insert into users(uid) values (?)', (uid, ))
			db.commit()

	def get_user(self, uid):
		with sqlite3.connect('db.db') as db:
			record = db.execute('select uid from users where uid = ?', (uid, )).fetchone()
			if record is not None:
				return True

	def add_fid(self, fid, uid):
		with sqlite3.connect('db.db') as db:
			record = db.execute('select link from files where uid = ? order by link desc', (uid, )).fetchone()
			if record is None:
				link = 1
			else:
				link = record[0] + 1
			db.execute('insert into files(fid, link, uid) values (?, ?, ?)', (fid, link, uid))
			db.commit()
		return link

	def get_fid(self, link, uid):
		with sqlite3.connect('db.db') as db:
			record = db.execute('select fid from files where (link, uid) = (?, ?)', (link, uid)).fetchone()
			if record is not None:
				return record[0]
	
	def get_rating_user(self, link, uid):
		with sqlite3.connect('db.db') as db:
			record = db.execute('select liked, disliked from files where (link, uid) = (?, ?)', (link, uid)).fetchone()
			if record is not None:
				liked, disliked = (list(record) for record in eval(str(record).replace("'", "")))
				if uid in liked + disliked:
					return True

	def add_view(self, link, uid):
		with sqlite3.connect('db.db') as db:
			db.execute('update files set views = views + 1 where (link, uid) = (?, ?)', (link, uid))
			db.commit()

	def add_download(self, link, uid):
		with sqlite3.connect('db.db') as db:
			db.execute('update files set downloads = downloads + 1 where (link, uid) = (?, ?)', (link, uid))
			db.commit()
	
	def like(self, link, uid):
		with sqlite3.connect('db.db') as db:
			liked, disliked = self.get_list_rated(link, uid)
			if uid in liked:
				liked.remove(uid)
			else:
				if uid in disliked:
					disliked.remove(uid)
				liked.append(uid)
			db.execute('update files set (liked, disliked) = (?, ?) where (link, uid) = (?, ?)', (str(liked), str(disliked), link, uid))
			db.commit()
	
	def dislike(self, link, uid):
		with sqlite3.connect('db.db') as db:
			liked, disliked = self.get_list_rated(link, uid)
			if uid in disliked:
				disliked.remove(uid)
			else:
				if uid in liked:
					liked.remove(uid)
				disliked.append(uid)
			db.execute('update files set (liked, disliked) = (?, ?) where (link, uid) = (?, ?)', (str(liked), str(disliked), link, uid))
			db.commit()

	def get_rating_file(self, link, uid):
		with sqlite3.connect('db.db') as db:
			record = db.execute('select liked, disliked from files where (link, uid) = (?, ?)', (link, uid)).fetchone()
			if record is not None:
				likes, dislikes = (len(list(record)) for record in eval(str(record).replace("'", "")))
				return likes, dislikes
			return 0, 0

	def get_list_rated(self, link, uid):
		with sqlite3.connect('db.db') as db:
			record = db.execute('select liked, disliked from files where (link, uid) = (?, ?)', (link, uid)).fetchone()
			if record is not None:
				liked, disliked = (list(record) for record in eval(str(record).replace("'", "")))
				return liked, disliked