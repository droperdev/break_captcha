from bs4 import BeautifulSoup
from break_captcha.captcha_break import get_predict
from break_captcha.helpers import *
import requests

BASE_URL = 'https://www.placas.pe/Public/CheckPlateStatus.aspx'


def get_information(placa):

    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'lxml')

    view_state = replace_param(soup.find(id="__VIEWSTATE").attrs['value'])
    event_validation = replace_param(
        soup.find(id="__EVENTVALIDATION").attrs['value'])
    image_url = 'https://www.placas.pe/UserControls/FrmCaptcha.aspx'

    response = requests.get(image_url)
    cookie = response.headers.get('Set-Cookie').split(';')[0]

    save_image(response.content, 'break_captcha/'+cookie.split("=")[1]+'.jpg')
    clear_image_to_replace('break_captcha/'+cookie.split("=")[1]+'.jpg')

    captcha = get_predict('break_captcha/'+cookie.split("=")[1]+'.jpg')
    print(captcha)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-419,es;q=0.9,ru;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '2634',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie+'; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1',
        'Host': 'www.placas.pe',
        'Origin': 'https://www.placas.pe',
        'Referer': 'https://www.placas.pe/Public/CheckPlateStatus.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }

    body = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+view_state+'&__VIEWSTATEGENERATOR=3C2DE8DB&__EVENTVALIDATION='+event_validation+'&ctl00%24MainContent%24wddTypePlate=0&ctl00%24MainContent%24txtPlateNumber='+placa + \
        '&ctl00%24MainContent%24txtRequirementPlateId=&ctl00%24MainContent%24wdpDateIni%24TxtFecha=05%2F09%2F2021&ctl00%24MainContent%24wdpDateIni%24meFecha_ClientState=&ctl00%24MainContent%24wdpDateFin%24TxtFecha=30%2F09%2F2050&ctl00%24MainContent%24wdpDateFin%24meFecha_ClientState=&ctl00%24MainContent%24txtimgcode='+captcha+'&ctl00%24MainContent%24wibSearch=Buscar'

    response = requests.post(BASE_URL, headers=headers, data=body)
    soup = BeautifulSoup(response.text, "lxml")

    result = {
        'numero_placa_anterior': soup.find(id="MainContent_lblPlatePrevious").text,
        'numero_placa_nueva': soup.find(id="MainContent_lblPlateNew").text,
        'numero_serie': soup.find(id="MainContent_lblSerialNumber").text,
        'marca': soup.find(id="MainContent_lblBrand").text,
        'modelo': soup.find(id="MainContent_lblModel").text,
        'propietario': soup.find(id="MainContent_lblOwnerCompleteName").text,
        'tipo_uso': soup.find(id="MainContent_lblTypeUse").text,
    }
    return result


def replace_param(data):
    return data.replace(
        "=", "%3D").replace("+", "%2B").replace("/", "%2F")
