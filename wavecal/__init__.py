import requests
from datetime import datetime
from bs4 import BeautifulSoup, NavigableString


def get_data(url):
    """
        <div class="d-none daybox" data-available="0" data-day="06/13/2022"
            data-generaladmission="false" data-totalavailable="24">

    """
    FORMAT = '%m/%d/%Y %H:%M %p'
    page = requests.get(url)

    page.raise_for_status()
    soup = BeautifulSoup(page.content, "html.parser")

    elem = soup.find(id='calendar-dp')

    if elem is None or isinstance(elem, NavigableString):
        raise Exception("couldn't find calendar element")

    events = [] 

    for child in elem.children:
        if not isinstance(child, str):
            date = child['data-day']
            for grandchild in child.find_all(class_="calendar-time"): 
                for gc in grandchild.find_all('input', type='submit'): 
                    t = gc['value']
                    events.append(
                        datetime.strptime(f"{date} {t}", FORMAT),
                    )

    return events
          
