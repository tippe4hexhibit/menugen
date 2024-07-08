import logging
import os

from pathlib import Path

from pyairtable import Api
from menugen.models.menu import DiningVendors, DiningEvents, DiningEventMenuItems
from menugen.models.yaml import YamlSchedule

log = logging.getLogger(__name__)


class MenuGenApp:

    @staticmethod
    def run():

        required_env_vars = [
            'AIRTABLE_API_KEY',
            'AIRTABLE_BASE',
            'OUTPUT_DIR',
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

        output_path = Path(os.environ['OUTPUT_DIR'])

        if not output_path.exists():
            log.error(f"OUTPUT_DIR ({os.environ['OUTPUT_DIR']}) does not exist.")
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

        # # Build the object structure from the Airtable data
        # full_schedule = FullSchedule(raw_schedule)
        #
        # # Dump out all the YAMLs for each schedule type, by date
        # schedule_prefix = None
        # for schedule_type, schedule in full_schedule.get_schedules().items():
        #     schedule_yamls = YamlSchedule(schedule)
        #     schedule_prefix = schedule.schedule_abbreviation + '_'
        #
        #     for yaml_date, yaml in schedule_yamls.get_yamls().items():
        #         schedule_filename = schedule_prefix + ''.join(yaml_date.split('-')) + '.yaml'
        #
        #         with open(output_path / schedule_filename, 'w') as yaml_out:
        #             log.info(f'Writing {schedule_type} schedule file for {yaml_date} called {schedule_filename}')
        #             yaml_out.write(yaml)
        #
