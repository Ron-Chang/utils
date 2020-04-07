import os
import time
from datetime import datetime, timedelta


class SpyderTimer:

    def __init__(self, start, sleep_length_seconds=60*60*24, update_duration=None, separator_symbol=None, **kwargs):
        self.start = start
        self.now = datetime.now()
        self.separator_symbol = separator_symbol
        self.update_duration = update_duration
        self.sleep_length_seconds = sleep_length_seconds
        self.extra_info_dict = kwargs

    def _get_divider(self):
        symbol = self.separator_symbol
        if (not symbol) or (type(symbol) is not str):
            symbol = '='
        print(symbol * os.get_terminal_size(0)[0])

    def _update_info(self):
        now = self.now
        duration = self.update_duration
        if not duration:
            return None
        update_start = (now - timedelta(days=duration)).strftime('%Y-%m-%d %H:%M')
        update_end = (now + timedelta(days=duration)).strftime('%Y-%m-%d %H:%M')
        print(f'[INFO      ]| UP TO DATE! [{update_start}] <-> [{update_end}]')

    def _sleep(self):
        now = self.now
        sleep_length = self.sleep_length_seconds
        sleep_length_hr = round(sleep_length/3600, 2)
        next_round = (now + timedelta(seconds=sleep_length)).strftime('%Y-%m-%d %H:%M:%S')
        print(f' = SLEEP FOR : {sleep_length_hr} hrs.')
        print(f' = NEXT ROUND STARTING AT : {next_round} ')
        time.sleep(sleep_length)

    def _consume(self):
        print(f' = CONSUME : {round(time.time() - self.start, 2)} sec.')

    def _extra_info(self):
        if self.extra_info_dict:
            print(' = [EXTRA_INFO]')
            for extra_info_key, extra_info_value in self.extra_info_dict.items():
                print(f' | {extra_info_key.upper()}: {extra_info_value}')
            print('-' * os.get_terminal_size(0)[0])
        return None

    def run(self):
        self._get_divider()
        self._extra_info()
        self._consume()
        self._update_info()
        self._sleep()
        self._get_divider()
