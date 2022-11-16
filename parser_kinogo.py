import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from pip._internal import req

red = Request(
    url='https://kinogo.biz',
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.77'
}
)
webpage = urlopen(req).read()


def get_html(url):

    s = requests.Session
    response = s.get(url=url, headers=headers)

    with open('index.html', 'w') as file:
        file.write(response.text)


def get_info():
    get_html(url='https://kinogo.biz')


if __name__ == '__main__':
    get_info()
