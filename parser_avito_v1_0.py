import time
import requests
from bs4 import BeautifulSoup
from random import randrange

start_time = time.time()

items = []
urls = []
text = []
cashes = []
images = []


def get_info(html_source):
    global items, urls, text, cashes, images

    page_info = BeautifulSoup(html_source, 'html.parser')

    furniture_objects = page_info.find_all('a', class_="iva-item-titleStep-pdebR")
    for objects in furniture_objects:
        items.append(objects.text)
        urls.append(f"https://www.avito.ru/sankt-peterburg/mebel_i_interer{objects['href']}")

    items_cashes = page_info.find_all('div', class_='body-priceRow-h69TD')
    for cashes in items_cashes:
        cashes.append(cashes.text)

    text_html = page_info.find_all('div', class_='iva-item-descriptionStep-C0ty1')
    for text in text_html:
        text.append(text.text)

    time.sleep(randrange(2, 5))


def get_html(pages: range):
    for page in pages:
        if page == 1:
            url = 'https://www.avito.ru/sankt-peterburg/mebel_i_interer?p=1'
        else:
            url = f'https://www.avito.ru/sankt-peterburg/mebel_i_interer?p={page}'
        response = requests.get(url=url)

        time.sleep(randrange(2, 5))

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
    all_info = list(zip(items, cashes, text, images, urls))
    for i in all_info:
        print(f'\n\n Мебель: {i[0]}, Цена: {i[1]}, Текст: {i[2]} Ссылка: {i[-1]} \n\n')
    print(len(all_info))
    end_time = time.time() - start_time
    print(f'\nВремя работы: {end_time} ceкунд')