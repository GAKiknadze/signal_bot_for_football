
# Proxies file
PROX_NAME = 'proxies'

# Data base NAME
DB_NAME = 'base.sqlite3'
# Telegram API Key
API_KEY = ''
# Chat id
CHAT_ID = ''

# USER_AGENT
HEADERS = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.27; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; InfoPath.1); UnAuth-State'}
# Hello msg
START_MSG = 'Вы подписаны на рассылку'
# Here We Go Again
RESTART_MSG = 'Перезагрузка!'
# Pattern of msg
PATTERN_MSG = 'Лига:\t{}\n{} / {}\nСчёт: {}/{}\nВремя: {}\nУгловые: {} / {}'

# Parsing URL
START_URL = 'http://www.nowgoal3.com/gf/data/bf_us.js?{}'
# Match URL
MATCH_URL = 'http://www.nowgoal3.com/match/live-{}'
MIN_TIME = 80
MAX_TIME = 90


# Compare match
COMPARE_MATCH_SQL = 'SELECT goals_a, goals_b, ugol_a, ugol_b, checked FROM football WHERE match = ?;'
# Update INFO
UPDATE_MATCH_SQL = 'UPDATE football SET goals_a = ?, goals_b = ?, ugol_a = ?, ugol_b = ?, time = ?, checked = ? WHERE match = ?;'
# Insert INFO
NEW_MATCH_SQL = 'INSERT INTO football VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);'
# Add new user
ADD_USER_SQL = 'INSERT INTO user VALUES (?, ?);'
# Get user
GET_USER_SQL = 'SELECT tg FROM user;'
# Get new matches
GET_NEW_MATCHES = 'SELECT match, ligue, name_a, name_b, goals_a, goals_b, ugol_a, ugol_b, time FROM football WHERE checked = ?;'
# Pin matches
PIN_NEW_MATCHES = 'UPDATE football SET checked = ? WHERE checked = ?;'
