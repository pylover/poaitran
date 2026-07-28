import pytest
from babel.messages.pofile import read_po

from poaitran import translatefile


def test_translate(mktmpfile, monkeytrans):
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
    translatefile(pofile)

    with open(pofile, 'r', encoding='utf-8') as f:
        catalog = read_po(f)

    assert catalog.get('foo').string == 'FOO'
    assert catalog.get('bar').string == 'bar'


def test_translate_missinglangugae(mktmpfile):
    pofilecontent = '''
msgid ""
msgstr ""
'''
    pofile = mktmpfile(pofilecontent, 'foo.po')
    with pytest.raises(ValueError) as e:
        translatefile(pofile)

    assert e.exconly() == f'ValueError: Missing "Language:" header in {pofile}'
