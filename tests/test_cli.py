from bddcli import stdout, status

import poaitran


def test_version(cliapp):
    with cliapp('--version'):
        assert status == 0
        assert stdout.strip() == poaitran.__version__


def test_help(cliapp):
    with cliapp('--help'):
        assert status == 0
        assert stdout.startswith('usage: poaitran')


# def test_translatefile():
