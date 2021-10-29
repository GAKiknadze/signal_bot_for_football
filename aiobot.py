import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from config import *
from time import sleep
from datetime import datetime
import aiosqlite

date_now = lambda: datetime.today().strftime("%Y-%m-%d %H.%M.%S")

bot = Bot(token=API_KEY)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


async def conn(vals=None, t='add'):
	db = await aiosqlite.connect(DB_NAME)
	cursor = await db.cursor()
	if t == 'add':
		try:
			await cursor.execute(ADD_USER_SQL, vals)
			msg = START_MSG
		except:
			msg = RESTART_MSG
	elif t == 'get':
		# await cursor.execute(GET_USER_SQL)
		# users = await cursor.fetchall()
		await cursor.execute(GET_NEW_MATCHES, (1,))
		data = await cursor.fetchall()
		await cursor.execute(PIN_NEW_MATCHES, (2, 1))
		msg = data
	await db.commit()
	await cursor.close()
	await db.close()
	return msg


# @dp.message_handler(commands="start")
# async def cmd_start(message: types.Message):
# 	uid = message.chat.id
# 	uname = message.from_user.username
# 	msg = await conn((uid, uname))
# 	await message.answer(msg)
# 	await send_message(message)


async def send_message():
	print(f'{date_now()}\tБот запущен!')
	while True:
		data = await conn(t='get')
		if data:
			mess = ''
			for i in data:
				if ((int(i[8]) < MIN_TIME - 45 or int(i[8]) > MAX_TIME - 45) and int(i[8]) < MIN_TIME) or int(i[8]) > MAX_TIME + 15:
					continue
				mess += PATTERN_MSG.format(i[1], i[2], i[3], i[4], i[5], i[8], i[6], i[7]) + '\n\n'
			if mess != '':
				print(f'{date_now()}\tНовые данные уже в канале')
				await bot.send_message(CHAT_ID, mess)
			# await bot.send_message(msg.chat.id, mess)
		sleep(3)


if __name__ == "__main__":
	while True:
		# asyncio.run(send_message())
		try:
			asyncio.run(send_message())
		except:
			print(f'{date_now()}\tПерезагрузка бота')
			sleep(10)
	# executor.start_polling(dp, skip_updates=True)
