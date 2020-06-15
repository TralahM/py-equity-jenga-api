import base64
import os
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from .exceptions import handle_response


class JengaAuth:
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
        jengabase = api.auth.JengaApi(
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
        env: str,
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

    @property
    def authorization_token(self):
        """
        .. code-block:: json

            {
            "token_type": "bearer",
            "issued_at": "1443102144106",
            "expires_in": "3599",
            "access_token": "ceTo5RCpluTfGn9B3OZXnnQkDVKM"
            }

        Returns a str like "Bearer ceTo5RCpluTfGn9B3OZXnnQkDVKM"

        """
        if self.env == "sandbox":
            url = self.sandbox_url + "/identity-test/v2/token"
        else:
            url = self.live_url + "/identity/v2/token"
        headers = {"Authorization": self.api_key}
        body = dict(username=self._username, password=self._password)
        response = requests.post(url, headers=headers, data=body)
        response = handle_response(response)
        return "Bearer " + response.get("access_token")

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
