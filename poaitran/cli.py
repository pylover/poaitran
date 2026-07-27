import easycli

from . import translator


class TranslateCommand(easycli.SubCommand):
    __command__ = 'translate'
    __aliases__ = ['t']
    __arguments__ = [
        easycli.Argument(
            'filename',
            nargs='?',
            metavar='FILENAME',
            help='PO file to translate and modify, if not given, it will '
                 'search for the "<lang>/LC_MESSAGES/*.po" file in the '
                 'current directory and translates all the directory'
        ),
    ]

    def __call__(self, args):
        if args.filename:
            translator.translatefile(args.filename)

        else:
            raise ValueError()


class Main(easycli.Root):
    __completion__ = True
    __arguments__ = [
        easycli.Argument('--version', action='store_true'),
        TranslateCommand,
    ]

    def __call__(self, args):
        if args.version:
            from poaitran import __version__
            print(__version__)
            return

        self._parser.print_help()
