import datetime

import requests
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
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
        if bGidoi or stQuery == dicHerri['nameEu']:
            stIdHerri = dicHerri['municipalityId']
            stIdProbintzi = dicHerri['provinceId']
            tGaur = datetime.date.today()
            tHileBarru = tGaur + relativedelta(months=1)
            if tGaur.day == 31 and tHileBarru.day == 1:
                tHileBarru.replace(day=28)
            lstEkintzak = []
            for iHile in range(2):
                response = requests.get(f"https://api.euskadi.eus/culture/events/v1.0/events/byMonth/{str(tGaur.year)}/{str(tGaur.month+iHile)}/byMunicipality/{stIdProbintzi}/{stIdHerri}?_elements=300&_page=1")
                lstEkintzak += response.json()['items']
                lstind = []
                # Gaur eta aurreragokoak bakarrik mantendu
                if iHile == 0:
                    for i in reversed(range(len(lstEkintzak))):
                        if datetime.datetime.strptime(lstEkintzak[i]['endDate'][:-10], '%Y-%m-%d').date() >= tGaur:
                            lstind.append(i)
                        else:
                            break
                    lstEkintzak = [lstEkintzak[j] for j in lstind]
            lstind = []
            # Euskarazkoak bakarrik mantendu
            for i in range(len(lstEkintzak)):
                if lstEkintzak[i]['language'] == 'EU': # FIXME: field hori ez badauka, ez da onartuko baina arazorik ez
                    lstind.append(i)
            lstEkintzak = [lstEkintzak[i] for i in lstind]

            #Inline zerrenda sortu
            results = []
            for dicEkintza in lstEkintzak:
                # TODO: ez dadila arazo izan field bat ez izatea. Tipa emotikono bidez?
                results.append(
                    InlineQueryResultArticle(
                        id=dicEkintza['id'],
                        title=dicEkintza['nameEu'],
                        description=dicEkintza['openingHoursEu'],
                        thumb_url=dicEkintza['images'][0]['imageUrl'],
                        thumb_width=None,
                        thumb_height=None,
                        input_message_content=InputTextMessageContent('Etorri nahi?')
                    )
                )
            update.inline_query.answer(results)


'''def chosen(update: Update, context: CallbackContext) -> None:
    # Ttantto bat gehitu aukeratutako dokumentuari
    [stCol, stId] = update.chosen_inline_result.result_id.split('_')
    stUser = update.chosen_inline_result.from_user'''
