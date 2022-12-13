import os
import sys
import aiohttp
import asyncio
import random
import logging
import json
import datetime
from faker import Faker
import string
import uuid

# Logger = prepare_logging(__name__, logging.INFO)

c4cuser = "C4CCNSS4OP"
c4cpassword = "Welcome1!#"

def create_account_body(count):
    def create_account(uuid):
        validfrom = datetime(timestamp).strftime("%Y-%m-%d")
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
                                "preferredCommunicationMediumType": null,
                                "correspondenceLanguage": "EN"
                            },
                            "postalAddress": [
                                {
                                    "country": fake.country(),
                                    "streetName": fake.street_name(),
                                    "houseId": fake.building_number(),
                                    "cityName": fake.city(),
                                    "districtName": null,
                                    "additionalStreetPrefixName": null,
                                    "postalCode": fake.postcode(),
                                    "streetSuffixName": null,
                                    "additionalStreetSuffixName": null,
                                    "streetPrefixName": null,
                                    "region": fake.state_abbr(),
                                    "countyName": null
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
                        "isDeleted": false,
                        "isNaturalPerson": false,
                        "person": {
                            "gender": null,
                            "nonVerbalCommunicationLanguage": null,
                            "name": {
                                "formOfAddress": null,
                                "givenName": fake.firstname(),
                                "familyName": fake.lastname(),
                                "middleName": null,
                                "maritalStatus": null,
                                "academicTitle": null,
                                "nationalityCountry": null
                            }
                        },
                        "isBlocked": false,
                        "organisation": {
                            "name": {
                                "fourthLineName": null,
                                "firstLineName": fake.company(),
                                "secondLineName": null,
                                "thirdLineName": null
                            },
                            "companyLegalForm": null
                        },
                        "isReleased": true,
                        "contactAllowed": null
                    }
                ],
                "id": uuid.lower(),
                "category": "2",
                "displayId": str(random.randrange(0000000000,9999999999))
            }
        }

    fake = Faker(['en_US'])
    header_uuid = str(uuid.uuid4())
    messageheader = {
        "messageheader": {
            "id": header_uuid.upper(),
            "receiverCommunicationSystemDisplayId": os.getenv('RECEIVER_SYSTEM'),
            "senderCommunicationSystemDisplayId": os.getenv('SENDER_SYSTEM'),
            "creationDateTime": datetime.datetime.utcnow().isoformat()[:-3] + "Z"
        },
    }
    messagerequests = {}
    messagerequests['messagerequests'] = [
        create_account(header_uuid) for i in range(count)
    ]

    return {
        **messageheader,
        **messagerequests
    }
iteration = 0
async def main():
    count = input("Enter the number of request: ")
    print(count)
    async def create_request():

        async with aiohttp.ClientSession() as session:

            url = 'https://service3.vlab.crm.cloud.sap/sap/c4c/api/v1/inbound-data-connector-service/messages/sap.crm.md.integrationmetadataservice.entity.businessPartnerS4ReplicationMessageIn'
            params = {}
            headers = {
                    "content-type": "application/json",
                    "accept-encoding": "gzip",
                    "Accept": "application/json",
            }
            body = create_account_body(count)
            async with session.post(
                url=url,
                params=params,
                headers=headers,
                auth=aiohttp.BasicAuth(c4cuser, c4cpassword),
                json=body
            ) as response:
                res = await response.read()
                if response.status != 202:
                    return False
                else:
                    return True

    if await create_request():
            iteration +=1
            create_request()
    else:
        return

asyncio.run(main())
