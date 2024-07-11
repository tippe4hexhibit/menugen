import logging

log = logging.getLogger(__name__)

MEAL_ORDER = ['Pre-Fair Breakfast', 'Pre-Fair Lunch', 'Breakfast', 'Snacks', 'All Day', 'Lunch', 'Dinner']
MEAL_ORDER_MAPPING = {meal: index for index, meal in enumerate(MEAL_ORDER)}


class DiningVendors:
    def __init__(self, vendor_data):
        log.info(f'Initializing {self.__class__}')
        self._vendor_data = vendor_data

    def get_vendor(self, vendor_id):

        for vendor in self._vendor_data:
            if 'id' in vendor.keys() and vendor['id'] == vendor_id:
                return vendor['fields']

        return None


class DiningEvents:
    def __init__(self, event_data):
        log.info(f'Initializing {self.__class__}')

        for i in event_data:
            print(i)

        self.events = sorted(event_data,
                             key=lambda x: (x["fields"]["Date"],
                                            MEAL_ORDER_MAPPING[x["fields"]["Meal"]]
                                            )
                             )
        self.events = [x['fields'] for x in self.events]

    def __getitem__(self, item):
        log.info(f'__getitem__({item})')
        return self.events[item]


class DiningEventMenuItems:
    def __init__(self, items_data):
        log.info(f'Initializing {self.__class__}')
        self._items_data = items_data

    def get_item(self, item_id):
        log.info(f'Getting {item_id}')

        results = []
        for item in self._items_data:
            if item["id"] == item_id:
                results.append(item['fields'])

                # Collect any child items related to this menu item
                # and stack them in the list
                if "Child Items" in item['fields'].keys():
                    for child_item in item['fields']['Child Items']:
                        results.append(self.get_item(child_item)[0])

        return results
