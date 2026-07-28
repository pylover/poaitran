import glob

from babel import Locale
from babel.messages.pofile import read_po, write_po

from . import azure


def translate(bundle, lang, settings):
    request = []

    for msg in bundle:
        request.append(msg.id)

    if settings.backend == 'azure':
        response = azure.translate(request, lang)
    else:
        raise NotImplementedError(settings.backend)

    for msg, result in zip(bundle, response):
        msg.string = result


def translatefile(filename, settings):
    bundlesize = settings[settings.backend].bundlesize
    bundle = []
    count = 0

    with open(filename, 'r', encoding='utf-8') as f:
        catalog = read_po(f)

    locale = Locale.parse(catalog.locale_identifier)

    def _translate():
        nonlocal bundle, count
        translate(bundle, locale.language, settings)
        bundle = []
        count = 0

    for message in catalog:
        # skip the blank header block
        if not message.id:
            continue

        if message.string.strip():
            continue

        print(f'{filename}:{message.lineno} translating: {message.id}')
        bundle.append(message)
        count += 1
        if count >= bundlesize:
            _translate()

    if count:
        _translate()

    with open(filename, 'wb') as f:
        write_po(f, catalog)


def translatedirectory(settings):
    for pofile in glob.glob('**/LC_MESSAGES/*.po'):
        translatefile(pofile, settings)
