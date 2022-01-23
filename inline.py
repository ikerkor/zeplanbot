import datetime

import requests
from telegram import Update
from telegram.ext import CallbackContext
from dateutil.relativedelta import relativedelta

def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    stQuery = update.inline_query.query
    # Herrien kodeak lortu
    response = requests.get("https://api.euskadi.eus/culture/events/v1.0/municipalities?_elements=300&_page=1")
    dicJson = response.json()
    lstHerriak = dicJson['items']
    '''
    iPages = dicJson['totalPages']
    for i in range(iPages-1):
        response = requests.get(f"https://api.euskadi.eus/culture/events/v1.0/municipalities?_elements=20&_page={i+2}")
        dicJson = response.json()
        lstHerriak += dicJson['items']'''

    for dicHerri in lstHerriak:
        lstGidoi = dicHerri['nameEu'].split('-')
        bGidoi = False
        for stZati in lstGidoi:
            if stQuery == stZati:
                bGidoi = True
                break
        if bGidoi:
            stIdHerri = dicHerri['municipalityId']
            stIdProbintzi = dicHerri['provinceId']
            tGaur = datetime.date.today()
            tHileBarru = tGaur + relativedelta(months=1)
            if tGaur.day == 31 and tHileBarru.day == 1:
                tHileBarru.day = 30
            lstEkintzak = []
            for iHile in range(2):
                response = requests.get(f"https://api.euskadi.eus/culture/events/v1.0/events/byMonth/{str(tGaur.year)}/{str(tGaur.month+1)}/byMunicipality/{stIdProbintzi}/{stIdHerri}?_elements=300&_page=1")
                lstEkintzak += response.json()['items']
                for i in range(len(lstEkintzak)):
                    if date(lstEkintzak[i]['startDate']) >
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
