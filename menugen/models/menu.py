import logging

from datetime import datetime
from datetime import timezone
from zoneinfo import ZoneInfo

log = logging.getLogger(__name__)

MEAL_ORDER = ['Breakfast', 'AllDay', 'Lunch', 'Dinner']
MEAL_ORDER_MAPPING = {meal: index for index, meal in enumerate(MEAL_ORDER)}


class DiningVendors:
    def __init__(self, vendor_data):
        log.info(f'Initializing {self.__class__}')


class DiningEvents:
    def __init__(self, event_data):
        log.info(f'Initializing {self.__class__}')
        self.event_data = event_data

        # from pprint import pprint
        # pprint(event_data)
        sorted_events = sorted(event_data,
                               key=lambda x: (x["fields"]["Date"],
                                              MEAL_ORDER_MAPPING[x["fields"]["Meal"]]
                                              )
                               )

        for event in sorted_events:
            print(f"{event['fields']['Date']} {event['fields']['Meal']} {event['fields']['Meal Headline']}")


class DiningEventMenuItems:
    def __init__(self, items_data):
        log.info(f'Initializing {self.__class__}')
        self.items_data = items_data

    def get_item(self, item_id):
        log.info(f'Getting {item_id}')

        results = []
        for item in self.items_data:
            if item["id"] == item_id:
                results.append(item)

                # Collect any child items related to this menu item
                # and stack them in the list
                if "Child Items" in item['fields'].keys():
                    for child_item in item['fields']['Child Items']:
                        results.append(self.get_item(child_item))

        return results
