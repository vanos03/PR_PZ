import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Ошибка при получении страницы:", response.status_code)
            return None
    except Exception as e:
        print("Ошибка:", e)
        return None

def extract_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)
    extracted_links = []
    for link in links:
        href = link['href']
        if href.startswith('/'):
            extracted_links.append(urljoin(base_url, href))
        elif re.match(r'^https?://', href):
            extracted_links.append(href)
        elif re.match(r'^http?://', href):
            extracted_links.append(href)
        elif re.match(r'^ftp://', href):
            extracted_links.append(href)
        else:
            print("Пропущенная ссылка:", href)
    return extracted_links

def recursive_link_parser(start_url, visited_urls=set()):
    if start_url in visited_urls:
        return
    visited_urls.add(start_url)
    print("Парсинг ссылки:", start_url)
    html = fetch_page(start_url)
    if html:
        links = extract_links(html, start_url)
        for link in links:
            recursive_link_parser(link, visited_urls)


start_url = "https://www.python.org"
recursive_link_parser(start_url)
