import settings
import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CallbackContext
from datetime import date

today = date.today()
print("Today's date:", today)


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    stQuery = update.inline_query.query
    stProbintzi = "Gipuzkoa"
    stHile = str(date.today().month)
    stUrte = str(date.today().year)
    response = requests.get("http://api.euskadi.eus/culture/events/v1.0/events/byMonth/"+stUrte+"/"+stHile+"/byMunicipality/"+stProbintzi+"/"+stQuery)
    results = []
    results.append(
        InlineQueryResultArticle(
            id='auskalo',
            title=stQuery,
            description='blabla',
            thumb_url=None,
            thumb_width=None,
            thumb_height=None,
            input_message_content=InputTextMessageContent(stQuery)
        )
    )
    update.inline_query.answer(results)


'''def chosen(update: Update, context: CallbackContext) -> None:
    # Ttantto bat gehitu aukeratutako dokumentuari
    [stCol, stId] = update.chosen_inline_result.result_id.split('_')
    stUser = update.chosen_inline_result.from_user'''
