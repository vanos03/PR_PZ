import requests
import json

def search_cve_for_cpe(cpe):
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:" + cpe
    # params = {"cpeMatchString": cpe}
    response = requests.get(base_url, params=None)
    
    # Проверяем статус ответа
    if response.status_code == 200:
        try:
            data = response.json()
            # print(str(data))
            return str(data)
        except Exception as e:
            # print("Error parsing JSON:", e)
            # print("Response Text:", response.text)
            return []
    else:
        # print("Error:", response.status_code)
        return []

def cve_search(cpe):
    
        # cpe = "cpe:/a:microsoft:sql_server:6.5".split(":/")
        findes_cve = {"CVE": list(), "CVSS": list()}
        cve_list = str(search_cve_for_cpe(cpe)).split(' ')
        for cve_item in cve_list:
            if "CVE" in cve_item:
                print(cve_item)
                findes_cve["CVE"].append(cve_item.replace(',', '').replace("'", ''))
            if "CVSS" in cve_item:
                print(cve_item)
                findes_cve["CVSS"].append(cve_item.replace(',', '').replace("'", ''))
        return findes_cve
