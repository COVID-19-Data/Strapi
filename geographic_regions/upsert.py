import os

import requests

STRAPI_BASE_URL = os.getenv('STRAPI_BASE_URL', 'https://strapi-jxyet6qmzq-ez.a.run.app')
SESSION = requests.Session()
TOKEN = None

def login():
    global TOKEN

    response = SESSION.post(
        'https://strapi-jxyet6qmzq-ez.a.run.app/auth/local',
        json={
            'identifier': os.getenv('STRAPI_USERNAME'),
            'password': os.getenv('STRAPI_PASSWORD')
        }
    )
    response.raise_for_status()
    TOKEN = response.json()['jwt']

def strapi_request(method, path, body=None, params=None):
    if not TOKEN:
        login()

    response = SESSION.request(
        method,
        '{}{}'.format(STRAPI_BASE_URL, path),
        json=body,
        params=params,
        headers={
            'Authorization': 'Bearer {}'.format(TOKEN)
        }
    )
    response.raise_for_status()
    return response.json()

def upsert_region(geographic_region, id=None):
    if id:
        return strapi_request('PUT', '/geographic-regions/{}'.format(id), body=geographic_region)

    return strapi_request('POST', '/geographic-regions', body=geographic_region)

def main():
    response = SESSION.get('https://raw.githubusercontent.com/olahol/iso-3166-2.json/master/iso-3166-2.json')
    response.raise_for_status()
    iso_3166_2 = response.json()

    existing_regions = strapi_request('GET', '/geographic-regions', params={'_limit': 10000})

    code_region_map = {}
    for region in existing_regions:
        code_region_map[region['code']] = region['id']

    for region_code, major_region in iso_3166_2.items():
        geographic_region = {
            'name': major_region['name'],
            'code': region_code,
            'type': 'COUNTRY'
        }

        children = []
        for division_code, division_name in major_region['divisions'].items():
            division_data = {
                'name': division_name,
                'code': division_code,
                'type': 'STATE_OR_PROVINCE'
            }

            print(division_data)
            print(division_code)
            print(code_region_map.get(division_code))

            division_data = upsert_region(division_data, id=code_region_map.get(division_code))

            children.append(division_data['id'])

        geographic_region['children'] = children

        print(geographic_region)
        print(code_region_map.get(region_code))
        upsert_region(geographic_region, id=code_region_map.get(region_code))

if __name__ == '__main__':
    main()
