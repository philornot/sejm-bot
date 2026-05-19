import yaml

GREAT_FILTER_PATH = 'the_great_filter.yaml'


def get_the_great_filter():
    with open(GREAT_FILTER_PATH, 'r') as filter_yaml_file:
        return yaml.safe_load(filter_yaml_file)
