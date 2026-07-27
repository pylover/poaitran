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


def test_translatefile(cliapp, mktmpfile):
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
    with cliapp(['translate', pofile]):
        assert stderr == ''
        assert status == 0
        assert stdout == f'{pofile}:9 translating: bar\n'

    with open(pofile, 'r', encoding='utf-8') as f:
        catalog = read_po(f)

    assert catalog.get('foo').string == 'FOO'
    assert catalog.get('bar').string == 'bar'
