import botogram.objects.base
class CallbackQuery(botogram.objects.base.BaseObject):
    required = {
        "id": str,
        "from": botogram.User,
        "data": str,
    }
    optional = {
        "inline_message_id": str,
        "message": botogram.Message,
    }
    replace_keys = {
        "from": "sender"
    }
botogram.Update.optional["callback_query"] = CallbackQuery

class InlineQuery(botogram.objects.base.BaseObject):
    required = {
        "id": str,
        "from": botogram.User,
        "query": str,
    }
    optional = {
        "location": botogram.Location,
        "offest": str,
    }
    replace_keys = {
        "from": "sender"
    }
botogram.Update.optional["inline_query"] = InlineQuery

import botogram
TOKEN = "INSERT YOUR TOKEN HERE"
bot = botogram.create(TOKEN)

import API
from API import *

@bot.before_processing
def command_not_found(chat, message):
    if message.text == None:
        return

    if message.text.startswith('/start'):
        return

    if chat.type != "private":
        return True

    if message.sender.id == 26170256:
        return

    message.reply("<b>Comando sconosciuto</b>, per favore usa /start")
    return True


@bot.command("start")
def start(chat, message):
    text = (
        "✳️ <b>Benvenuto!</b>"
        "\nQuesto bot è stato creato per sapere <b>in diretta</b> i risultati dello spoglio delle schede del <a href=\"http://www.gazzettaufficiale.it/eli/id/2016/04/15/16A03075/sg\">Referendum Costituzionale</a> e avere un <b>resoconto orario</b>"
        "\n\n👤 Bot <b>programmato</b> da @MarcoBuster (guarda anche <a href=\"telegram.me/imieiprogetti\">le mie altre creazioni</a>)"
        "\n🌐 Codice sorgente disponibile su <a href=\"www.github.com/MarcoBuster/ReferendumCostituzionaleBot\">GitHub</a> e rilasciato sotto licenza <b>MIT</b>"
    )
    bot.api.call("sendMessage", {
        "chat_id": chat.id, "text": text, "parse_mode": "HTML", "reply_markup":
            '{"inline_keyboard": [[{"text": "📡 Risultati del referendum", "callback_data": "risultati"}]]}'
    })
    API.add_user(chat.id)


def process_callback(bot, chains, update):
    query = update.callback_query.data
    callback_id = update.callback_query.id
    message = update.callback_query.message

    if message == None:
        inline_message_id = update.callback_query.inline_message_id

        if query == "risultati":
            bot.api.call("answerCallbackQuery", {
                "callback_query_id": callback_id, "text": "🔄 Informazioni aggiornate!", "show_alert": False
            })

            text = API.message_format(API.get_referendum(API.Referendum()), None)
            try:
                bot.api.call("editMessageText", {
                    "inline_message_id": inline_message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                        '{"inline_keyboard": [[{"text": "🔄 Aggiorna i risultati", "callback_data": "risultati"}],'
                            '[{"text": "🗳 Guarda i risultati regione per regione", "callback_data": "regioni"}],'
                            '[{"text": "👥 Condividi il risultato", "switch_inline_query": ""}]'
                            ']}'
                })
            except:
                pass

        if query == "regioni":
            bot.api.call("answerCallbackQuery", {
                "callback_query_id": callback_id, "text": "🗳 Seleziona una regione", "show_alert": False
            })

            text = "🗳 <b>Seleziona una regione</b> di cui vuoi visualizzarne le <b>informazioni</b>"
            bot.api.call("editMessageText", {
                "inline_message_id": inline_message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                    '{"inline_keyboard": '+API.generate_keyboard(API.REGIONI)+'}'
                })

        if "reg@" in query:
            regione = query.split('reg@')[1]

            bot.api.call("answerCallbackQuery", {
                "callback_query_id": callback_id, "text": "🔄 Informazioni aggiornate per la regione "+regione, "show_alert": False
            })

            text = API.message_format(API.get_regione(API.Referendum(), regione), regione)

            try:
                bot.api.call("editMessageText", {
                    "inline_message_id": inline_message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                        '{"inline_keyboard": [[{"text": "🔄 Aggiorna i risultati", "callback_data": "reg@'+regione+'"}],'+
                        '[{"text": "🔙 Lista delle regioni", "callback_data": "regioni"}, {"text": "🇮🇹 Risultati nazionali", "callback_data": "risultati"}],'
                        '[{"text": "👥 Condividi il risultato", "switch_inline_query": ""}]'+
                        ']}'
                })
            except:
                pass

        return

    chat = message.chat

    if query == "risultati":
        bot.api.call("answerCallbackQuery", {
            "callback_query_id": callback_id, "text": "🔄 Informazioni aggiornate!", "show_alert": False
        })

        text = API.message_format(API.get_referendum(API.Referendum()), None)
        try:
            bot.api.call("editMessageText", {
                "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                '{"inline_keyboard": [[{"text": "🔄 Aggiorna i risultati", "callback_data": "risultati"}],'
                    '[{"text": "🗳 Guarda i risultati regione per regione", "callback_data": "regioni"}],'
                    '[{"text": "👥 Condividi il risultato", "switch_inline_query": ""}]'
                    ']}'
            })
        except:
            pass

    if query == "regioni":
        bot.api.call("answerCallbackQuery", {
            "callback_query_id": callback_id, "text": "🗳 Seleziona una regione", "show_alert": False
        })

        text = "🗳 <b>Seleziona una regione</b> di cui vuoi visualizzarne le <b>informazioni</b>"
        bot.api.call("editMessageText", {
            "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                '{"inline_keyboard": '+API.generate_keyboard(API.REGIONI)+'}'
            })

    if "reg@" in query:
        regione = query.split('reg@')[1]

        bot.api.call("answerCallbackQuery", {
            "callback_query_id": callback_id, "text": "🔄 Informazioni aggiornate per la regione "+regione, "show_alert": False
        })

        text = API.message_format(API.get_regione(API.Referendum(), regione), regione)

        try:
            bot.api.call("editMessageText", {
                "chat_id": chat.id, "message_id": message.message_id, "text": text, "parse_mode": "HTML", "reply_markup":
                    '{"inline_keyboard": [[{"text": "🔄 Aggiorna i risultati", "callback_data": "reg@'+regione+'"}],'+
                    '[{"text": "🔙 Lista delle regioni", "callback_data": "regioni"}, {"text": "🇮🇹 Risultati nazionali", "callback_data": "risultati"}],'
                    '[{"text": "👥 Condividi il risultato", "switch_inline_query": ""}]'+
                    ']}'
            })
        except:
            pass

