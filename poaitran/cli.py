import os

import easycli

from . import translator
from .settings import settings


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
        easycli.Argument(
            '-C', '--directory',
            default='.',
            help='Change to this path before starting, default is: `.`'
        ),
        easycli.Argument(
            '--openai-model',
            default=settings.openai.model,
            help=f'The OpenAI model to use, default: {settings.openai.model}'
        ),
    ]

    def __call__(self, args):
        if args.filename:
            translator.translatefile(args.filename, settings)

        else:
            if args.directory != '.':
                os.chdir(args.directory)

            translator.translatedirectory(os.curdir, settings)


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
