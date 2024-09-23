import requests
from pydantic import BaseModel

class ProviderIndex(BaseModel):
    kyruusId: float
    url: str

def get_provider_index():
    url = 'https://www.baystatehealth.org/-/media/api-feeds/providers.json'
    response = requests.get(url)
    response.raise_for_status()
    providers = response.json()['items']
    provider_ids = []
    for provider in providers:
        ProviderIndex(**provider)
        provider_ids.append(provider['kyruusId'])
    return provider_ids

class Provider


