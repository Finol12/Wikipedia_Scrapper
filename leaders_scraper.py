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
        for i in range(0,len(leaders_per_country[country])): 
            wikipedia_url = leaders_per_country[country][i]['wikipedia_url']
            first_paragraph = get_first_paragraph(wikipedia_url, session)  # Pass the session object as an argument
            leaders_per_country[country][i]['first_paragraph'] = first_paragraph

    return leaders_per_country, countries


"""
Retrieves the first paragraph from the given Wikipedia URL using a Session object
Parameters:
        - wikipedia_url (str): The URL of the Wikipedia page.
        - session (Session): The Session object used for making requests.

Returns:
        - first_paragraph (str): The sanitized first paragraph of the Wikipedia page.
"""
def get_first_paragraph(wikipedia_url,Session):
    print(wikipedia_url)
    req_text= Session.get(wikipedia_url)
    bs=BeautifulSoup(req_text.content,"html.parser")
    paragraphs = bs.findAll("p")
    for paragraph in paragraphs:
        if paragraph.text.split() :
            first_paragraph = paragraph.text
            break
    # Sanitize the first paragraph by removing unwanted elements using regex
    # (the regex part should be improved to clean all the paragraphs for different countries.)    
    first_paragraph= re.sub(r"\[[0-9a-zA-Z]+\]|\xa0–|\n", ' ', first_paragraph)
    return first_paragraph


"""
    Saves the leaders_per_country dictionary as a JSON file.
    Parameters:
        - leaders_per_country (dict): The dictionary containing leaders data.
"""
def save(leaders_per_country):
    with open("leaders.json","w") as leaders:
        json.dump(leaders_per_country,leaders)
    return   


leaders_per_country=get_leaders()
print(leaders_per_country)
save(leaders_per_country)


