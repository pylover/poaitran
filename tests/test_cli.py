from bddcli import stdout, status, stderr
from babel.messages.pofile import read_po

import poaitran


def test_version(cliapp):
    with cliapp('--version'):
        assert status == 0
        assert stdout.strip() == poaitran.__version__


def test_help(cliapp):
    with cliapp('--help'):
        assert status == 0
        assert stdout.startswith('usage: poaitran')

    with cliapp():
        assert status == 0
        assert stdout.startswith('usage: poaitran')


def test_translatefile(cliapp, mktmpfile, bddcli_bootpatch):
    pofilecontent = '''
msgid ""
msgstr ""
"Language: ar\\n"

msgid "foo"
msgstr "FOO"

msgid "bar"
msgstr ""

'''
    pofile = mktmpfile(pofilecontent, 'foo.po')
    patchcode = \
        'import poaitran\n' \
        'translate = lambda m, l: m\n' \
        'poaitran.azure.translate = translate\n'

    with bddcli_bootpatch(patchcode), cliapp(['translate', pofile]):
        assert stderr == ''
        assert status == 0
        assert stdout == f'{pofile}:9 translating: bar\n'

    with open(pofile, 'r', encoding='utf-8') as f:
        catalog = read_po(f)

    assert catalog.get('foo').string == 'FOO'
    assert catalog.get('bar').string == 'bar'


def test_translatedirectory(cliapp, mktmptree, bddcli_bootpatch):
    pofilecontent = '''
msgid ""
msgstr ""
"Language: ar\\n"

msgid "foo"
msgstr "FOO"

msgid "bar"
msgstr ""

'''
    rootdir = mktmptree({
        'fa_IR': {
            'LC_MESSAGES': {
                'messages.po': pofilecontent
            }
        },
        'ar_OM': {
            'LC_MESSAGES': {
                'messages.po': pofilecontent
            }
        },
    })
    patchcode = \
        'import poaitran\n' \
        'translate = lambda m, l: m\n' \
        'poaitran.azure.translate = translate\n'

    with bddcli_bootpatch(patchcode), cliapp(f'translate -C {rootdir}'):
        assert stderr == ''
        assert status == 0
        assert stdout == \
            'fa_IR/LC_MESSAGES/messages.po:9 translating: bar\n' \
            'ar_OM/LC_MESSAGES/messages.po:9 translating: bar\n'

    with open(f'{rootdir}/fa_IR/LC_MESSAGES/messages.po', 'r') as f:
        catalog = read_po(f)

    assert catalog.get('foo').string == 'FOO'
    assert catalog.get('bar').string == 'bar'
