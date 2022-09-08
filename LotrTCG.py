#scrape the Lotr site

import requests
from bs4 import BeautifulSoup

URL = "https://lotrtcgwiki.com/wiki/grand" # site url
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

cards_table = soup.find_all('table', class_='inline') # look for class in div 


#look for specific tags
for cards in cards_table:
    rows = cards.find_all('tr')
    #print(rows)
    for row in rows:
        card_id = row.find('td')
        card_name = row.find('td', class_= 'col1').a
        card_type = row.find('td', class_= 'col2').a
        print(card_id.text)
        print(card_name)
        print(card_type)
        
    
    
    