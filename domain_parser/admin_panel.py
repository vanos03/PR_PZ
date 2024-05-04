import threading
import time

import requests

requests.packages.urllib3.disable_warnings()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                  'Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 '
}

suffics = ['wp-admin', 'wp-', 'wp-login', 'admin', '?q=admin', 'bitrix', 'auth', 'phpMyAdmin', 'bitrix/admin',
           'administrator', 'panel', 'ckeditor', 'adm', 'manager', 'user/login', 'netcat', 'typo3', 'admin.php',
           'admin.js', 'user/register', 'register', '?do=register', 'do=', 'netcat/admin', 'koobooCMS/admin',
           'apanel', '_ аdmin/indеx.php', 'login', 'admincp', 'db', 'dbadmin', 'myadmin', 'mysql', 'mysqladmin',
           'mysql-admin', 'phpmyadmin', 'acart', 'access', 'citrix', 'cgi-bin', 'administrator.php', 'cpanel',
           'klarnetCMS', 'cabinet', 'plesk-stat', 'geomiXCMS', 'portal', 'loginpanel', 'memberlogin', 'wpadmin.html']


adm_list = set()


def req_robots(domain):
    print('. robots.txt inf:')
    try:
        resp = requests.get(f'https://{domain}/robots.txt', headers=headers, verify=False, timeout=10)
    except requests.exceptions.ConnectionError:
        return
    robot_line = resp.text.splitlines()
    for line in robot_line:
        for suf in suffics:
            if suf in line:
                if 'base64' in line:
                    return
                try:
                    adm_list.add(f'https://{domain}{line.split(":")[1].strip()}')
                except IndexError:
                    adm_list.add(f'https://{domain}{line.strip()}')


def req_search(domain, suf):
    try:
        resp = requests.head(f'https://{domain}/{suf}', headers=headers, verify=False, timeout=5)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return
    if resp.status_code == 200:
        adm_list.add(resp.url)
    time.sleep(0.4)


def start_adm_search(domain):
    adm_list.clear()
    req_robots(domain)
    # thread_func(domain)

    return adm_list