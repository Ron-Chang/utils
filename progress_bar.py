import os
import time


class ProgressBar:

    @staticmethod
    def _get_console_width():
        columns, rows = os.get_terminal_size(0)
        return columns

    @staticmethod
    def _get_proceed_percent(count, amount):
        return count/amount * 100

    @staticmethod
    def _progress_bar(proceed_percent, bar_width, bar_fg_unit='#', bar_bg_unit='_'):
        fg_length = int(bar_width * proceed_percent/100)
        bg_length = bar_width - fg_length

        bar_fg = bar_fg_unit * fg_length
        bar_bg = bar_bg_unit * bg_length

        return bar_fg + bar_bg

    @staticmethod
    def _get_display_info(count, amount, proceed_percent, info, description):
        title_str = f'[{str(info)[:10]:<10}]| ' if info else '[INFO      ]| '
        amount_str = f'{str(description)[:20]:<20} | ' if description else f'{count:,} of {amount:,} | '
        proceed_percent_str = f'[{proceed_percent:>6,.2f}%] '
        display_info = title_str + amount_str + proceed_percent_str
        length = len(display_info)
        return length, display_info

    @classmethod
    def display(cls, count, amount, info=None, description=None):
        """
        :info: only display the first 10 letters.
        :description: only display the first 16 letters.
        """
        console_width = cls._get_console_width()
        proceed_percent = cls._get_proceed_percent(count=count, amount=amount)
        length, display_info = cls._get_display_info(
            count=count,
            amount=amount,
            proceed_percent=proceed_percent,
            info=info,
            description=description
        )
        bar_width = console_width - length - 10
        progress_bar = f'{display_info}|{cls._progress_bar(proceed_percent=proceed_percent, bar_width=bar_width)}|'
        if not proceed_percent == 100:
            print(progress_bar, end='\r', flush=True)
        else:
            print(progress_bar+' DONE!')


if __name__ == '__main__':

    for i in range(1,123+1):
        ProgressBar.display(count=i, amount=123)
        time.sleep(0.2)
