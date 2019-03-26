import requests
from bs4 import BeautifulSoup


db = {}
tag = ['a', 'title']
domain = None
protocols = ('http://www.', 'https://www.', 'http://', 'https://', 'www.')
main_url = None

def site_map(url):
    global main_url
    check_main_url(url)
    if not url.startswith('http://'): url = 'http://' + url
    main_url = url
    get_url_content([url])

def get_url_content(urls):
    for url in urls:
        if url in db: continue
        try:
            plain = requests.get(url).text
        except:
            continue
        soup = BeautifulSoup(plain, 'html.parser')
        tag_finder(url, soup)

def tag_finder(url, soup):
    links = soup.findAll('a')
    title = soup.find('title')
    crowl_links(url, links, title)

def crowl_links(url, links, title):
    l = [] # i w check_href operuje na 'l' który przekazuje do zapisu w save_content
    for link in links:
        href = (link.get('href'))
        check_href(href, l)
    save_content(url, title, l)
    if len(l) > 0:
        get_url_content(l)

def check_href(href, l):
    if href and (domain in href):
        for item in protocols:
            if href.startswith(item):
                protocol_parts = href.split(item)
                if protocol_parts[1].startswith(domain):
                    l.append(href)
                elif protocol_parts[1].split('.', 1)[1].startswith(domain):
                    l.append(href)
                break
    elif href and not href.startswith('//') and href.startswith('/'):
        l.append(main_url + href)


def check_main_url(url):
    global domain
    for item in protocols:
        if url.startswith(item):
            domain = url.split(item)[1]
            break


def save_content(url, title, l):
    if not title:
        title = 'nothing'
    else:
        title = title.string
    db.update({url: {'title': title, 'links': set(l)}})


def display(db):
    for k, v in db.items():
        print(f'{k} {v}')


site_map('www.bankier.pl')
print('***************************')

display(db)


