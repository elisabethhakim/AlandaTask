# title           :main.py
# description     :Webscraping of Purplebricks, a UK online estate agent, on information of current listings
# author          :Elisabeth Hakim
# date            :20210321
# version         :1.0.0
# notes           :
# python_version  :Python 3.9.2
# ======================================================================================================================

import requests as rq

from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import json


# Function to build URL string by fetching in page number, radius and location
def build_url(p_num: int, rad: int, loc: str) -> str:
    templ_url = (
        'https://www.purplebricks.co.uk/search/property-for-sale/'
        '?betasearch=true&page={p_num}&searchRadius={rad}'
        '&searchType=ForSale&soldOrLet=false&sortBy=2&location={loc} '
    )
    rq_url = templ_url.format(
        **{
            "p_num": p_num,
            "rad": rad,
            "loc": loc
        }
    )
    return rq_url


# Function to create session and send a get request to server
def get_res(url: str) -> rq:
    # Use pre-defined header from browser to avoid bad response from server
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36',
        'connection': 'keep-alive',
        'content-type': 'application/json',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'path': '/static-new-search/_next/data/PFRbQwuxxWBDUqXuQAPzL/search.json',
        'authority': 'www.purplebricks.co.uk',
        'cache': 'no-cache',
        'cache-control': 'no-cache',
        'pragma': 'no-cache'
    }

    with rq.Session() as session:
        r = session.get(url, headers=headers, stream=True)
        if r.status_code != 200:
            print('Bad response ' + r.status_code)
    return r


# Function to calculate the total number of pages to loop through
def get_loop_num(r: rq) -> int:
    soup = BeautifulSoup(r.content, 'html.parser')

    # Number of properties stored in top pane, <strong> nested in a <span>
    num_properties = soup.find('span', {"data-testid": "search-results-number"}).find('strong').text

    # Number of properties / number of properties per page
    loop_num = round(int(num_properties) / 10)
    return loop_num


# Function to retrieve list of results tags
def get_res_tags(loop_num: int, rad: int, loc: str) -> list:
    res_tags = []
    # Loop through each page of property search and retrieve results list tags
    for p_num in range(1, loop_num + 1):
        # Build URL string and send HTTP request
        url = build_url(p_num, rad, loc)
        p_r = get_res(url)

        # Create BeautifulSoup object
        soup = BeautifulSoup(p_r.content, 'html5lib')

        # Up to 10 listing results are stored on each page within the ul tag
        tag = soup.find("ul", {"data-testid": "results-list"})
        res_tags.append(tag)
    return res_tags


# Function to isolate the features of interest of the results tags and save it in a format consistent with json
def parse_data(tags: list) -> dict:
    prop_dict = {}
    for tag in tags:
        # Property features stored within attribute tags
        tags_a = tag.find_all('a')

        # Loop through each of the 10 properties within a result tag
        for tag_a in tags_a:
            # Use href to obtain property id
            # e.g. 975717 in "/property-for-sale/3-bedroom-flat-battersea-975717"
            href = tag_a.get('href')
            prop_id = href.rsplit('-', 1)[-1]

            # Three features of interest are stores within the 'aria-label' attribute
            features = tag_a.get('aria-label').split(' ')
            prop_dict[prop_id] = {}
            prop_rooms = features[0] + ' ' + features[1]
            prop_type = " ".join(features[2:][:-2])

            # Format string to be easy convertible to numeric value
            prop_value = features[-1].translate(str.maketrans('', '', ' £,'))
            prop_dict[prop_id]["num_rooms"] = prop_rooms
            prop_dict[prop_id]["type"] = prop_type
            prop_dict[prop_id]["price"] = prop_value
    return prop_dict


# Function to create directory for data storage
def make_dt_path(loc: str, rad: int) -> Path:
    ROOT = Path(__file__).parent
    DATA = ROOT.joinpath("Data")
    today = datetime.today().date()
    _loc_name = DATA.joinpath(loc + "_" + str(rad))
    pth = _loc_name.joinpath(str(today))
    pth.mkdir(parents=True, exist_ok=True)
    print('Directory successfully created')
    return pth


# Void function to store data
def store_data(prop_dict: dict, file_dir=None):
    scrape_time = datetime.today().time().strftime('%H%M%S')
    file_dir = make_dt_path(location, radius)
    filename = file_dir.joinpath(scrape_time + ".json")
    with open(filename, 'w') as f:
        json.dump(prop_dict, f)
    return


if __name__ == "__main__":
    radius = 30
    location = "london"

    # Step 1: Calculate the total number of pages to loop through
    url_rest = build_url(1, radius, location)
    response = get_res(url_rest)
    number_of_pages = get_loop_num(response)

    # Step 2: Retrieve property features
    list_of_tags = get_res_tags(number_of_pages, radius, location)
    data = parse_data(list_of_tags)

    # Step 3: Save results in a json file
    store_data(data)
