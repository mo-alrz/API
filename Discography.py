import pandas as pd

r = pd.read_html('https://en.wikipedia.org/wiki/Red_Hot_Chili_Peppers_discography')
print(r[1]['Title'][:13])

