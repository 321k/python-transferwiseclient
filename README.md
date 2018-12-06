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

Profiles = TW.get_profiles().json()
pprint.pprint(Profiles)

print('=========')
ProfileAccounts = TW.get_profile_accounts(Profiles[0]['id']).json()
pprint.pprint(ProfileAccounts)

print('=========')
pprint.pprint(TW.get_account(ProfileAccounts[0]['id']).json())

print('=========')
pprint.pprint(TW.get_account_statement(ProfileAccounts[0]['id'], ProfileAccounts[0]['balances'][0]['currency'], '2018-12-01', '2018-12-06').json())
```
