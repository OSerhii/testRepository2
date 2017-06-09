#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import base64
from time import sleep
from random import randint

# Fill in variables internal_id and number_of_bids with your custom data
internal_id = "17c5ed057d3b4893b101c19060c5825c"
number_of_bids = 4
########################################################################

host = "https://lb.api-sandbox.openprocurement.org"
api_version = "dev"
auth_key = base64.b64encode(bytes("643c85c821fb426faf17a798030c1f12:"), "utf-8")


headers = {"Authorization": "Basic {}".format(auth_key),
          "Content-Length": "2347",
          "Content-Type": "application/json",
          "Host": "lb.api-sandbox.openprocurement.org"}


bid_body = {
    "data": {
        "status": "draft",
        "selfEligible": True,
        "selfQualified": True,
        "value": {
            "amount": randint(100, 500),
            "valueAddedTaxIncluded": True
        },
        "tenderers": [
            {
                "contactPoint": {
                    "telephone": "+380 (432) 21-69-30",
                    "name": "Сергій Олексюк",
                    "name_en": "Serg Oleksiuk",
                    "email": "soleksuk@gmail.com"
                },
                "identifier": {
                    "scheme": "UA-EDR",
                    "id": randint(1000000000, 9999999999),
                    "uri": "http://www.sc.gov.ua/"
                },
                "name": "ДКП «Школяр»",
                "address": {
                    "countryName": "Україна",
                    "postalCode": "21100",
                    "region": "м. Вінниця",
                    "streetAddress": "вул. Островського, 33",
                    "locality": "м. Вінниця"
                }
            }
        ]
    }
}


activate_bid_body = {
    "data": {
        "status": "pending"
    }
}


def send_bid(internal_id):
    s = requests.Session()
    s.request("HEAD", "{}/api/{}/spore".format(host, api_version))
    r = requests.Request('POST',
                         "{}/api/{}/tenders/{}/bids".format(host, api_version, internal_id),
                         data=json.dumps(bid_body),
                         headers=headers,
                         cookies=requests.utils.dict_from_cookiejar(s.cookies))
    prepped = s.prepare_request(r)
    resp = s.send(prepped)
    print("Send bid:")
    print("       status code:  {}".format(resp.status_code))
    print("       response content:  {}".format(resp.content))
    return resp


def activate_bid(internal_id, bid_id, acc_token):
    s = requests.Session()
    s.request("HEAD", "{}/api/{}/spore".format(host, api_version))
    r = requests.Request('PATCH',
                         "{}/api/{}/tenders/{}/bids/{}?acc_token={}".format(host, api_version, internal_id, bid_id, acc_token),
                         data=json.dumps(activate_bid_body),
                         headers=headers,
                         cookies=requests.utils.dict_from_cookiejar(s.cookies))
    prepped = s.prepare_request(r)
    resp = s.send(prepped)
    print ("Activate bid status code:  " + str(resp.status_code))
    return resp


def send_bids(id, bids_number):
    for i in range(bids_number):
        res = send_bid(id)
        activate_bid(id, res.json()["data"]["id"], res.json()["access"]["token"])


send_bids(internal_id, number_of_bids)
