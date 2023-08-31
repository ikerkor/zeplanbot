from telegram.ext import Updater, InlineQueryHandler

import inline
import settings


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(settings.TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # EMOJI, ESAMOLDE, GOITIZEN, HERRI egoeradun elkarrizketa kudeatzailea sortu eta gehitu.
   # dispatcher.add_handler(elkarrizketa.conv_handler)

    # DIAL, ERANTZUN egoeradun elkarrizketa kudeatzailea sortu eta gehitu.
    #dispatcher.add_handler(elkarrizketa.conv_handler_oharra)

    # Lerro barneko queryaren kudeatzailea gehitu
    dispatcher.add_handler(InlineQueryHandler(inline.inlinequery))

    # Hasi bot-a
    if settings.B4A == '0':

        updater.start_polling()
    elif settings.HEROKU == '1':
        updater.start_webhook(listen="0.0.0.0",
                              port=int(settings.PORT),
                              url_path=settings.TELEGRAM_TOKEN,
                              webhook_url='https://zeplanbot.herokuapp.com/' + settings.TELEGRAM_TOKEN)

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()