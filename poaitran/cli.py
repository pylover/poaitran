import easycli


class Main(easycli.Root):
    __completion__ = True
    __arguments__ = [
        easycli.Argument(
            'filename',
            nargs='?',
            metavar='FILENAME',
            help='PO file to translate and modify, if not given, it will '
                 'search for the "<lang>/LC_MESSAGES/*.po" file in the '
                 'current directory and translates all the directory'
        ),
        easycli.Argument('--version', action='store_true'),
    ]

    def __call__(self, args):
        if args.version:
            from poaitran import __version__
            print(__version__)
            return

        if args.filename:
            translator.translate(args.filename)
