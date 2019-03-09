import requests
from bs4 import BeautifulSoup

db = {}
tag = ['a', 'title']


def site_map(url):
    global main_url
    if not url.startswith('http://'): url = 'http://' + url
    main_url = url
    get_url_content([url])

def get_url_content(urls):
    for url in urls:
        if url in db: break
        plain = requests.get(url).text
        soup = BeautifulSoup(plain, 'html.parser')
        tag_finder(url, soup)

def tag_finder(url, soup):
    links = soup.findAll('a')
    title = soup.find('title')
    crowl_links(url, links, title)

def crowl_links(url, links, title):
    for link in links:
        i = links.index(link)
        href = (link.get('href'))
        check_href(href, links, i)
    save_content(url, title, links)
    if len(links) > 0:
        get_url_content(links)

def save_content(url, title, links):
    db.update({url: {'title': title.string, 'links': set(links)}})

def check_href(href, links, i):
    if not href.startswith('http'):
        href = main_url + href
        links[i] = href
    elif href.startswith(main_url):
        links[i] = href
    else:
        links.pop(i)

def display(db):
    for k, v in db.items():
        print(f'{k} {v}')


site_map('http://interia.pl')
print('***************************')

display(db)

