from bs4 import BeautifulSoup
import requests
import re

import sqlite3
conn = sqlite3.connect('Bot.db')
c = conn.cursor()

try:
    c.execute('CREATE TABLE users(user_id INTEGER)')
except sqlite3.OperationalError: #table already exists
    pass
conn.commit()

REGIONI = [
    'Abruzzo',
    'Basilicata',
    'Calabria',
    'Campania',
    'Emilia Romagna',
    'Friuli Venezia Giulia',
    'Lazio',
    'Liguria',
    'Lombardia',
    'Marche',
    'Molise',
    'Piemonte',
    'Puglia',
    'Sardegna',
    'Sicilia',
    'Toscana',
    'Trentino Alto Adige',
    'Umbria',
    'Valle d\'Aosta',
    'Veneto'
]


class Referendum():
    pass


def add_user(user_id):
    c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    found = c.fetchall()

    if not found:
        c.execute('INSERT INTO users VALUES(?)', (user_id,))

    conn.commit()


def remove_user(user_id):
    c.execute('DELETE * FROM users WHERE user_id=?', (user_id,))
    conn.commit()


def clean_html(raw_html):
    raw_html = str(raw_html)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_data(var):
    return clean_html(var.contents[1]), clean_html(var.contents[3])


def get_referendum(Referendum):
    BASE_URL = "http://www.repubblica.it/static/speciale/2016/referendum/costituzionale/"

    url_data = requests.get(BASE_URL)
    soup = BeautifulSoup(url_data.text, "html.parser")

    si = soup.find('dl', {'class': 'content si'})
    no = soup.find('dl', {'class': 'content no'})
    schede = soup.find('ul', {'class': 'schede'})
    affluenza = soup.find('li', {'class': 'percentage'})
    sezioni = soup.find('li', {'class': 'sezioni'})
    ultimo_aggiornamento = soup.find('li', {'class': 'ora'})

    si_percent, Referendum.si_numero = get_data(si)
    no_percent, Referendum.no_numero = get_data(no)

    Referendum.si_percent, Referendum.no_percent = si_percent.replace('SÃ¬ ', ''), no_percent.replace('SÃ¬ ', '')

    Referendum.schede_bianche = clean_html(schede.contents[1]).replace('Schede bianche: ', '')
    Referendum.schede_nulle = clean_html(schede.contents[3]).replace('Schede nulle: ', '')
    Referendum.schede_contestate = clean_html(schede.contents[5]).replace('Schede contestate: ', '')

    Referendum.affluenza = clean_html(affluenza.contents[1])
    Referendum.sezioni = clean_html(sezioni)
    Referendum.ultimo_aggiornamento = clean_html(ultimo_aggiornamento.contents[0]).replace('Ultimo aggiornamento: ', '')

    return Referendum


def generate_keyboard(regioni):
    inline_keyboard = '['
    for object in regioni:
        inline_keyboard += '[{"text": "🗳 '+object+'", "callback_data": "reg@'+object+'"}],'

    inline_keyboard += '[{"text": "🔙 Indietro", "callback_data": "risultati"}]]'

    return inline_keyboard


def get_regione(Referendum, regione):
    regione = regione.lower().replace(' ', '_').replace('\'', '')
    BASE_URL = "http://www.repubblica.it/static/speciale/2016/referendum/costituzionale/{regione}.html".format(regione=regione)

    url_data = requests.get(BASE_URL)
    soup = BeautifulSoup(url_data.text, "html.parser")

    si = soup.find('dl', {'class': 'content si'})
    no = soup.find('dl', {'class': 'content no'})
    schede = soup.find('ul', {'class': 'schede'})
    affluenza = soup.find('li', {'class': 'percentage'})
    sezioni = soup.find('li', {'class': 'sezioni'})
    ultimo_aggiornamento = soup.find('li', {'class': 'ora'})

    si_percent, Referendum.si_numero = get_data(si)
    no_percent, Referendum.no_numero = get_data(no)

    Referendum.si_percent, Referendum.no_percent = si_percent.replace('SÃ¬ ', ''), no_percent.replace('SÃ¬ ', '')

    Referendum.schede_bianche = clean_html(schede.contents[1]).replace('Schede bianche: ', '')
    Referendum.schede_nulle = clean_html(schede.contents[3]).replace('Schede nulle: ', '')
    Referendum.schede_contestate = clean_html(schede.contents[5]).replace('Schede contestate: ', '')

    Referendum.affluenza = clean_html(affluenza.contents[1])
    Referendum.sezioni = clean_html(sezioni)
    Referendum.ultimo_aggiornamento = clean_html(ultimo_aggiornamento.contents[0]).replace('Ultimo aggiornamento: ', '')

    return Referendum


def message_format(Referendum, regione):
    r = Referendum
    if regione == None:
        text = (
            "<b>Referendum costituzionale • spoglio schede</b>"
            "\n✅ <b>SÌ</b>: {si_percent} • {si_numero}"
            "\n❎ <b>NO</b>: {no_percent} • {no_numero}"
            "\n🗒 <b>Schede bianche</b>: {bianche}"
            "\n❌ <b>Schede nulle</b>: {nulle}"
            "\n⁉️ <b>Schede contestate</b>: {contestate}"
            "\n👥 <b>Affluenza</b>: {affluenza}%"
            "\n👀 <b>Contate</b>: {sezioni}"
            "\n🕒 <b>Ultimo aggiornamento</b>: {ultimo_aggiornamento}"
            .format(si_percent=r.si_percent, si_numero=r.si_numero, no_percent=r.no_percent, no_numero=r.no_numero,
                bianche=r.schede_bianche, nulle=r.schede_nulle, contestate=r.schede_contestate,
                affluenza=r.affluenza, sezioni=r.sezioni, ultimo_aggiornamento=r.ultimo_aggiornamento
                )
        )
    else:
        text = (
            "<b>Referendum costituzionale • spoglio schede • regione {regione}</b>"
            "\n✅ <b>SÌ</b>: {si_percent} • {si_numero}"
            "\n❎ <b>NO</b>: {no_percent} • {no_numero}"
            "\n🗒 <b>Schede bianche</b>: {bianche}"
            "\n❌ <b>Schede nulle</b>: {nulle}"
            "\n⁉️ <b>Schede contestate</b>: {contestate}"
            "\n👥 <b>Affluenza</b>: {affluenza}%"
            "\n👀 <b>Contate</b>: {sezioni}"
            "\n🕒 <b>Ultimo aggiornamento</b>: {ultimo_aggiornamento}"
            .format(si_percent=r.si_percent, si_numero=r.si_numero, no_percent=r.no_percent, no_numero=r.no_numero,
                bianche=r.schede_bianche, nulle=r.schede_nulle, contestate=r.schede_contestate,
                affluenza=r.affluenza, sezioni=r.sezioni, ultimo_aggiornamento=r.ultimo_aggiornamento, regione=regione
                )
        )

    return text
