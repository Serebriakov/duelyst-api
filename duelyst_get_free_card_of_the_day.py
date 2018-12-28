#!/usr/bin/env python3

import requests

login_url="https://play.duelyst.com/session/bnea_login"
data={"password":"moo","email":"whynot_use@posteo.de"}

print("Login in...")
r = requests.post(login_url, data=data)

if not (r.status_code == requests.codes.ok):
  print("Couldn't log in")
  exit(1)

token = r.json()["token"]
headers = {"Authorization": "Bearer %s" % token}

print("Claiming free card of the day...")
url = "https://play.duelyst.com/api/me/inventory/free_card_of_the_day"
r = requests.post(url, headers=headers)

print("Removing duplicates in collection...")
url = "https://play.duelyst.com/api/me/inventory/card_collection/duplicates"
r = requests.delete(url, headers=headers)
if (r.status_code == requests.codes.ok):
  print("Spirit: %d" % r.json()["wallet"]["spirit_amount"])
