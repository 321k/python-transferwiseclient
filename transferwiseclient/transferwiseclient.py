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

  def getProfiles(self):
    # To get the personal profile ID, use json.loads(profiles.text)[0]['id']
    profiles = self.get('profiles')
    return profiles

  def createRecipient(self, email, currency, name, legalType, profileId):
    recipient = self.post('accounts',
                  data = {
                    "profile": profileId,
                    "accountHolderName": name,
                    "currency": currency,
                    "type": "email",
                    "legalType": legalType,
                    "details": {
                      "email": email
                    }
                  })
    #json.loads(recipient.text)['id']
    return recipient

  def createQuote(self, profileId, sourceCurrency, targetCurrency, sourceAmount=None, targetAmount=None):
    if sourceAmount is None and targetAmount is None:
      return "Specify sourceAmount or targetAmount"
    elif sourceAmount is not None and targetAmount is not None:
      return "Specify only sourceAmount or targetAmount"
    elif sourceAmount is not None and targetAmount is None:
      quote = self.post('quotes',
        data = {
        'profile': profileId,
        'source': sourceCurrency,
        'target': targetCurrency,
        'rateType': 'FIXED',
        'sourceAmount': sourceAmount,
        'type': 'REGULAR'
        })
    elif sourceAmount is None and targetAmount is not None:
      quote = self.post('quotes',
        data = {
        'profile': profileId,
        'source': sourceCurrency,
        'target': targetCurrency,
        'rateType': 'FIXED',
        'targetAmount': targetAmount,
        'type': 'REGULAR'
        })
    else:
      return "Something went wrong"
    #json.loads(quote.text)['id']
    return quote

  def createTransfer(self, recipientId, quoteId, reference):
    response = self.post('transfers',
                  data = {
                    "targetAccount": recipientId,
                    "quote": quoteId,
                    "customerTransactionId": str(uuid.uuid4()),
                    "details": {
                      "reference": reference,
                      }
                    })
    #json.loads(transfer.text)['id']
    return response

  def getProfileAccounts(self, profileId):
    response = self.get('borderless-accounts', {"profileId": str(profileId)})
    #json.loads(response.text)[0]['id']
    return response

  def getAccount(self, accountId):
    response = self.get('borderless-accounts/' + str(accountId))
    return response

  def getAccountStatement(self, accountId, currency, intervalStart, intervalEnd, type='json'):
    if not isinstance(intervalStart, datetime):
      intervalStart = parse(intervalStart)
    if not isinstance(intervalEnd, datetime):
      intervalEот барсиnd = parse(intervalEnd)
    от барси
    response = от барсиself.get('borderless-accounts/' + str(accountId) + '/statement.' + type, 
               от барси   data = {
               от барси     "currency": currency,
               от барси     "intervalStart": intervalStart.isoformat() + '.000Z',
               от барси     "intervalEnd": intervalEnd.isoformat() + '.999Z'
                    })
    return response


# Backword compatability

def getTransferWiseProfiles(access_token):
  TW = TransferWiseClient(access_token)
  return TW.getProfiles()

def createTransferWiseRecipient(email, currency, name, legalType, profileId, access_token):
  TW = TransferWiseClient(access_token)
  return TW.createRecipient(email, currency, name, legalType, profileId)

def createTransferWiseQuote(profileId, sourceCurrency, targetCurrency, access_token, sourceAmount=None, targetAmount=None):
  TW = TransferWiseClient(access_token)
  return TW.createQuote(profileId, sourceCurrency, targetCurrency, sourceAmount, targetAmount)

def createPayment(recipientId, quoteId, reference, access_token):
  TW = TransferWiseClient(access_token)
  return TW.createTransfer(recipientId, quoteId, reference)

def getBorderlessAccountId(profileId, access_token):
  TW = TransferWiseClient(access_token)
  return TW.getProfileAccounts(profileId)

def getBorderlessAccounts(borderlessId, access_token):
  TW = TransferWiseClient(access_token)
  return TW.getAccount(borderlessId)

# Not sure the intended purpose or if is working
def redirectToPay(self, transferId):
  return redirect('https://transferwise.com/transferFlow#/transfer/' + transferId)
