import csv
import io

from collections import OrderedDict

import os.path
import yaml

import requests

from django.core.management import BaseCommand


class Command(BaseCommand):
    url = 'https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv'

    def handle(self, *args, **options):
        filename = os.path.join(os.path.dirname(__file__), '..', '..', 'fixtures', 'initial.yaml')
        print(filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        data = []
        response = requests.get(self.url, stream=True)
        reader = csv.DictReader(io.StringIO(response.text))

        for row in reader:
            data.append(OrderedDict((
                ('model', 'nationality.Country'),
                ('pk', int(row['ISO3166-1-numeric'])),
                ('fields', OrderedDict((
                    ('label', row['official_name_en']),
                    ('alpha_2', row['ISO3166-1-Alpha-2'] or None),
                    ('alpha_3', row['ISO3166-1-Alpha-3'] or None),
                    ('numeric', row['ISO3166-1-numeric']),
                )))
            )))

        response.close()

        with open(filename, 'w') as f:
            represent_dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
            yaml.add_representer(OrderedDict, represent_dict_order)
            yaml.dump(data, f, default_flow_style=False)
