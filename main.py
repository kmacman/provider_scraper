import requests
from pydantic import BaseModel
import pandas as pd

ACCESS_TOKEN='7cd580d6f68341e1900f3981c50a910c'
class ProviderIndex(BaseModel):
    kyruusId: float
    url: str

def get_provider_index():
    provider_url = 'https://www.baystatehealth.org/-/media/api-feeds/providers.json'
    response = requests.get(provider_url)
    response.raise_for_status()
    providers = response.json()['items']
    provider_ids = []
    for provider in providers:
        ProviderIndex(**provider)
        provider_ids.append(provider['kyruusId'])
    return provider_ids

def get_provider_details(provider_id):
    provider_url = f'https://api.kyruus.com/v9/baystate/providers/{provider_id}?context=baystate_pmc&access_token={ACCESS_TOKEN}'
    response = requests.get(provider_url)
    response.raise_for_status()
    first = response.json()['provider']['name']['first']
    middle = response.json()['provider']['name']['middle']
    last = response.json()['provider']['name']['last']
    dept = response.json()['provider']['departments'][0]
    return {'provider_id':provider_id, 'first':first, 'middle':middle, 'last':last, 'dept':dept}

def get_all_providers():
    rows_list = []
    provider_ids = get_provider_index()
    for provider_id in provider_ids:
        dict1 = {}
        provider = get_provider_details(provider_id)
        print(provider)
        dict1.update(provider)
        rows_list.append(dict1)
    df = pd.DataFrame(rows_list)
    return df


