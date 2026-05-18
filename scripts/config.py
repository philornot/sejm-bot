import yaml

CONFIG_PATH = '../config.example.yaml'

with open(CONFIG_PATH, 'r') as config_file:
    yaml_config = yaml.safe_load(config_file)
    TERM = yaml_config['term']
    BASE_API_URL = yaml_config['base_api_url']
