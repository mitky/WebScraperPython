#mitky practice
import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/" # site url
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer") # div id from the site

html_tags = soup.find_all('h2') # all h2 tags
#print(html_tags)

#for jobs in html_tags:
    #print(jobs.text.strip())  # print as text not as tags

jobs_cards = soup.find_all('div', class_='media-content') # look for class in div 


#look for specific tags
for jobs in jobs_cards:
    job_name = jobs.h2.text.strip() #take name(price, ect), text.split()[-1] take last element
    print(job_name) 
