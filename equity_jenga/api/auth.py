import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


class JengaAuth:
    def __init__(
        self,
        authorization_token: str,
        private_key: str,
        merchant_code: str,
        env: str,
        sandbox_url: str,
        live_url: str,
        *args,
        **kwargs
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

    def authenticate(self, *args, **kwargs):
        """
        Returns a dict of authentication headers required for authentication
        Example:
        **Headers**
        :Authorization: the bearer token used to access the API
        :signature: A SHA-256 signature to proof that this request
        is coming from the merchant.


        The Authentication Method should be implemented by each Subclass
        to meet the required authentication for its use case
        as some require additional fields to be included in the generation of
        the signature

        """
        return {
            "Authorization": self.authorization_token,
        }

    def signature(self, request_hash_fields: tuple):
        """
        Build a String of concatenated values of the request fields with
        following order: as specificied by the API endpoint
        The resulting text is then signed with Private Key and Base64 encoded.

        Takes a tuple of request fields in the order that they should be
        concatenated, hashes them with SHA-256,signs the resulting hash and
        returns a Base64 encoded string of the resulting signature
        """
        data = "".join(request_hash_fields).encode()
        private_key = open(self.private_key, "r").read()
        rsa_key = RSA.importKey(private_key)
        signer = PKCS1_v1_5.new(rsa_key)
        digest = SHA256.new()
        digest.update(data)
        sign = signer.sign(digest)
        return base64.b64encode(sign)
