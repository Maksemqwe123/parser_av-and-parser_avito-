import time
import requests
from bs4 import BeautifulSoup


start_time = time.time()

items = []
urls = []
years = []
cashes = []
mileages = []
locations = []


def get_info(html_source):
    global items, urls, years, mileages, locations, cashes

    page_info = BeautifulSoup(html_source, 'html.parser')

    car_names = page_info.find_all('a', class_='listing-item__link')
    for name in car_names:
        items.append(name.text)
        urls.append(f"https://cars.av.by/bmw{name['href']}")

    items_cashes = page_info.find_all('div', class_='listing-item__priceusd')
    for cash in items_cashes:
        cashes.append(cash.text.replace('&nbsp;', ' '))

    years_html = page_info.find_all('div', class_="listing-item__params")
    for year in years_html:
        for i in year:
            years.append(i.text)
            break

    mileages_html = page_info.find_all('div', class_="listing-item__params")
    for mileage in mileages_html:
        for a in mileage:
            mileages.append(a.text)
            break

    locations_html = page_info.find_all('div', class_="listing-item__location")
    for location in locations_html:
        locations.append(location.text)


def get_html(pages: range):
    for page in pages:
        if page == 1:
            url = 'https://cars.av.by/filter?brands[0][brand]=8&sort=4'
        else:
            url = f'https://cars.av.by/filter?page={page}&brands[0][brand]=8&sort=4'
        response = requests.get(url=url)

        try:
            assert response.status_code == 200
            html_source = response.text
            get_info(html_source)
        except AssertionError as e:
            print(f'ERROR: {repr(e)}')
            print(response.status_code)


if __name__ == '__main__':
    pages = range(1, 2)
    get_html(pages)
    all_info = list(zip(items, years, cashes, mileages, locations, urls))
    for i in all_info:
        print(f'\n\nМарка: {i[0]}, Год: {i[1]}, Цена: {i[2]}, Пробег: {i[3]}, Локация: {i[4]} Ссылка: {i[-1]}\n\n')
    print(len(all_info))
    end_time = time.time() - start_time
    print(f'\nВремя работы: {end_time} секунд')
