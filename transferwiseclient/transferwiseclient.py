import uuid
import requests
import json
from dateutil.parser import parse
from datetime import datetime


class TransferWiseClient:
  def __init__(self, access_token):
    self.access_token = access_token
    self.api_url = 'https://api.transferwise.com/v1/'
    self.headers={'Authorization': 'Bearer '+ self.access_token,
                  'Content-Type': 'application/json'}

  def get(self, method, data=None):
    if data is None:
      data = {}
    return requests.get(self.api_url + method, params=data, headers=self.headers)
  
  def post(self, method, data=None):
    if data is None:
      data = {}
    return requests.post(self.api_url + method, data=json.dumps(data), headers=self.headers)

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

  def get_account_statement(self, account_id, currency, interval_start, interval_end, type='json'):
    if not isinstance(interval_start, datetime):
      interval_start = parse(interval_start)
    if not isinstance(interval_end, datetime):
      interval_end = parse(interval_end)
    response = self.get('borderless-accounts/' + str(account_id) + '/statement.' + type, 
                  data = {
                    "currency": currency,
                    "intervalStart": interval_start.isoformat() + '.000Z',
                    "intervalEnd": interval_end.isoformat() + '.999Z'
                    })
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
