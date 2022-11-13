import time
import requests
from bs4 import BeautifulSoup


start_time = time.time()

items = []
years = []
cashes = []
locations = []
urls = []


class Parser:
    def __init__(self, pages: range):
        self.pages = pages
        self.items = items
        self.years = years
        self.cashes = cashes
        self.locations = locations
        self.urls = urls

        self._get_html()

    def _get_html(self):
        for page in self.pages:
            if page == 1:
                url = 'https://cars.av.by/filter?brands[0][brand]=8&sort=4'
            else:
                url = f'https://cars.av.by/filter?page={page}&brands[0][brand]=8&sort=4'

            response = requests.get(url=url)

            try:
                assert response.status_code == 200
                html_source = response.text
                self._get_info(html_source)
            except AssertionError as e:
                print(f'ERROR: {repr(e)}')
                print(response.status_code)

    def _get_info(self, html_source):
        pages_info = BeautifulSoup(html_source, 'html.parser')

        car_names = pages_info.find_all('a', class_='listing-item__link')
        for name in car_names:
            self.items.append(name.text)
            self.urls.append(f"https://cars.av.by/bmw{name['href']}")

        items_cashes = pages_info.find_all('div', class_='listing-item__priceusd')
        for cash in items_cashes:
            self.cashes.append(cash.text.replace('&nbsp;', ' '))

        years_html = pages_info.find_all('div', class_="listing-item__params")
        for year in years_html:
            self.years.append(year.text)

        # mileages_html = pages_info.find_all('div', class_="listing-item__params")
        # for mileage in mileages_html:
        #     self.mileages.append(mileage.text)

        locations_html = pages_info.find_all('div', class_="listing-item__location")
        for location in locations_html:
            self.locations.append(location.text)


if __name__ == '__main__':
    parse = Parser(range(1, 2))
    all_info = list(zip(items, years, cashes, locations, urls))
    for i in all_info:
        print(f'\n\nМарка: {i[0]}, Год: {i[1]}, Цена: {i[2]}, Локация: {i[4]} Ссылка: {i[-1]}\n\n')
    end_time = time.time() - start_time
    print(f'\nВремя работы: {end_time} секунд')
