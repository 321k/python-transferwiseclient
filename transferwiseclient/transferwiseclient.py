import uuid
import requests
import json

def getTransferWiseProfileId(isBusiness, access_token):
  profiles = requests.get('https://api.transferwise.com/v1/profiles',
             headers={
                 'Authorization': 'Bearer '+ access_token,
                 'Content-Type': 'application/json'})

  if profiles.status_code == 200:
    if isBusiness == True:
      return json.loads(profiles.text)[1]['id']

    else:
      return json.loads(profiles.text)[0]['id']

  else:
    return 'Failed to get profile'

def createTransferWiseRecipient(email, currency, name, legalType, profileId, access_token):
  recipient = requests.post('https://api.transferwise.com/v1/accounts',
                data = json.dumps({
                  "profile": profileId,
                  "accountHolderName": name,
                  "currency": currency,
                  "type": "email",
                  "legalType": legalType,
                  "details": {
                    "email": email
                  }
                }),
                headers={
                   'Authorization': 'Bearer '+ access_token,
                   'Content-Type': 'application/json'})

  if recipient.status_code == 200:
      return json.loads(recipient.text)['id']

  else:
   return 'Failed to create recipient'

def createTransferWiseQuote(profileId, sourceCurrency, targetCurrency, transferType, access_token, sourceAmount=None, targetAmount=None):
  if sourceAmount is None and targetAmount is None:
    return "Specify sourceAmount or targetAmount"

  elif sourceAmount is not None and targetAmount is not None:
    return "Specify only sourceAmount or targetAmount"

  elif sourceAmount is not None and targetAmount is None:
    quote = requests.post('https://api.transferwise.com/v1/quotes',
                              data = json.dumps({
                              'profile': profileId,
                              'source': sourceCurrency,
                              'target': targetCurrency,
                              'rateType': 'FIXED',
                              'sourceAmount': sourceAmount,
                              'type': transferType
                              }),
                              headers={
                                'Authorization': 'Bearer '+ access_token,
                                'Content-Type': 'application/json'})

  elif targetAmount is None and targetAmount is not None:
    quote = requests.post('https://api.transferwise.com/v1/quotes',
                              data = json.dumps({
                              'profile': profileId,
                              'source': sourceCurrency,
                              'target': targetCurrency,
                              'rateType': 'FIXED',
                              'targetAmount': targetAmount,
                              'type': transferType
                              }),
                              headers={
                                'Authorization': 'Bearer '+ access_token,
                                'Content-Type': 'application/json'})

  else:
   return "Something went wrong"

  if quote.status_code == 200:
      return json.loads(quote.text)['id']

  else:
   return 'Failed to create quote'



def createPayment(recipientId, quoteId, reference, access_token):
  transfer = requests.post('https://api.transferwise.com/v1/transfers',
                data = json.dumps({
                  "targetAccount": recipientId,
                  "quote": quoteId,
                  "customerTransactionId": str(uuid.uuid4()),
                  "details": {
                    "reference": reference,
                    }
                  }),
                headers={
                   'Authorization': 'Bearer '+ access_token,
                   'Content-Type': 'application/json'})

  if transfer.status_code == 200:
      return json.loads(transfer.text)['id']

  else:
   return 'Failed to create transfer'

def redirectToPay(transferId):
  return redirect('https://transferwise.com/transferFlow#/transfer/' + requestId)