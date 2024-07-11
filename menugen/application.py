import logging
import os
from datetime import datetime

from pathlib import Path

from pyairtable import Api
from menugen.models.menu import DiningVendors, DiningEvents, DiningEventMenuItems

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

Dumper.ignore_aliases = lambda *args : True

log = logging.getLogger(__name__)

CATEGORY_ORDER = ['Entrées', 'Drinks', 'À La Carte', 'Other Items']
CATEGORY_ORDER_MAPPING = {category: index for index, category in enumerate(CATEGORY_ORDER)}


class MenuGenApp:

    @staticmethod
    def run():

        required_env_vars = [
            'AIRTABLE_API_KEY',
            'AIRTABLE_BASE',
            'MENU_OUTPUT_DIR',
            'TABLE_DINING_VENDORS',
            'TABLE_DINING_EVENTS',
            'TABLE_DINING_EVENTMENUITEMS'
        ]

        check_env_vars = [x in os.environ for x in required_env_vars]

        if not all(check_env_vars):
            log.error(f'{required_env_vars}: {check_env_vars}')
            log.error('Ensure all environment variables are set properly')
            exit(255)
        else:
            for env_var in required_env_vars:
                if 'KEY' in env_var:
                    log.info(f'{env_var} is set')
                else:
                    log.info(f'{env_var} is {os.environ[env_var]}')

        output_path = Path(os.environ['MENU_OUTPUT_DIR'])

        if not output_path.exists():
            log.error(f"OUTPUT_DIR ({os.environ['MENU_OUTPUT_DIR']}) does not exist.")
            exit(254)

        api = Api(os.environ['AIRTABLE_API_KEY'])

        raw_dining_vendors = api.get_table(os.environ['AIRTABLE_BASE'],
                                           os.environ['TABLE_DINING_VENDORS']).all()

        raw_dining_events = api.get_table(os.environ['AIRTABLE_BASE'],
                                          os.environ['TABLE_DINING_EVENTS']).all()

        raw_dining_eventmenuitems = api.get_table(os.environ['AIRTABLE_BASE'],
                                                  os.environ['TABLE_DINING_EVENTMENUITEMS']).all()

        dining_vendors = DiningVendors(raw_dining_vendors)
        dining_events = DiningEvents(raw_dining_events)
        dining_eventmenuitems = DiningEventMenuItems(raw_dining_eventmenuitems)
        dining_eventitem = dining_eventmenuitems.get_item('recmbIgNCywbSHjBG')

        from pprint import pprint

        current_date = ""
        full_event_list = None
        for dining_event in dining_events:
            if not current_date:
                current_date = dining_event['Date']
                full_event_list = {'dates': {}}

            if current_date != dining_event['Date']:
                current_date = dining_event['Date']

            if current_date not in full_event_list['dates'].keys():
                full_event_list['dates'][current_date] = {}
                full_event_list['dates'][current_date]['events'] = []
                full_event_list['dates'][current_date]['longdate'] = datetime.strptime(current_date, '%Y-%m-%d').strftime('%A, %B %d, %Y')

            if "Food Vendor" in dining_event.keys():
                dining_event['Food Vendor Data'] = dining_vendors.get_vendor(dining_event['Food Vendor'][0])
            if "Menu Items IDs" in dining_event.keys():
                dining_event['Menu Items'] = []
                for item_id in dining_event['Menu Items IDs']:
                    dining_event['Menu Items'] += dining_eventmenuitems.get_item(item_id)

                dining_event['Menu Items'] = sorted(dining_event['Menu Items'],
                                                    key=lambda x: (CATEGORY_ORDER_MAPPING[x['Tag'][0]])
                                                    )

            full_event_list['dates'][current_date]['events'].append(dining_event)

        for event_date in full_event_list['dates']:
            filename = 'dining_' + ''.join(event_date.split('-'))

            yaml_data = yaml.dump(full_event_list['dates'][event_date], Dumper=Dumper, sort_keys=False)

            with open(output_path.joinpath(filename).with_suffix('.yaml'), 'w') as f:
                log.info(f'Writing {event_date} to {output_path.joinpath(filename).with_suffix('.yaml')}')
                f.write(yaml_data)

