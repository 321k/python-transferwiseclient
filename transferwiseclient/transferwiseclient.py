import uuid
import requests
import json
import base64
import rsa
from dateutil.parser import parse
from datetime import datetime


class TransferWiseClient:
  def __init__(self, access_token, private_key=None):
    self.access_token = access_token
    self.api_url = 'https://api.transferwise.com/'
    self.headers={'Authorization': 'Bearer '+ self.access_token,
                  'Content-Type': 'application/json'}
    if private_key:
      self.private_key_path = private_key

  def get(self, method, data=None, version='v1'):
    if data is None:
      data = {}
    return self.request(method, data=data, version=version)
  
  def post(self, method, data=None, version='v1'):
    if data is None:
      data = {}
    return self.request(method, data=json.dumps(data), type='POST', version=version)

  def request(self, method, data=None, type='GET', version='v1', one_time_token=None):
    headers = self.headers.copy()
    if one_time_token:
      headers['x-2fa-approval'] = one_time_token
      headers['X-Signature'] = self.do_sca_challenge(one_time_token)

    if type == 'GET':
      res = requests.get(self.api_url + version + '/' + method, params=data, headers=headers)
    else:
      res = requests.post(self.api_url + version + '/' + method, data=data, headers=headers)

    if res.status_code == 403 and 'x-2fa-approval' in res.headers and not one_time_token:
      res = self.request(method=method, data=data, type=type, version=version, one_time_token=res.headers['x-2fa-approval'])

    return res

  def do_sca_challenge(self, one_time_token):

    # Read the private key file as bytes.
    with open(self.private_key_path, 'rb') as f:
      private_key_data = f.read()

    private_key = rsa.PrivateKey.load_pkcs1(private_key_data, 'PEM')

    # Use the private key to sign the one-time-token that was returned 
    # in the x-2fa-approval header of the HTTP 403.
    signed_token = rsa.sign(
        one_time_token.encode('ascii'), 
        private_key, 
        'SHA-256')

    # Encode the signed message as friendly base64 format for HTTP 
    # headers.
    signature = base64.b64encode(signed_token).decode('ascii')

    return signature

  def get_profiles(self):
    # To get the personal profile ID, use json.loads(profiles.text)[0]['id']
    return self.get('profiles')

  def create_recipient(self, email, currency, name, legal_type, profile_id):
    recipient = self.post('accounts',
                  data = {
                    "profile": profile_id,
                    "accountHolderName": name,
                    "currency": currency,
                    "type": "email",
                    "legalType": legal_type,
                    "details": {
                      "email": email
                    }
                  })
    #json.loads(recipient.text)['id']
    return recipient

  def create_quote(self, profile_id, source_currency, target_currency, source_amount=None, target_amount=None):
    if source_amount is None and target_amount is None:
      return "Specify source_amount or target_amount"
    elif source_amount is not None and target_amount is not None:
      return "Specify only source_amount or target_amount"
    elif source_amount is not None and target_amount is None:
      quote = self.post('quotes',
        data = {
        'profile': profile_id,
        'source': source_currency,
        'target': target_currency,
        'rateType': 'FIXED',
        'sourceAmount': source_amount,
        'type': 'REGULAR'
        })
    elif source_amount is None and target_amount is not None:
      quote = self.post('quotes',
        data = {
        'profile': profile_id,
        'source': source_currency,
        'target': target_currency,
        'rateType': 'FIXED',
        'targetAmount': target_amount,
        'type': 'REGULAR'
        })
    else:
      return "Something went wrong"
    #json.loads(quote.text)['id']
    return quote

  def create_transfer(self, recipient_id, quote_id, reference):
    response = self.post('transfers',
                  data = {
                    "targetAccount": recipient_id,
                    "quote": quote_id,
                    "customerTransactionId": str(uuid.uuid4()),
                    "details": {
                      "reference": reference,
                      }
                    })
    #json.loads(transfer.text)['id']
    return response

  def get_profile_accounts(self, profile_id):
    response = self.get('borderless-accounts', {"profileId": str(profile_id)})
    #json.loads(response.text)[0]['id']
    return response

  def get_account(self, account_id):
    response = self.get('borderless-accounts/' + str(account_id))
    return response

  def get_account_statement(self, profile_id, account_id, currency, interval_start, interval_end, type='json'):
    if not isinstance(interval_start, datetime):
      interval_start = parse(interval_start)
    if not isinstance(interval_end, datetime):
      interval_end = parse(interval_end)
    response = self.get('/profiles/' + str(profile_id) + '/borderless-accounts/' + str(account_id) + '/statement.' + type, 
                  data = {
                    "currency": currency,
                    "intervalStart": interval_start.isoformat() + '.000Z',
                    "intervalEnd": interval_end.isoformat() + '.999Z'
                    }, version='v3')
    return response


# Backward compatability

def getTransferWiseProfiles(access_token):
  TW = TransferWiseClient(access_token)
  return TW.get_profiles()

def createTransferWiseRecipient(email, currency, name, legalType, profileId, access_token):
  TW = TransferWiseClient(access_token)
  return TW.create_recipient(email, currency, name, legalType, profileId)

def createTransferWiseQuote(profileId, sourceCurrency, targetCurrency, access_token, sourceAmount=None, targetAmount=None):
  TW = TransferWiseClient(access_token)
  return TW.create_quote(profileId, sourceCurrency, targetCurrency, sourceAmount, targetAmount)

def createPayment(recipientId, quoteId, reference, access_token):
  TW = TransferWiseClient(access_token)
  return TW.create_transfer(recipientId, quoteId, reference)

def getBorderlessAccountId(profileId, access_token):
  TW = TransferWiseClient(access_token)
  return TW.get_profile_accounts(profileId)

def getBorderlessAccounts(borderlessId, access_token):
  TW = TransferWiseClient(access_token)
  return TW.get_account(borderlessId)

# Not sure the intended purpose or if is working
def redirectToPay(self, transferId):
  return redirect('https://transferwise.com/transferFlow#/transfer/' + transferId)
