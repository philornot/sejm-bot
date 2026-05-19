import yaml

from keyword_detector.config import GREAT_FILTER_PATH

with open(GREAT_FILTER_PATH, 'r') as filter_yaml_file:
    great_filter = yaml.safe_load(filter_yaml_file)

print(great_filter)