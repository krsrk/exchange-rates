import json
import urllib.request as request
from datetime import datetime
from bs4 import BeautifulSoup


class FixerProvider:
    base_url = 'http://data.fixer.io/api/latest?'  # In basic plan restricted to http
    api_token = '0d9afb0c6b5e5d319eb49ca65a722cad'
    base = 'EUR'  # This data is for restricctions in Fixer.io basic plan
    symbols = ['USD', 'MXN']  # This data is for restricctions in Fixer.io basic plant

    def __init__(self):
        # TODO: init data if fixer.io is not a basic plan
        pass

    def get_exchange_rates(self):
        url = self.base_url + 'access_key={}'.format(self.api_token) + '&symbols=' + \
              ','.join(self.symbols) + '&format=1'
        req = request.Request(url=url)
        fix_usd_mxn = 0

        with request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            """Due to fixer.io basic plan has limited request, so when return None 
            in the fix valu, it passed that limit"""
            if data['success']:
                """Due to fixer.io basic plan we need to calculate de USD-MXN rate"""
                fix_usd_mxn = data["rates"]['MXN'] / data["rates"]['USD']

        return {
            'provider': 'fixer',
            'fix': fix_usd_mxn
        }


class BanxicoProvider:
    base_url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/'
    api_token = 'fe12b90a9e0e6dece61925c77bcb0d058bfe864c80fa6dc002ce6dc133eb7d8d'  # TODO: change this to config file

    def get_exchange_rates(self):
        now_date = datetime.now().strftime("%Y-%m-%d")
        url = self.base_url + '/{}/{}/?mediaType=json&token={}'.format(now_date, now_date, self.api_token)
        req = request.Request(url=url)

        with request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            fix_usd_mxn = 0 if 'datos' not in data['bmx']['series'][0] \
                else float(data['bmx']['series'][0]['datos'][0]['dato'])
        return {
            'provider': 'banxico',
            'fix': fix_usd_mxn
        }


class DofProvider:
    url = "https://www.banxico.org.mx/tipcamb/tipCamMIAction.do"

    def get_exchange_rates(self):
        fix_usd_mxn = 0

        try:
            page = request.urlopen(self.url)
            soup = BeautifulSoup(page.read(), "html.parser")
            html_parse = soup.find_all("tr", class_="renglonNon")
            td_elements = html_parse[0].find_all("td", attrs={"align": "right"})
            fix_usd_mxn = float(" ".join(td_elements[1].string.split()))
        except Exception as e:
            print(str(e))

        return {
            'provider': 'dof',
            'fix': fix_usd_mxn
        }
