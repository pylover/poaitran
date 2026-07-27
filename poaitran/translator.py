from babel.messages.pofile import read_po, write_po


def translate(exp):
    return exp


def translatefile(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        catalog = read_po(f)

    lang = catalog.locale_identifier
    if lang is None or not lang.strip():
        raise ValueError(f'Missing "Language:" header in {filename}')

    for message in catalog:
        # Skips the blank header block
        if not message.id:
            continue

        if message.string.strip():
            continue

        print(f'{filename}:{message.lineno} translating: {message.id}')
        message.string = translate(message.id)

    with open(filename, 'wb') as f:
        write_po(f, catalog)
