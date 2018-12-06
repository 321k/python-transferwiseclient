# python-transferwiseclient

``` bash
git clone https://github.com/321k/python-transferwiseclient.git
pip install -r requirements.txt
```

## Quich example

``` python
import transferwiseclient as TWClient
import pprint

TW = TWClient.TransferWiseClient('xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')

Profiles = TW.getProfiles().json()
pprint.pprint(Profiles)

print('=========')
ProfileAccounts = TW.getProfileAccounts(Profiles[1]['id']).json()
pprint.pprint(ProfileAccounts)

print('=========')
pprint.pprint(TW.getAccount(ProfileAccounts[0]['id']).json())

print('=========')
pprint.pprint(TW.getAccountStatement(ProfileAccounts[0]['id'], ProfileAccounts[0]['balances'][0]['currency'], '2018-12-01', '2018-12-06').json())
```
