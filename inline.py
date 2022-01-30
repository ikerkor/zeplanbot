import datetime

import requests
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext
from dateutil.relativedelta import relativedelta
import settings

def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    stQuery = update.inline_query.query
    # Herrien kodeak lortu
    response = requests.get("https://api.euskadi.eus/culture/events/v1.0/municipalities?_elements=300&_page=1")
    dicJson = response.json()
    lstHerriak = dicJson['items']

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
            for iHile in range(3):
                response = requests.get(f"https://api.euskadi.eus/culture/events/v1.0/events?_elements=100&_page=1&language=eu&month={str(tGaur.month+iHile)}&municipalityNoraCode={stIdHerri}&provinceNoraCode={stIdProbintzi}&year={str(tGaur.year)}")
                # response = requests.get(f"https://api.euskadi.eus/culture/events/v1.0/events/byMonth/{str(tGaur.year)}/{str(tGaur.month+iHile)}/byMunicipality/{stIdProbintzi}/?_elements=300&_page=1")
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
            #ID errepikatuko ekintzak ezabatu
            lstind = []
            lstID = []
            for i in range(len(lstEkintzak)):
                if lstEkintzak[i]['id'] not in lstID:
                    lstID.append(lstEkintzak[i]['id'])
                    lstind.append(i)
            lstEkintzak = [lstEkintzak[i] for i in lstind]
            # 50 ekintzako muga ezarri
            if len(lstEkintzak) > 50:
                lstEkintzak = lstEkintzak[0:49]
            #Inline zerrenda sortu
            results = []
            for dicEkintza in lstEkintzak:
                stTitle = ''
                if settings.dicMotaEmoji.get(dicEkintza.get('typeEu')):
                    stTitle += settings.dicMotaEmoji.get(dicEkintza.get('typeEu'))+' '
                if dicEkintza.get('nameEu'):
                    stTitle += dicEkintza.get('nameEu')
                stStartDate = datetime.datetime.strptime(dicEkintza['startDate'][:-10], '%Y-%m-%d').strftime("%Y/%m/%d")
                stEndDate = datetime.datetime.strptime(dicEkintza['endDate'][:-10], '%Y-%m-%d').strftime("%Y/%m/%d")
                if stStartDate == stEndDate:
                    stDescription = f"{stStartDate} "
                else:
                    stDescription = f"{stStartDate} - {stEndDate} "
                if dicEkintza.get('openingHoursEu'):
                    stDescription += f"({dicEkintza.get('openingHoursEu')}) "
                if dicEkintza.get('priceEu'):
                    stDescription += f"[{dicEkintza.get('priceEu')}]"
                if dicEkintza.get('establishmentEu'):
                    stDescription += f"\n{dicEkintza.get('establishmentEu')}"
                stThumbUrl = ''
                if len(dicEkintza.get('images')) != 0:
                    stThumbUrl = dicEkintza.get('images')[0].get('imageUrl')
                stMessage = f'Nor animatuko da?\n*{stTitle}*\n{stDescription}\n'
                # if dicEkintza.get("sourceUrlEu"):
                #     stMessage += f'[inlne URL]({dicEkintza["sourceUrlEu"]})'
                results.append(
                    InlineQueryResultArticle(
                        id=dicEkintza['id'],
                        title=stTitle,
                        description=stDescription,
                        thumb_url=stThumbUrl,
                        thumb_width=None,
                        thumb_height=None,
                        input_message_content=InputTextMessageContent(stMessage, parse_mode='Markdown') # TODO: Mezua osatu
                    )
                )
                update.inline_query.answer(results)


'''def chosen(update: Update, context: CallbackContext) -> None:
    # Ttantto bat gehitu aukeratutako dokumentuari
    [stCol, stId] = update.chosen_inline_result.result_id.split('_')
    stUser = update.chosen_inline_result.from_user'''
