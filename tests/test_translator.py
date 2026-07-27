from babel.messages.pofile import read_po

from poaitran import translatefile


pofilecontent = '''
msgid ""
msgstr ""
"Project-Id-Version: foo 0.1.0\\n"
"Report-Msgid-Bugs-To: EMAIL@ADDRESS\\n"
"POT-Creation-Date: 2026-07-27 12:36+0400\\n"
"PO-Revision-Date: 2026-07-26 15:55+0400\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language: ar\\n"
"Language-Team: ar <LL@li.org>\\n"
"Plural-Forms: nplurals=6; plural=(n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 "
"&& n%100<=10 ? 3 : n%100>=0 && n%100<=2 ? 4 : 5);\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: Babel 2.18.0\\n"

msgid "foo"
msgstr "FOO"

msgid "bar"
msgstr ""

'''


def test_translate(mktmpfile):
    pofile = mktmpfile(pofilecontent, 'foo.po')
    translatefile(pofile)

    with open(pofile, 'r', encoding='utf-8') as f:
        catalog = read_po(f)

    assert catalog.get('foo').string == 'FOO'
    assert catalog.get('bar').string == 'bar'
