import requests
from requests.api import head
from bs4 import BeautifulSoup
import time
from random import randrange

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.77'
}


start_time = time.time()

items = []
urls = []
names = []
genres = []
quality = []
years = []


class Parser:
    def __init__(self, pages: range):
        self.pages = pages
        self.items = items
        self.names = names
        self.genres = genres
        self.quality = quality
        self.years = years
        self.urls = urls

        self._get_html('url')

    def _get_html(self, url):
        for page in self.pages:
            if page == 1:
                url = 'https://kinogo.biz/page'
            else:
                url = f'https://kinogo.biz/page/2/'
            s = requests.Session
            response = s.get(url=url, headers=headers)

            with open('kinogo.html', 'w') as file:
                file.write(response.text)

            time.sleep(randrange(5, 10))

            try:
                assert response.status_code == 200
                html_source = response.text
                self._get_info(html_source)
            except AssertionError as e:
                print(f'ERROR: {repr(e)}')
                print(response.status_code)

    def _get_info(self, html_source):

        page_info = BeautifulSoup(html_source, 'html.parser')

        object_1 = page_info.find_all('div', class_='shortstory__body')

        for name in object_1:
            items.append(name.text)
            self.urls.append(f"https://kinogo.biz{name['href']}")


if __name__ == '__main__':
    parser = Parser(range(1, 2))
    all_info = list(zip(items, urls))
    for i in all_info:
        print(f'\n\n Название автобусов: {items[0]},  Ссылка: {urls[-1]} \n\n')
    end_time = time.time() - start_time
    print(f'\nВремя работы: {end_time} ceкунд')
