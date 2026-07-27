import functools

import pytest
import bddcli


@pytest.fixture
def cliapp():
    app = bddcli.Application('poaitran', 'poaitran.cli:Main.quickstart')
    return functools.partial(bddcli.Given, app)
