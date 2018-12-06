# python-transferwiseclient

``` bash
git clone https://github.com/321k/python-transferwiseclient.git
pip install -r requirements.txt
```

## Quick example

``` python
import transferwiseclient as TWClient
import pprint

TW = TWClient.TransferWiseClient('xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')

profiles = TW.get_profiles().json()
pprint.pprint(profiles)

print('=========')
profile_accounts = TW.get_profile_accounts(profiles[0]['id']).json()
pprint.pprint(profile_accounts)

print('=========')
pprint.pprint(TW.get_account(profile_accounts[0]['id']).json())

print('=========')
pprint.pprint(TW.get_account_statement(profile_accounts[0]['id'], profile_accounts[0]['balances'][0]['currency'], '2018-12-01', '2018-12-06').json())
```
