import base64
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


class JengaAuth:
    """
    Jenga Base Authentication Class

    **Params**

    :authorization_token:: the bearer token used to access the API, i.e  apiKey
    :merchant_code:: the merchant code provided by JengaHQ
    :private_key:: the path to the merchant private key default is "~/.JengaAPI/keys/privatekey.pem"
    :env:: the environment in which  the API is to be used either *sandbox* or *production*
    :sandbox_url:: the url used to access the Sandbox API
    :live_url:: the url used to access the Production API

    **Example**

    .. code-block:: python

        from equity_jenga import api
        jengabase = api.auth.JengaApi(
        authorization_token="Bearer TofFGUeU9y448idLCKVAe35LmAtL",
        merchant_code="4144142283",
        env="sandbox",
        )
        # Similarly for all classes Inheriting from JengaAuth
        acc_Bal = api.auth.account_services.balances.AccountBalance(
        authorization_token="Bearer TofFGUeU9y448idLCKVAe35LmAtL",
        merchant_code="4144142283",
        env="sandbox",
        )
        # Get Available Balances
        available_bal=acc_Bal.available(countryCode='KE',accountId="0011547896523")
        print(available_bal)
        # Opening and Closing Balances
        opening_and_closing_bal=acc_Bal.get_opening_and_closing(accountId="0011547896523"countryCode='KE',date="2020-03-21")
        print(opening_and_closing_bal)

    """

    def __init__(
        self,
        authorization_token: str,
        merchant_code: str,
        env: str,
        private_key=os.path.expanduser("~") + "/.JengaApi/keys/privatekey.pem",
        sandbox_url="https://sandbox.jengahq.io",
        live_url="",
    ):
        """
        :authorization_token: the bearer token used to access the API
        :merchant_code: the merchant code provided by JengaHQ
        :private_key: the path to the merchant private key
        :env: the environment in which  the API is to be used
        :sandbox_url: the url used to access the Sandbox API
        :live_url: the url used to access the Production API

        """
        self.authorization_token = authorization_token
        self.sandbox_url = sandbox_url
        self.live_url = live_url
        self.private_key = private_key
        self.merchant_code = merchant_code

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
