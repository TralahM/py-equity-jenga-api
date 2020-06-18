import base64
import os
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from .exceptions import handle_response, generate_reference
from . import helpers


class JengaAPI:
    """
    Jenga API CORE  Class Representation

    Jenga Payment Gateway and Jenga API support the OAuth 2.0 Authentication Framework, requiring you to provide a username and password, as well as an API key that you generate on Jenga HQ part of HTTP Basic Authentication to generate a Bearer token.

    Once you have a token you can make subsequent requests to initiate payments, check completed transactions and more.

    Only load your API keys as environment variables and do not share your credentials to anyone over email or any other method of communication.

    **Params**

    :api_key: Your Jenga API Key
    :password: Your Jenga API Password
    :merchant_code:: the merchant code provided by JengaHQ
    :env:: the environment in which  the API is to be used either *sandbox* or *production*
    :private_key:: the path to the merchant private key default is "~/.JengaAPI/keys/privatekey.pem"
    :sandbox_url:: the url used to access the Sandbox API
    :live_url:: the url used to access the Production API

    **Example**

    .. code-block:: python

        from equity_jenga import api
        jengaApi = api.auth.JengaAPI(
        api_key="Basic TofFGUeU9y448idLCKVAe35LmAtLU9y448idLCKVAe35LmAtL",
        password="TofFGUeU9y448idLCKVAe35LmAtL",
        merchant_code="4144142283",
        env="sandbox",
        )

    """

    def __init__(
        self,
        api_key: str,
        password: str,
        merchant_code: str,
        env="sandbox",
        private_key=os.path.expanduser("~") + "/.JengaApi/keys/privatekey.pem",
        sandbox_url="https://sandbox.jengahq.io",
        live_url="https://api.jengahq.io",
    ):
        """

        """
        self.api_key = api_key
        self._username = merchant_code
        self._password = password
        self.sandbox_url = sandbox_url
        self.live_url = live_url
        self.private_key = private_key
        self.merchant_code = merchant_code
        self.env = env
        self._last_auth = None
        self._prev_token = None

    @property
    def authorization_token(self) -> str:
        """

        Returns a str like to be used in header as Authorization value

        ..code-block:: python

            "Bearer ceTo5RCpluTfGn9B3OZXnnQkDVKM"

        """
        if (
            self._last_auth is not None
            and self._prev_token is not None
            and not helpers.token_expired(self._last_auth)
        ):
            return self._prev_token
        if self.env == "sandbox":
            url = self.sandbox_url + "/identity-test/v2/token"
        else:
            url = self.live_url + "/identity/v2/token"
        headers = {"Authorization": self.api_key}
        body = dict(username=self._username, password=self._password)
        response = requests.post(url, headers=headers, data=body)
        response = handle_response(response)
        token = "Bearer " + response.get("access_token")
        self._prev_token = token
        self._last_auth = helpers.timenow()
        return token

    def signature(self, request_hash_fields: tuple):
        """
        Build a String of concatenated values of the request fields with
        following order: as specificied by the API endpoint
        The resulting text is then signed with Private Key and Base64 encoded.

        Takes a tuple of request fields in the order that they should be
        concatenated, hashes them with SHA-256,signs the resulting hash and
        returns a Base64 encoded string of the resulting signature
        """
        data = "".join(request_hash_fields).encode("utf-8")
        with open(self.private_key, "r") as pk:
            rsa_key = RSA.importKey(pk.read())
        signer = PKCS1_v1_5.new(rsa_key)
        digest = SHA256.new()
        digest.update(data)
        sign = signer.sign(digest)
        return base64.b64encode(sign)

    def get_pesalink_linked_accounts(self, mobile_number):
        """
        This webservice returns the recipients’ Linked Banks linked to the
        provided phone number on PesaLink
        """
        headers = {
            "Authorization": self.authorization_token,
            "Content-Type": "application/json",
        }
        data = {
            "mobileNumber": mobile_number,
        }
        if self.env == "sandbox":
            url = self.sandbox_url + "/transaction-test/v2/pesalink/inquire"
        else:
            url = self.live_url + "/transaction/v2/pesalink/inquire"
        response = requests.post(url, headers=headers, data=data)
        return handle_response(response)

    def get_transaction_status(self, requestId, transferDate):
        """
        Use this API to check the status of a B2C transaction
        """
        headers = {
            "Authorization": self.authorization_token,
            "Content-Type": "application/json",
        }
        data = {
            "requestId": requestId,
            "destination": {"type": "M-Pesa"},
            "transfer": {"date": transferDate},
        }
        if self.env == "sandbox":
            url = self.sandbox_url + "/transaction-test/v2/b2c/status/query"
        else:
            url = self.live_url + "/transaction/v2/b2c/status/query"
        response = requests.post(url, headers=headers, data=data)
        return handle_response(response)

    def get_all_eazzypay_merchants(self, numPages=1, per_page=10):
        """
        This webservice returns all EazzyPay merchants .
        """
        headers = {"Authorization": self.authorization_token}
        params = {"page": numPages, "per_page": per_page}
        if self.env == "sandbox":
            url = self.sandbox_url + "/transaction-test/v2/merchants"
        else:
            url = self.live_url + "/transaction/v2/merchants"
        response = requests.get(url, headers=headers, params=params)
        return handle_response(response)

    def get_all_billers(self, numPages=1, per_page=10):
        """
        This web service returns a paginated list of all billers
        """
        headers = {"Authorization": self.authorization_token}
        params = {"page": numPages, "per_page": per_page}
        if self.env == "sandbox":
            url = self.sandbox_url + "/transaction-test/v2/billers"
        else:
            url = self.live_url + "/transaction/v2/billers"
        response = requests.get(url, headers=headers, params=params)
        return handle_response(response)

    def get_payment_status(self, transactionReference):
        """
        The webservice enables an application track the status of a payment
        that is linked to the Receive Payments - Eazzypay Push web service
        especially in failure states.
        """
        headers = {"Authorization": self.authorization_token}
        if self.env == "sandbox":
            url = (
                self.sandbox_url
                + "/transaction-test/v2/payments/"
                + transactionReference
            )
        else:
            url = self.live_url + "/transaction/v2/payments/" + transactionReference
        response = requests.get(url, headers=headers)
        return handle_response(response)

    def get_transaction_details(self, transactionReference):
        """
        This webservice enables an application or service to query a
        transactions details and status
        """
        headers = {"Authorization": self.authorization_token}
        if self.env == "sandbox":
            url = (
                self.sandbox_url
                + "/transaction-test/v2/payments/details/"
                + transactionReference
            )
        else:
            url = (
                self.live_url
                + "/transaction/v2/payments/details/"
                + transactionReference
            )
        response = requests.get(url, headers=headers)
        return handle_response(response)

    def purchase_airtime(self, customer: dict, airtime: dict) -> dict:
        """
        This gives an application the ability to purchase airtime from any telco in
        East and Central Africa.

        Example Request

        :Customer::

        .. code-block:: json

            {
                "countryCode": "KE",
                "mobileNumber": "0765555131"
            }

        *countryCode*: the telco's ISO country code

        *mobileNumber*: the mobile number you are purchasing airtime for

        :Airtime::


        .. code-block:: json

            {
                "amount": "100",
                "reference": "692194625798",
                "telco": "Equitel"
            }

        *telco* the telco/provider. For example: Equitel, Safaricom , Airtel.

        *reference* your transaction references. Should always be a 12 digit string

        *amount* the airtime amount string


        Example Response

        .. code-block:: json

            {
                "referenceNumber": "4568899373748",
                "status": "SUCCESS"
            }

        """

        airtime["reference"] = generate_reference()
        payload = {
            "customer": customer,
            "airtime": airtime,
        }
        merchantCode = (self.merchant_code,)
        airtimeTelco = (airtime.get("telco"),)
        airtimeAmount = (airtime.get("amount"),)
        airtimeReference = (airtime.get("reference"),)
        fields = (merchantCode, airtimeTelco, airtimeAmount, airtimeReference)
        headers = {
            "Authorization": self.authentication_token,
            "Content-Type": "application/json",
            "signature": self.signature(fields),
        }
        if self.env == "sandbox":
            url = self.sandbox_url + "/transaction-test/v2/airtime"
            response = requests.post(url=url, headers=headers, data=payload)
            return handle_response(response)
        else:
            url = self.live_url + "/transaction/v2/airtime"
            response = requests.post(url=url, headers=headers, data=payload)
            return handle_response(response)

    def kyc_search_verify(self, identity: dict):
        """
        Params:

        :identitiy:
            :documentType: string the document type of the customer.  for example ID, PASSPORT, ALIENID

            :firstName: string first name as per identity document type

            :lastName: string last name as per identity document type

            :dateOfBirth: string optional date in YYYY-MM-DD format

            :documentNumber: string the document id number

            :countryCode: string the country in which the document relates to (only KE and RW enabled for now)


        Example Reponse

        .. code-block:: json

            {
                "identity": {
                    "customer": {
                        "fullName": "John Doe ",
                        "firstName": "John",
                        "middlename": "",
                        "lastName": "Doe",
                        "ShortName": "John",
                        "birthDate": "1900-01-01T00:00:00",
                        "birthCityName": "",
                        "deathDate": "",
                        "gender": "",
                        "faceImage": "/9j/4AAQSkZJRgABAAEAYABgA+H8qr6n4e1O71SGFbV/sEOF3O6/N/eb71d/FGkaBVXaq9KfRRRRRUMsKSIdyr0r/9k=",
                        "occupation": "",
                        "nationality": "Refugee"
                    },
                    "documentType": "ALIEN ID",
                    "documentNumber": "654321",
                    "documentSerialNumber": "100500425",
                    "documentIssueDate": "2002-11-29T12:00:00",
                    "documentExpirationDate": "2004-11-28T12:00:00",
                    "IssuedBy": "REPUBLIC OF KENYA",
                    "additionalIdentityDetails": [
                        {
                            "documentNumber": "",
                            "documentType": "",
                            "issuedBy": ""
                        }
                    ],
                    "address": {
                        "provinceName": " ",
                        "districtName": "",
                        "locationName": "",
                        "subLocationName": "",
                        "villageName": ""
                    }
                }
            }
        """
        documentNumber = identity.get("documentNumber")
        countryCode = identity.get("countryCode")
        merchantCode = self.merchant_code
        headers = {
            "Authorization": self.authorization_token,
            "Content-Type": "application/json",
            "signature": self.signature((merchantCode, documentNumber, countryCode)),
        }
        data = {"identity": identity}
        if self.env == "sandbox":
            url = self.sandbox_url + "/customer-test/v2/identity/verify"
        else:
            url = self.live_url + "/customer/v2/identity/verify"

        response = requests.post(url, headers=headers, data=data)
        return handle_response(response)

    def loans_credit_score(self, customer: list, bureau: dict, loan: dict) -> dict:
        """
        Example Request Payload
        customer,bureau,loan

        .. code-block:: json

            {
                "customer": [{
                    "id": "",
                    "fullName": "",
                    "firstName": "",
                    "lastName": "",
                    "shortName": "",
                    "title": "",
                    "mobileNumber": "",
                    "dateOfBirth": "1999-01-31",
                    "identityDocument": {
                        "documentType": "NationalID",
                        "documentNumber": "12365478"
                    }
                }],
                "bureau": {
                    "reportType": "Mobile",
                    "countryCode": "KE"
                },
                "loan": {
                    "amount": "5000"
                }
            }

        Example Response

        .. code-block:: json

            {
                "Person": {
                    "PersonName": {},
                    "IdentityDocument": {
                        "IdentityDocumentID": "1234568",
                        "IdentityDocumentType": "National ID"
                    }
                },
                "CreditAccountsSummary": [
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "17012014",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "65000.00000",
                            "65000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "5000.00000",
                        "LastPaymentReceivedDate": "20062014",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "30062014",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "09",
                        "AccountOpenDate": "09062011",
                        "AccountOwnership": "true",
                        "Balance": "106458.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "200000.00000",
                            "200000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "1667.00000",
                        "LastPaymentReceivedDate": "15062018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "30062018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "14052014",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "80000.00000",
                            "80000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "6960.00000",
                        "LastPaymentReceivedDate": "15122014",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31122014",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "22092014",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "1000.00000",
                            "1000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "1000.00000",
                        "LastPaymentReceivedDate": "15102014",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31102014",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "29122014",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "80000.00000",
                            "80000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "6666.67000",
                        "LastPaymentReceivedDate": "16032015",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31032015",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "36",
                        "AccountOpenDate": "20032015",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "80000.00000",
                            "80000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "6666.67000",
                        "LastPaymentReceivedDate": "16012016",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31012016",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "N:000019:01:2015",
                            "AccountCurrency": {}
                        },
                        "AccountType": "23",
                        "AccountOpenDate": "06012015",
                        "AccountOwnership": "false",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "300000.00000",
                            "300000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "20562.00000",
                        "LastPaymentReceivedDate": "27102017",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31122017",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "068-P-12365478",
                            "AccountCurrency": {}
                        },
                        "AccountType": "04",
                        "AccountOpenDate": "13102011",
                        "AccountOwnership": "true",
                        "Balance": "39844.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "40000.00000",
                            "40000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "2500.00000",
                        "LastPaymentReceivedDate": "16072018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31072018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "068-P-25417854",
                            "AccountCurrency": {}
                        },
                        "AccountType": "04",
                        "AccountOpenDate": "19082015",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "50000.00000",
                            "50000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "2500.00000",
                        "LastPaymentReceivedDate": "13022018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31072018",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "0011547896523",
                            "AccountCurrency": {}
                        },
                        "AccountType": "23",
                        "AccountOpenDate": "02022016",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "80000.00000",
                            "80000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "6666.67000",
                        "LastPaymentReceivedDate": "16122016",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31012017",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "2569774",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "02062016",
                        "AccountOwnership": "false",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "3000.00000",
                            "3000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "3726.00000",
                        "LastPaymentReceivedDate": "26122016",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "30062018",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "11110571749286",
                            "AccountCurrency": {}
                        },
                        "AccountType": "23",
                        "AccountOpenDate": "14022017",
                        "AccountOwnership": "true",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "120000.00000",
                            "120000.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "10000.00000",
                        "LastPaymentReceivedDate": "15112017",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31122017",
                        "AccountStatus": "F",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "JKCBDL1724301111",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "30082017",
                        "AccountOwnership": "false",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "5400.00000",
                            "5400.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "None",
                        "LastPaymentReceivedDate": "None",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "13122017",
                        "AccountStatus": "A",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "BCKMLD1802229762",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "08042018",
                        "AccountOwnership": "false",
                        "Balance": "0.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "5400.00000",
                            "5400.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "None",
                        "LastPaymentReceivedDate": "11062018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "21062018",
                        "AccountStatus": "A",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "MKDLCB1814647289",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "26052018",
                        "AccountOwnership": "false",
                        "Balance": "5400.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "5400.00000",
                            "5400.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "5400.00000",
                        "LastPaymentReceivedDate": "26052018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31052018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "MKCDLB1818039369",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "29062018",
                        "AccountOwnership": "false",
                        "Balance": "2150.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "2150.00000",
                            "2150.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "2150.00000",
                        "LastPaymentReceivedDate": "29062018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "30062018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    },
                    {
                        "AccountIdentifier": {
                            "AccountID": "MDLBBCK1821123688",
                            "AccountCurrency": {}
                        },
                        "AccountType": "12",
                        "AccountOpenDate": "29072018",
                        "AccountOwnership": "false",
                        "Balance": "2150.00000",
                        "DelinquencyStatus": "No delinquency",
                        "Original_Amount": [
                            "2150.00000",
                            "2150.00000"
                        ],
                        "PastDueAmount": "0.00000",
                        "LastPaymentAmount": "2150.00000",
                        "LastPaymentReceivedDate": "30072018",
                        "NoofDelayed_Payments": "0",
                        "PostedDateTime": "31072018",
                        "AccountStatus": "W",
                        "LoanAccount": {
                            "PastDueDate": {},
                            "LoanHighestDaysInArrears": {}
                        }
                    }
                ],
                "CreditBureau": {
                    "score": "772",
                    "creditApplications90Days": "0",
                    "creditApplications180Days": "0",
                    "creditApplications365Days": "0",
                    "crbEnqiry90Days": "0",
                    "crbEnqiry180Days": "0",
                    "crbEnqiry365Days": "0",
                    "BouncedCheques90Days": "0",
                    "BouncedCheques180Days": "0",
                    "BouncedCheques365Days": "0",
                    "AcctNonPerformingCurrent": "0",
                    "AcctNonPerformingHisto": "0",
                    "AcctPerformingCurrent": "15",
                    "AcctPerformingHisto": "NaN",
                    "IsFraud": "false",
                    "isGuarantor": "false",
                    "delinquency_code": "No delinquency"
                }
            }

        """
        payload = {"customer": customer, "bureau": bureau, "loan": loan}
        dateOfBirth = payload.get("customer")[0].get("dateOfBirth")
        merchantCode = self.merchant_code
        documentNumber = (
            payload.get("customer")[0].get(
                "identityDocument").get("documentNumber")
        )
        headers = {
            "Authorization": self.authentication_token,
            "Content-Type": "application/json",
            "signature": self.signature((dateOfBirth, merchantCode, documentNumber)),
        }
        if self.env == "sandbox":
            url = self.sandbox_url + "/customer-test/v2/creditinfo"
        else:
            url = self.live_url + "/customer/v2/creditinfo"
        response = requests.post(url=url, headers=headers, data=payload)
        return handle_response(response)

    def get_forex_rates(self, countryCode: str, currencyCode: str) -> dict:
        """
        Params

        :countryCode:: the country for which rates are being requested.
            Valid values are KE, TZ, UG, RW.

        :currencyCode:: the currency code of the currency
            that is being converted from in ISO 4217 format

        Example Request

        .. code-block:: json

            {
            "countryCode": "KE",
            "currencyCode": "USD"
            }


        Example Response
        :currencyRates:: list of conversion rates for major currencies

        .. code-block:: json

            {
            "currencyRates":[],
            "fromCurrency": "KES",
            "rate":101.3,
            "toCurrency": "USD"
            }


        """
        headers = {
            "Authorization": self.authentication_token,
            "Content-Type": "application/json",
        }
        data = {
            "countryCode": countryCode,
            "currencyCode": currencyCode,
        }
        if self.env == "sandbox":
            url = self.sandbox_url + "/transaction-test/v2/foreignexchangerates"
        else:
            url = self.live_url + "/transaction/v2/foreignexchangerates"

        response = requests.post(url=url, headers=headers, data=data)
        return handle_response(response)

    def get_account_available_balance(self, countryCode, accountId) -> dict:
        """
        Retrieve the current and available balance of an account

        200 Success Response Schema

        .. code-block:: json

            {
                "currency": "KES",
                "balances": [
                    {
                        "amount": "997382.57",
                        "type": "Current"
                    },
                    {
                        "amount": "997382.57",
                        "type": "Available"
                    }
                ]
            }

        """
        headers = {
            "Authorization": self.authorization_token,
            "signature": self.signature((countryCode, accountId)),
        }
        if self.env == "sandbox":
            resource = f"/account-test/v2/accounts/balances/{countryCode}/{accountId}"
            url = self.sandbox_url + resource
        else:
            resource = f"/account/v2/accounts/balances/{countryCode}/{accountId}"
            url = self.live_url + resource
        response = requests.get(url, headers=headers)
        return handle_response(response)

    def get_account_opening_and_closing_balance(self, accountId, countryCode, date):
        """
        Example Request

        .. code-block:: json

            {
            "countryCode": "KE",
            "accountId": "0011547896523",
            "date": "2017-09-29"
            }


        Example Response

        .. code-block:: json

                {
                    "balances": [
                        {
                            "type": "Closing Balance",
                            "amount": "10810.00"
                        },
                        {
                            "type": "Opening Balance",
                            "amount": "103.00"
                        }
                    ]
                }

        """
        headers = {
            "Authorization": self.authorization_token,
            "signature": self.signature((accountId, countryCode, date)),
        }
        data = {
            "countryCode": countryCode,
            "accountId": accountId,
            "date": date,
        }
        if self.env == "sandbox":
            resource = "/account-test/v2/accounts/accountbalance/query"
            url = self.sandbox_url + resource
        else:
            resource = "/account/v2/accounts/accountbalance/query"
            url = self.live_url + resource
        response = requests.post(url, headers=headers, data=data)
        return handle_response(response)

    def get_account_mini_statement(self, countryCode, accountNumber):
        """
        Example Response

        .. code-block:: json

            {
                "accountNumber": "0011547896523",
                "currency": "KES",
                "balance": 1000,
                "transactions": [
                    {
                        "chequeNumber": null,
                        "date": "2017-01-01T00:00:00",
                        "description": "EAZZY-FUNDS TRNSF TO A/C XXXXXXXXXXXX",
                        "amount": "100",
                        "type": "Debit"
                    },
                    {
                        "chequeNumber": null,
                        "date": "2017-01-03T00:00:00",
                        "description": "SI ACCOUNT TO ACCOUNT THIRD PA",
                        "amount": "51",
                        "type": "Debit"
                    },
                    {
                        "chequeNumber": null,
                        "date": "2017-01-05T00:00:00",
                        "description": "CHARGE FOR OTC ECS TRAN",
                        "amount": "220",
                        "type": "Debit"
                    },
                    {
                        "chequeNumber": null,
                        "date": "2017-01-05T00:00:00",
                        "description": "SI ACCOUNT TO ACCOUNT THIRD PA",
                        "amount": "20",
                        "type": "Debit"
                    }
                ]
            }
        """
        headers = {
            "Authorization": self.authorization_token,
            "Content-Type": "application/json",
            "signature": self.signature((countryCode, accountNumber)),
        }
        if self.env == "sandbox":
            resource = (
                f"/account-test/v2/accounts/ministatement/{countryCode}/{accountNumber}"
            )
            url = self.sandbox_url + resource
        else:
            resource = (
                f"/account/v2/accounts/ministatement/{countryCode}/{accountNumber}"
            )
            url = self.live_url + resource
        response = requests.get(url, headers=headers)
        return handle_response(response)

    def get_account_full_statement(
        self, countryCode, accountNumber, fromDate, toDate, limit=10
    ):
        """

        Example Response

        .. code-block:: json

            {
                "accountNumber": "0011547896523",
                "currency": "KES",
                "balance": 997382.57,
                "transactions": [
                    {
                        "reference": 541,
                        "date": "2018-07-13T00:00:00.000",
                        "description": "EQUITEL-BUNDLE/254764555383/8755",
                        "amount": 900,
                        "serial": 1,
                        "postedDateTime": "2018-07-13T09:51:27.000",
                        "type": "Debit",
                        "runningBalance": {
                            "currency": "KES",
                            "amount": 1344.57
                        }
                    },
                    {
                        "reference": "S4921027",
                        "date": "2018-07-18T00:00:00.000",
                        "description": "EAZZY-AIRTIME/EQUITEL/254764555383/100000939918/18",
                        "amount": 200,
                        "serial": 1,
                        "postedDateTime": "2018-07-18T16:27:18.000",
                        "type": "Debit",
                        "runningBalance": {
                            "currency": "KES",
                            "amount": 1144.57
                        }
                    },
                    {
                        "reference": 5436,
                        "date": "2018-07-19T00:00:00.000",
                        "description": "CREDIT TRANSFER",
                        "amount": 1000000,
                        "serial": 2,
                        "postedDateTime": "2018-07-19T12:01:47.000",
                        "type": "Credit",
                        "runningBalance": {
                            "currency": "KES",
                            "amount": 1001144.57
                        }
                    }
                ]
            }

        """
        payload = {
            "countryCode": countryCode,
            "accountNumber": accountNumber,
            "fromDate": fromDate,
            "toDate": toDate,
            "limit": limit,
        }

        accountNumber = payload.get("accountNumber")
        countryCode = payload.get("countryCode")
        toDate = payload.get("toDate")
        headers = {
            "Authorization": self.authorization_token,
            "Content-Type": "application/json",
            "signature": self.signature((accountNumber, countryCode, toDate)),
        }
        if self.env == "sandbox":
            resource = "/account-test/v2/accounts/fullstatement/"
            url = self.sandbox_url + resource
        else:
            resource = "/account/v2/accounts/fullstatement/"
            url = self.live_url + resource
        response = requests.post(url, headers=headers, data=payload)
        return handle_response(response)


def generate_key_pair():
    """
    Generates a Public/Public RSA Key Pair which is store in the current User's
    **HOME** directory  under the **.JengaAPI/keys/** Directory
    """
    import os

    home_dir = os.path.expanduser("~")
    if not os.path.exists(home_dir + "/.JengaApi"):
        os.mkdir(home_dir + "/.JengaApi")
    keypath = os.path.join(home_dir, ".JengaApi", "keys")
    if not os.path.exists(keypath):
        os.mkdir(keypath)
        print(f"created {keypath}")

    os.system(
        f"cd {keypath};openssl genrsa -out privatekey.pem 2048;openssl rsa -in privatekey.pem -outform PEM -pubout -out publickey.pem"
    )
    os.system(f"ls {keypath}")
