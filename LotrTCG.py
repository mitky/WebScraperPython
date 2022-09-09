from requests import request
import requests
from gql import Client, gql
from bs4 import BeautifulSoup
from gql.transport.requests import RequestsHTTPTransport
URL = "https://lotrtcgwiki.com/wiki/grand" # site url
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

HASURA_URL = "https://lotrwebscrapper.herokuapp.com/v1/graphql"
transport = RequestsHTTPTransport(
    url=HASURA_URL,
    verify=True,
    retries=3,
)


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
for cards in cards_table:
    rows = cards.find_all('tr')
    for row in rows:
        card_id = row.find('td')
        card_name = row.find('td', class_= 'col1').string
        card_type = row.find('td', class_= 'col2').string
        runGQL(str(card_name),str(card_name))
    
