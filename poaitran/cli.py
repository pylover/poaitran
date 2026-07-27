import easycli


class Main(easycli.Root):
    __completion__ = True
    __arguments__ = [
        easycli.Argument('--version', action='store_true')
    ]

    def __call__(self, args):
        if args.version:
            from poaitran import __version__
            print(__version__)
            return

        self._parser.print_help()
