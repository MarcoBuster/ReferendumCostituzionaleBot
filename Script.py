# By starting this script, a post with hourly stats will sent to all users

from Bot import *
import API

import sqlite3
conn = sqlite3.connect('/home/marcobuster/ReferendumCostituzionaleBot/Bot.db')
c = conn.cursor()

c.execute('SELECT * FROM users')
rows = c.fetchall()
conn.commit()

text = "<b>RESOCONTO ORARIO REFERENDUM</b>" + API.message_format(API.get_referendum(API.Referendum())).replace('<b>Referendum costituzionale • spoglio schede</b>', '')

for res in rows:
    try:
        bot.chat(res[0]).send(text, notify=False)
    except botogram.api.ChatUnavailableError:
        API.remove_user(res[0])
    except Exception as e:
        continue
