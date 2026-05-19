import yaml
import pathlib

repo_root = pathlib.Path(__file__).parent.parent
CONFIG_PATH = repo_root / "scraper" / "config.yaml"
BASE_API_URL = 'https://api.sejm.gov.pl/sejm'

with open(CONFIG_PATH, 'r') as config_file:
    yaml_config = yaml.safe_load(config_file)
    TERM = yaml_config['term']


def get_the_great_filter():
    with open(GREAT_FILTER_PATH, 'r') as filter_yaml_file:
        return yaml.safe_load(filter_yaml_file)
