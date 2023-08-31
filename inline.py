import datetime
import requests
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext
from dateutil.relativedelta import relativedelta
import settings

# Aldagai globalak
iErabilera = 0 # Zenbagailua


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    global iErabilera
    iErabilera += 1
    if iErabilera == 10:
        context.bot.send_message(chat_id=settings.MY_TELEGRAM_USER, text='10 erabilera!')
        iErabilera = 0
    stQuery = update.inline_query.query
    # Herrien kodeak lortu
    response = requests.get("https://api.euskadi.eus/culture/events/v1.0/municipalities?_elements=300&_page=1")
    dicJson = response.json()
    lstHerriak = dicJson['items']
    results = []
    bTopo = False
    for dicHerri in lstHerriak:
        if stQuery == dicHerri['nameEu']:
            bTopo = True
            dicHerria = dicHerri
            break
        else:
            if '/' in dicHerri['nameEu']:
                lstGidoi = dicHerri['nameEu'].split('/')
            else:
                lstGidoi = dicHerri['nameEu'].split('-')
            for stZati in lstGidoi:
                if stQuery.lower().split() == stZati.lower().split():
                    bTopo = True
                    dicHerria = dicHerri
                    break
            if bTopo:
                break
    if bTopo or stQuery.lower() == 'altza':
        if stQuery.lower() == 'altza':
            stIdHerri = '82'
            stIdProbintzi = '20'
        else:
            stIdHerri = dicHerria['municipalityId']
            stIdProbintzi = dicHerria['provinceId']
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
                lstEkintzak = [lstEkintzak[j] for j in reversed(lstind)]
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
            # Mezua
            stMessage = 'Hara, plan puska! Animatuko?\n'
            stIzenburua = ''
            if dicEkintza.get('nameEu'):
                stMessage += f"*{dicEkintza.get('nameEu')}*".upper()
            if dicEkintza.get('typeEu'):
                stMessage += f" _({dicEkintza.get('typeEu')})_"
            if stStartDate == stEndDate:
                stMessage += f"\n\U0001F4C6 {stStartDate}"
            else:
                stMessage += f"\n\U0001F4C6 {stStartDate} - {stEndDate}"
            if dicEkintza.get('openingHoursEu'):
                stMessage += f"\n\U000023F0 {dicEkintza.get('openingHoursEu')} "
            if dicEkintza.get('establishmentEu'):
                stMessage += f"\n\U0001F4CD {dicEkintza.get('municipalityEu')} ({dicEkintza.get('establishmentEu')})"
            if dicEkintza.get('priceEu'):
                stMessage += f"\n\U0001F39F\U0000FE0F {dicEkintza.get('priceEu')}"
            if stThumbUrl:
                stMessage += f"[ ]({stThumbUrl})"
            if dicEkintza.get("sourceUrlEu"):
                stMessage += f'\n[info+]({dicEkintza["sourceUrlEu"]})'
            if dicEkintza.get("purchaseUrlEu"):
                if not dicEkintza.get("sourceUrlEu"):
                    stMessage += f" ([sarrerak]({dicEkintza['purchaseUrlEu']}))"
                else:
                    stMessage += f" / [sarrerak]({dicEkintza['purchaseUrlEu']})"
            if dicEkintza.get('sourceUrlEu'):
                stMessage += f" / @zeplanBot / [bot+](https://t.me/esamojiBot)"
            results.append(
                InlineQueryResultArticle(
                    id=dicEkintza['id'],
                    title=stTitle,
                    description=stDescription,
                    thumb_url=stThumbUrl,
                    thumb_width=None,
                    thumb_height=None,
                    input_message_content=InputTextMessageContent(stMessage, parse_mode="Markdown")
                    )
              )
        if len(lstEkintzak) == 0:
            results.append(
                InlineQueryResultArticle(
                    id='EzAurkitua',
                    title=' \U0001F61E ez da ekintzarik aurkitu herri horretan',  # \U000026A0',
                    description='',
                    thumb_url=None,
                    thumb_width=None,
                    thumb_height=None,
                    input_message_content=InputTextMessageContent('\U0001F4A9'))
            )
    if not bTopo and stQuery != '':
        results.append(
            InlineQueryResultArticle(
                id='EzAurkitua',
                title=' \U0001F937\U0000200D\U00002640\U0000FE0F ez da halako herririk aurkitu',  # \U000026A0',
                description='',
                thumb_url=None,
                thumb_width=None,
                thumb_height=None,
                input_message_content=InputTextMessageContent('\U0001F4A9'))
           )
    update.inline_query.answer(results)

'''def chosen(update: Update, context: CallbackContext) -> None:
    # Ttantto bat gehitu aukeratutako dokumentuari
    [stCol, stId] = update.chosen_inline_result.result_id.split('_')
    stUser = update.chosen_inline_result.from_user'''
