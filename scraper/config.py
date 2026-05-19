import yaml

CONFIG_PATH = 'config.yaml'
BASE_API_URL = 'https://api.sejm.gov.pl/sejm'

with open(CONFIG_PATH, 'r') as config_file:
    yaml_config = yaml.safe_load(config_file)
    TERM = yaml_config['term']

