import settings
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CallbackContext
import requests
import datetime


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    stQuery = update.inline_query.query
    # Herrien kodeak lortu
    lstHerriak = []
    response = requests.get("https://api.euskadi.eus/culture/events/v1.0/municipalities?_elements=20&_page=1")
    dicJson = response.json()
    lstHerriak += dicJson['items']
    iPages = dicJson['totalPages']
    for i in range(iPages-1):
        response = requests.get(f"https://api.euskadi.eus/culture/events/v1.0/municipalities?_elements=20&_page={i+2}")
        dicJson = response.json()
        lstHerriak += dicJson['items']

    for dicHerri in lstHerriak:
        if dicHerri['nameEu'] == stQuery:
            stIdHerri = dicHerri['municipalityId']
            stIdProbintzi = dicHerri['provinceId']
            tGaur = datetime.date.today()
            response = requests.get(f"https://api.euskadi.eus/culture/events/v1.0/events/byMonth/{str(tGaur.year)}/{str(tGaur.month)}/byMunicipality/{stIdProbintzi}/{stIdHerri}?_elements=50&_page=1")
            dicJson = response.json()
            print(dicJson)
            break

'''   results = []
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
    update.inline_query.answer(results)'''


'''def chosen(update: Update, context: CallbackContext) -> None:
    # Ttantto bat gehitu aukeratutako dokumentuari
    [stCol, stId] = update.chosen_inline_result.result_id.split('_')
    stUser = update.chosen_inline_result.from_user'''
