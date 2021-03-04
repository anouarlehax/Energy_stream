'''
Create a script to call RTE API to get PP1 days

 
'''

import requests 
import base64
import datetime as dt
from dateutil.parser import isoparse

RTE_HOST = "https://digital.iservices.rte-france.com"
CLIENT_ID = "f9aec6a9-e749-4f8d-b5ae-51c71ca7604c"
CLIENT_SECRET = "07892817-f433-43bf-91ff-7bb38846b4f7"

def get_token(client_id: str, client_secret: str) -> str:
    encoded = f"{client_id}:{client_secret}".encode("ascii")
    b64encoded = base64.b64encode(encoded).decode("ascii")

    response = requests.post(RTE_HOST+"/token/oauth/", headers={"Authorization":"Basic "+ b64encoded})
    response.raise_for_status()

    return response.json()["access_token"]


def get_pp1(year: int):
    start_date = dt.datetime(year, 1, 1).isoformat() + "+02:00"
    end_date = dt.datetime(year, 12, 31).isoformat() + "+02:00"
    token = get_token(CLIENT_ID, CLIENT_SECRET)
    response = requests.get(url=RTE_HOST+"/open_api/signal/v1/signals", 
                            headers={"Authorization":"Bearer "+ token},
                            params={"start_date": start_date, "end_date": end_date})
    response.raise_for_status()

    PP1_list = []

    for signal in response.json()["signals"]:
        if signal["type"] != "PP1":
            continue

        for value in signal["values"]:
            if value["value"] is True:
                PP1_list.append(isoparse(value["start_date"]))
    return PP1_list

for pp1 in get_pp1(2020):
    print(pp1)

