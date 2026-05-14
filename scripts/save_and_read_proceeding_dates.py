import json
from pathlib import Path

import requests

BASE_API_URL = 'https://api.sejm.gov.pl/sejm'


def save_proceeding_dates_to_file(term):
    """Fetches proceeding dates for a given Sejm term and saves them to a JSON file.

    Args:
        term: Sejm term number (kadencja).

    Returns:
        A list of date strings if successful, None otherwise.
    """
    file_path = f'../proceeding_dates/term{term}.json'
    url = f'{BASE_API_URL}/term{term}/proceedings'
    response = requests.get(url)
    if not response.ok:
        return None

    proceedings_raw = response.json()
    proceedings = []
    for proceeding_raw in proceedings_raw:
        proceeding = proceeding_raw
        keys_to_delete = ['agenda', 'current', 'title']
        for key in keys_to_delete:
            if key in proceeding:
                del proceeding[key]
        proceedings.append(proceeding)

    dates = {}
    for proceeding in proceedings:
        proceeding_dates = proceeding['dates']
        proceeding_number = proceeding['number']
        dates[proceeding_number] = [date for date in proceeding_dates]

    json_str = json.dumps(dates, indent=4)
    # print(json_str)
    Path("../proceeding_dates").mkdir(exist_ok=True)
    with open(file_path, 'w') as json_file:
        json_file.write(json_str)
        return dates


def read_proceeding_dates_from_file(term):
    """Reads proceeding dates for a given Sejm term from a local JSON file.

    Args:
        term: Sejm term number (kadencja).

    Returns:
        A dict of numbers and date strings loaded from the file.
    """
    file_path = f'../proceeding_dates/term{term}.json'
    with open(file_path, 'r') as json_file:
        proceedings = json.load(json_file)
    return proceedings


for term in range(7, 11):
    save_proceeding_dates_to_file(term)
