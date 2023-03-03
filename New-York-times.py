import requests

my_key = 'jhGQxXRZzKbl6oDtcRInVY8R2PgzPgEn'
subj = 'moon landing by Apollo 11'
response = requests.get(f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={subj}&api-key={my_key}')
jsonified = response.json()

for k1, v1 in jsonified.items():
    if k1 == 'response':
        for k2, v2 in v1.items():
            if k2 == 'docs':
                for i in v2:
                    for k3, v3 in i.items():
                        print(f'Headline:{i["headline"]} Snippet:{i["snippet"]} '
                              f'Publication date:{i["pub_date"]}')
                        break
