import pandas
import requests


# Initialization
output_list = []

df = pandas.read_csv("input.csv", dtype='str').drop_duplicates()[['Company', 'Street', 'City', 'St', 'ZIPCode']]
for details in df.to_dict('records'):
    headers = {
        'authority': 'tools.usps.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'sec-ch-ua-platform': '"Linux"',
        'origin': 'https://tools.usps.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://tools.usps.com/zip-code-lookup.htm?byaddress',
        'accept-language': 'en-GB,en;q=0.9',
    }

    data = {
        'companyName': details['Company'],
        'address1': details['Street'],
        'address2': '',
        'city': details['City'],
        'state': details['St'],
        'urbanCode': '',
        'zip': details['ZIPCode']
    }

    response = requests.post('https://tools.usps.com/tools/app/ziplookup/zipByAddress', headers=headers, data=data)
    try:
        data = response.json()
    except Exception:
        pass  # Log to check Json Parser Error

    status = 'SUCCESS'
    if data.get('resultStatus', '') != 'SUCCESS':
        status = data.get('resultStatus', '')

    details['Status'] = status
    output_list.append(details)

# Writing to output file as csv
df = pandas.DataFrame.from_dict(output_list)
df.to_csv('output.csv', index=False, header=True)
