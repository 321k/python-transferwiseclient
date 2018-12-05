import uuid
import requests
import json

class TransferWiseClient:
  def __init__(self, access_token):
    self.access_token = access_token
    self.api_url = 'https://api.transferwise.com/v1/'
    self.headers={'Authorization': 'Bearer '+ self.access_token,
                  'Content-Type': 'application/json'}

  def get(self, method, data = {}):
    return requests.get(self.api_url + method, params = data, headers = self.headers)
  
  def post(self, method, data = {}):
    return requests.post(self.api_url + method, data = data, headers = self.headers)

  def getTransferWiseProfiles(self):
    # To get the personal profile ID, use json.loads(profiles.text)[0]['id']
    profiles = self.get('profiles')
    return profiles

  def createTransferWiseRecipient(self, email, currency, name, legalType, profileId):
    recipient = self.post('accounts',
                  data = json.dumps({
                    "profile": profileId,
                    "accountHolderName": name,
                    "currency": currency,
                    "type": "email",
                    "legalType": legalType,
                    "details": {
                      "email": email
                    }
                  }))
    #json.loads(recipient.text)['id']
    return recipient

  def createTransferWiseQuote(self, profileId, sourceCurrency, targetCurrency, sourceAmount=None, targetAmount=None):
    if sourceAmount is None and targetAmount is None:
      return "Specify sourceAmount or targetAmount"
    elif sourceAmount is not None and targetAmount is not None:
      return "Specify only sourceAmount or targetAmount"
    elif sourceAmount is not None and targetAmount is None:
      quote = self.post('quotes',
        data = json.dumps({
        'profile': profileId,
        'source': sourceCurrency,
        'target': targetCurrency,
        'rateType': 'FIXED',
        'sourceAmount': sourceAmount,
        'type': 'REGULAR'
        }))
    elif sourceAmount is None and targetAmount is not None:
      quote = self.post('quotes',
        data = json.dumps({
        'profile': profileId,
        'source': sourceCurrency,
        'target': targetCurrency,
        'rateType': 'FIXED',
        'targetAmount': targetAmount,
        'type': 'REGULAR'
        }))
    else:
      return "Something went wrong"
    #json.loads(quote.text)['id']
    return quote

  def createPayment(self, recipientId, quoteId, reference):
    response = self.post('transfers',
                  data = json.dumps({
                    "targetAccount": recipientId,
                    "quote": quoteId,
                    "customerTransactionId": str(uuid.uuid4()),
                    "details": {
                      "reference": reference,
                      }
                    }))
    #json.loads(transfer.text)['id']
    return response

  def getBorderlessAccountId(self, profileId):
    response = self.get('borderless-accounts', {"profileId": str(profileId)})
    #json.loads(response.text)[0]['id']
    return response

  def getBorderlessAccounts(self, borderlessId):
    response = self.get('borderless-accounts/' + str(borderlessId))
    return response


# Backword compatability

def getTransferWiseProfiles(access_token):
  TW = TransferWiseClient(access_token)
  return TW.getTransferWiseProfiles()

def createTransferWiseRecipient(email, currency, name, legalType, profileId, access_token):
  TW = TransferWiseClient(access_token)
  return TW.createTransferWiseRecipient(email, currency, name, legalType, profileId)

def createTransferWiseQuote(profileId, sourceCurrency, targetCurrency, access_token, sourceAmount=None, targetAmount=None):
  TW = TransferWiseClient(access_token)
  return TW.createTransferWiseQuote(profileId, sourceCurrency, targetCurrency, sourceAmount, targetAmount)

def createPayment(recipientId, quoteId, reference, access_token):
  TW = TransferWiseClient(access_token)
  return TW.createPayment(recipientId, quoteId, reference)

def getBorderlessAccountId(profileId, access_token):
  TW = TransferWiseClient(access_token)
  return TW.getBorderlessAccountId(profileId)

def getBorderlessAccounts(borderlessId, access_token):
  TW = TransferWiseClient(access_token)
  return TW.getBorderlessAccounts(borderlessId)

# Not sure the intended purpose or if is working
def redirectToPay(self, transferId):
  return redirect('https://transferwise.com/transferFlow#/transfer/' + transferId)
