import os
import sys

import snam


DEFAULT_SETTINGS = '''

openai:
  bundlesize: 100
  model: gpt-5.5

azure:
  bundlesize: 100
  apiversion: 3.0
  clientid:
  endpoint:
  key:
  region:

backend: azure
'''


settings = snam.loads(DEFAULT_SETTINGS)


def loadrcfiles():
    global settings

    appname = os.path.basename(sys.argv[0])
    user = os.environ.get('USER')
    filename = f'/home/{user}/.config/{appname}.yml'
    if not os.path.exists(filename):
        filename = f'/home/{user}/.config/{appname}/{appname}.yml'

    if os.path.exists(filename):  # pragma: no cover
        settings <<= filename


loadrcfiles()
