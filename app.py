from emulator import emulator
import logging
import sys
import argparse

if __name__ == '__main__':
    log = logging.getLogger('WordClock')
    formatter = logging.Formatter('%(threadName)s:[%(levelname)s] %(message)s')

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)

    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    log.info('Running.')

    # usage ./generate_layout.py "sheet_id" "range_name"
    parser = argparse.ArgumentParser()
    parser.add_argument('spreadsheet_id', type=str)
    parser.add_argument('range_name', type=str)
    args = parser.parse_args()
    emulator = emulator.Emulator(args, log)
    emulator.run()
