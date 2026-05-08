import json


def read_proceeding_dates_from_file(term):
    """Reads proceeding dates for a given Sejm term from a local JSON file.

    Args:
        term: Sejm term number (kadencja).

    Returns:
        A list of date strings loaded from the file.
    """
    file_path = f'../proceeding_dates/term{term}.json'
    with open(file_path, 'r') as json_file:
        dates = json.load(json_file)
    return dates
