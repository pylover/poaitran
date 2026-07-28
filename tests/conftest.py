import functools

import pytest
import bddcli
from bddcli.fixtures import bootstrapper_patch


@pytest.fixture
def cliapp():
    app = bddcli.Application('poaitran', 'poaitran.cli:Main.quickstart')
    return functools.partial(bddcli.Given, app)


@pytest.fixture
def bddcli_bootpatch():
    return bootstrapper_patch


@pytest.fixture
def monkeytrans():
    import poaitran

    def translate(messages, lang):
        return messages

    poaitran.azure.translate = translate
