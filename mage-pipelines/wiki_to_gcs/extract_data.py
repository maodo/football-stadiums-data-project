import io
import pandas as pd
import requests
from bs4 import BeautifulSoup
from geopy import Nominatim

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'

def get_html_page(url):
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f'Error getting wikipedia data {e}')

def get_table_data(url):
    soup = get_html_page(url)
    table = soup.find_all("table", {"class":"wikitable"})[1]
    table_rows = table.find_all("tr")
    return table_rows

data = []
def extract_data(url):
    table_rows = get_table_data(url)
    for i in range(1,len(table_rows)):
        table_data = table_rows[i].find_all('td')
    
        description_url = 'https://en.m.wikipedia.org' + table_data[0].find('a').get('href')
        desc_html = get_html_page(description_url)
        section_content = desc_html.find_all("section",{"class":"mf-section-0"})
        if section_content:
            p_len = len(section_content[0].find_all("p"))
            if p_len == 1:
                description = section_content[0].find_all("p")[0].text
            elif p_len == 2:
                description = section_content[0].find_all("p")[1].text
            elif p_len > 2:
                description = section_content[0].find_all("p")[1].text + "-" + section_content[0].find_all("p")[2].text
        else :
            description = 'No description available for this stadium'
            
        table_values = {
            'rank' : i,
            'stadium' : table_data[0].text,
            'description' : description,
            'capacity' : table_data[1].text,
            'region' : table_data[2].text,
            'country' : table_data[3].text,
            'city' : table_data[4].text,
            'home_team' : table_data[6].text,
            'image_url' : 'https:' + table_data[5].find('img').get('src') if table_data[5].find('img') else NO_IMAGE
        }
        data.append(table_values)
    return pd.DataFrame(data)

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity'

    print('Getting data from wikipedia pages...')
    df_stadiums = extract_data(url)
    print('Data successfully extracted...')

    return df_stadiums


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
