import re
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_args():
    args = argparse.ArgumentParser(description='Parser by domain company')

    args.add_argument('-u', '--url',  
                      required=True, 
                      help='Target domain address')
    args.add_argument('-o', '--out', 
                      help='Set output file')
    args.add_argument('-p', '--links_protocol', 
                      default=['https'],
                      nargs='+', 
                      help='Set type parse links (default = https)')
    args.add_argument('-s', '--show_err',
                      action='store_true', 
                      help='Show bad links')
    args.add_argument('-v', '--visible_links',
                      action='store_true', 
                      help='Show bad links')

    args = args.parse_args()

    return args

def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            if args.show_err == True:
                print(response.status_code, "Ошибка при получении страницы: ", url)
            return None
    except Exception as e:
        if args.show_err == True:
            print("Ошибка: ", e, "url: ", url)
        return None

def extract_links(html, base_url, f_out, visited_urls):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)
    extracted_links = []
   
    for link in links:
        for prtcl in args.links_protocol:
            href = link['href']
            if href.startswith('/'):
                extracted_links.append(urljoin(base_url, href))
            elif re.match(f'{prtcl}://', href):
                extracted_links.append(href)
                # if href not in visited_urls:
                #     if args.visible_links:
                #         print(href)
                #     if f_out is not None:
                #         f_out.write(href + '\n')
                #     visited_urls.add(href)

    return extracted_links

def recursive_link_parser(start_url, target_domain, f_out, visited_urls):
    visited_urls.add(start_url)
    html = fetch_page(start_url)
    if html:
        links = extract_links(html, start_url, f_out, visited_urls)
        
        for link in links:
            parsed_link = urlparse(link)
            if link not in visited_urls:
                if args.visible_links: print(link)
                if f_out is not None: f_out.write(link + '\n')

                if parsed_link.netloc == target_domain:
                    recursive_link_parser(link, target_domain, f_out, visited_urls)

def start_parse(args):
    start_url = args.url
    f_out = None
    if args.out is not None:
        f_out = open(args.out, 'w+')
    target_domain = urlparse(start_url).netloc
    visited_urls = set()
    recursive_link_parser(start_url, target_domain, f_out, visited_urls)

if __name__ == "__main__":
    args = get_args()
    start_parse(args)
