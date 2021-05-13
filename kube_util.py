"""
Ron's lazy KUBECTL CLI
"""
import argparse
import re
import os
import subprocess
import sys

class ColorTag:
    RESET = '\x1b[0m'

    RED = '\x1b[5;31;40m'
    BLUE = '\x1b[5;34;40m'
    CYAN = '\x1b[5;36;40m'
    GRAY = '\x1b[5;37;40m'
    GREEN = '\x1b[5;32;40m'
    YELLOW = '\x1b[5;33;40m'

    ON_RED = '\x1b[5;30;41m'
    ON_BLUE = '\x1b[5;30;44m'
    ON_CYAN = '\x1b[5;30;46m'
    ON_GRAY = '\x1b[5;30;47m'
    ON_GREEN = '\x1b[5;30;42m'
    ON_YELLOW = '\x1b[5;30;43m'

    RED_ON_YELLOW = '\x1b[5;31;43m'
    BLUE_ON_YELLOW = '\x1b[3;34;43m'
    GRAY_ON_CYAN = '\x1b[3;37;46m'
    GRAY_ON_RED = '\x1b[3;37;41m'
    YELLOW_ON_RED = '\x1b[5;33;41m'
    YELLOW_ON_BLUE = '\x1b[5;33;44m'


class KubeUtil:
    """
    - switch context
    - list pods
    - cp file <src> <dest>
    - exec pods
    - get pods log
    """

    _LIST_REGEX = re.compile(r'[A-Z]+ *')

    _FG_COLORS = [
        ColorTag.CYAN,
        ColorTag.GRAY,
        ColorTag.GREEN,
        ColorTag.YELLOW,
        ColorTag.RED,
        ColorTag.BLUE,
    ]

    _BG_COLORS = [
        ColorTag.ON_CYAN,
        ColorTag.ON_GRAY,
        ColorTag.ON_GREEN,
        ColorTag.ON_YELLOW,
        ColorTag.ON_RED,
        ColorTag.ON_BLUE,
    ]

    try:
        _TERMINAL_SIZE_WIDTH = os.get_terminal_size().columns
    except:
        _TERMINAL_SIZE_WIDTH = 90

    @classmethod
    def _help(cls):
        print(cls.__doc__)
        sys.exit()

    @classmethod
    def _get_args(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--download',
            action='store_true',
            help='Download File or Folder',
        )
        parser.add_argument(
            '-l', '--list',
            action='store_true',
            help='List the pods of the current context',
        )
        parser.add_argument(
            '-c', '--context',
            help='Specify Context',
            type=str,
        )
        parser.add_argument(
            '-n', '--namespace',
            help='Specify Namespace',
            type=str,
        )
        parser.add_argument(
            '-p', '--pod',
            help='Specify Pod',
            type=str,
        )
        parser.add_argument(
            '-s', '--src',
            help='Specify Source',
            type=str,
        )
        parser.add_argument(
            '-d', '--dest',
            help='Specify Destination',
            type=str,
        )
        return parser.parse_args()

    @classmethod
    def _stdout(cls, output, tag=None):
        header = str()
        if tag:
            badge = f' [{tag.upper()}] '
            header = f'{ColorTag.ON_CYAN}{badge:-^{cls._TERMINAL_SIZE_WIDTH}}{ColorTag.RESET}\n'
        sys.stdout.write(
            f'{header}'
            f'{ColorTag.CYAN}{output}{ColorTag.RESET}'
        )

    @classmethod
    def _stderr(cls, output, tag=None):
        header = str()
        if tag:
            badge = f' [{tag.upper()}] '
            header = f'{ColorTag.ON_RED}{badge:-^{cls._TERMINAL_SIZE_WIDTH}}{ColorTag.RESET}\n'
        sys.stderr.write(
            f'{header}'
            f'{ColorTag.RED}{output}{ColorTag.RESET}\n'
        )

    @classmethod
    def _exec(cls, cmd):
        try:
            output = subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT,
                shell=True,
                timeout=3,
                universal_newlines=True,
            )
        except subprocess.CalledProcessError as e:
            cls._stderr(output=e.output, tag='error')
        else:
            cls._stdout(output=output, tag='info')

    # @staticmethod
    # def _exec_foreground(command):
        # os.system(f'{command}')

    # @staticmethod
    # def _exec_background(command):
        # return subprocess.getoutput(command)

    # @classmethod
    # def _get_fg_color(cls, index):
        # return cls._FG_COLORS[index % len(cls._FG_COLORS)]

    # @classmethod
    # def _get_bg_color(cls, index):
        # return cls._BG_COLORS[index % len(cls._BG_COLORS)]

    # def _format_form(text, color):
        # return f'{color}{text}{ColorTag.RESET}'

    # @classmethod
    # def _get_settings(cls, headers):
        # subjects = cls._LIST_REGEX.findall(headers)
        # settings = list()
        # if not subjects:
            # return settings
        # pointer = int()
        # form = str()
        # for index, subject in enumerate(subjects):
            # start = pointer
            # end = pointer + len(subject)
            # pointer = end
            # text_color = cls._get_fg_color(index=index)
            # title_color = cls._get_bg_color(index=index)
            # settings.append({
                # 'start': start,
                # 'end': end,
                # 'color': text_color,
            # })
            # form += cls._format_form(text=headers[start:end], color=title_color)
        # print('_'*len(headers))
        # print(form)
        # print('‾'*len(headers))
        # # print('￣'*int(len(headers)/2))
        # return settings

    # @classmethod
    # def _list_pods(cls):
        # command = f'kubectl get pods'
        # stdout = cls._exec_background(command=command)
        # data = stdout.split('\n')
        # headers = data[0]
        # lines = data[1:]
        # settings = cls._get_settings(headers=headers)
        # for line in lines:
            # form = str()
            # for setting in settings:
                # start = setting['start']
                # end = setting['end']
                # color = setting['color']
                # form += cls._format_form(text=line[start:end], color=color)
            # print(form)

    @classmethod
    def _switch_context(cls, args):
        cmd = f'kubectl config set-context --current --namespace={args.context}'
        cls._exec(cmd=cmd)
        # cls._exec_foreground(command=command)

    @classmethod
    def _download(cls, args):
        if not args.pod:
            exit(f'Missing Key: -p, --pod')
        if not args.src:
            exit(f'Missing Key: -s, --source')
        if not args.dest:
            exit(f'Missing Key: -d, --dest')
        command = f'kubectl cp {args.pod}:{args.src} {args.dest}'
        cls._exec_foreground(command=command)

    @classmethod
    def cli(cls):
        if len(sys.argv) == 1:
            cls._help()
        args = cls._get_args()
        if args.list:
            cls._list_pods()
        if args.context:
            cls._switch_context(args=args)
        if args.download and not args.upload:
            cls._download(args=args)

if __name__ == '__main__':
    KubeUtil.cli()

