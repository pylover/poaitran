import requests

from .settings import settings


def _validatesettings():
    cfg = settings.azure
    if cfg.endpoint is None:
        raise ValueError('azure.endpoint must be set')

    if cfg.region is None:
        raise ValueError('azure.region must be set')

    return cfg


def translate(messages, lang):
    cfg = _validatesettings()
    url = f'{cfg.endpoint.rstrip("/")}/translate'

    params = {
        'api-version': cfg.apiversion,
        'from': 'en',
        'to': lang,
    }

    headers = {
        'Ocp-Apim-Subscription-Key': cfg.key,
        'Ocp-Apim-Subscription-Region': cfg.region,
        'Content-type': 'application/json',
    }

    if cfg.clientid:
        headers['X-ClientTraceId'] = cfg.clientid

    body = []
    for msg in messages:
        body.append(dict(text=msg))

    request = requests.post(url, params=params, headers=headers, json=body)
    result = []
    for res in request.json():
        result.append(res['translations'][0]['text'])

    return result
