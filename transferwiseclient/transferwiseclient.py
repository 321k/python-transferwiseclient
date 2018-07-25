import uuid
import requests
import json

def getTransferWiseProfiles(access_token):
  # To get the personal profile ID, use json.loads(profiles.text)[0]['id']

  profiles = requests.get('https://api.transferwise.com/v1/profiles',
    headers={
    'Authorization': 'Bearer '+ access_token,
    'Content-Type': 'application/json'})
  
  return profiles

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
  #json.loads(recipient.text)['id']
  return recipient

def createTransferWiseQuote(profileId, sourceCurrency, targetCurrency, access_token, sourceAmount=None, targetAmount=None):
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
      'type': 'REGULAR'
      }),
      headers={
      'Authorization': 'Bearer '+ access_token,
      'Content-Type': 'application/json'})
  elif sourceAmount is None and targetAmount is not None:
    quote = requests.post('https://api.transferwise.com/v1/quotes',
      data = json.dumps({
      'profile': profileId,
      'source': sourceCurrency,
      'target': targetCurrency,
      'rateType': 'FIXED',
      'targetAmount': targetAmount,
      'type': 'REGULAR'
      }),
      headers={
      'Authorization': 'Bearer '+ access_token,
      'Content-Type': 'application/json'})
  else:
   return "Something went wrong"
  #json.loads(quote.text)['id']
  return quote

def createPayment(recipientId, quoteId, reference, access_token):
  response = requests.post('https://api.transferwise.com/v1/transfers',
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
  #json.loads(transfer.text)['id']
  return response

def redirectToPay(transferId):
  return redirect('https://transferwise.com/transferFlow#/transfer/' + requestId)


def getBorderlessAccountId(profileId, access_token):
  response = requests.get('https://api.transferwise.com/v1/borderless-accounts?profileId=' + str(profileId),
                headers={
                   'Authorization': 'Bearer '+ access_token,
                   'Content-Type': 'application/json'})
  #json.loads(response.text)[0]['id']
  return response

def getBorderlessAccounts(borderlessId, access_token):
  response = requests.get('https://api.transferwise.com/v1/borderless-accounts/' + str(borderlessId),
                headers={
                   'Authorization': 'Bearer '+ access_token,
                   'Content-Type': 'application/json'})
  return response
