import time
import requests
from bs4 import BeautifulSoup
from random import randrange

start_time = time.time()

items = []
text = []
cashes = []
urls = []


class Parser:
    def __init__(self, pages: range):
        self.pages = pages
        self.text = text
        self.cashes = cashes
        self.urls = urls

        self._get_html()

    def _get_html(self):
        for page in self.pages:
            if page == 1:
                url = 'https://www.avito.ru/sankt-peterburg/mebel_i_interer'
            else:
                url = f'https://www.avito.ru/sankt-peterburg/mebel_i_interer?p={page}'
            response = requests.get(url=url)

            time.sleep(randrange(2, 5))

            try:
                assert response.status_code == 200
                html_source = response.text
                self._get_info(html_source)
            except AssertionError as e:
                print(f'ERROR: {repr(e)}')
                print(response.status_code)

    def _get_info(self, html_source):

        pages_info = BeautifulSoup(html_source, 'html.parser')

        furniture_objects = pages_info.find_all('a', class_="iva-item-titleStep-pdebR")
        for object in furniture_objects:
            items.append(object.text)
            self.urls.append(f"https://www.avito.ru/sankt-peterburg/mebel_i_interer{object['href']}")

        items_cashes = pages_info.find_all('div', class_='body-priceRow-h69TD')
        for cashe in items_cashes:
            self.cashes.append(cashe.text)

        text_html = pages_info.find_all('div', class_='iva-item-descriptionStep-C0ty1')
        for text in text_html:
            self.text.append(text.text)


if __name__ == '__main__':
    parser = Parser(range(1, 2))
    all_info = list(zip(items, cashes, text, urls))
    for i in all_info:
        print(f'\n\n Мебель: {items[0]}, Цена: {cashes[1]}, Текст: {text[2]},  Ссылка: {urls[-1]} \n\n')
    end_time = time.time() - start_time
    print(f'\nВремя работы: {end_time} ceкунд')