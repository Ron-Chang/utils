"""Naval Fate.

Usage:
  flask_new.py ship new <name>...
  flask_new.py ship <name> move <x> <y> [--speed=<kn>]
  flask_new.py ship shoot <x> <y>
  flask_new.py mine (set|remove) <x> <y> [--moored | --drifting]
  flask_new.py (-h | --help)
  flask_new.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='new-flask-project beta')
    print(arguments)
