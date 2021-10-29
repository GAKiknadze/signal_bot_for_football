from time import time_ns, sleep
from datetime import datetime
from random import randint
from requests import get
import aiosqlite
import asyncio
from config import *

date_now = lambda: datetime.today().strftime("%Y-%m-%d %H.%M.%S")


def time_zone(start, end, smeh):
	form = '%Y-%m-%d %H:%M:%S'
	now = datetime.utcnow().strftime(form)
	calc = datetime.strptime(now, form) - datetime.strptime(end, form)
	k = calc.total_seconds() // 60
	if smeh in [3, 4]:
		k += 45
	return start, end, k


def random_proxy():
	f = open(PROX_NAME)
	proxies = f.read().split('\n')
	f.close()
	ind = randint(0, len(proxies) - 1)
	proxy = proxies[ind]
	return proxy


def parse_start():
	while True:
		proxy = random_proxy()
		print(f'{date_now()}\tИспользуемые прокси {proxy}')
		r = get(START_URL.format(time_ns()), proxies={'http://': proxy,})
		try:
			
			if r.status_code != 200:
				print(f'{date_now()}\tСтатус соедениения {r.status_code}')
				Exception()
			break
		except:
			print(f'{date_now()}\tОшибка соединения с сервером!')
			sleep(5)
	all_data, data, tmp, kmp, all_legue = [], [], [], [], []
	for i in r.text.split(';'):
		if i.startswith('\r\nA['):
			tmp.append(i)
		if i.startswith('\r\nB['):
			kmp.append(i)
	for j in tmp:
		line = []
		crop = j.find(']=[')
		pre_line = j[crop + 3:-2:]
		for k in pre_line.split(','):
			line.append(k.replace("'", ""))
		all_data.append(line)
	for j in kmp:
		line = []
		crop = j.find(']=[')
		pre_line = j[crop + 3:-2:]
		for k in pre_line.split(','):
			line.append(k.replace("'", ""))
		all_legue.append(line)
	for l in all_data:
		try:
			start, end, loc_time = time_zone(l[6], l[7], int(l[8]))
		except:
			continue
		if loc_time < 0 or loc_time > 105:
			continue
		index = int(l[1]) - 1
		try:
			ligue = all_legue[index][2]
		except:
			ligue = 'XXXXXXX'
		li = {
			'id': l[0],
			'ligue': ligue,
			'com_A': l[4].replace('<font color=#880000>(N)</font>', ''),
			'com_B': l[5].replace('<font color=#880000>(N)</font>', ''),
			'goals_A': l[9],
			'goals_B': l[10],
			'ugol_A': l[-8],
			'ugol_B': l[-7],
			'ts_start': start,
			'ts_end': end,
			'time': loc_time,
		}
		data.append(li)
	return data


async def start():
	print(f'{date_now()}\tПарсер работает')
	db = await aiosqlite.connect(DB_NAME)
	cursor = await db.cursor()
	while True:
		matches = parse_start()
		print(f'{date_now()}\tКол-во подходящих матчей:{len(matches)}')
		await cursor.execute(GET_USER_SQL)
		users = await cursor.fetchall()
		for i in matches:
			await cursor.execute(COMPARE_MATCH_SQL, (i['id'],))
			row = await cursor.fetchone()
			if row:
				t = row[4] if row[2] == int(i['ugol_A']) and row[3] == int(i['ugol_B']) else 1
				try:
					vals = (i['goals_A'], i['goals_B'], i['ugol_A'], i['ugol_B'], i['time'], t, i['id'],)
					await cursor.execute(UPDATE_MATCH_SQL, vals)
				except:
					pass
			else:
				vals = i.values()
				await cursor.execute(NEW_MATCH_SQL, (None, *vals, 2,))
		await db.commit()
		sleep(15)

while True:
	# asyncio.run(start())
	try:
		asyncio.run(start())
	except:
		sleep(3)
		print(f'{date_now()}\tПерезапуск парсера')
