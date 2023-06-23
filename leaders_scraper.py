import requests
from bs4 import BeautifulSoup
import re 
import json


""""
Retrieves data on country leaders from the country-leaders API and extracts the first paragraph from their Wikipedia pages
"""
def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    countries_url = root_url + "/countries"
    cookie_url = root_url + "/cookie"
    leaders_url = root_url + "/leaders"

    session = requests.Session()  # Create a Session object
    cookies = session.get(cookie_url).cookies  # Use the session object for cookie retrieval
    countries = session.get(countries_url, cookies=cookies).json()  # Use the session object for the countries request
    leaders_per_country = {}

    for country in countries:
        leaders_per_country[country] = requests.get(leaders_url, cookies=cookies, params={"country": country}).json()

    # Pass the session object to the get_first_paragraph() function
    for country in countries:
        for i in range(0, 3): ######## required improvement to find the number of the leaders in a smart way
            wikipedia_url = leaders_per_country[country][i]['wikipedia_url']
            first_paragraph = get_first_paragraph(wikipedia_url, session)  # Pass the session object as an argument
            leaders_per_country[country][i]['first_paragraph'] = first_paragraph

    return leaders_per_country, countries



def get_first_paragraph(wikipedia_url,Session):
    print(wikipedia_url)
    req_text= Session.get(wikipedia_url)
    bs=BeautifulSoup(req_text.content,"html.parser")
    paragraphs = bs.findAll("p")
    for paragraph in paragraphs:
        if paragraph.text.split() :
            first_paragraph = paragraph.text
            break
    ######## the regex part should be imroved to clean all the paragraphs for different countries    
    first_paragraph= re.sub(r"\[[0-9a-zA-Z]+\]|\xa0–|\n", ' ', first_paragraph)
    return first_paragraph

def save(leaders_per_country):
    with open("leaders.json","w") as leaders:
        json.dump(leaders_per_country,leaders)
    return   


leaders_per_country=get_leaders()
print(leaders_per_country)
save(leaders_per_country)


