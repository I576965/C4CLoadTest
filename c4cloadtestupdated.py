import asyncio
import datetime
import json
import os
import random
import uuid

import aiohttp
import requests
from faker import Faker

async def make_request(token, body):
    # Create an HTTP client
    async with aiohttp.ClientSession() as session:
        # Make the request
        headers = {
            "x-sap-crm-token": token,
            "content-type": "application/json",
            "accept-encoding": "gzip",
            "Accept": "application/json",
        }
        #print("hi")
        async with session.post(
                "https://service3.vlab.crm.cloud.sap/sap/c4c/api/v1/inbound-data-connector-service/messages/sap.crm.md.integrationmetadataservice.entity.businessPartnerS4ReplicationMessageIn",
                headers=headers, data=body) as response:
            # Get the response data
            data = response.status
            print(data)
            full = await response.json()
            print(full)
            return data


def auth_request():
    username = 'C4CCNSS4OP'
    password = 'Welcome1!#'
    response = requests.get('https://service3.vlab.crm.cloud.sap/auth/token', auth=(username, password))
    data = response.json()
    #print(data)
    token = data['value']['access_token']
    return token


def create_account_body(count):  # Number of Payload created per request
    def create_account(uuid):
        validfrom = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        return {
            "messageHeader": {
                "messageEntityName": "sap.crm.md.integrationmetadataservice.entity.businessPartnerS4ReplicationMessageIn",
                "actionCode": "SAVE",
                "id": uuid.lower()
            },
            "body": {
                "addresses": [
                    {
                        "validityPeriod": {
                            "validFrom": validfrom,
                            "validTo": "9999-12-31"
                        },
                        "address": {
                            "communicationPreference": {
                                "preferredCommunicationMediumType": None,
                                "correspondenceLanguage": "EN"
                            },
                            "postalAddress": [
                                {
                                    "country": "US",
                                    "streetName": fake.street_name(),
                                    "houseId": fake.building_number(),
                                    "cityName": fake.city(),
                                    "districtName": None,
                                    "additionalStreetPrefixName": None,
                                    "postalCode": fake.postcode(),
                                    "streetSuffixName": None,
                                    "additionalStreetSuffixName": None,
                                    "streetPrefixName": None,
                                    "region": fake.state_abbr(),
                                    "countyName": None
                                }
                            ]
                        },
                        "id": uuid.lower(),
                        "addressUsage": [
                            {
                                "validityPeriod": {
                                    "validFrom": validfrom,
                                    "validTo": "9999-12-31"
                                },
                                "code": "XXDEFAULT"
                            }
                        ]
                    }
                ],
                "role": [
                    {
                        "validityPeriod": {
                            "validFrom": validfrom,
                            "validTo": "9999-12-31"
                        },
                        "code": "TR0110"
                    }
                ],
                "common": [
                    {
                        "isDeleted": False,
                        "isNaturalPerson": False,
                        "person": {
                            "gender": None,
                            "nonVerbalCommunicationLanguage": None,
                            "name": {
                                "formOfAddress": None,
                                "givenName": fake.name(),
                                "familyName": fake.name(),
                                "middleName": None,
                                "maritalStatus": None,
                                "academicTitle": None,
                                "nationalityCountry": None
                            }
                        },
                        "isBlocked": False,
                        "organisation": {
                            "name": {
                                "fourthLineName": None,
                                "firstLineName": fake.company(),
                                "secondLineName": None,
                                "thirdLineName": None
                            },
                            "companyLegalForm": None
                        },
                        "isReleased": True,
                        "contactAllowed": None
                    }
                ],
                "id": uuid.lower(),
                "category": "2",
                "displayId": str(random.randrange(0000000000, 9999999999))
            }
        }

    fake = Faker(['en_US'])
    header_uuid = str(uuid.uuid4())
    #print(header_uuid)
    messageheader = {
        "messageHeader": {
            "id": header_uuid.upper(),
            "receiverCommunicationSystemDisplayId": "sap_cloud_crm_service3",
            "senderCommunicationSystemDisplayId": "C4CCNSS4OP",
            "creationDateTime": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        },
    }
    messagerequests = {}
    messagerequests['messageRequests'] = [
        create_account(header_uuid) for i in range(count)
    ]

    return {
        **messageheader,
        **messagerequests
    }


async def main():
    token = auth_request()
    #print(token)
    body = create_account_body(1)
    clean = json.dumps(body)
    print(clean)

    #asyncio.run(make_request(token, clean))

    future = asyncio.Future()
    asyncio.ensure_future(make_request(token,body))
    result = await future
    print(result)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

#if __name__ == '__main__':
 #   main()
