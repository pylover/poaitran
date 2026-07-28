import pytest
from babel import UnknownLocaleError
from babel.messages.pofile import read_po

from poaitran import translatefile, translatedirectory
from poaitran.settings import settings


def test_translatefile(mktmpfile, monkeytrans):
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
    translatefile(pofile, settings)

    with open(pofile, 'r', encoding='utf-8') as f:
        catalog = read_po(f)

    assert catalog.get('foo').string == 'FOO'
    assert catalog.get('bar').string == 'bar'


def test_translatefile_bundlesize(mktmpfile, monkeytrans):
    pofilecontent = '''
msgid ""
msgstr ""
"Language: ar\\n"

msgid "foo"
msgstr "FOO"

msgid "bar"
msgstr ""
'''

    bsbackup = settings[settings.backend].bundlesize
    settings[settings.backend].bundlesize = 1
    pofile = mktmpfile(pofilecontent, 'foo.po')
    translatefile(pofile, settings)

    with open(pofile, 'r', encoding='utf-8') as f:
        catalog = read_po(f)

    assert catalog.get('foo').string == 'FOO'
    assert catalog.get('bar').string == 'bar'
    settings[settings.backend].bundlesize = bsbackup


def test_translatedirectory(mktmptree, monkeytrans, chdir):
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
    with chdir(rootdir):
        translatedirectory(settings)
        with open('fa_IR/LC_MESSAGES/messages.po') as f:
            catalog = read_po(f)

        assert catalog.get('foo').string == 'FOO'
        assert catalog.get('bar').string == 'bar'

        with open('ar_OM/LC_MESSAGES/messages.po') as f:
            catalog = read_po(f)

        assert catalog.get('foo').string == 'FOO'
        assert catalog.get('bar').string == 'bar'


def test_translate_missinglangugae(mktmpfile):
    pofilecontent = '''
msgid ""
msgstr ""
'''
    pofile = mktmpfile(pofilecontent, 'foo.po')
    with pytest.raises(TypeError) as e:
        translatefile(pofile, settings)

    assert e.exconly().startswith(
        'TypeError: Empty locale identifier value: None'
    )

    pofilecontent = '''
msgid ""
msgstr ""

"Language: xx_YY\\n"
'''
    pofile = mktmpfile(pofilecontent, 'foo.po')
    with pytest.raises(UnknownLocaleError) as e:
        translatefile(pofile, settings)

    assert e.exconly() == \
        'babel.core.UnknownLocaleError: unknown locale \'xx_YY\''
