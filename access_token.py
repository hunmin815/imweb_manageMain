
def create_token():
  import requests
  import configparser

  config = configparser.ConfigParser()
  config.read('config.ini')

  Acess_Token = ''
  access_Token_url = "https://api.imweb.me/v2/auth"

  access_Token_querystring = {"key":config['TOKEN']['KEY'], "secret":config['TOKEN']['SECRET']}

  payload = ""

  response = requests.request("GET", access_Token_url, data=payload, params=access_Token_querystring)
  access_Token_jsonObject = response.json()
  Acess_Token = access_Token_jsonObject["access_token"]
  
  return Acess_Token