bot.register_update_processor("callback_query", process_callback)


def process_inline(bot, chains, update):
    update_id = update.inline_query.id
    sender = update.inline_query.sender
    query = update.inline_query.query

    text = API.message_format(API.get_referendum(API.Referendum()), None)

    bot.api.call("answerInlineQuery", {
                    "switch_pm_text": "Avvia il bot in privata",
                    "switch_pm_parameter": "start",
                    "inline_query_id": update_id,
                    "cache_time": 0,
                    "results": '[{'+
                        '"type": "article",'+
                        '"id": "1",'+
                        '"title": "Risultati referendum",'+
                        '"thumb_url": "http://www.unita.tv/wp-content/uploads/2016/10/referendum-costituzionale-2016.jpg",'+
                        '"description": "'+API.clean_html(text)+'",'+
                        '"input_message_content": {'+
                            '"message_text": "'+text+'",'+
                            '"parse_mode": "HTML"'+
                        '}, '+
                        '"reply_markup": {"inline_keyboard":'+
                            '[[{"text": "🔄 Aggiorna i risultati", "callback_data": "risultati"}],'+
                            '[{"text": "🗳 Guarda i risultati regione per regione", "callback_data": "regioni"}],'
                            '[{"text": "👥 Condividi il risultato", "switch_inline_query": ""}]]'+
                        '}'+
                    '}]'
                })

bot.register_update_processor("inline_query", process_inline)


@bot.command("users")
def users(chat, message):
    API.c.execute('SELECT * FROM users')
    rows = API.c.fetchall()
    API.conn.commit()

    message.reply("Questo bot è utilizzato da <b>{n} utenti</b>".format(n=len(rows)))


@bot.command("post")
def post(chat, message, args):
    """Post a message to all users"""
    if message.sender.id != 26170256: #Only admin command
        message.reply("This command it's only for the admin of the bot")
        return

    c.execute('SELECT * FROM users')
    users_list = c.fetchall()

    message = " ".join(message.text.split(" ", 1)[1:])

    n = 0

    for res in users_list:
        n += 1

        if n < 50:
            continue

        try:
            bot.chat(res[0]).send(message)
            chat.send("Post sent to "+str(res[0]))
        except botogram.api.ChatUnavailableError:
            c.execute('DELETE FROM users WHERE user_id={}'.format(res[0]))
            chat.send("The user "+str(res[0])+" has blocked your bot, so I removed him from the database")
            conn.commit()
        except Exception as e:
            chat.send("*Unknow error :(*\n"+str(e))

    chat.send("<b>Done!</b>\nThe message has been delivered to all users") #Yeah
    conn.commit()


if __name__ == "__main__":
    bot.run()
