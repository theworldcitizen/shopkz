from typing import List

import requests
from bs4 import BeautifulSoup
import json
from models import Ad

BASE_URL = 'https://shop.kz'


class Crawler:
    headers = {
        'authority': 'shop.kz',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        # 'referer': 'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/?PAGEN_1=12',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'iRegionSectionId=9; iRegionSectionName=%D0%90%D0%BB%D0%BC%D0%B0%D1%82%D1%8B; LIVECHAT_GUEST_HASH=3cc482fa60459e7ef4adaceda57cf9da; rrpvid=875964550757541; _gcl_au=1.1.2024388877.1662654053; __auc=2ad788c81831de77c862d01f063; _gid=GA1.2.1253645743.1662654054; show_region_popup=0; rcuid=631a166bf007f33b0651f66b; tmr_lvid=1ff761e4e60084217ce8173894f5c45c; tmr_lvidTS=1662654059432; _ym_uid=16626540601005268109; _ym_d=1662654060; BX_USER_ID=d4865fda7cf3aa4b134108b0200cd20f; _ym_isad=2; _fbp=fb.1.1662654059953.18821908; _ms=a8b2685c-0369-420c-b390-8abc40cf5f41; BITRIX_CONVERSION_CONTEXT_ru=%7B%22ID%22%3A27%2C%22EXPIRE%22%3A1662746340%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; rrlevt=1662703908496; PHPSESSID=SO0psgUjyo0l1zIDgUBEdASx2dJEtt1n; __asc=bb5ed9e5183215d57fd60f9a88b; _ym_visorc=b; _ga=GA1.2.651545052.1662654054; _ga_VQ49ETWVSY=GS1.1.1662712108.4.1.1662712134.34.0.0; tmr_detect=0%7C1662712135908; tmr_reqNum=49',
    }
    cookies = {
        'iRegionSectionId': '9',
        'iRegionSectionName': '%D0%90%D0%BB%D0%BC%D0%B0%D1%82%D1%8B',
        'LIVECHAT_GUEST_HASH': '3cc482fa60459e7ef4adaceda57cf9da',
        'rrpvid': '875964550757541',
        '_gcl_au': '1.1.2024388877.1662654053',
        '__auc': '2ad788c81831de77c862d01f063',
        '_gid': 'GA1.2.1253645743.1662654054',
        'show_region_popup': '0',
        'rcuid': '631a166bf007f33b0651f66b',
        'tmr_lvid': '1ff761e4e60084217ce8173894f5c45c',
        'tmr_lvidTS': '1662654059432',
        '_ym_uid': '16626540601005268109',
        '_ym_d': '1662654060',
        'BX_USER_ID': 'd4865fda7cf3aa4b134108b0200cd20f',
        '_ym_isad': '2',
        '_fbp': 'fb.1.1662654059953.18821908',
        '_ms': 'a8b2685c-0369-420c-b390-8abc40cf5f41',
        'BITRIX_CONVERSION_CONTEXT_ru': '%7B%22ID%22%3A27%2C%22EXPIRE%22%3A1662746340%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
        'rrlevt': '1662703908496',
        'PHPSESSID': 'SO0psgUjyo0l1zIDgUBEdASx2dJEtt1n',
        '__asc': 'bb5ed9e5183215d57fd60f9a88b',
        '_ym_visorc': 'b',
        '_ga': 'GA1.2.651545052.1662654054',
        '_ga_VQ49ETWVSY': 'GS1.1.1662712108.4.1.1662712134.34.0.0',
        'tmr_detect': '0%7C1662712135908',
        'tmr_reqNum': '49',
    }

    def make_request(self, url):
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        if response.ok:
            return response.text

    def get_soup(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_links(self, soup) -> List:
        links = []
        items = soup.find_all('div', class_='bx_catalog_item double')
        for item in items:
            div1 = item.find('div', class_='bx-catalog-title-part')
            main_div = div1.find('div', class_='bx_catalog_item_title')
            a = main_div.find('a')
            url = a.get('href')
            # url = BASE_URL + url
            links.append(url)
        return links

    def get_pagination(self, soup):
        div = soup.find('div', class_='bx-pagination bx-blue')
        main_div = div.find('div', class_='bx-pagination-container row')
        ul = main_div.find('ul')
        items = ul.find_all('li')
        item = items[-1]
        try:
            a = item.find('a')
            if a == None:
                return
            url = a.get('href')
            return url
        except Exception:
            return

    def get_info(self, links):
        output = []

        for link in links:


            link = BASE_URL + link
            html = self.make_request(link)
            soup = self.get_soup(html)
            name = self.get_title(soup)
            articul = self.get_articul(soup)
            price = self.get_price(soup)
            memory_size = self.get_memory_size(soup)

            res = Ad(name=name, price=price, articul=articul, memory_size=memory_size, link=link).dict()
            output.append(res)

            # data = json.dumps(res, indent=5)
            # file = open('smartphones.json', 'a')
            # file.write(data)
            # file.close()

        return output

    def write_to_file(self, data):
        with open('smart.json', 'a') as file:
            json.dump(data, file, indent=5)
            file.close()

    def loop(self, soup):
        links = self.get_links(soup)
        output = self.get_info(links)
        self.write_to_file(output)

        # data = json.dumps(output, indent=5)
        # file = open('smartphones.json', 'a')
        # file.write(data)
        # file.close()

        return self.get_pagination(soup)

    def main(self):
        html = self.make_request(BASE_URL + '/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/')
        soup = self.get_soup(html)
        link = self.loop(soup)
        while True:
            html = self.make_request(BASE_URL + link)
            soup = self.get_soup(html)
            link = self.loop(soup)
            if link == None:
                break
        return

    @staticmethod
    def get_title(soup: BeautifulSoup):
        try:
            name = soup.find('h1', class_='bx-title dbg_title').text.strip()
            return name
        except Exception:
            return None

    @staticmethod
    def get_articul(soup: BeautifulSoup):
        try:
            div = soup.find('div', class_='bx_item_container')
            div = div.find('div', class_='row')
            ul = div.find('ul', class_='bx-card-mark col-lg-4 col-xs-12 col-sm-6')
            items = ul.find_all('li')
            li = items[0].text.split()
            articul = li[-1]
            return articul
        except Exception:
            return None

    @staticmethod
    def get_price(soup: BeautifulSoup):
        try:
            price = soup.find('div', class_='item_current_price').text
            return price
        except Exception:
            return None

    @staticmethod
    def get_memory_size(soup: BeautifulSoup):
        try:
            div = soup.find('dl', class_='bx_detail_chars')
            divs = div.find_all('div', class_='bx_detail_chars_i')
            for di in divs:
                i = di.find('dt', class_='bx_detail_chars_i_title')
                span = i.find('span', class_='glossary-term')
                name_of_field = span.text
                if name_of_field == 'Объем встроенной памяти':
                    memory = di.find('dd', class_='bx_detail_chars_i_field').text
                    return memory
        except Exception:
            return None


obj = Crawler()
obj.main()
