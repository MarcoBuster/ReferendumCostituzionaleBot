# Referendum Costituzionale Bot [![Bot](https://img.shields.io/badge/Telegram-@ReferendumCostituzionaleBot-red.svg?style=flat)][Bot]
**Referendum Costituzionale Bot** era un **bot per Telegram** per ricevere i risultati dello spoglio delle schede elettorali del *Referendum Costituzionale 04/12/2016* e di ricevere notifiche ogni ora con l'aggiornamento dei risultati

### Funzionalità e utilizzo
Il bot era raggiungibile su Telegram cercando `@ReferendumCostituzionaleBot`, utilizzava **HTML Parsing** dal [sito di Repubblica.it][Repubblica]. Il bot è ora **deprecato**, ma i sorgenti rimmarranno pubblicamente disponibili.

### Installazione
Per installare questo bot sulla tua VPS Linux Ubuntu, devi:

    $ python3 -m pip install botogram
    $ git clone https://www.github.com/MarcoBuster/ReferendumCostituzionaleBot.git && cd ReferendumCostituzionaleBot
    $ python3 "Bot.py"

> Attenzione! Modificare la variabile TOKEN nel file Bot.py prima di avviare il bot

### Licenza e crediti
Il bot è stato programmato da [MarcoBuster][Marco] e rilasciato sotto licenza [MIT][MIT], raggiungibile su Telegram tramite [questo indirizzo][Bot].

[Bot]: https://telegram.me/ReferendumCostituzionaleBot
[Marco]: https://www.github.com/MarcoBuster
[MIT]: https://opensource.org/licenses/MIT
[Repubblica]: http://www.repubblica.it/static/speciale/2016/referendum/costituzionale/?refresh_cens
