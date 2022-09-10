from requests import request
import requests
from gql import Client, gql
from bs4 import BeautifulSoup
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import re

now = now = datetime.now()

URL = "https://lotrtcgwiki.com/wiki/grand" 
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

HASURA_URL = "https://lotrwebscrapper.herokuapp.com/v1/graphql"
transport = RequestsHTTPTransport(
    url=HASURA_URL,
    verify=True,
    retries=3,
)

editions_dict = {
  "1": "The-Fellowship-of-the-Ring",
  "2": "Mines-of-Moria",
  "3": "Realms-of-the-Elf-lords",
  "4": "The-Two-Towers",
  "5": "Battle-of-helms-deep",
  "6": "Ents-of-Fangorn",
  "7": "Battle-of-Helms-Deep",
  "8": "The-Return-of-the-King",
  "9": "Siege-of-Gondor", 
  "10": "Reflections",
  "11": "Mount-Doom",
  "12": "Shadows",
  "13": "Black Rider",
  "14": "Bloodlines",
  "15": "Expanded Middle earth",
  "16": "The Hunters",
  "17": "The Wraith Collection",
  "18": "Rise of Saruman", 
  "19": "Treachery & Deceit",
  "0": "lotr-promotional",
  "": "empty"
}

client = Client(transport=transport, fetch_schema_from_transport=True)

def runGQL(name, edition):

    query = gql("""mutation MyMutation($name: String!, $edition: String!) {
      insert_lotr_all_cards(objects: {name: $name, edition: $edition}) {
        affected_rows
      }
    }""")

    params = {
        "name": name,
        "edition": edition
    }
    result = client.execute(query, variable_values=params)

cards_table = soup.find_all('table', class_='inline') # look for class in div 

#look for specific tags
print("Process Start:", now.strftime("%d/%m/%Y %H:%M:%S"))
for cards in cards_table:
    rows = cards.find_all('tr')
    for row in rows:
        card_id = str(row.find('td').string)
        card_name = row.find('td', class_= 'col1').string
        #will fix this tomorrow, too sleepy to make dict
        card_name_cleaned = str(card_name).replace(",","").replace(" ","-").replace("•","").replace("-(D)","").replace("-(M)","").replace("-(D)","").replace("-(SPD)","").replace("-(W)","").replace("-(P)","").replace("-(AFD)","").replace("-(T)","")
        card_id_regex = re.compile(r"^([^a-zA-Z]*)")
        edition = re.search(card_id_regex, card_id).group(0)
        try:
           
            #card_type = row.find('td', class_= 'col2').string   
            runGQL(card_name_cleaned,editions_dict[edition].replace(" ","-"))
            pass
        except TypeError as numerr:
            card_name.string =='Number'
            print(numerr)
    """     except TypeError as outside:
            card_
            print(outside)
            """
            
print("Process End:", now.strftime("%d/%m/%Y %H:%M:%S"))