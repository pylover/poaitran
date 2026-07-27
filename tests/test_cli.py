from bddcli import Given, stdout, Application, when, given, status

import poaitran


def test_version():
    cliapp = Application('poaitran', 'poaitran.cli:Main.quickstart')
    with Given(cliapp, '--version'):
        assert status == 0
        assert stdout.strip() == poaitran.__version__
